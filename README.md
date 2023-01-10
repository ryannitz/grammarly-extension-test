# Python grammarly extension UI test script

See previous failed attempt with wdio and my aspirations to use POM (details below): https://github.com/ryannitz/pagefreezer-failed-attempt/tree/main/test/pageobjects

## Setup

### 1. Clone or download the repository

### 2. Prerequisites:

Enure the following items can be executed/accessed from the root of the repo:

- python (3.10 was used)
- pip or your favorite python package manager (pip 22.3.1 was used)
- selenium

```
pip install –U selenium
```

- pytest (7.2.0 was used)

```
pip install -U pytest
```

## Test Cases

See Excel file in the root of the repo.

## Executing the test cases

In the root of the repo, run pytest:

```
pytest -v
```

Note: Shadow dom and actions.perform() make the test flaky when user interacts with the chrome page during certain steps.
Do not interact with the chrome browser while the test is executing. Extensions prevent headless execution. Ideally this would run via jenkins for nightlies and such.

## Generated test case report:

```
pytest --junitxml="{path/name}"
```

The above command will generate a standard junit xml report. Here is an example of a failed test:

```
<?xml version="1.0" encoding="utf-8"?>
<testsuites>
    <testsuite name="pytest" errors="0" failures="1" skipped="0" tests="3" time="76.838" timestamp="2023-01-06T03:52:32.789708" hostname="DESKTOP-J53FC7N">
    <testcase classname="grammarly_test" name="test_grammarly_installed_and_active" time="5.502">
        <failure message="AssertionError: assert 'enabled' == 'enable'&#10;  - enable&#10;  + enabled&#10;  ?       +">def test_grammarly_installed_and_active():
                driver = get_driver()
                before_all(driver)
                #verify we are on the extensions page
                menu_bars = driver.execute_script(selector_strings.menu_bars)
                #print(menu_bars.is_displayed())
                extension_list_container = driver.execute_script(selector_strings.extension_list_container)
                #print(extension_list_container.is_displayed())
                #verify the grammarly card is there
                grammarly_card = driver.execute_script(selector_strings.grammarly_card)
                #print(grammarly_card.is_displayed())
                #verify the grammarly extension is enabled (the user has selected it to be on)
                grammarly_card_check = driver.execute_script(selector_strings.grammarly_card_check)
        &gt;       assert grammarly_card_check.get_attribute('class') == 'enable'
        E       AssertionError: assert 'enabled' == 'enable'
        E         - enable
        E         + enabled
        E         ?       +

        grammarly_test.py:51: AssertionError</failure>
    </testcase>
    <testcase classname="grammarly_test" name="test_grammarly_correct_suggestion" time="35.517" />
    <testcase classname="grammarly_test" name="test_grammarly_incorrect_suggestion" time="35.621" />
    </testsuite>
</testsuites>
```

## Expected terminal output:

```
$ pytest -v
=================================== test session starts ====================================
platform win32 -- Python 3.10.9, pytest-7.2.0, pluggy-1.0.0 -- C:\Users\rnitz\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe
cachedir: .pytest_cacherootdir: C:\Users\rnitz\Desktop\pagefreezer-python
collected 3 items

grammarly_test.py::test_grammarly_installed_and_active
DevTools listening on ws://127.0.0.1:61779/devtools/browser/c9abd633-bdae-4af1-afaa-51bf98ee805d
PASSED                         [ 33%]
grammarly_test.py::test_grammarly_correct_suggestion
DevTools listening on ws://127.0.0.1:61892/devtools/browser/906043ad-44e1-4bb2-b8bc-778f39eeb749
PASSED                           [ 66%]
grammarly_test.py::test_grammarly_incorrect_suggestion
DevTools listening on ws://127.0.0.1:62020/devtools/browser/c998dae4-2673-4a70-a7b4-4f1fb7e3dd4c
PASSED                         [100%]

=============================== 3 passed in 82.12s (0:01:22) ===============================
```

Example of failed test in terminal output:

