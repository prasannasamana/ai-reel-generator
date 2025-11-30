"""
Simple script to test the API endpoints.
Run this after starting the server to verify everything works.
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_api_info():
    """Test API info endpoint"""
    print("Testing API info endpoint...")
    response = requests.get(f"{BASE_URL}/api/")
    if response.status_code == 200:
        print("✓ API info endpoint works!")
        print(f"  API Name: {response.json()['name']}")
        return True
    else:
        print(f"✗ API info failed: {response.status_code}")
        return False

def test_create_reel(image_path, script):
    """Test creating a reel"""
    print(f"\nTesting create reel endpoint with image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {
                'script': script,
                'tone': 'friendly',
                'use_rewrite': 'true',
                'max_seconds': '30'
            }
            response = requests.post(f"{BASE_URL}/api/reels/", files=files, data=data)
            
            if response.status_code in [200, 201]:
                reel_data = response.json()
                print("✓ Reel created successfully!")
                print(f"  Reel ID: {reel_data['id']}")
                print(f"  Status: {reel_data['status']}")
                return reel_data['id']
            else:
                print(f"✗ Create reel failed: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
    except FileNotFoundError:
        print(f"✗ Image file not found: {image_path}")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def test_list_reels():
    """Test listing reels"""
    print("\nTesting list reels endpoint...")
    response = requests.get(f"{BASE_URL}/api/reels/")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ List reels works! Found {data['count']} reels")
        return True
    else:
        print(f"✗ List reels failed: {response.status_code}")
        return False

def test_get_reel(reel_id):
    """Test getting reel details"""
    print(f"\nTesting get reel endpoint for ID: {reel_id}")
    response = requests.get(f"{BASE_URL}/api/reels/{reel_id}/")
    if response.status_code == 200:
        reel_data = response.json()
        print("✓ Get reel works!")
        print(f"  Status: {reel_data['status']}")
        print(f"  Video URL: {reel_data.get('video_url', 'Not available yet')}")
        return True
    else:
        print(f"✗ Get reel failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("AI Reel Generator API Test")
    print("=" * 50)
    
    # Test API info
    if not test_api_info():
        print("\nMake sure the server is running: python manage.py runserver")
        sys.exit(1)
    
    # Test list reels
    test_list_reels()
    
    # Test create reel (if image provided)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        script = sys.argv[2] if len(sys.argv) > 2 else "Hello, this is a test script for the reel generator API."
        reel_id = test_create_reel(image_path, script)
        
        if reel_id:
            # Test get reel
            test_get_reel(reel_id)
    else:
        print("\nTo test reel creation, provide an image path:")
        print("  python test_api.py path/to/image.jpg 'Your script here'")
    
    print("\n" + "=" * 50)
    print("API Test Complete!")
    print("=" * 50)

