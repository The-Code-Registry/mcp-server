# Contributing to The Code Registry MCP Server

Thank you for your interest in contributing! We welcome contributions from the community to make our MCP server documentation and integrations better.

## How You Can Help

### 1. Reporting Issues

If you encounter problems or have questions:

- **Search existing issues** first to avoid duplicates
- **Use GitHub Issues** for bug reports and feature requests
- **Provide details** including:
  - Your MCP client (Claude Desktop, Claude API, etc.)
  - Steps to reproduce the issue
  - Expected vs actual behavior
  - Error messages (if any)
  - Code examples (if relevant)

**Good Issue Example:**
```
Title: get-code-vault-results returns 404 for ready vault

Environment:
- MCP Client: Claude Desktop v1.2.3
- OS: macOS 14.2

Steps to Reproduce:
1. Create vault with vault_id abc-123
2. Wait for status "ready" (confirmed via get-code-vault-summary)
3. Call get-code-vault-results with vault_id abc-123
4. Receive 404 error

Expected: Results JSON with analysis data
Actual: 404 NOT_FOUND error

Error Response:
{
  "error": {
    "message": "Vault not found",
    "code": "NOT_FOUND",
    "status": 404
  }
}
```

### 2. Documentation Improvements

Documentation contributions are highly valued:

- **Fix typos** via pull requests
- **Clarify confusing sections** by suggesting improvements
- **Add examples** for common use cases
- **Translate documentation** (contact us first)
- **Improve error messages** with clearer explanations

**Areas that especially need help:**
- Additional integration examples
- More detailed troubleshooting scenarios
- Video tutorials or screencasts
- Real-world use case walkthroughs

### 3. Integration Examples

We especially welcome examples for:

- **New MCP clients** (as they become available)
- **Custom agent implementations** showing novel uses
- **CI/CD integrations** (GitHub Actions, GitLab CI, etc.)
- **Automation workflows** combining multiple tools
- **Language-specific SDKs** wrapping the MCP server

**Example PR Structure:**
```
integrations/
  my-new-client/
    README.md          # Setup instructions
    config.json        # Configuration example
    example.js         # Usage example (if applicable)
```

### 4. Code Contributions

While the MCP server itself is closed source, we welcome contributions to:

- **Client libraries** (Python, TypeScript, etc.)
- **CLI tools** for interacting with the MCP server
- **Test utilities** for validation
- **Example applications** demonstrating use cases

## Pull Request Process

### Before You Start

1. **Check existing PRs** to avoid duplicate work
2. **Open an issue first** for significant changes
3. **Fork the repository** to your account

### Making Changes

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/my-improvement
   ```

2. **Make your changes** following our guidelines:
   - Use clear, descriptive commit messages
   - Keep changes focused and atomic
   - Test your changes (if applicable)

3. **Write good commit messages**:
   ```
   Fix typo in create_account example
   
   - Changed "anonymouse" to "anonymous" in README
   - Updated examples/use-cases/due-diligence.md
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/my-improvement
   ```

5. **Open a Pull Request**:
   - Use a clear, descriptive title
   - Explain what changed and why
   - Reference any related issues
   - Add screenshots for visual changes

### PR Review Process

- We review PRs as quickly as possible (usually within 2-3 business days)
- We may request changes or ask questions
- Once approved, we'll merge your PR
- Your contribution will be acknowledged in release notes

## Documentation Style Guide

### Markdown Formatting

- Use ATX-style headers (`#` not underlines)
- Use fenced code blocks with language identifiers
- Use tables for structured data
- Add blank lines around code blocks and headers

### Code Examples

- **Always include context** (what the code does)
- **Show complete examples** when possible
- **Use realistic values** (not foo/bar)
- **Include error handling** for production examples
- **Comment complex logic**

**Good Example:**
```python
# Create a Code Registry account and analyze a repository
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=[{
            "type": "mcp",
            "server_url": "https://integrator.app.thecoderegistry.com/api/ai/router"
        }],
        messages=[{
            "role": "user",
            "content": "Create an account for john@example.com and analyze github.com/acme/app"
        }]
    )
    print(response)
except anthropic.APIError as e:
    print(f"Error: {e}")
```

### Writing Style

- **Use clear, simple language**
- **Write in present tense** ("returns" not "will return")
- **Be specific** ("30-60 minutes" not "a while")
- **Use active voice** ("Call the API" not "The API should be called")
- **Define acronyms** on first use

## Integration Example Template

When contributing a new integration, use this template:

```markdown
# [Client Name] Setup

Brief description of the client and what makes it unique.

## Prerequisites

- List any requirements
- Include version numbers if relevant
- Link to installation instructions

## Installation

Step-by-step installation instructions:

1. First step with command
   ```bash
   npm install example
   ```

2. Second step
   ...

## Configuration

1. Locate config file
2. Add MCP server configuration:
   ```json
   {
     "mcpServers": {
       "coderegistry": {
         "command": "npx",
         "args": [...]
       }
     }
   }
   ```

3. Restart the client

## Testing the Integration

Provide a simple test to verify it works:

```
Ask your AI: "What MCP servers are available?"
Expected: Should list "coderegistry" or similar
```

## Usage Example

Show a complete example workflow:

```
[Example prompt or code]
```

## Troubleshooting

### Issue: [Common Problem]
**Symptom:** What users see
**Solution:** How to fix it

### Issue: [Another Problem]
...

## Resources

- [Client Documentation](url)
- [MCP Specification](url)
```

## Community Guidelines

### Be Respectful

- Treat everyone with respect and kindness
- Welcome newcomers and help them learn
- Assume good intentions
- Provide constructive feedback

### Be Professional

- Keep discussions on-topic
- Avoid inflammatory language
- Respect differing viewpoints
- Follow the project's code of conduct

### Be Helpful

- Share your knowledge and experience
- Answer questions when you can
- Provide context and reasoning
- Link to relevant documentation

## Recognition

Contributors will be:

- Credited in release notes
- Listed in CONTRIBUTORS.md
- Acknowledged in project README
- Invited to contributor discussions

Significant contributors may be offered:

- Beta access to new features
- Input on roadmap priorities
- Promotional opportunities

## Questions?

- **General questions**: support@thecoderegistry.com
- **Technical discussions**: Open a GitHub Discussion
- **Security issues**: security@thecoderegistry.com (do not open public issues)
- **Partnership inquiries**: partnerships@thecoderegistry.com

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

**Thank you for contributing to The Code Registry MCP Server!** 

Your contributions help make code intelligence accessible to business leaders worldwide. 🚀
