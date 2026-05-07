import pytest
from playwright.sync_api import Page
import time
from playwright.sync_api import expect
import json

with open("credentials.json") as f:
    test_data = json.load(f)
    user_credentials_list = test_data["user_credentials"]

def test_firstcase(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://google.com")
    

def test_secondcase(page:Page):
    page.goto("https://google.com")
    # page.locator(".truncate").fill("hello")
    page.get_by_role("combobox").fill("hello")

@pytest.mark.parametrize('credential',user_credentials_list)
# @pytest.fixture
def test_login(page:Page,credential):
    page.goto("https://amazon.in")
    # page.pause()
    # time.sleep(5)
    # page.get_by_text("Hello, sign in").click()
    page.locator("#nav-link-accountList-nav-line-1").click()
    # page.get_by_role("button",name="Sign in").click()
    page.locator("#ap_email_login").fill(credential["username"])
    page.get_by_role("button").click()
    page.locator("#ap_password").fill(credential["password"])
    page.get_by_role("button",name="Sign in").click()
    page.wait_for_load_state("domcontentloaded")
    assert page.title() == "Online Shopping site in India: Shop Online for Mobiles, Books, Watches, Shoes and More - Amazon.in"


def test_addtocart(login,page:Page):   #add item to cart
    page.get_by_role("searchbox").fill("I phone 16")
    page.locator("#nav-search-submit-button").click()
    product = page.locator(
        "[data-component-type='s-search-result']"
    ).filter(
        has=page.locator("h2 span", has_text="Apple iPhone 15")
    ).first
    # Click Add to Cart inside that product
    product.locator("button:has-text('Add to cart')").click()
    time.sleep(5)

def test_removeitem(login,page:Page):   #remove item from cart
    page.locator(".nav-cart-icon").click()
    page.pause()
    # page.locator("h3 span.a-truncate:has-text('OnePlus 15R')").click()
    # item = page.locator("ul.a-unordered-list").filter(has=page.locator("h3 span.a-truncate:has-text('OnePlus 15R')"))
    item = page.locator("ul[data-name='Active Items'].a-unordered-list>div").filter(has=page.locator("h3 span",has_text='OnePlus 15R'))
    item.locator("button[data-a-selector='decrement']").click()

def test_logout(login,page:Page):   #logout functionality
    data = page.locator("#nav-link-accountList-nav-line-1").text_content()
    print(data)
    # page.pause()
    if data == "Hello, Leena":
        page.locator("button[aria-label='Expand Account and Lists']").click()
        page.get_by_text("Sign Out").click()
        # page.locator("#nav-link-accountList").click()
        # page.locator("h2:has-text('Login & security')").click()
        signOut = page.locator(".a-size-medium-plus").text_content()
        assert signOut.strip() == 'Sign in or create account'

def test_countcartitem(login,page:Page):    #count cart item
    page.locator(".nav-cart-icon").click()
    page.wait_for_selector("ul>div.sc-list-item")
    countitem = page.locator("ul>div.sc-list-item").count()
    print(countitem)

def test_searchfunctionality(login,page:Page):  #verify if search result is display
    page.get_by_role("searchbox").fill("I phone 16")
    page.locator("#nav-search-submit-button").click()
    page.wait_for_selector("div.s-main-slot>div[role='listitem']")
    count = page.locator("div.s-main-slot>div[role='listitem']").count()
    assert count > 0

def test_searchboxvisibleornot(login,page:Page):  #verify search box visibility
    page.locator("input#twotabsearchtextbox").is_visible()

def test_autosuggestion(login,page:Page):   #verify autosuggest feature
    # page.pause()
    page.get_by_role("searchbox").fill("phone")
    time.sleep(5)
    count = page.locator(".s-suggestion-container").count()
    assert count > 0

def test_filterfunctionality(login,page:Page):   #verify if filter function works or not
    # page.pause()
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    page.get_by_role("link",name="Apply the filter HP to narrow results").click()
    page.wait_for_selector("[data-component-type='s-search-result']")
    time.sleep(10)
    data = page.locator("[data-component-type='s-search-result']")
    count = data.count()
    print(count)
    for i in range(count):
        print("hello")
        product = data.nth(i)
        title = product.locator("h2 span").inner_text()
        assert "HP" in title

def test_pricepresent(login,page:Page):   #verify if price is mention for a product
    page.get_by_role("searchbox").fill("laptop")
    # page.pause()
    page.locator("#nav-search-submit-button").click()
    first_item = page.locator("[data-component-type='s-search-result']").first
    price = first_item.locator(".a-price-whole").inner_text()
    print(price)
    assert price != ""

def test_nextpagefunctionality(login,page:Page):   #verify if next page functionality
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    first_url = page.url
    page.locator("[aria-label='Go to next page, page 2']").click()
    second_url = page.url
    print(first_url,second_url)
    assert first_url == second_url

def test_sortbyprice(login,page:Page):   #verify if sorted filter for price works or not
    price = []
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    page.pause()
    page.get_by_role("combobox",name="Sort by").select_option("Price: Low to High")
    # time.sleep(10)
    # page.wait_for_selector("div#search",state="visible")
    page.locator("div.s-main-slot").wait_for()
    page.wait_for_selector("div.s-main-slot")
    # time.sleep(10)
    data = page.locator("div.s-main-slot>div[role='listitem']")
    count = data.count()
    for i in range(count):
        price.append(data.nth(i).locator(".a-price-whole").inner_text())
    print(price)
    assert price == sorted(price)

def test_verifycartempty(login,page:Page): #verify cart is empty in first time login
    page.locator(".nav-cart-icon").click()
    assert "Your Amazon Cart is empty" == page.locator("div.a-cardui-body>h3.a-size-large").text_content().strip()

def test_childwindow(login,page:Page): #verify child window
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    with page.expect_popup() as new_page:
        data = page.locator("div.s-main-slot>[role='listitem']").first
        data.locator("h2 span",has_text="HP Omnibook 5 OLED (Previously Pavilion), Snapdragon X Processor (16GB LPDDR5x,1TB SSD) 2K OLED,16''/40.6cm, Win11, M365*Office24, Glacier Silver, 1.59kg, fb0001QU, Backlit, Next-Gen AI Laptop").click()
        time.sleep(10)
        childwindow = new_page.value
        print(childwindow.title())

def test_validatepricefilter(login,page:Page):  #verify price for all product comes under price filter only
    # page.get_by_role("searchbox").fill("laptop")
    # page.locator("#nav-search-submit-button").click()
    page.goto("https://www.amazon.in/s?k=laptop&rh=p_36%3A2000000-5000000")
    # page.pause()
    # page.get_by_role("link",name="₹46,000 - ₹85,000").click()
    data = page.locator("div[role='listitem'].s-widget-spacing-small")
    count = data.count()
    for i in range(count):
        assert int(data.nth(i).locator(".a-price-whole").inner_text().replace(",","")) >= 20000 and int(data.nth(i).locator(".a-price-whole").inner_text().replace(",","")) <= 50000

def test_validatelocationchange(login,page:Page):  #verify location change filter
    page.locator("#nav-global-location-popover-link").click()
    page.pause()
    page.locator("#GLUXZipUpdateInput").clear()
    page.locator("#GLUXZipUpdateInput").fill("452001")
    page.locator("#GLUXZipUpdate").click()
    # pincode = page.locator("#glow-ingress-line2").inner_text()
    # print(pincode)
    assert "Indore 452001" == page.locator("#glow-ingress-line2").inner_text().replace("\u200c","")

def test_verifypagination(login,page:Page): #next page validation
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    page.get_by_role("button",name="Next").click()
    pagenumber = page.locator(".s-pagination-selected").inner_text()
    assert int(pagenumber) == 2

def test_titleconsistency(login,page:Page): #verify title on search page and on product page
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    page.pause()
    first = page.locator("[data-component-type='s-search-result']").first
    title = first.locator("h2 span").inner_text()
    print(title)
    with page.expect_popup() as newpage:
        page.locator("a>h2.a-size-medium").first.click()
        page1 = newpage.value
        title1 = page1.locator("span#productTitle").inner_text()
        print(title1)

def test_removeitemfromcart(login,page:Page): #add item to cart and then remove it from cart and verify if item remove or not
    page.get_by_role("searchbox").fill("tv")
    page.locator("#nav-search-submit-button").click()
    page.pause()
    data = page.locator("div.puisg-col-inner>div.a-spacing-small").first
    data.get_by_text("Add to cart").click()
    # div.atc-faceout-container>form.a-spacing-none
    page.locator(".nav-cart-icon").click()
    page.get_by_role("listitem").locator("[data-a-selector='decrement-icon']").click()
    page.reload()
    text = page.locator(".sc-your-amazon-cart-is-empty").inner_text().strip()
    assert text == "Your Amazon Cart is empty"

def test_verifytodaysdealoption(login,page:Page): #verify today's deal option working properly
    page.get_by_text("Today's deal").click()
    page.wait_for_selector(".GridItem-module__container_PW2gdkwTj1GQzdwJjejN")
    items = page.locator(".GridItem-module__container_PW2gdkwTj1GQzdwJjejN").count()
    assert items > 0

def test_verifyifcustomerreviewoptionavailable(login,page:Page): #verify customer review option is avl
    page.get_by_role("searchbox").fill("laptop")
    page.locator("#nav-search-submit-button").click()
    # page.pause()
    with page.expect_popup() as newpage:
        page.locator("a>h2.a-size-medium").first.click()
        page1 = newpage.value
        page1.wait_for_load_state("domcontentloaded")
        assert page1.locator("div#customerReviews").is_visible()

    

    
    


    


   
    

        
    
    



