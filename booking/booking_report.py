# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement
# --- CHANGE 1: Import By ---
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        # --- CHANGE 2: Updated find_elements_by_class_name to By.CLASS_NAME ---
        return self.boxes_section_element.find_elements(
            By.CLASS_NAME, 'sr_property_block'
        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # --- CHANGE 3: Updated find_element_by_class_name to By.CLASS_NAME ---
            hotel_name = deal_box.find_element(
                By.CLASS_NAME, 'sr-hotel__name'
            ).get_attribute('innerHTML').strip()
            
            # --- CHANGE 4: Updated find_element_by_class_name to By.CLASS_NAME ---
            hotel_price = deal_box.find_element(
                By.CLASS_NAME, 'bui-price-display__value'
            ).get_attribute('innerHTML').strip()
            
            hotel_score = deal_box.get_attribute(
                'data-score'
            ).strip()

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        return collection
