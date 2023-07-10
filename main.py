"""
This script adds views to a YouTube video using Selenium WebDriver.

It simulates user interactions, such as scrolling, clicking, and watching the video for a random duration.

Tg: @ivan_busy_man
"""
import time
import logging
import random
import keyboard

from selenium import webdriver

from youtube_page import YouTubePage
from utilities import Config

# Logging settings
logging.basicConfig(level=logging.DEBUG)

# TODO: Add logic to parse it from sep file
# User account credentials
accounts = [
    {'email': 'vi8581708@gmail.com', 'password': 'vi8581708vi8581708'},
    # TODO: Add more user account credentials here
]
# TODO: Make it as input parameter for script
# YouTube video URL
video_url = 'https://www.youtube.com/watch?v=wXLUvI-TSi8&ab_channel=Lukeytz-Tema '

# Initialize Chrome WebDriver
options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Uncomment to enable headless mode
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# Initialize an instance of the YouTubePage class using the driver object
youtube_page = YouTubePage(driver)


def randomly_pause_video():
    """
    Randomly pauses the video and resumes after a pause duration.
    """
    pause_duration = 0
    if random.random() < Config.PAUSE_VID_PROBABILITY:
        # Simulate pressing the Space-bar key to pause the video
        keyboard.press("space")
        logging.info("Video paused.")

        # Wait for a pause duration
        pause_duration = random.uniform(Config.PAUSE_MIN_DURATION, Config.PAUSE_MAX_DURATION)
        logging.info(f"Waiting for {pause_duration} seconds...")
        time.sleep(pause_duration)

        # TODO: Move to sep function()
        # if pause_duration >= 4:  # TODO: create const # TODO: Set to 9.7
        #    youtube_page.search_query()

        # Simulate pressing the Space-bar key again to resume the video
        keyboard.press("space")
        logging.info("Video resumed.")

    return pause_duration


def watch_video():
    """
    Simulates watching a YouTube video.
    """
    # Start watching the video
    start_time = time.time()
    current_time = start_time
    total_wait_time = youtube_page.generate_random_video_time()
    active_watching_time = 0

    while current_time - start_time <= total_wait_time:
        # Check if an advertisement is playing
        youtube_page.check_advertisement()

        # Update current time
        current_time = time.time()

        youtube_page.decide_to_scroll(Config.SCROLL_PROBABILITY)

        pause_duration = randomly_pause_video()
        start_time += pause_duration

        # TODO: Move to sep function
        # TODO create sep var for chance calculating
        # should_scroll = random.random() < 0.5
        # youtube_page.click_show_more_button()

        # Update the active watching time
        active_watching_time = current_time - start_time

    logging.debug(f"Active video watching time: {active_watching_time} seconds.")
    logging.info("Video watching completed.")


def simulate_user(url: str):
    """
    Simulates a user watching a YouTube video.

    :param url: The URL of the YouTube video.
    """
    driver.get(url)
    time.sleep(Config.DEFAULT_SLEEP_TIME)

    youtube_page.click_play_button()  # Note: NEEDED FOR EXECUTION WITHOUT LOGGING INTO USER!
    youtube_page.check_advertisement()
    watch_video()


def main():
    """
    The main function that orchestrates the script's execution.
    """
    for account in accounts:
        user_email, user_password = account['email'], account['password']
        logging.info(f"Current user: {user_email}")
        # youtube_page.login_user(account['email'], user_password)  # TODO: Uncomment for authorized user's

        simulate_user(video_url)
        logging.info(f"View added for {user_email} user")

    # Close the browser session
    driver.quit()


if __name__ == '__main__':
    main()
