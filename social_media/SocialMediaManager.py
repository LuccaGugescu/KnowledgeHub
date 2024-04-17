from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class SocialMediaManager:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=C:\\Users\\lucca\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        self.driver = webdriver.Chrome(options=chrome_options)

    def upload_video_to_youtube(self, video_path, title, description, tags, privacy_status='public'):
        self.driver.get("https://www.youtube.com/upload")
        time.sleep(5)  # Adjust the sleep time according to your internet speed

        # Check if login is required
        if "accounts.google.com" in self.driver.current_url:
            # Entering email
            email_input = self.driver.find_element_by_id("identifierId")
            email_input.send_keys("giugitsucorporation@gmail.com")
            next_button = self.driver.find_element_by_id("identifierNext")
            next_button.click()
            time.sleep(5)  # Adjust the sleep time according to your internet speed

            # Entering password
            password_input = self.driver.find_element_by_xpath("//input[@name='password']")
            password_input.send_keys("your_password")  # Replace "your_password" with your actual password
            next_button = self.driver.find_element_by_id("passwordNext")
            next_button.click()
            time.sleep(5)  # Adjust the sleep time according to your internet speed

        # Uploading video
        upload_input = self.driver.find_element_by_xpath("//input[@type='file']")
        upload_input.send_keys(video_path)
        time.sleep(5)  # Adjust the sleep time according to your internet speed

        # Filling video details
        title_input = self.driver.find_element_by_id("textbox")
        title_input.send_keys(title)
        description_input = self.driver.find_element_by_id("description")
        description_input.send_keys(description)
        tags_input = self.driver.find_element_by_xpath("//textarea[@placeholder='Add tags']")
        tags_input.send_keys(tags)

        # Setting privacy
        privacy_button = self.driver.find_element_by_xpath("//button[@aria-label='Privacy settings']")
        privacy_button.click()
        time.sleep(1)  # Adjust the sleep time according to your internet speed
        if privacy_status == 'public':
            public_button = self.driver.find_element_by_xpath("//div[contains(text(), 'Public')]")
            public_button.click()
        elif privacy_status == 'private':
            private_button = self.driver.find_element_by_xpath("//div[contains(text(), 'Private')]")
            private_button.click()

        # Submitting
        done_button = self.driver.find_element_by_xpath("//span[contains(text(), 'Next')]")
        done_button.click()
        time.sleep(5)  # Adjust the sleep time according to your internet speed

        # Getting video id
        video_id = self.driver.current_url.split('=')[-1]
        return video_id

    def close(self):
        self.driver.quit()
