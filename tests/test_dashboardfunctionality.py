from pages.dashboard import Dashboard
from playwright.sync_api import Page
import pytest
import json

dashboardObj = Dashboard()

with open("testdata/dashboard.json") as f:
    test_data = json.load(f)

@pytest.mark.signout
def test_signoutfunctionality(login,page:Page):
    logout = dashboardObj.signout(page)
    assert logout == test_data['logout']

@pytest.mark.cart
def test_emptycartverification(login,page:Page):
    dashboardObj.carts(page)
    assert page.locator("div.ng-star-inserted>h1").inner_text().strip() == test_data['emptycart']

@pytest.mark.cart
@pytest.mark.xfail(reason="expected failure")
def test_cartwithitems(login,page:Page):
    # page.pause()
    dashboardObj.carts(page)
    assert page.locator("ul.cartWrap").count() > 0

@pytest.mark.item
def test_additem(login,page:Page):
    productadded = dashboardObj.additemtocart(page,test_data['item'])
    assert productadded == test_data['productadded']

@pytest.mark.item
def test_searchitem(login,page:Page):
    items = dashboardObj.searchfunctionlity(page,test_data['item2'])
    assert items > 0

@pytest.mark.view
def test_view_functionality(login,page:Page):
    item = dashboardObj.viewbutton(page,test_data['item'])
    assert item == test_data['item']
