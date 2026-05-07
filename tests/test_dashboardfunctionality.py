from pages.dashboard import Dashboard
from playwright.sync_api import Page
import pytest

dashboardObj = Dashboard()

def test_signoutfunctionality(login,page:Page):
    logout = dashboardObj.signout(page)
    assert logout == "Logout Successfully"

def test_emptycartverification(login,page:Page):
    dashboardObj.carts(page)
    assert page.locator("div.ng-star-inserted>h1").inner_text().strip() == "No Products in Your Cart !"

def test_cartwithitems(login,page:Page):
    # page.pause()
    dashboardObj.carts(page)
    assert page.locator("ul.cartWrap").count() > 0

def test_additem(login,page:Page):
    productadded = dashboardObj.additemtocart(page,"ADIDAS ORIGINAL")
    assert productadded == "Product Added To Cart"

def test_searchitem(login,page:Page):
    items = dashboardObj.searchfunctionlity(page,"ZARA")
    assert items > 0

def test_view_functionality(login,page:Page):
    item = dashboardObj.viewbutton(page,"ADIDAS ORIGINAL")
    assert item == "ADIDAS ORIGINAL"
