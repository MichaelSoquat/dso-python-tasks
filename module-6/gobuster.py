import argparse
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Own 'Gobuster' with selenium")
    parser.add_argument("-url", "--url", type=str, required=True, help="Enter the base URL")
    parser.add_argument("-wordlist", type=str, required=True, help="Path of wordlist")
    args = parser.parse_args()

    url = args.url
    wordlist_path = args.wordlist

    # Configuration of selenium
    driver_path = "/usr/local/bin/geckodriver" 
    options = Options()
    options.add_argument("--headless")
    service = Service(executable_path=driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    # Check dirs
    def check_for_dirs(driver, base_url, directory):
        full_url = f"{base_url}/{directory}"
        
        try:
            driver.get(full_url)
            time.sleep(2)
            base_content= driver.page_source

            driver.get(full_url)
            time.sleep(2)  
            
            full_content = driver.page_source
            
            if base_content != full_content:
                print(f"Found dir: {full_url}")
        
        except Exception as e:
            print(f"An error occurred with {full_url}: {str(e)}")
            
    # Open wordlist and check lines
    try:
        with open(wordlist_path, 'r') as file:
            dirs = [line.strip() for line in file]
        for dir in dirs:
            check_for_dirs(driver, url, dir)
    except FileNotFoundError:
        print(f"Wordlist not found under {wordlist_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
