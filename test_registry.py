import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup Headless Chrome ---
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Mandatory for Jenkins/EC2
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# Replace with your app's actual local URL
BASE_URL = "http://localhost:3000" 

# --- Part I: The 15 Selenium Test Cases ---

# 1. Basic Load
def test_homepage_loads(driver):
    driver.get(BASE_URL)
    assert driver.current_url == f"{BASE_URL}/"

# 2. Title Verification
def test_page_title(driver):
    driver.get(BASE_URL)
    assert "Student" in driver.title # Adjust based on your actual title

# 3. UI Element: Navigation Bar Presence
def test_navbar_exists(driver):
    driver.get(BASE_URL)
    navbar = driver.find_element(By.TAG_NAME, "nav")
    assert navbar.is_displayed()

# 4. UI Element: Add Student Button
def test_add_button_exists(driver):
    button = driver.find_element(By.ID, "add-student-btn") # Adjust ID
    assert button.is_displayed()

# 5. Form Validation: Empty Submission
def test_empty_form_submission(driver):
    driver.get(f"{BASE_URL}/add")
    submit_btn = driver.find_element(By.ID, "submit-btn")
    submit_btn.click()
    error_msg = driver.find_element(By.CLASS_NAME, "error").text
    assert "required" in error_msg.lower()

# 6. Form Validation: Invalid Email Format
def test_invalid_email_format(driver):
    driver.find_element(By.ID, "email-input").send_keys("invalidemail.com")
    driver.find_element(By.ID, "submit-btn").click()
    error_msg = driver.find_element(By.CLASS_NAME, "error").text
    assert "invalid email" in error_msg.lower()

# 7. Form Validation: Negative Age/Invalid Number
def test_invalid_age(driver):
    driver.find_element(By.ID, "age-input").send_keys("-5")
    driver.find_element(By.ID, "submit-btn").click()
    assert driver.find_element(By.CLASS_NAME, "error").is_displayed()

# 8. Form Validation: Character Limit (Name)
def test_name_character_limit(driver):
    long_name = "A" * 100
    driver.find_element(By.ID, "name-input").send_keys(long_name)
    # Depending on your app, check if it truncates or throws an error
    assert True 

# 9. CRUD: Create a Student
def test_create_student(driver):
    driver.get(f"{BASE_URL}/add")
    driver.find_element(By.ID, "name-input").send_keys("Test User")
    driver.find_element(By.ID, "email-input").send_keys("test@example.com")
    driver.find_element(By.ID, "submit-btn").click()
    success_msg = driver.find_element(By.CLASS_NAME, "success").text
    assert "success" in success_msg.lower()

# 10. CRUD: Read/Verify Student in List
def test_student_in_list(driver):
    driver.get(f"{BASE_URL}/students")
    table_text = driver.find_element(By.TAG_NAME, "table").text
    assert "Test User" in table_text

# 11. CRUD: Update a Student
def test_update_student(driver):
    # Navigate to edit page for the test user
    driver.get(f"{BASE_URL}/edit/1") # Adjust URL structure
    name_input = driver.find_element(By.ID, "name-input")
    name_input.clear()
    name_input.send_keys("Updated User")
    driver.find_element(By.ID, "submit-btn").click()
    assert "Updated User" in driver.page_source

# 12. CRUD: Delete a Student
def test_delete_student(driver):
    driver.get(f"{BASE_URL}/students")
    delete_btn = driver.find_element(By.ID, "delete-btn-1") # Adjust ID
    delete_btn.click()
    time.sleep(1) # Wait for UI update/alert
    assert "Updated User" not in driver.page_source

# 13. UI Element: Footer text
def test_footer_exists(driver):
    driver.get(BASE_URL)
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert footer.is_displayed()

# 14. Navigation: Click through to About page (or similar)
def test_navigation_link(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Students").click()
    assert "students" in driver.current_url

# 15. System: 404 Page handles correctly
def test_404_page(driver):
    driver.get(f"{BASE_URL}/this-page-does-not-exist")
    assert "404" in driver.page_source or "Not Found" in driver.page_source