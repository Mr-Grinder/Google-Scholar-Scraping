import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

# ——————————————————
# CSV
CSV_FILE = "scholar_profile_urls.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])


all_urls = set()
with open(CSV_FILE, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        all_urls.add(row[0])

# ——————————————————
# Browser
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

driver.get("https://scholar.google.lt/citations?view_op=search_authors&hl=en&mauthors=label:biocatalysis")
print("⏳ Зайди в Google та пройди верифікацію (маєш 30 с)…")
time.sleep(30)

wait = WebDriverWait(driver, 15)
page_count = 0

while True:
    try:
        elems = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gs_ai_name")))
        new_links = []
        for e in elems:
            href = e.find_element(By.TAG_NAME, "a").get_attribute("href")
            if href not in all_urls:
                all_urls.add(href)
                new_links.append(href)

        # Saving
        if new_links:
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                for link in new_links:
                    writer.writerow([link])

        print(f"✅ Сторінка {page_count + 1} | Додано: {len(new_links)} | Усього: {len(all_urls)}")
        page_count += 1

        # Botton next
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "gsc_pgn_pnx")))
            btn.click()
            time.sleep(3)
        except Exception as e:
            print(f"🚩 Кінець або помилка з кнопкою Next: {e}")
            break

    except Exception as e:
        print(f"❌ Помилка на сторінці {page_count + 1}: {e}")
        break

driver.quit()
print("🎉 Готово! Збережено", len(all_urls), "унікальних URL.")
