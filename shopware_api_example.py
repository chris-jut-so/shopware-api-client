import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ShopwareAdminAPI:
    def __init__(self, access_key: str, secret_key: str, api_url: str):
        """
        Initialize the Shopware Admin API client.
        
        Args:
            access_key (str): The access key for authentication
            secret_key (str): The secret key for authentication
            api_url (str): The base URL of your Shopware instance
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_url = api_url.rstrip('/')
        self.token = None
        self.token_expires = None

    def _get_authentication_token(self) -> str:
        """
        Get the OAuth access token for API authentication.
        
        Returns:
            str: The access token
        """
        auth_string = f"{self.access_key}:{self.secret_key}"
        auth_base64 = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{self.api_url}/api/oauth/token",
            headers=headers,
            json={
                "grant_type": "client_credentials"
            }
        )
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expires = datetime.now().timestamp() + token_data['expires_in']
        
        return self.token

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers required for API requests.
        
        Returns:
            Dict[str, str]: Headers dictionary
        """
        if not self.token or datetime.now().timestamp() >= self.token_expires:
            self._get_authentication_token()
            
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_products(self, limit: int = 10, page: int = 1) -> Dict:
        """
        Retrieve products from Shopware.
        
        Args:
            limit (int): Number of products per page
            page (int): Page number
        
        Returns:
            Dict: Response containing products and metadata
        """
        params = {
            'limit': limit,
            'page': page
        }
        
        response = requests.get(
            f"{self.api_url}/api/product",
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        
        return response.json()


def main():
    # Get configuration from environment variables
    access_key = os.getenv('SHOPWARE_ACCESS_KEY')
    secret_key = os.getenv('SHOPWARE_SECRET_KEY')
    api_url = os.getenv('SHOPWARE_API_URL')

    # Validate environment variables
    if not all([access_key, secret_key, api_url]):
        raise ValueError("Missing required environment variables. Please check your .env file.")
    
    # Initialize API client
    api_client = ShopwareAdminAPI(access_key, secret_key, api_url)
    
    try:
        # Get products
        products = api_client.get_products(limit=1, page=1)
        
        # Print results
        print("Retrieved products:")
        print(json.dumps(products, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching products: {e}")

if __name__ == "__main__":
    main() 