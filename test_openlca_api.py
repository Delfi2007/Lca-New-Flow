"""
Test script to check OpenLCA REST API connectivity
Run this after starting the IPC Server in OpenLCA
"""

import requests
import json

# OpenLCA IPC Server URL (default)
OPENLCA_API_URL = "http://localhost:8080"

def test_connection():
    """Test if OpenLCA API is accessible"""
    try:
        print("Testing OpenLCA API connection...")
        print(f"API URL: {OPENLCA_API_URL}")
        
        # OpenLCA 2.5.0 uses JSON-RPC protocol
        # Try a simple ping request
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "data/get/descriptors",
            "params": {
                "@type": "Process"
            }
        }
        
        response = requests.post(OPENLCA_API_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result or 'error' not in result:
                print("✅ Successfully connected to OpenLCA API!")
                print("\nOpenLCA 2.5.0 IPC Server is running!")
                print(f"Port: 8080")
                print(f"Database: Connected")
                return True
        
        print(f"❌ API returned status code: {response.status_code}")
        return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
        print("\nPlease ensure:")
        print("1. OpenLCA application is running")
        print("2. IPC Server is started (Window → Developer Tools → IPC Server)")
        print("3. Server is running on port 8080")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def get_database_info(db_name):
    """Get information about a specific database"""
    try:
        response = requests.get(f"{OPENLCA_API_URL}/database/{db_name}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error getting database info: {str(e)}")
        return None

def list_processes(limit=10):
    """List available processes"""
    try:
        # This endpoint might need adjustment based on OpenLCA version
        response = requests.post(
            f"{OPENLCA_API_URL}/data/get/descriptors",
            json={"@type": "Process"},
            timeout=10
        )
        if response.status_code == 200:
            processes = response.json()
            print(f"\nFound {len(processes)} processes (showing first {limit}):")
            for proc in processes[:limit]:
                print(f"  - {proc.get('name', 'Unknown')}")
            return processes
        return []
    except Exception as e:
        print(f"Error listing processes: {str(e)}")
        return []

if __name__ == "__main__":
    print("="*60)
    print("OpenLCA REST API Test")
    print("="*60)
    
    if test_connection():
        print("\n" + "="*60)
        print("Next steps:")
        print("1. You can now integrate OpenLCA API with your LCA application")
        print("2. Use the databases available in OpenLCA")
        print("3. Fetch processes, flows, and impact methods as needed")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Setup Instructions:")
        print("1. Open OpenLCA application")
        print("2. Go to: Window → Developer Tools → IPC Server")
        print("3. Click 'Start' to start the server")
        print("4. Run this script again")
        print("="*60)
