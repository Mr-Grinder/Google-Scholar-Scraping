import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get url
with open("scholar_profile_urls.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    profile_urls = [row[0] for row in reader]

# Browser
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Data
results = []

for url in profile_urls:
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "gsc_prf_in")))
        time.sleep(2)  # невелика пауза

        full_name = driver.find_element(By.ID, "gsc_prf_in").text
        position = driver.find_element(By.CLASS_NAME, "gsc_prf_il").text
        email_el = driver.find_elements(By.CLASS_NAME, "gsc_prf_ila")
        email_domain = email_el[0].text if email_el else ""

        cited_el = driver.find_elements(By.CLASS_NAME, "gsc_rsb_std")
        cited_by = cited_el[0].text if cited_el else "0"

        tag_elements = driver.find_elements(By.CLASS_NAME, "gsc_prf_inta")
        tags = ", ".join([tag.text for tag in tag_elements])

        results.append({
            "Повне імʼя": full_name,
            "Посада": position,
            "Домен електронної пошти": email_domain,
            "Кількість цитованих": cited_by,
            "Теги": tags,
            "URL профілю": url
        })

        print(f"✅ Зібрано: {full_name}")

    except Exception as e:
        print(f"⚠️ Помилка з профілем: {url} — {e}")

driver.quit()

# Saving in file
with open("scholar_profile_details.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
