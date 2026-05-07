from playwright.sync_api import Page
import pytest
import json


with open("credentials.json") as f:
    test_data = json.load(f)
    test_data_list = test_data['correct_credentials']
    username = test_data_list['username']
    password = test_data_list['password']

@pytest.fixture()
def login(page:Page):
        page.goto("https://rahulshettyacademy.com/client/#/auth/login")
        page.get_by_placeholder("email@example.com").fill(username)
        page.locator("#userPassword").fill(password)
        page.get_by_role("button",name="Login").click()