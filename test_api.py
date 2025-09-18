import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_response_details(response):
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response Body: {response.text}")
    print("-" * 50)

def test_api():
    # 1. Get authentication token
    print("Getting authentication token...")
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "test@example.com", "password": "testpassword123"}
    )
    print("\nAttempting to get token...")
    print_response_details(response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Token received successfully!")
    else:
        print("Failed to get token")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a category
    print("\nCreating a category...")
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and accessories"
    }
    response = requests.post(
        f"{BASE_URL}/categories/",
        headers=headers,
        json=category_data
    )
    if response.status_code == 200:
        category = response.json()
        print("Category created successfully:", category)
    else:
        print("Failed to create category:", response.text)
        return

    # 3. Create a product
    print("\nCreating a product...")
    product_data = {
        "name": "Smartphone",
        "description": "Latest model smartphone",
        "price": 999.99,
        "quantity": 10,
        "category_id": category["id"]
    }
    response = requests.post(
        f"{BASE_URL}/products/",
        headers=headers,
        json=product_data
    )
    if response.status_code == 200:
        product = response.json()
        print("Product created successfully:", product)
    else:
        print("Failed to create product:", response.text)
        return

    # 4. List products with filter
    print("\nListing products filtered by category...")
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers,
        params={"category_id": category["id"]}
    )
    if response.status_code == 200:
        products = response.json()
        print("Products in category:", products)
    else:
        print("Failed to list products:", response.text)

    # 5. Export products as JSON
    print("\nExporting products as JSON...")
    response = requests.get(
        f"{BASE_URL}/export/products/json",
        headers=headers
    )
    if response.status_code == 200:
        products = response.json()
        print("Exported products:", products)
    else:
        print("Failed to export products:", response.text)

if __name__ == "__main__":
    test_api()
