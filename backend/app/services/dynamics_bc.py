import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app.core.config import settings

class DynamicsBCService:
    def __init__(self):
        self.base_url = settings.DYNAMICS_BC_BASE_URL
        self.company_id = settings.DYNAMICS_BC_COMPANY_ID
        self.environment = settings.DYNAMICS_BC_ENVIRONMENT
        self.client_id = settings.DYNAMICS_BC_CLIENT_ID
        self.client_secret = settings.DYNAMICS_BC_CLIENT_SECRET
        self.tenant_id = settings.DYNAMICS_BC_TENANT_ID
        self.access_token = None
        self.token_expires = datetime.now()
    
    def _get_access_token(self) -> str:
        """Get OAuth access token for Dynamics BC API"""
        if self.access_token and self.token_expires > datetime.now():
            return self.access_token
        
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': f'{self.base_url}/.default'
        }
        
        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expires = datetime.now() + timedelta(seconds=token_data['expires_in'] - 300)
            
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Error getting Dynamics BC token: {e}")
            # In a real app, raise a specific exception or handle appropriately
            raise Exception("Failed to authenticate with Dynamics BC")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Dynamics BC API requests"""
        return {
            'Authorization': f'Bearer {self._get_access_token()}',
            'Content-Type': 'application/json'
        }
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get all items (products) from Dynamics BC"""
        url = f"{self.base_url}/v2.0/{self.environment}/api/v2.0/companies({self.company_id})/items"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json().get('value', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching items from Dynamics BC: {e}")
            return []
    
    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific item by ID"""
        url = f"{self.base_url}/v2.0/{self.environment}/api/v2.0/companies({self.company_id})/items({item_id})"
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching item {item_id} from Dynamics BC: {e}")
            return None
    
    def get_item_ledger_entries(self, item_id: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get item ledger entries (sales data) from Dynamics BC"""
        url = f"{self.base_url}/v2.0/{self.environment}/api/v2.0/companies({self.company_id})/itemLedgerEntries"
        
        # Build filter
        filters = []
        if item_id:
            # Assuming item_id is the Dynamics BC GUID for the item
            filters.append(f"itemId eq {item_id}") # Use the correct field name if different
        if start_date:
            filters.append(f"postingDate ge {start_date}")
        if end_date:
            filters.append(f"postingDate le {end_date}")
        
        params = {}
        if filters:
            filter_str = " and ".join(filters)
            params['$filter'] = filter_str
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json().get('value', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching item ledger entries from Dynamics BC: {e}")
            return []
    
    def get_inventory_levels(self, item_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get current inventory levels from Dynamics BC"""
        # Note: The exact endpoint for inventory might differ based on BC version/customization.
        # This uses a common pattern, adjust if needed.
        base_item_url = f"{self.base_url}/v2.0/{self.environment}/api/v2.0/companies({self.company_id})/items"
        
        inventory_data = []
        try:
            if item_id:
                # Fetch inventory for a specific item
                item_url = f"{base_item_url}({item_id})"
                response = requests.get(item_url, headers=self._get_headers(), params={'$expand': 'itemInventory'})
                response.raise_for_status()
                item_data = response.json()
                # Extract inventory info (adjust field names as needed)
                inventory_info = {
                    'itemId': item_data.get('id'),
                    'itemNumber': item_data.get('number'),
                    'quantityOnHand': item_data.get('inventory', 0) # Example field
                }
                inventory_data.append(inventory_info)
            else:
                # Fetch inventory for all items (might need pagination in real app)
                response = requests.get(base_item_url, headers=self._get_headers(), params={'$expand': 'itemInventory'})
                response.raise_for_status()
                items = response.json().get('value', [])
                for item_data in items:
                    inventory_info = {
                        'itemId': item_data.get('id'),
                        'itemNumber': item_data.get('number'),
                        'quantityOnHand': item_data.get('inventory', 0) # Example field
                    }
                    inventory_data.append(inventory_info)
            return inventory_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching inventory levels from Dynamics BC: {e}")
            return []

