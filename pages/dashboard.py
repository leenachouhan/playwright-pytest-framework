from playwright.sync_api import Page
import time

class Dashboard:

    def orders(page:Page):
        page.get_by_role("button",name="ORDERS").click()

    def carts(self,page):
        # page.get_by_role("link",name="/dashboard/cart").click()
        page.locator("i.fa-shopping-cart").nth(0).click()

    def signout(self,page):
        # page.pause()
        page.get_by_role("button",name="Sign Out").click()
        logout = page.get_by_text("Logout Successfully").text_content().strip()
        return logout

    
    def additemtocart(self,page,itemname):
        # page.pause()
        product = page.locator(".card-body",has_text=itemname)
        product.get_by_role("button",name="Add To Cart").click()
        productadded = page.get_by_text("Product Added To Cart").text_content().strip()
        return productadded
    
    def searchfunctionlity(self,page,itemname):
        page.get_by_role("textbox",name="search").fill(itemname)
        page.press("#sidebar input[name='search']","Enter")
        # page.wait_for_selector("#products div.mb-3")
        time.sleep(5)
        items = page.locator("#products div.mb-3").count()
        # print(items)
        return items 
    
    def viewbutton(self,page,itemname):
        item = page.locator("#products div.mb-3",has_text=itemname)
        item.get_by_role("button",name="View").click()
        value = page.locator("div.rtl-text h2").inner_text()
        return value
        
