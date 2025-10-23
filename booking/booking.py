import booking.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable

class Booking:
    def __init__(self, teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def handle_cookie_banner(self, timeout=10): # Increased timeout
        """
        Waits for and clicks the 'Decline' button, then
        waits for the banner to become invisible.
        """
        try:
            decline_button_id = "onetrust-reject-all-handler"
            wait = WebDriverWait(self.driver, timeout)
            
            # 1. Wait for the button to be clickable
            decline_button = wait.until(
                EC.element_to_be_clickable((By.ID, decline_button_id))
            )
            
            # 2. Click it
            decline_button.click()
            print("Cookie banner declined.")

            # 3. --- NEW, CRUCIAL STEP ---
            #    Now, we wait for the banner's container to disappear.
            #    This proves the page has finished reacting to the click.
            #    (I inspected the page to find the banner's main container ID)
            banner_container_id = "onetrust-banner-sdk"
            wait.until(
                EC.invisibility_of_element_located((By.ID, banner_container_id))
            )
            print("Cookie banner has disappeared.")
            
        except TimeoutException:
            # If the button doesn't appear after 'timeout' seconds,
            # we assume it's not there and just continue.
            print("Cookie banner not found or already dismissed. Continuing...")
            pass

    # --- ADDING A NEW METHOD ---
    def handle_signin_popup(self, timeout=5):
        """
        Waits for and clicks the 'Dismiss' button on the 
        'Sign in, save money' pop-up.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            # I found this selector by inspecting the 'x' button
            close_button_selector = 'button[aria-label="Dismiss sign-in info."]'
            
            close_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, close_button_selector))
            )
            close_button.click()
            print("Sign-in pop-up dismissed.")

            # Also wait for the pop-up container (dialog) to disappear
            popup_dialog_selector = 'div[role="dialog"]'
            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, popup_dialog_selector))
            )
            print("Sign-in pop-up has disappeared.")

        except TimeoutException:
            # If the pop-up isn't found, no problem, just continue.
            print("Sign-in pop-up not found or already dismissed. Continuing...")
            pass


    def land_first_page(self):
        self.driver.get(const.BASE_URL)
        # This will now wait until the banner is fully gone
        self.handle_cookie_banner()
        
        # --- ADDED THIS CALL ---
        # After handling cookies, we handle the sign-in pop-up
        self.handle_signin_popup()

    def change_currency(self, currency=None):
        try:
            # Now that the page is stable, this wait will work
            wait = WebDriverWait(self.driver, 10)
            
            currency_button_selector = 'button[data-testid="header-currency-picker-trigger"]'
            currency_element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, currency_button_selector))
            )
            currency_element.click()

            # I also found a better selector for the currency item
            selected_currency_selector = (
                f'//button[@data-testid="selection-item"]'
                f'[.//div[text()="{currency}"]]'
            )
            selected_currency_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, selected_currency_selector))
            )
            selected_currency_element.click()
            print(f"Currency changed to {currency}.")
            
        except Exception as e:
            print(f"Error changing currency to {currency}.")
            print("The website's structure may have changed again.")
            print(f"Error details: {e}")
            raise

    # --- THIS METHOD IS UPDATED ---
    def select_place_to_go(self, place_to_go):
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # The ID 'ss' is gone, but the 'name' attribute 'ss' still exists.
            # We'll wait for it to be clickable.
            search_field = wait.until(
                EC.element_to_be_clickable((By.NAME, 'ss'))
            )
            
            search_field.clear()
            search_field.send_keys(place_to_go)
            
            # Now wait for the first result to appear
            first_result = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-i="0"]'))
            )
            first_result.click()
            print(f"Selected destination: {place_to_go}")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error selecting destination: {place_to_go}")
            print("The website's structure for the destination search may have changed.")
            print(f"Error details: {e}")
            raise

    def select_dates(self, check_in_date, check_out_date):
        # This part is fragile. The calendar selectors might
        # be the next thing to break.
        check_in_element = self.driver.find_element(
            By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.driver.find_element(
            By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.driver.find_element(By.ID, 'xp__guests__toggle')
        selection_element.click()
        
        # Wait for the menu to be visible
        wait = WebDriverWait(self.driver, 5)
        wait.until(
            EC.visibility_of_element_located((
                By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]'
            ))
        )

        while True:
            decrease_adults_element = self.driver.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            
            adults_value_element = self.driver.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute('value')

            if int(adults_value) == 1:
                break

        increase_button_element = self.driver.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self.driver)
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_lowest_first()

    def refresh(self):
        self.driver.refresh()

    def report_results(self):
        wait = WebDriverWait(self.driver, 10)
        hotel_boxes = wait.until(
            EC.visibility_of_element_located((By.ID, 'hotellist_inner'))
        )
        
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)



