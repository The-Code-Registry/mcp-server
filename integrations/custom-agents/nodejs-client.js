const https = require('https')

const data = JSON.stringify({
  jsonrpc: '2.0',
  method: 'tools/call',
  params: {
    name: 'list_projects',
    arguments: {}
  },
  id: 1
})

const req = https.request(
  'https://integrator.app.thecoderegistry.com/api/ai/router',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length,
      'X-API-Key': 'your-api-key'
    }
  },
  res => {
    let body = ''
    res.on('data', chunk => (body += chunk))
    res.on('end', () => {
      const payload = JSON.parse(body)
      const text = payload.result.content[0].text
      console.log(JSON.parse(text))
    })
  }
)

req.on('error', console.error)
req.write(data)
req.end()
