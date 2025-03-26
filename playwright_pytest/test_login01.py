import pytest
from playwright.sync_api import Page, sync_playwright
from test_logger import log_result

# ------------------------------------------------------------------------------------
# Positive Test Scenario 01: ทดสอบกรณีเข้าสู่ระบบด้วยข้อมูลที่ถูกต้อง
# ------------------------------------------------------------------------------------

def test_login01_pos01():
    with sync_playwright() as p:    #check ว่าถูกปิดหลังทำงานfinishแล้ว
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ไปที่หน้า Login
        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        # กรอกข้อมูลเข้าสู่ระบบ (ข้อมูลที่ถูกต้อง)
        page.locator('input[name="f_uid"]').fill("65502100038-6")       #valid
        page.locator('input[name="f_pwd"]').fill("nan18331")            #valid
        page.locator('input[name="f_idcard"]').fill("1100801492928")    #valid

        # คลิกเข้าสู่ระบบ
        page.locator('input[type="submit"]').click()
        page.wait_for_load_state("networkidle") #wait for network(ไม่มีการเรียกข้อมูลใหม่)

        print(f"📌 DEBUG: Current Page URL → {page.url}")   # URL

        # ตรวจสอบว่าหน้าเปลี่ยนรหัสผ่านถูกต้อง
        expected_url_prefix = "https://reg.rmutk.ac.th/registrar/changepwd.asp"
        
        if page.url.startswith(expected_url_prefix):
            actual_result = f"✅ Login successful, redirected to 'Change Password' page: {page.url} "
        else:
            actual_result = f"❌ Login successful but redirected to wrong page: {page.url}"

        log_result("login01_pos01", actual_result, page=page)

        # Assert ตรวจสอบว่า URL ถูกต้อง
        assert page.url.startswith(expected_url_prefix), "❌ Login did not redirect to Change Password page!"

        browser.close()

# ------------------------------------------------------------------------------------
# Positive Test Scenario 01 END 
# ------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------
# Negative Test Scenario 01: ทดสอบกรณีล็อกอินด้วยข้อมูลที่ไม่ถูกต้อง (รหัสผ่านและ ID ผิด)
# โดยคาดหวังให้แสดงข้อความแจ้งเตือนที่มีสีสีน้ำเงิน
# ------------------------------------------------------------------------------------

def is_blue(rgb_string):
    rgb_values = [int(x) for x in rgb_string.replace("rgb(", "").replace(")", "").split(",")]
    r, g, b = rgb_values
    return r < 30 and g < 30 and b > 200 # returns T

