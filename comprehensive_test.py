import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_test_header(test_name):
    print("\n" + "="*50)
    print(f"Testing: {test_name}")
    print("="*50)

def print_response(response, description):
    print(f"\n{description}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print("-"*50)

def test_api():
    # 1. Authentication Tests
    print_test_header("Authentication")
    
    # Get token
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "admin@example.com", "password": "testpass123"}
    )
    print_response(response, "Login attempt")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print("Authentication failed! Cannot continue tests.")
        return

    # 2. Category Tests
    print_test_header("Categories")

    # Create new category
    new_category = {
        "name": "Test Category",
        "description": "This is a test category"
    }
    response = requests.post(
        f"{BASE_URL}/categories/",
        headers=headers,
        json=new_category
    )
    print_response(response, "Create category")
    test_category_id = response.json()["id"]

    # List all categories
    response = requests.get(
        f"{BASE_URL}/categories/",
        headers=headers
    )
    print_response(response, "List all categories")

    # Get specific category
    response = requests.get(
        f"{BASE_URL}/categories/{test_category_id}",
        headers=headers
    )
    print_response(response, f"Get category {test_category_id}")

    # 3. Product Tests
    print_test_header("Products")

    # Create new product
    new_product = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99,
        "quantity": 50,
        "category_id": test_category_id
    }
    response = requests.post(
        f"{BASE_URL}/products/",
        headers=headers,
        json=new_product
    )
    print_response(response, "Create product")
    test_product_id = response.json()["id"]

    # List all products
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers
    )
    print_response(response, "List all products")

    # Get specific product
    response = requests.get(
        f"{BASE_URL}/products/{test_product_id}",
        headers=headers
    )
    print_response(response, f"Get product {test_product_id}")

    # Filter products by category
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers,
        params={"category_id": test_category_id}
    )
    print_response(response, f"Filter products by category {test_category_id}")

    # Search products by name
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers,
        params={"name": "Test"}
    )
    print_response(response, "Search products by name 'Test'")

    # Update product
    updated_product = {
        "name": "Updated Test Product",
        "description": "This is an updated test product",
        "price": 149.99,
        "quantity": 75,
        "category_id": test_category_id
    }
    response = requests.put(
        f"{BASE_URL}/products/{test_product_id}",
        headers=headers,
        json=updated_product
    )
    print_response(response, f"Update product {test_product_id}")

    # 4. Export Tests
    print_test_header("Export Functionality")

    # Export as JSON
    response = requests.get(
        f"{BASE_URL}/export/products/json",
        headers=headers
    )
    print_response(response, "Export products as JSON")

    # Export as CSV
    response = requests.get(
        f"{BASE_URL}/export/products/csv",
        headers=headers
    )
    print_response(response, "Export products as CSV")

    # 5. Cleanup Test
    print_test_header("Cleanup")

    # Delete test product
    response = requests.delete(
        f"{BASE_URL}/products/{test_product_id}",
        headers=headers
    )
    print_response(response, f"Delete product {test_product_id}")

    print("\nTest suite completed!")

if __name__ == "__main__":
    test_api()
