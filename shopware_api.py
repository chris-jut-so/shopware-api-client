import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import base64


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

    def update_product(self, product_id: str, data: Dict) -> Dict:
        """
        Update a product with the given data.
        
        Args:
            product_id (str): The ID of the product to update
            data (Dict): The data to update. Only include fields that need to be updated.
                        Example: {"name": "New Name", "active": True}
        
        Returns:
            Dict: Status information about the update
        
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.api_url}/api/product/{product_id}"
        
        response = requests.patch(
            url,
            headers=self._get_headers(),
            json=data
        )
        
        response.raise_for_status()
        
        # Shopware returns 204 No Content on successful updates
        if response.status_code == 204:
            return {
                "success": True,
                "message": "Product updated successfully",
                "product_id": product_id
            }
            
        # In case the API changes and returns content
        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "success": True,
                "message": "Product updated successfully (no content)",
                "product_id": product_id
            } 