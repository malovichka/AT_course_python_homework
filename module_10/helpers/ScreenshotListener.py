from robot.libraries.BuiltIn import BuiltIn


class ScreenshotListener:
    """
    Listener that takes a screenshot after execution of a keyword with the tag "Screenshot".
    """

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.selenium_lib = None

    def start_suite(self, name, attributes):  
        self.selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")

    def end_keyword(self, name, attributes):
        if "Screenshot" in attributes["tags"]:
            screenshot_path = self.selenium_lib.capture_page_screenshot()
            BuiltIn().log(f"Screenshot captured: {screenshot_path}", "INFO")


if __name__ == "__main__":
    BuiltIn().import_library(ScreenshotListener(), "listener")
