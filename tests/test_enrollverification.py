import pytest
from pages.registration import Register
from pages.login import Login
from playwright.sync_api import Page
import json

registerObj = Register()
loginObj = Login()

with open("credentials.json") as f:
    test_data = json.load(f)
    test_data_list = test_data['user_credentials']


def test_verifyregisterfunctionality(page:Page):
    
    text = registerObj.register(page,"Leena","Chouhan","leenaA@gmail.com","1234567890","Engineer","Female","Leena@123","Leena@123")
    assert text == "Account Created Successfully"

@pytest.mark.parametrize('testing_data',test_data_list)
def test_loginfunctionality(page:Page,testing_data):
    title = loginObj.login(page,testing_data['username'],testing_data['password'])
    assert title == "Let's Shop"
    
