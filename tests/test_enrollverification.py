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

with open("testdata/enrollverification.json") as f:
    signupdata = json.load(f)

@pytest.mark.signup
def test_verifyregisterfunctionality(page:Page):
    text = registerObj.register(page,signupdata['firstname'],signupdata['lastname'],signupdata['email'],signupdata['phonenumber'],signupdata['occupation'],signupdata['gender'],signupdata['password'],signupdata['confirmpassword'])
    assert text == signupdata['accountcreationmessage']

@pytest.mark.parametrize('testing_data',test_data_list)
def test_loginfunctionality(page:Page,testing_data):
    title = loginObj.login(page,testing_data['username'],testing_data['password'])
    assert title == "Let's Shop"
    
