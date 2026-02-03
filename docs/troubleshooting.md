# Troubleshooting

## Cold start timeouts
Our MCP server host may scale to zero; the first request can time out. Retry with exponential backoff.

## Analysis still processing
If `status` is `processing`, wait and retry `get-code-vault-summary` and `get-code-vault-results`.

## Permission errors
Ensure the `X-API-Key` is set and belongs to the team that owns the vault.

## Network issues
For GIT/FILE_ARCHIVE sources, verify the URL is reachable by The Code Registry's platform at analysis time.
If IP addresses need to be whitelisted so these code sources can be accessed, we have this information from our knowledge base:

### Whitelisting The Code Registry's IP addresses in your GIT provider
Some GIT repository providers - for example GitHub Enterprise - allow you to whitelist a specific set of IP addresses that are allowed to access your repositories.

In these cases, you'll also need to whitelist The Code Registry's IP addresses so that we can sync your repository properly.

Because our infrastructure is scalable and we have various services that do different jobs, we don't have a single fixed IP address. We have a range of IP addresses - any of which could be used - so they all need to be whitelisted.

#### GitHub Enterprise users - install our app
If you're using GitHub Enterprise with an IP allow list, you can install our Enterprise GitHub app and allow our app to automatically add our IP addresses to your allow list:

First, allow GitHub apps to update your IP allow list by following these instructions from GitHub:

https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps

Then install this app for your GitHub organization, and that should be it!

https://github.com/apps/the-code-registry-enterprise

#### GitLab self-hosted users - manually add our IP addresses
Unfortunately, GitLab doesn't provide a way to automate the process of managing IP allow lists, unlike some other Git providers. This means you'll need to manually add our IP addresses to ensure The Code Registry can access your repositories.

This only applies if you restrict API calls to your GitLab instance, or the ability for users to run "git clone" commands on your GitLab instance repositories.

The process for self-hosted GitLab instances depends on your specific server configuration. Generally, you'll need to:

1. Contact your GitLab administrator or your IT department.
2. Provide them with our list of IP addresses (find these below).
3. Ask them to add these IP addresses to your GitLab server's firewall allow list.

If you're the GitLab administrator:

1. Access your GitLab server.
2. Update your firewall rules to allow incoming connections from our IP addresses.
3. The exact commands will depend on your firewall software. For UFW (Uncomplicated Firewall), you would use something like this for each IP address:
```
sudo ufw allow from <IP_ADDRESS> to any port 80 proto tcp
sudo ufw allow from <IP_ADDRESS> to any port 443 proto tcp
```
Replace `<IP_ADDRESS>` with each of our IP addresses.

Note:
* Port 80 is for HTTP access (which typically redirects to HTTPS)
* Port 443 is for HTTPS access (for both web and API access)
* We don't need to open port 22 (SSH) because GitLab allows cloning over HTTPS

4. Remember to apply the changes to your firewall after adding all the rules.

#### The full IP address list
Here's the full list of addresses that need to be whitelisted:

```
52.151.232.37
52.179.115.85
52.188.38.160
20.42.34.0
20.42.34.103
20.42.34.127
20.42.36.182
20.42.37.79
20.42.39.183
52.188.40.50
52.188.40.190
52.188.40.212
52.188.42.76
52.188.42.131
52.188.43.40
52.188.43.177
52.188.43.221
52.188.44.142
52.188.74.218
52.142.29.202
52.147.216.212
52.147.216.250
52.147.217.187
52.147.217.236
20.49.104.9
52.188.142.126
52.188.143.57
52.188.141.62
40.71.232.88
40.71.233.96
40.71.233.218
40.71.234.29
40.71.234.60
40.71.235.182
40.71.236.158
40.71.237.2
40.71.237.25
40.71.238.120
40.71.238.125
52.151.238.38
40.71.238.146
40.71.238.252
40.71.239.94
20.75.135.76
20.75.135.109
20.75.132.243
20.75.135.148
20.75.135.175
20.75.132.169
20.49.104.23
4.156.128.35
4.156.128.71
4.156.128.99
4.156.128.113
4.156.130.122
4.156.128.55
20.102.24.20
20.241.132.109
20.241.132.153
20.241.133.48
20.241.134.181
20.241.134.239
20.253.64.249
20.253.65.166
20.253.66.31
20.253.66.60
20.253.66.250
20.253.68.7
20.253.68.145
20.253.69.44
20.253.70.240
20.253.71.136
20.253.71.184
20.253.71.243
4.156.128.35
4.156.128.71
4.156.128.99
4.156.128.113
4.156.130.122
4.156.128.55
4.156.128.91
4.156.130.209
4.156.131.7
4.156.131.102
4.156.131.141
4.156.131.146
20.119.8.58
```

## Web app login problems
Users must login with the same email used to create their MCP account.
