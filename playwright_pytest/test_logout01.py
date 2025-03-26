# Credit: https://www.browserstack.com/guide/playwright-python-tutorial

import pytest
from playwright.sync_api import Page, sync_playwright
from test_logger import log_result

""" Logout Test Scenario START """
# ตรวจสอบว่า Logout สำเร็จและกลับไปที่หน้า Login

def test_logout01_pos01():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # กำหนด URL ที่คาดหวังหลังจากทำการ logout
        expected_url = "http://reg.rmutk.ac.th/registrar/home.asp"

        # ไปที่หน้า Login
        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")
        
        page.locator('input[name="f_uid"]').fill("65502100038-6")
        page.locator('input[name="f_pwd"]').fill("nan18331")
        page.locator('input[name="f_idcard"]').fill("1100801492928")
        
        page.locator('input[type="submit"]').click()
        page.wait_for_load_state("networkidle")

        try:
            # # ค้นหา element ที่เป็นปุ่ม Logout
            logout_element = page.locator("a[onclick*='Setpostform']").first
            assert logout_element.is_visible(), "❌ Logout button not found"

            # ดึงค่าของ attribute "onclick"
            onclick_attr = logout_element.get_attribute("onclick")
            import re
            # ค้นหาข้อความในรูปแบบ Setpostform('URL') 
            match = re.search(r"Setpostform\('(.+?)'", onclick_attr)
            
            if match:
                logout_url = match.group(1)             # ถ้าพบ match ให้ดึง logout URL จาก group แรก ofgroup
                page.goto(logout_url)                   # ไปที่ logout URL เพื่อทำการ Logout
                page.wait_for_load_state("networkidle") # รอจนหน้าลงโหลดเสร็จ

                current_url = page.url  ## รับ URL ปัจจุบันหลังจากทำการ logout
                
                # ตรวจสอบว่า URL ปัจจุบัน
                if "reg.rmutk.ac.th/registrar/home.asp" in current_url:
                    actual_result = f"✅ Logout successful, redirected to {current_url}"
                    status = "PASS"
                else:
                    actual_result = f"❌ Logout did not redirect to expected URL (url={current_url})"
                    status = "FAIL"
            #ไม่สามารถดึง logout URL
            else:
                actual_result = "❌ Could not parse logout URL from onclick attribute"
                status = "FAIL"

        except Exception as e:
            # ถ้ามีข้อผิดพลาดเกิดขึ้นระหว่างกระบวนการ logout
            actual_result = f"❌ Error during logout: {str(e)}"
            status = "FAIL"

        
        log_result("logout01_pos01", actual_result, page=page)      # บันทึกผลการทดสอบลงใน log file ,call fn() log_result
        assert status == "PASS", "❌ Logout test failed!"          # ทำ assertion เพื่อยืนยันว่าการ logout สำเร็จ (status ต้องเป็น PASS)
        browser.close()                                         

""" Logout Test Scenario END """
