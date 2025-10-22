import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Setup ---
# This automatically sets up the correct driver for your version of Chrome
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

print("Opening browser...")
# We can use a "data URI" to load our own simple HTML
# This is just a mini-webpage with a button and some hidden text
driver.get("""
    data:text/html,
    <html>
        <body>
            <button 
                id="myButton" 
                onclick="document.getElementById('hiddenText').style.display='block'">
                Show Text
            </button>
            <div id="hiddenText" style="display:none">
                Hello, Selenium!
            </div>
        </body>
    </html>
""")

try:
    # --- Step 1: Find the elements ---
    # Find the text element we want to read
    text_element = driver.find_element(By.ID, "hiddenText")
    
    # Find the button we want to click
    button_element = driver.find_element(By.ID, "myButton")
    
    # --- Step 2: Check before clicking ---
    print(f"Is text visible before click? {text_element.is_displayed()}")

    # --- Step 3: Interact with the page ---
    print("Clicking the button...")
    button_element.click()
    
    # Wait 1 second for the JavaScript to run
    time.sleep(1) 

    # --- Step 4: Check after clicking ---
    print(f"Is text visible after click?  {text_element.is_displayed()}")
    print(f"The hidden text is: '{text_element.text}'")

finally:
    # --- Cleanup ---
    print("Closing browser.")
    driver.quit()