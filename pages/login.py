from playwright.sync_api import Page
class Login:

    def login(self,page,username,password):
        page.goto("https://rahulshettyacademy.com/client/#/auth/login")
        page.get_by_placeholder("email@example.com").fill(username)
        page.locator("#userPassword").fill(password)
        page.get_by_role("button",name="Login").click()
        title = page.title()
        # print(title)
        return title