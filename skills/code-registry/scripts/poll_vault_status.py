#!/usr/bin/env python3
"""Poll Code Registry MCP endpoints until report-completion rules are satisfied."""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict

DEFAULT_MCP_URL = "https://integrator.app.thecoderegistry.com/api/ai/router"

class RpcClient:
    def __init__(self, mcp_url: str, api_key: str, api_key_in_body: bool, request_timeout: int) -> None:
        self.mcp_url = mcp_url
        self.api_key = api_key
        self.api_key_in_body = api_key_in_body
        self.request_timeout = request_timeout
        self.request_id = 1

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        args = dict(arguments)
        if self.api_key_in_body:
            args["api_key"] = self.api_key

        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
            "id": self.request_id,
        }
        self.request_id += 1

        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if not self.api_key_in_body:
            headers["X-API-Key"] = self.api_key

        last_error = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(self.mcp_url, data=body, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.request_timeout) as response:
                    wrapper = json.loads(response.read().decode("utf-8"))
                return self._unwrap_tool_result(wrapper)
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    break

        raise RuntimeError(f"RPC call failed for {name}: {last_error}")

    def _unwrap_tool_result(self, wrapper: Dict[str, Any]) -> Dict[str, Any]:
        if "error" in wrapper:
            raise RuntimeError(f"JSON-RPC error: {wrapper['error']}")

        result = wrapper.get("result")
        if not isinstance(result, dict):
            raise RuntimeError("Missing JSON-RPC result payload")

        content = result.get("content")
        if isinstance(content, list) and content:
            first = content[0]
            if isinstance(first, dict) and isinstance(first.get("text"), str):
                text = first["text"]
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, dict):
                        return parsed
                    raise RuntimeError("Tool text payload is not a JSON object")
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Unable to parse tool payload JSON: {exc}") from exc

        if isinstance(result, dict):
            return result
        raise RuntimeError("Unexpected tool response format")


def extract_report_status(summary: Dict[str, Any], reports: Dict[str, Any]) -> Dict[str, Any]:
    analysis = summary.get("analysis") if isinstance(summary.get("analysis"), dict) else summary
    report = reports.get("report") if isinstance(reports.get("report"), dict) else reports

    status = analysis.get("status") or report.get("status") or "unknown"
    version = analysis.get("version") or report.get("version")

    snapshot_url = None
    comparison_url = None

    snapshot_report = report.get("snapshot_report")
    if isinstance(snapshot_report, dict):
        snapshot_url = snapshot_report.get("url")

    comparison_report = report.get("comparison_report")
    if isinstance(comparison_report, dict):
        comparison_url = comparison_report.get("url")

    complete = False
    if version == "1.0.0":
        complete = bool(snapshot_url)
    elif isinstance(version, str) and version:
        complete = bool(comparison_url)

    return {
        "status": status,
        "version": version,
        "snapshot_url": snapshot_url,
        "comparison_url": comparison_url,
        "complete": complete,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Poll The Code Registry MCP server until vault report completion criteria are met."
    )
    parser.add_argument("--vault-id", required=True, help="Code vault ID to poll")
    parser.add_argument("--api-key", required=True, help="The Code Registry API key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP JSON-RPC endpoint URL")
    parser.add_argument(
        "--api-key-in-body",
        action="store_true",
        help="Send api_key in tool arguments instead of X-API-Key header",
    )
    parser.add_argument("--initial-delay", type=int, default=5, help="Initial backoff delay in seconds")
    parser.add_argument("--max-delay", type=int, default=60, help="Maximum backoff delay in seconds")
    parser.add_argument("--timeout", type=int, default=3600, help="Overall timeout in seconds")
    parser.add_argument("--request-timeout", type=int, default=60, help="Per-request timeout in seconds")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print final status as JSON in addition to human-readable output",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = RpcClient(args.mcp_url, args.api_key, args.api_key_in_body, args.request_timeout)

    start = time.time()
    attempt = 1

    while True:
        elapsed = int(time.time() - start)
        if elapsed > args.timeout:
            print("Timed out before completion criteria were met.", file=sys.stderr)
            return 1

        try:
            summary = client.call_tool("get-code-vault-summary", {"vault_id": args.vault_id})
            reports = client.call_tool("get-code-vault-reports", {"vault_id": args.vault_id})
        except RuntimeError as exc:
            print(f"Attempt {attempt}: request failed: {exc}", file=sys.stderr)
            wait = min(args.max_delay, args.initial_delay * (2 ** max(0, attempt - 1)))
            print(f"Retrying in {wait}s...", file=sys.stderr)
            time.sleep(wait)
            attempt += 1
            continue

        status = extract_report_status(summary, reports)
        print(
            f"Attempt {attempt}: status={status['status']} version={status['version']} "
            f"snapshot_ready={bool(status['snapshot_url'])} comparison_ready={bool(status['comparison_url'])}"
        )

        if status["status"] == "failed":
            print("Analysis failed. Stop polling and inspect vault details.", file=sys.stderr)
            return 2

        if status["complete"]:
            print("Completion criteria met.")
            if status["snapshot_url"]:
                print(f"Snapshot report: {status['snapshot_url']}")
            if status["comparison_url"]:
                print(f"Comparison report: {status['comparison_url']}")
            if args.json:
                print(json.dumps(status, indent=2, sort_keys=True))
            return 0

        wait = min(args.max_delay, args.initial_delay * (2 ** max(0, attempt - 1)))
        print(f"Not complete yet, waiting {wait}s...")
        time.sleep(wait)
        attempt += 1


if __name__ == "__main__":
    raise SystemExit(main())
