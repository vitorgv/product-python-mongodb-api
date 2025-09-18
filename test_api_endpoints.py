import requests
import json
from datetime import datetime
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "admin@example.com",
    "password": "testpass123"
}

def print_response(description, response, show_body=True):
    """Print formatted response details"""
    print(f"\n{Fore.CYAN}Testing: {description}{Style.RESET_ALL}")
    print(f"Status Code: {response.status_code}")
    if show_body:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    print("-" * 50)
    return response.status_code == 200

def run_test(description, func):
    """Run a test function with error handling"""
    try:
        result = func()
        if result:
            print(f"{Fore.GREEN}✓ {description} - Passed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {description} - Failed{Style.RESET_ALL}")
        return result
    except Exception as e:
        print(f"{Fore.RED}✗ {description} - Error: {str(e)}{Style.RESET_ALL}")
        return False

def test_authentication():
    """Test authentication endpoint"""
    print(f"\n{Fore.YELLOW}=== Testing Authentication ==={Style.RESET_ALL}")
    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    success = print_response("Login", response)
    if success:
        return response.json()["access_token"]
    return None

def test_categories(token):
    """Test category endpoints"""
    print(f"\n{Fore.YELLOW}=== Testing Categories ==={Style.RESET_ALL}")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create category
    category_data = {
        "name": f"Test Category {datetime.now().strftime('%H:%M:%S')}",
        "description": "Test category description"
    }
    response = requests.post(
        f"{BASE_URL}/categories/",
        headers=headers,
        json=category_data
    )
    success = print_response("Create category", response)
    if not success:
        return None
    
    category_id = response.json()["id"]
    
    # List categories
    response = requests.get(
        f"{BASE_URL}/categories/",
        headers=headers
    )
    print_response("List categories", response)
    
    # Get specific category
    response = requests.get(
        f"{BASE_URL}/categories/{category_id}",
        headers=headers
    )
    print_response(f"Get category {category_id}", response)
    
    return category_id

def test_products(token, category_id):
    """Test product endpoints"""
    print(f"\n{Fore.YELLOW}=== Testing Products ==={Style.RESET_ALL}")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create product
    product_data = {
        "name": f"Test Product {datetime.now().strftime('%H:%M:%S')}",
        "description": "Test product description",
        "price": 99.99,
        "quantity": 50,
        "category_id": category_id
    }
    response = requests.post(
        f"{BASE_URL}/products/",
        headers=headers,
        json=product_data
    )
    success = print_response("Create product", response)
    if not success:
        return None
    
    product_id = response.json()["id"]
    
    # List products
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers
    )
    print_response("List all products", response)
    
    # Filter products by category
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers,
        params={"category_id": category_id}
    )
    print_response(f"Filter products by category {category_id}", response)
    
    # Search products by name
    response = requests.get(
        f"{BASE_URL}/products/",
        headers=headers,
        params={"name": "Test"}
    )
    print_response("Search products by name", response)
    
    # Update product
    update_data = {
        "name": f"Updated Test Product {datetime.now().strftime('%H:%M:%S')}",
        "description": "Updated test product description",
        "price": 149.99,
        "quantity": 75,
        "category_id": category_id
    }
    response = requests.put(
        f"{BASE_URL}/products/{product_id}",
        headers=headers,
        json=update_data
    )
    print_response(f"Update product {product_id}", response)
    
    return product_id

def test_export(token):
    """Test export functionality"""
    print(f"\n{Fore.YELLOW}=== Testing Export Functionality ==={Style.RESET_ALL}")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Export as JSON
    response = requests.get(
        f"{BASE_URL}/export/products/json",
        headers=headers
    )
    print_response("Export products as JSON", response)
    
    # Export as CSV
    response = requests.get(
        f"{BASE_URL}/export/products/csv",
        headers=headers
    )
    print_response("Export products as CSV", response, show_body=False)

def test_cleanup(token, product_id):
    """Test cleanup (delete) operations"""
    print(f"\n{Fore.YELLOW}=== Testing Cleanup ==={Style.RESET_ALL}")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Delete product
    response = requests.delete(
        f"{BASE_URL}/products/{product_id}",
        headers=headers
    )
    print_response(f"Delete product {product_id}", response)

def main():
    """Main test runner"""
    print(f"{Fore.GREEN}Starting API Tests...{Style.RESET_ALL}")
    print(f"Testing API at: {BASE_URL}")
    print("-" * 50)
    
    # Test authentication
    token = test_authentication()
    if not token:
        print(f"{Fore.RED}Authentication failed. Cannot continue tests.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Test categories
    category_id = test_categories(token)
    if not category_id:
        print(f"{Fore.RED}Category creation failed. Cannot continue tests.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Test products
    product_id = test_products(token, category_id)
    if not product_id:
        print(f"{Fore.RED}Product creation failed. Cannot continue tests.{Style.RESET_ALL}")
        sys.exit(1)
    
    # Test export functionality
    test_export(token)
    
    # Test cleanup
    test_cleanup(token, product_id)
    
    print(f"\n{Fore.GREEN}All tests completed successfully!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
