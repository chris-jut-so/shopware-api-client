# Shopware Admin API Client

A Python client for interacting with the Shopware Admin API. This client provides a simple interface to access Shopware's API endpoints, with initial support for product management.

## Features

- OAuth2 authentication with automatic token management
- Product retrieval with pagination support
- Product update capabilities
- Environment variable configuration
- Type hints for better code quality

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chris-jut-so/shopware-api-client.git
   cd shopware-api-client
   ```

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

## Configuration

Set up your environment variables in the `.env` file:

```env
SHOPWARE_ACCESS_KEY=your_access_key_here
SHOPWARE_SECRET_KEY=your_secret_key_here
SHOPWARE_API_URL=https://your-shopware-instance.com
```

## Usage

### Basic Usage

```python
from shopware_api import ShopwareAdminAPI

# Initialize the client
api_client = ShopwareAdminAPI(
    access_key="your_access_key",
    secret_key="your_secret_key",
    api_url="https://your-shopware-instance.com"
)

# Get products
products = api_client.get_products(limit=10, page=1)

# Update a product
update_data = {
    "name": "New Product Name",
    "active": True
}
result = api_client.update_product("product_id", update_data)
```

### Using Environment Variables

```python
import os
from dotenv import load_dotenv
from shopware_api import ShopwareAdminAPI

# Load environment variables
load_dotenv()

# Initialize the client using environment variables
api_client = ShopwareAdminAPI(
    access_key=os.getenv('SHOPWARE_ACCESS_KEY'),
    secret_key=os.getenv('SHOPWARE_SECRET_KEY'),
    api_url=os.getenv('SHOPWARE_API_URL')
)
```

### Example Script

Check out `test_api.py` for a complete example of using the API client. Run it with:

```bash
python test_api.py
```

## API Methods

### get_products(limit: int = 10, page: int = 1) -> Dict
Retrieves a list of products with pagination support.

Parameters:
- `limit`: Number of products per page (default: 10)
- `page`: Page number (default: 1)

Returns: Dictionary containing product data and metadata

### update_product(product_id: str, data: Dict) -> Dict
Updates a product with the specified data.

Parameters:
- `product_id`: The ID of the product to update
- `data`: Dictionary containing the fields to update

Returns: Dictionary with update status information

Example update data:
```python
update_data = {
    "name": "New Product Name",
    "active": True,
    "stock": 100,
    "price": [{
        "currencyId": "...",
        "gross": 99.99,
        "net": 83.99,
        "linked": True
    }]
}
```

## Error Handling

The API client uses requests' built-in error handling. All methods may raise:
- `requests.exceptions.RequestException`: Base exception class for all requests exceptions
- `requests.exceptions.HTTPError`: Raised for 4XX and 5XX status codes
- `ValueError`: Raised for invalid input or missing configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 