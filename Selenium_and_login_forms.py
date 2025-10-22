import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Setup ---
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

print("Opening browser to the login page...")
driver.get("http://quotes.toscrape.com/login")

try:
    # --- Step 1: Find the username field and type in it ---
    # The field is <input type="text" name="username">
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys("my_test_user") # Type text
    print("Entered username.")

    # --- Step 2: Find the password field and type in it ---
    # The field is <input type="password" name="password">
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("my_test_password") # Type text
    print("Entered password.")

    # --- Step 3: Find the login button and click it ---
    # The button is <input type="submit" value="Login">
    # We can use a CSS selector to find it based on its attributes.
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    print("Clicking login button...")
    login_button.click()
    
    # Wait for the page to load
    time.sleep(2) 

    # --- Step 4: Verify the login (or failure) ---
    # If login is successful, we'll see a "Logout" link.
    # If it fails, we'll see an error message.
    try:
        logout_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
        print(f"Login successful! Found: {logout_link.text}")
    except:
        # We can find the error by its class
        error_message = driver.find_element(By.CLASS_NAME, "alert-danger")
        print(f"Login failed! Message: {error_message.text}")

finally:
    # --- Cleanup ---
    print("Closing browser.")
    driver.quit()