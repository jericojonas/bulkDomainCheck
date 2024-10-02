import time
import os
import subprocess  # Import subprocess to run the tele.py script
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Call gs.py to fetch data from Google Sheets and write to domain files
subprocess.run(["python3", "gs.py"])

# Set up Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

# Initialize the Chrome WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# Maximize the browser window
driver.maximize_window()

# List of domain files and corresponding result files
domain_files = {
    "domain/sheet1.txt": "result/sheet1.txt",
    "domain/sheet2.txt": "result/sheet2.txt",
    "domain/sheet3.txt": "result/sheet3.txt",
    "domain/sheet4.txt": "result/sheet4.txt",
    "domain/sheet5.txt": "result/sheet5.txt",
    "domain/sheet6.txt": "result/sheet6.txt"
}

# Function to clear the "blocked.txt" file and add initial line
def initialize_blocked_file():
    with open("blocked.txt", "w") as blocked_file:
        blocked_file.write("All Domains Active\n")

# Function to update the "blocked.txt" file with blocked domains
def update_blocked_file(blocked_data):
    with open("blocked.txt", "a") as blocked_file:
        blocked_file.write(blocked_data + "\n")

# Function to process each domain file and save the results
def process_domains(input_file, output_file):
    # Open the website
    driver.get("https://trustpositif.kominfo.go.id")

    # Read the domains from the input file
    with open(input_file, "r") as file:
        domains = file.read().strip().split('\n')

    # Join the domains into a single string with each domain on a new line
    domains_str = '\n'.join(domains)

    blocked_domains_flag = False  # Flag to check if any domain is blocked

    try:
        # Find and click the input field to trigger the modal
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "press-to-modal"))
        )
        input_field.click()

        # Wait for the modal to appear
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-dialog"))
        )

        # Find the textarea element
        textarea = modal.find_element(By.ID, "input-data")

        # Check if the textarea is visible and enabled
        if textarea.is_displayed() and textarea.is_enabled():
            # Set the domains string in the textarea using JavaScript
            driver.execute_script("arguments[0].value = arguments[1];", textarea, domains_str)
        else:
            print("Textarea is not visible or enabled.")

        # Scroll the "CARI DATA" button into view and wait for it to be clickable
        cari_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", cari_button)

        # Click the "CARI DATA" button
        cari_button.click()

        # Wait for the results to load and the table to be visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "daftar-block"))
        )

        # Wait for the results to be populated in the table
        time.sleep(1.5)  # Adding sleep to wait for the data to be populated

        # Get the data results
        result_table = driver.find_element(By.ID, "daftar-block")  # Change to the correct ID
        rows = result_table.find_elements(By.TAG_NAME, "tr")

        if not rows:
            print(f"No data found in the table for {input_file}.")
        else:
            print(f"Data found in the table for {input_file}. Writing to {output_file}...")

        # Open the output file for writing
        with open(output_file, "w") as file:
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > 1:  # Change this to correctly process the row
                    domain = cells[0].text
                    status = cells[1].text  # 'Ada' should be in the second column (index 1)
                    formatted_data = f"{domain} - {status}"
                    file.write(formatted_data + "\n")  # Write formatted data to the file
                    print(formatted_data)  # Print the formatted data as well
                    if status == "Ada":
                        update_blocked_file(formatted_data)  # Update blocked file if status is "Ada"
                        blocked_domains_flag = True  # Set flag to True if any domain is blocked

    finally:
        # Execute JavaScript to log "finish" to the console
        time.sleep(3)
        driver.execute_script('console.log("finish");')

    return blocked_domains_flag

# Initialize the "blocked.txt" file
initialize_blocked_file()

# Iterate over each domain file and process it
blocked_domains_exist = False  # Flag to check if any blocked domains exist
for domain_file, result_file in domain_files.items():
    if process_domains(domain_file, result_file):
        blocked_domains_exist = True  # Set flag to True if any blocked domains are found

# Update the "blocked.txt" file based on the existence of blocked domains
if not blocked_domains_exist:
    with open("blocked.txt", "w") as blocked_file:
        blocked_file.write("All Domains Active\n")  # If no blocked domains exist, write initial line
    print("No domains are blocked. Updated 'blocked.txt' with 'All Domains Active'.")
else:
    # Remove the line "All Domains Active" if there are blocked domains
    with open("blocked.txt", "r+") as blocked_file:
        lines = blocked_file.readlines()
        if "All Domains Active\n" in lines:
            lines.remove("All Domains Active\n")
            blocked_file.seek(0)
            blocked_file.writelines(lines)
            blocked_file.truncate()
    print("Blocked domains found. 'blocked.txt' has been updated.")

# Close the browser window
driver.quit()

# Call tele.py to send the blocked domains to Telegram
subprocess.run(["python3", "fire.py"])
subprocess.run(["python3", "tele.py"])
