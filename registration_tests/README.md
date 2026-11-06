# Registration Tests

Automated browser tests for the registration and onboarding flow at `https://app.xtenav.com/register`. The tests use Selenium with Chrome and pytest.

## Requirements

- Python 3.10 or later
- Google Chrome
- Internet access (the test suite opens the live registration site; `webdriver-manager` may also download ChromeDriver)

## Setup on Windows

Open PowerShell in the project directory (the directory containing `requirements.txt`), then run:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell prevents virtual environment activation, either use Command Prompt:

```bat
venv\Scripts\activate.bat
```

or run the environment's Python directly without activating it:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the tests

With the virtual environment activated:

```powershell
pytest
```

Or, without activating it:

```powershell
.\venv\Scripts\python.exe -m pytest
```

To run one test module:

```powershell
pytest tests/test_registration.py
```

The browser is launched by the test fixture and navigates to the live registration page. The valid-registration test submits the registration form and proceeds through onboarding, so run it only when you are authorized to use the site and its test data.

## Test output

- Pytest runs verbosely and writes a self-contained HTML report to `report.html` (configured in `pytest.ini`).
- A screenshot is saved under `screenshots/` when a test fails during its call phase.
- The test fixture closes the browser after each test.

## Project layout

```text
base/       Selenium WebDriver fixture
pages/      Registration page interactions and locators
tests/      Pytest registration tests and fixtures
utils/      Shared helper functions
```
