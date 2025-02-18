# Shopware API Client

A Python client for interacting with the Shopware Admin API. This client provides a simple interface to access Shopware's API endpoints, with initial support for product retrieval.

## Features

- OAuth2 authentication with automatic token management
- Product retrieval with pagination support
- Environment variable configuration
- Type hints for better code quality

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Shopware API credentials:
   ```bash
   cp .env.example .env
   ```

## Usage

```python
from shopware_api_example import ShopwareAdminAPI

api_client = ShopwareAdminAPI(access_key, secret_key, api_url)
products = api_client.get_products(limit=10, page=1)
```

## Environment Variables

- `SHOPWARE_ACCESS_KEY`: Your Shopware API access key
- `SHOPWARE_SECRET_KEY`: Your Shopware API secret key
- `SHOPWARE_API_URL`: Your Shopware instance URL 