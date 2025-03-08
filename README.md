# Trottola

It might spins around but at the end you will get the HTML.

```json
{
  "url": "https://example.com",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  "headers": {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
  }
}
```

```bash
curl -X POST http://localhost:5000/proxy \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.idealista.it/affitto-case/bologna-bologna/", "user_agent": "Mozilla/5.0", "headers": {"Accept-Language": "en-US,en;q=0.9"}}'
```
