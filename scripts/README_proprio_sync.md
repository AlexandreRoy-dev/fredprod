# Sync Proprio Direct listings (Frédéric Roy)

Discovers listings from [Frédéric’s Proprio Direct page](https://propriodirect.com/frederic-roy/), downloads full photo galleries from Centris (fallback: Proprio Direct CDN for sold), generates **1200×630** share images, rebuilds `proprietes.html` + SEO detail pages, and updates homepage map pins.

## Local run

```bash
pip install -r scripts/requirements.txt
python scripts/proprio_sync.py
```

Useful flags: `--exclude-sold`, `--max-listings 20`, `--skip-generate`

## Outputs

- `data/properties.json`, `data/listings_sync.json`, `data/transaction_pins.json`
- `assets/img/proprietes/<uls>/`
- `proprietes.html` + `ca/qc/.../`

## GitHub Actions

`.github/workflows/proprio-sync.yml` (daily + manual). Optional var: `PROPRIO_AGENT_URL`.
