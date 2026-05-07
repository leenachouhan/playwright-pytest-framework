import pytest
# from playwright.sync_api import Page

class Register:


    def register(self,page,FirstName,LastName,email,number,occupation,gender,password,confirmpassword):
        page.goto("https://rahulshettyacademy.com/client/#/auth/register")
        page.get_by_placeholder("First Name").fill(FirstName)
        page.get_by_placeholder("Last Name").fill(LastName)
        page.get_by_placeholder("email@example.com").fill(email)
        page.get_by_placeholder("enter your number").fill(number)
        page.locator(".custom-select").select_option(occupation)
        page.locator(f"[type='radio'][value='{gender}']").check()
        page.locator("#userPassword").fill(password)
        page.locator("#confirmPassword").fill(confirmpassword)
        page.get_by_role("checkbox").click()
        page.get_by_role("button",name="Register").click()
        text = page.locator("h1.headcolor").inner_text().strip()
        return text