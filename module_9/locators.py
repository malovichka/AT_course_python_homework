
# test_search_for_position_based_on_criteria
careers_link = 'Careers'  # LinkText locator
keyword_field = "new_form_job_search-keyword"  # ID locator
location_field = "recruiting-search__location"  # ClassName locator
location_option = '.select2-results__options > [title = "{}"]'  # CSS locator
remote = '//*[@type="checkbox" and @name="remote"]/../label'  # XPath locator with any operator  # XPath locator with axes
find_button = '//button[contains (text(), "Find")]'  # XPath locator (Relative path) # XPath locator with any operator 
search_result_list = "search-result__list"  # ClassName locator
search_result_item = "search-result__item"  # ClassName locator
view_apply_button = '//a[contains (text(), "View and apply")]'  # XPath locator (Relative path) # XPath locator with any operator 
vacancy_header = "h1"  # TagName locator

# test_global_search
search_icon = "search-icon" # ClassName locator
search_box = 'q'  # Name locator
global_search_find_button = "custom-search-button"  # ClassName locator
article = "article" # TagName locator
link_text = '{}'  # PartialLinkText locator, used with corresponding method in test
article_description = "search-results__description" # ClassName locator
article_link = "search-results__title-link" # ClassName locator




