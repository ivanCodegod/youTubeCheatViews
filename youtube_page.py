import time
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utilities import Config, generate_random_search_query


class YouTubePage:
    """
    Represents a YouTube page and provides methods to interact with the page.
    """

    def __init__(self, driver):
        """
        Initializes a YouTubePage object.

        :param driver: The WebDriver instance to use for interacting with the page.
        """
        self.driver = driver

    def wait_for_element(self, locator, timeout=Config.WAIT_FOR_ELEM_TIME):
        """
        Waits for an element to be present on the page.

        :param locator: The locator for the element to wait for.
        :param timeout: The maximum time to wait for the element (in seconds).
        :return: The WebElement object of the element found.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))

    def get_video_duration(self):
        """
        Retrieves the duration of the current video.

        :return: The duration of the video in seconds.
        """
        script = "return document.querySelector('.html5-main-video').duration;"
        duration = self.driver.execute_script(script)
        total_duration = int(duration)
        logging.debug(f"Video duration: {total_duration}")
        return total_duration

    def login_user(self, email: str, password: str):
        """
        Logs in the user with the provided email and password.

        :param email: The user's email.
        :param password: The user's password.
        """
        self.driver.get('https://accounts.google.com')
        email_field = self.wait_for_element((By.CSS_SELECTOR, 'input[type="email"]'))
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        time.sleep(Config.DEFAULT_SLEEP_TIME)  # Wait for the page to load

        password_field = self.wait_for_element((By.CSS_SELECTOR, 'input[type="password"]'))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(Config.DEFAULT_SLEEP_TIME)  # Wait for the page to load

    # def click_next_video(self):  # TODO: Implement the logic to click next video
    #     """
    #     Clicks the "Next Video" button to go to the next video in the playlist.
    #     """
    #     next_video_button = self.wait_for_element((By.CSS_SELECTOR, '.ytp-next-button'))
    #     next_video_button.click()

    def click_play_button(self):
        """
        Clicks the "Play" button to start playing the video.
        """
        play_button = self.wait_for_element((By.CSS_SELECTOR, '.ytp-play-button'))
        play_button.click()

    def is_advertisement_playing(self):
        """
        Checks if an advertisement is currently playing.

        :return: True if an advertisement is playing, False otherwise.
        """
        try:
            ad_element = WebDriverWait(self.driver, 5).until(  # TODO: create constant
                EC.presence_of_element_located((By.XPATH, "//div[@class='ytp-ad-player-overlay']")))
            return ad_element.is_displayed()
        except (NoSuchElementException, TimeoutException):
            return False

    def check_advertisement(self):
        """
        Checks if an advertisement is playing and skips it if necessary.
        """
        if self.is_advertisement_playing():
            logging.debug("Advertisement is playing...")
            self.wait_and_click_ad_skip_button()
            logging.debug("Advertisement finished playing.")

    def wait_and_click_ad_skip_button(self, timeout=20):  # TODO: create constant
        """
        Waits for the ad skip button to become clickable and clicks it.

        :param timeout: The maximum time to wait for the skip button (in seconds).
        """
        try:
            # Wait for the skip button to become clickable for a maximum of 20 seconds
            wait = WebDriverWait(self.driver, timeout)
            skip_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='ytp-ad-text ytp-ad-skip-button-text']")))
            skip_button.click()
        except TimeoutException:
            pass

    def scroll_up(self):
        """
        Scrolls up on the YouTube page.
        """
        scroll_distance = random.randint(100, 200)  # Random distance to scroll up # TODO: create constant
        body = self.driver.find_element(By.TAG_NAME, 'body')

        for _ in range(scroll_distance // 100):
            body.send_keys(Keys.PAGE_UP)

    def scroll_down(self):
        """
        Scrolls down on the YouTube page.
        """
        scroll_distance = random.randint(100, 200)  # Random distance to scroll down # TODO: create constant
        scroll_steps = scroll_distance // 10  # Number of scroll steps

        for _ in range(scroll_steps):
            scroll_value = random.uniform(15, 60)  # TODO: create constant
            self.driver.execute_script(f"window.scrollBy(0, {scroll_value});")
            time.sleep(0.005)  # Adjust the sleep duration as needed # TODO: create constant

    def scroll_randomly(self):
        """
        Scrolls up or down randomly on the YouTube page.
        """
        scroll_direction = random.choice(["up", "down"])

        if scroll_direction == "up":
            self.scroll_up()
        else:
            self.scroll_down()

    # def click_show_more_button(self):  # TODO: implement logic
    #     """
    #     TODO
    #
    #     :return:
    #     """
    #     try:
    #         show_more_button = self.driver.find_element(By.XPATH,
    #                                                     '//*[@id="browse-itemsprimary"]/li[2]/button/span/span[2]')
    #
    #         # Scroll to the element to make it clickable
    #         self.scroll_to_element(show_more_button)
    #
    #         # Check if the element is visible and clickable
    #         if show_more_button.is_displayed() and show_more_button.is_enabled():
    #             # Click the "Show more" button
    #             show_more_button.click()
    #         else:
    #             logging.warning("The 'Show more' button is not currently interactable.")
    #     except NoSuchElementException:
    #         logging.warning("The 'Show more' button element was not found.")

    # def scroll_to_element(self, element):  # TODO: implement logic
    #     """
    #     TODO
    #
    #     :param element:
    #     :return:
    #     """
    #     # Scroll to the element using JavaScript
    #     self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def generate_random_video_time(self):
        """
        Generates a random time duration for the YouTube video.

        For example, if video is 1min than the value returned would be generated randomly between 30s and 45s.

        :return: Random time duration for the YouTube video.
        """
        video_duration = self.get_video_duration()
        middle_time = video_duration / 2
        middle_between_middle_and_end = (middle_time + video_duration) / 2

        result = random.uniform(middle_time, middle_between_middle_and_end)
        logging.info(f"Calculated random time to watch the video: {result}")
        return result

    def decide_to_scroll(self, probability: float):
        """
        Randomly decides whether to scroll or not based on the given probability.

        :param probability: The probability of scrolling, between 0 and 1.
        """
        should_scroll = random.random() < probability
        if should_scroll:
            # Scroll up or down randomly
            self.scroll_randomly()

    # def search_query(self):
    #     """
    #     TODO
    #
    #     :return:
    #     """
    #     query = generate_random_search_query()
    #
    #     # Locate the search field on the YouTube page
    #     search_field = self.wait_for_element((By.CSS_SELECTOR, 'input#search'))
    #
    #     # Type the query in the search field with varying delays between letters
    #     for letter in query:
    #         search_field.send_keys(letter)
    #         delay = random.uniform(0.1, 0.3)  # Adjust the delay range as needed # Create constants
    #         time.sleep(delay)
    #
    #     return query