```
$ pytest --junitxml="report"
=========================================================================================== test session starts ===========================================================================================
platform win32 -- Python 3.10.9, pytest-7.2.0, pluggy-1.0.0
rootdir: C:\Users\rnitz\Desktop\pagefreezer-python
collected 3 items

grammarly_test.py
DevTools listening on ws://127.0.0.1:62590/devtools/browser/1137095e-2a1e-4d7d-8f1d-52e13628b3cf
F
DevTools listening on ws://127.0.0.1:62700/devtools/browser/48ef653a-cb64-41a2-9a51-40ad7fd9f8f0
.
DevTools listening on ws://127.0.0.1:62805/devtools/browser/6b055bc3-a3b8-4a9a-903c-a302bab1b54a
.                                                                                                                                                                                [100%]

================================================================================================ FAILURES =================================================================================================
___________________________________________________________________________________ test_grammarly_installed_and_active ___________________________________________________________________________________

    def test_grammarly_installed_and_active():
        driver = get_driver()
        before_all(driver)
        #verify we are on the extensions page
        menu_bars = driver.execute_script(selector_strings.menu_bars)
        #print(menu_bars.is_displayed())
        extension_list_container = driver.execute_script(selector_strings.extension_list_container)
        #print(extension_list_container.is_displayed())
        #verify the grammarly card is there
        grammarly_card = driver.execute_script(selector_strings.grammarly_card)
        #print(grammarly_card.is_displayed())
        #verify the grammarly extension is enabled (the user has selected it to be on)
        grammarly_card_check = driver.execute_script(selector_strings.grammarly_card_check)
>       assert grammarly_card_check.get_attribute('class') == 'enable'
E       AssertionError: assert 'enabled' == 'enable'
E         - enable
E         + enabled
E         ?       +

grammarly_test.py:51: AssertionError
------------------------------------------------------------------ generated xml file: C:\Users\rnitz\Desktop\pagefreezer-python\report -------------------------------------------------------------------
========================================================================================= short test summary info =========================================================================================
FAILED grammarly_test.py::test_grammarly_installed_and_active - AssertionError: assert 'enabled' == 'enable'
================================================================================= 1 failed, 2 passed in 76.87s (0:01:16) ==================================================================================
```

## Automation approach

I originally intended to use the wdio framework with jasmine testing, coupled with a standard POM architecture. This would have been a quick and elegant solution... Holy was I in for a nightmare. The initial setup went great and my pages were automating nicely. After about a day, I ran into a plethora of issues: wdio/jasmine testrunner does not permit extensions on the chromedriver in wdio.conf.ts. Whether it be via 'options', 'args', 'extensions', 'fs', or launching chromedriver with user profiles/accounts. I spent well over 8 hours trying to debug this to no avail. The last option I tried was to automate signing in to an existing chrome account that had the extension and sync enabled. It looked promising until I discovered that chromedriver launches with sync turned off. Turning sync on via automation doesn't work because the popup is browser based and not dom/web based. Changing the launch args to allow sync did nothing. That option was now off the table. No wdio for me.

Note: These chromedriver issues were only encountered through wdio framework. A lot of extra work would be required to get it running the way I needed.

After that small defeat, I looked into other options. Cucumber, python, raw js, raw java. I ended up using python because:

- No large boilerplate/plugins needed (unlike cucumber with groovy/geb/stepdefs/features etc)
- I have used python selenium scripts in the past
- chromedriver accepted the extension in zip format and launched with no other requirements

If this was an enterprise solution that needed to scale and run multi-threaded etc, I would have gone with a more robust framework or implemented POM/classes/decorators/etc in python.

## Issues / Challenges

(Apart from what is mentioned above)

- The most shadow doms I have ever seen. Seems to be the latest and greatest nightmare among UI testers right now.
- Shadow doms prevented me from using standard waits based on element display/visbility/existance. This forced me to use hardcoded waiting (The worst thing ever ever ever).
- Cannot automate the download of extensions. The accept popup is browser based and not dom/web based.
- A day and a half wasted on troubleshooting chromedriver extension issues. Extension testing is an interesting concept!
- Me not checking my spam folder to see this challenge!!

-- Ryan
