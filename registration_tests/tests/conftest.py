import pytest
from base.base_test import driver  # makes the driver fixture available


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # take screenshot when a test fails
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            file_name = "screenshots/" + item.name.replace("[", "_").replace("]", "") + ".png"
            driver.save_screenshot(file_name)