def test_login01_neg01():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # ไปที่หน้า Login
        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        page.locator('input[name="f_uid"]').fill("65502100038-6")   #valid
        page.locator('input[name="f_pwd"]').fill("wrongpassword")   #invalid
        page.locator('input[name="f_idcard"]').fill("555555")       #invalid

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            # ค้นหา element ที่แสดงข้อความแจ้งเตือนผ่าน XPath
            error_element = page.locator("xpath=//font[contains(text(),'ก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง')]").first
            assert error_element.is_visible()

            # ดึงค่าสีของข้อความแจ้งเตือน
            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_blue(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีน้ำเงิน"
                status = "PASS"
            else:
                actual_result = f"❌ พบข้อความแจ้งเตือน แต่สีไม่ถูกต้อง เป็นสีแดง"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg01", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่พบ หรือ สีไม่ถูกต้อง!"
        browser.close()

# ------------------------------------------------------------------------------------
# Negative Test Scenario 01 END
# ------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------
# Negative Test Scenario 02: ทดสอบกรณีล็อกอินด้วยรหัสที่ผิด (แต่ password ถูกต้อง)
# โดยคาดหวังให้แสดงข้อความแจ้งเตือนสีแดง
# ------------------------------------------------------------------------------------

def test_login01_neg02():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        page.locator('input[name="f_uid"]').fill("65502100038-6")       #valid
        page.locator('input[name="f_pwd"]').fill("nan18331")            #valid
        page.locator('input[name="f_idcard"]').fill("wrongidcard")      #invalid

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            error_element = page.locator("xpath=//font[contains(text(),'ก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง')]").first
            assert error_element.is_visible(), "❌ ไม่พบข้อความแจ้งเตือน"

            actual_result = "✅ พบข้อความก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง"
            status = "PASS"

        except Exception:
            actual_result = "❌ ไม่พบข้อความก รุ ณ า ป้ อ น ร หั ส ป ร ะ จ ำ ตั ว น ศ .ร หั ส บั ต ร ป ร ะ ช า ช น แ ล ะ ร หั ส ผ่ า น ใ ห้ ถู ก ต้ อ ง"
            status = "FAIL"

        log_result("login01_neg02", actual_result, page=page)
        assert status == "PASS", "❌ ไม่พบข้อความแจ้งเตือน!"
        browser.close()

# ------------------------------------------------------------------------------------
# Negative Test Scenario 02 END 
# ------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------
# Negative Test Scenario 03: ทดสอบกรณีล็อกอินด้วยข้อมูลที่ว่างเปล่า
# โดยคาดหวังให้แสดงข้อความแจ้งเตือนและตรวจสอบว่าข้อความแจ้งเตือนนั้นมีสีแดง
# ------------------------------------------------------------------------------------

def is_red(rgb_string):
    rgb_values = [int(x) for x in rgb_string.replace("rgb(", "").replace(")", "").split(",")]
    r, g, b = rgb_values
    return r > 200 and g < 50 and b < 50


def test_login01_neg03():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        page.locator('input[name="f_uid"]').fill("")  
        page.locator('input[name="f_pwd"]').fill("")  
        page.locator('input[name="f_idcard"]').fill("")  

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            error_element = page.locator("xpath=//font[contains(text(),'กรุณาป้อนรหัสประจำตัวและรหัสผ่านให้ถูกต้อง')]").first
            assert error_element.is_visible(), "❌ ไม่พบข้อความแจ้งเตือน"

            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_red(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีแดง"
                status = "PASS"
            else:
                actual_result = f"❌ พบข้อความ แต่สีไม่ถูกต้อง (color={color})"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg03", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่เจอ หรือ สีไม่เป็นสีแดง!"
        browser.close()

# ------------------------------------------------------------------------------------
# Negative Test Scenario 03 END 
# ------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------
# Negative Test Scenario 04 START
# ------------------------------------------------------------------------------------

def test_login01_neg04():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://reg.rmutk.ac.th/registrar/login.asp")

        page.locator('input[name="f_uid"]').fill("")  
        page.locator('input[name="f_pwd"]').fill("")  
        page.locator('input[name="f_idcard"]').fill("")  

        page.locator('input[type="submit"]').click()
        page.wait_for_timeout(2000)

        try:
            error_element = page.locator("xpath=//font[contains(text(),'กรุณาป้อนรหัสประจำตัวและรหัสผ่านให้ถูกต้อง')]").first
            assert error_element.is_visible(), "❌ ไม่พบข้อความแจ้งเตือน"

            color = error_element.evaluate("el => window.getComputedStyle(el).color")
            print(f"📌 DEBUG: สีของข้อความแจ้งเตือน → {color}")

            if is_red(color):
                actual_result = "✅ พบข้อความแจ้งเตือน และเป็นสีแดง"
                status = "PASS"
            else:
                actual_result = f"❌ พบข้อความ แต่สีไม่ถูกต้อง (color={color})"
                status = "FAIL"

        except Exception:
            actual_result = "❌ ไม่พบข้อความแจ้งเตือน"
            status = "FAIL"

        log_result("login01_neg04", actual_result, page=page)
        assert status == "PASS", "❌ ข้อความไม่เจอ หรือ สีไม่เป็นสีแดง!"
        browser.close()

# ------------------------------------------------------------------------------------
# Negative Test Scenario 04 END 
# ------------------------------------------------------------------------------------




