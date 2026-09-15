"""Thin wrapper around ParaBank's REST endpoints (parabank/services/bank/*)."""
import requests


class ParaBankApiClient:
    def __init__(self, base_url: str):
        self.base_url = f"{base_url.rstrip('/')}/services/bank"
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/login/{username}/{password}")

    def get_customer_accounts(self, customer_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/customers/{customer_id}/accounts")

    def get_account(self, account_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/accounts/{account_id}")

    def get_transactions(self, account_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/accounts/{account_id}/transactions")
