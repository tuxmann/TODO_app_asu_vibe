"""
Test script for authentication routes
Run the FastAPI app first, then run this script
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_auth_routes():
    """Test all authentication routes"""
    
    print_section("Testing Authentication Routes")
    
    # Test data
    test_user = {
        "username": "test_auth_user",
        "password": "TestAuth123",
        "email": "testauth@example.com",
        "full_name": "Test Auth User"
    }
    
    # 1. Register a new user
    print("\n1️⃣  Testing User Registration (POST /auth/register)")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            user_data = response.json()
            print(f"   ✅ User registered successfully!")
            print(f"   📝 Username: {user_data['username']}")
            print(f"   📧 Email: {user_data['email']}")
            print(f"   🆔 ID: {user_data['id']}")
        elif response.status_code == 400:
            print(f"   ℹ️  User might already exist: {response.json()['detail']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Login with form data (OAuth2)
    print("\n2️⃣  Testing Login with Form Data (POST /auth/login)")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login successful!")
            print(f"   🔑 Token: {access_token[:50]}...")
            print(f"   📋 Type: {token_data['token_type']}")
        else:
            print(f"   ❌ Error: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 3. Login with JSON
    print("\n3️⃣  Testing Login with JSON (POST /auth/login/json)")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/json",
            json={
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ JSON login successful!")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Test wrong password
    print("\n4️⃣  Testing Wrong Password")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": test_user["username"],
                "password": "WrongPassword123"
            }
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Wrong password correctly rejected!")
        else:
            print(f"   ❌ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Get current user info
    print("\n5️⃣  Testing Get Current User (GET /auth/me)")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ User info retrieved!")
            print(f"   👤 Username: {user_data['username']}")
            print(f"   📧 Email: {user_data['email']}")
            print(f"   🟢 Active: {user_data['is_active']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Test authentication test endpoint
    print("\n6️⃣  Testing Auth Test Endpoint (GET /auth/test)")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"{BASE_URL}/auth/test",
            headers=headers
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
            print(f"   👤 Username: {data['username']}")
            print(f"   🔐 Superuser: {data['is_superuser']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 7. Refresh token
    print("\n7️⃣  Testing Token Refresh (POST /auth/refresh)")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            headers=headers
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            new_token_data = response.json()
            new_token = new_token_data["access_token"]
            print(f"   ✅ Token refreshed!")
            print(f"   🔑 New Token: {new_token[:50]}...")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 8. Test without token (should fail)
    print("\n8️⃣  Testing Without Token (Should Fail)")
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected request without token!")
        else:
            print(f"   ❌ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 9. Test with invalid token
    print("\n9️⃣  Testing With Invalid Token (Should Fail)")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Correctly rejected invalid token!")
        else:
            print(f"   ❌ Unexpected response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 10. Logout
    print("\n🔟 Testing Logout (POST /auth/logout)")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(
            f"{BASE_URL}/auth/logout",
            headers=headers
        )
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
            print(f"   📝 {data['detail']}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print_section("All Tests Completed!")
    print("\n💡 Tips:")
    print("   - Check the API docs at: http://localhost:8000/docs")
    print("   - Use the 'Authorize' button in Swagger UI to test with tokens")
    print("   - Token expires in 30 minutes by default")
    print()

if __name__ == "__main__":
    print("\n🚀 Authentication Routes Test Script")
    print("=" * 60)
    print("⚠️  Make sure the FastAPI server is running!")
    print("   Run: python -m app.main")
    print("   Or: uvicorn app.main:app --reload")
    print()
    
    try:
        test_auth_routes()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
