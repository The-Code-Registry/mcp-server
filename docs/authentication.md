# Authentication

## create_account
`create_account` is the only action that does not require an API key.
The response includes:
- `credentials.api_key`
- `user.id`
- `team.id`

## API key usage
For all other actions, include the API key in the request header:

```
X-API-Key: <api_key>
```

If your MCP client cannot set custom headers, pass the key inside tool arguments as `api_key`. Header auth is preferred when available.

## Web app access
Users can view analysis results in the web app at:
https://app.thecoderegistry.com

They'll need to login with the same email address used to create their account via MCP.
