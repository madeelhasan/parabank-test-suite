"""Opens an account through the UI, then verifies it exists via the REST API."""
from pages.open_account_page import OpenAccountPage


def test_new_account_is_visible_via_api(logged_in_page, funded_account_ids, api_client, customer_id):
    from_id, _ = funded_account_ids

    open_account_page = OpenAccountPage(logged_in_page).navigate()
    new_account_id = open_account_page.open_account(OpenAccountPage.CHECKING, from_id)

    response = api_client.get_account(new_account_id)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == int(new_account_id)
    assert body["customerId"] == customer_id
    assert body["type"] == "CHECKING"

    accounts = api_client.get_customer_accounts(customer_id).json()
    assert new_account_id in [str(acc["id"]) for acc in accounts]
