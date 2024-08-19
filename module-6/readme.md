# Script Overview

This script is a simple web directory brute-forcer, similar to "Gobuster," but implemented using Selenium. 

## Key Functionality:
- **Argument Parsing:** The script accepts two arguments:
  - `-url`: The base URL to test.
  - `-wordlist`: The path to a file containing a list of directory names to test against the base URL.

- **Selenium Configuration:** 
  - The script uses Selenium with Firefox in headless mode to navigate web pages.

- **Directory Checking:**
  - For each directory name in the wordlist, the script appends it to the base URL and tries to load the resulting URL.
  - It compares the content of the base URL with the content of the full URL.
  - If the contents differ, it indicates that the directory likely exists on the server.

- **Error Handling:**
  - The script handles exceptions related to file reading, Selenium operations, and URL loading.

- **Cleanup:**
  - The Selenium WebDriver is properly closed after all checks are complete.

## Quickstart

1. Clone the repository
2. Install dependencies
   ```
   pip install selenium==4.9.0
   ```
3. Download the geckodriver. Be sure that the geckodriver is installed under this path: `/usr/local/bin/geckodriver`
4. Be sure that you have the path to your wordlist
5. Start the script with:
   ```
   python gobuster.py -url <base-url> -wordlist <path/to/wordlist>

## Alternative

- The path to the geckodriver is hard coded. If you want you can add a arg parse for it to be flexible
- The script only prints out the found path. If you want to see the path he didnt find add an else block under the if block and print it out
