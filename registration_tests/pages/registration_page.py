from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:

    # step 1 locators
    name_input = (By.ID, "username")
    email_input = (By.ID, "user-email")
    org_input = (By.ID, "organisation-name")
    password_input = (By.ID, "id_password1")
    terms_checkbox = (By.ID, "terms")
    continue_button = (By.ID, "continueBtn")

    # step 2 locators
    country_box = (By.XPATH, "(//span[contains(@class,'select2-selection--single')])[1]")
    country_select = (By.ID, "id_country")
    state_box = (By.XPATH, "//span[@aria-labelledby='select2-id_state-container']")
    state_select = (By.ID, "id_state")
    dropdown_search = (By.CSS_SELECTOR, "input.select2-search__field")
    phone_input = (By.ID, "phone")
    sms_checkbox = (By.ID, "smsOptIn")
    signup_button = (By.ID, "register_button")

    # onboarding pages that open after signup
    team_buttons = (By.CSS_SELECTOR, ".team-button")
    role_buttons = (By.CSS_SELECTOR, ".role-button")
    proposal_card = (By.CSS_SELECTOR, ".explore-card[data-value='proposal']")
    next_button = (By.ID, "next-btn")

    # error divs shown under each field
    name_error = (By.ID, "username-error")
    email_error = (By.ID, "email-error")
    org_error = (By.ID, "organization-error")
    password_error = (By.ID, "password-error")
    terms_error = (By.ID, "terms-error")
    phone_error = (By.ID, "phone-error")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- step 1 ----------
    def enter_name(self, name):
        self.wait.until(EC.visibility_of_element_located(self.name_input)).send_keys(name)

    def enter_email(self, email):
        self.driver.find_element(*self.email_input).send_keys(email)

    def enter_org(self, org):
        self.driver.find_element(*self.org_input).send_keys(org)

    def enter_password(self, password):
        field = self.driver.find_element(*self.password_input)
        field.send_keys(password)
        field.send_keys(Keys.TAB)  # moving out of the field so validation runs

    def accept_terms(self):
        checkbox = self.driver.find_element(*self.terms_checkbox)
        if not checkbox.is_selected():
            # checkbox is custom styled, normal click doesn't work so using JS
            self.driver.execute_script("arguments[0].click();", checkbox)

    def is_continue_enabled(self):
        button = self.driver.find_element(*self.continue_button)
        return "disabled" not in button.get_attribute("class")

    def click_continue(self):
        # button stays disabled until the form is valid
        self.wait.until(lambda d: self.is_continue_enabled())
        self.driver.find_element(*self.continue_button).click()

    # ---------- step 2 ----------
    def _select_dropdown_value(self, select_locator, dropdown_locator, value):
        if self.driver.find_element(*select_locator).get_attribute("value") == value:
            return

        self.wait.until(
            lambda driver: any(
                option.get_attribute("value") == value
                for option in driver.find_element(*select_locator).find_elements(By.TAG_NAME, "option")
            )
        )
        self.wait.until(EC.element_to_be_clickable(dropdown_locator)).click()
        self.wait.until(
            lambda driver: driver.find_element(*select_locator).get_attribute("value") == value
            or any(
                field.is_displayed()
                for field in driver.find_elements(*self.dropdown_search)
            )
        )
        if self.driver.find_element(*select_locator).get_attribute("value") == value:
            self.driver.find_element(*dropdown_locator).send_keys(Keys.ESCAPE)
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".select2-dropdown"))
            )
            return

        self.wait.until(EC.visibility_of_element_located(self.dropdown_search)).send_keys(value)
        option = (
            By.XPATH,
            "//li[contains(@class,'select2-results__option') and normalize-space(.)='" + value + "']",
        )
        self.wait.until(
            lambda driver: driver.find_element(*select_locator).get_attribute("value") == value
            or any(
                element.is_displayed()
                for element in driver.find_elements(*option)
            )
        )
        if self.driver.find_element(*select_locator).get_attribute("value") != value:
            try:
                self.wait.until(EC.element_to_be_clickable(option)).click()
            except StaleElementReferenceException:
                if self.driver.find_element(*select_locator).get_attribute("value") != value:
                    raise
        self.wait.until(
            lambda driver: driver.find_element(*select_locator).get_attribute("value") == value
        )

    def select_country(self, country):
        self._select_dropdown_value(self.country_select, self.country_box, country)

    def select_state(self, state):
        self._select_dropdown_value(self.state_select, self.state_box, state)

    def enter_phone(self, phone):
        field = self.wait.until(EC.visibility_of_element_located(self.phone_input))
        field.clear()
        field.send_keys(phone)
        field.send_keys(Keys.TAB)

    def check_sms_optin(self):
        checkbox = self.driver.find_element(*self.sms_checkbox)
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

    def click_signup(self):
        self.wait.until(EC.element_to_be_clickable(self.signup_button)).click()

    # ---------- checks for tests ----------
    def is_step2_displayed(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.phone_input))
            return True
        except Exception:
            return False

    def get_error(self, locator):
        # error div is empty until validation fails, so wait for some text
        try:
            self.wait.until(lambda d: d.find_element(*locator).text.strip() != "")
        except Exception:
            return ""
        return self.driver.find_element(*locator).text.strip()

    def is_registered(self):
        try:
            self.wait.until(EC.url_contains("/get-started"))
            return True
        except TimeoutException:
            return False

    def is_onboarding_complete(self):
        try:
            self.wait.until(EC.url_contains("/all-proposals"))
            return True
        except TimeoutException:
            return False

    # ---------- onboarding after signup ----------
    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.next_button)).click()

    def complete_onboarding(self):
        # page 1: team size, pick the first option
        self.wait.until(EC.element_to_be_clickable(self.team_buttons)).click()
        self.click_next()

        # page 2: role, pick the first option
        self.wait.until(EC.element_to_be_clickable(self.role_buttons)).click()
        self.click_next()

        # page 3: what to explore, choose proposal and press Done
        self.wait.until(EC.element_to_be_clickable(self.proposal_card)).click()
        self.click_next()