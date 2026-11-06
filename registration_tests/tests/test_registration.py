import pytest
from selenium.webdriver.common.keys import Keys
from pages.registration_page import RegistrationPage



def fill_step1(page, email="imvishaldhangar@gmail.com", password="Test@121212", terms=True):
    page.enter_name("Test User")
    page.enter_email(email)
    page.enter_org("Test Org")
    page.enter_password(password)
    if terms:
        page.accept_terms()


def fill_step2(page, phone="8826794520"):
    page.select_country("India")
    page.select_state("Haryana")
    page.enter_phone(phone)


def test_valid_registration(driver):
    page = RegistrationPage(driver)
    fill_step1(page)
    page.click_continue()
    assert page.is_step2_displayed(), "step 2 did not open"

    fill_step2(page)
    page.click_signup()
    assert page.is_registered(), (
        "registration did not reach /get-started; "
        f"current URL: {driver.current_url}"
    )
    page.complete_onboarding()
    assert page.is_onboarding_complete(), (
        "onboarding did not reach /all-proposals; "
        f"current URL: {driver.current_url}"
    )


def test_empty_form(driver):
    page = RegistrationPage(driver)
    # nothing entered, continue button should stay disabled
    assert not page.is_continue_enabled(), "continue is enabled on empty form"
    assert not page.is_step2_displayed()


@pytest.mark.parametrize(
    "email",
    [
        "plainaddress",
        "user@",
        "@gmail.com",
        "user@gmail",
        "user@@example.com",
        "user name@example.com",
    ],
)
def test_invalid_email(driver, email):
    page = RegistrationPage(driver)
    fill_step1(page, email=email)
    assert page.get_error(page.email_error) != "", "no error shown for " + email
    assert not page.is_continue_enabled()


@pytest.mark.parametrize(
    "missing_field,locator,error_locator",
    [
        ("name", RegistrationPage.name_input, RegistrationPage.name_error),
        ("email", RegistrationPage.email_input, None),
        ("organization", RegistrationPage.org_input, RegistrationPage.org_error),
        ("password", RegistrationPage.password_input, RegistrationPage.password_error),
        ("terms", None, None),
    ],
)
def test_required_field_missing(driver, missing_field, locator, error_locator):
    page = RegistrationPage(driver)
    fill_step1(page, terms=missing_field != "terms")
    if locator is not None:
        field = driver.find_element(*locator)
        field.clear()
        field.send_keys(Keys.TAB)

    if missing_field == "terms":
        assert not page.is_continue_enabled(), "continue is enabled without accepting terms"
    else:
        page.click_continue()

    assert not page.is_step2_displayed(), (
        "step 2 opened with the "
        + missing_field
        + " field empty or unchecked"
    )
    if error_locator is not None:
        assert page.get_error(error_locator) != "", (
            "no validation error shown for missing "
            + missing_field
        )
    elif missing_field == "email":
        assert not driver.execute_script(
            "return arguments[0].validity.valid",
            driver.find_element(*locator),
        ), "empty email is considered valid"


def test_password_mismatch(driver):
    # this page has no confirm password field so there is nothing to compare
    pytest.skip("No confirm password field on the registration page")


def test_terms_not_accepted(driver):
    page = RegistrationPage(driver)
    fill_step1(page, terms=False)
    assert not page.is_continue_enabled(), "continue enabled without accepting terms"
    assert not page.is_step2_displayed()


@pytest.mark.parametrize("phone", ["12345", "1234567890123456", "1234567890"])
def test_invalid_phone_number(driver, phone):
    page = RegistrationPage(driver)
    fill_step1(page)
    page.click_continue()
    fill_step2(page, phone=phone)
    page.click_signup()
    assert page.get_error(page.phone_error) != "", "no error shown for " + phone
    assert not page.is_registered(), "short phone number was accepted"
