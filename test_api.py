import os
from datetime import datetime
from dotenv import load_dotenv
from shopware_api import ShopwareAdminAPI

def main():
    # Load environment variables from .env file
    load_dotenv()
    
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
        # Example 1: Get products
        print("\nExample 1: Fetching products...")
        products = api_client.get_products(limit=1, page=1)
        
        if not products.get('data'):
            print("No products found!")
            return
        
        # Get the first product's ID and details
        product_id = products['data'][0]['id']
        original_name = products['data'][0].get('name', 'Unknown')
        
        print(f"\nFound product:")
        print(f"ID: {product_id}")
        print(f"Original name: {original_name}")
        
        # Example 2: Update a product
        print("\nExample 2: Updating product...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_data = {
            "name": f"{original_name} (Updated at {timestamp})"
        }
        
        result = api_client.update_product(product_id, update_data)
        print(f"Update status: {result['message']}")
        
        # Verify the update
        print("\nVerifying update...")
        updated_product = api_client.get_products(limit=1, page=1)
        
        if updated_product.get('data'):
            updated_name = updated_product['data'][0].get('name', 'Unknown')
            print(f"New name: {updated_name}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main() 