import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

baslik = input("Entrylerin çekileceği başlık: ")
dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
dosya_adi = dosya_adi + ".xlsx"
entry_texts = []
author_texts = []
date_texts = []
scrape_date = True
scrape_author = True
path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(path)

time.sleep(1)

driver.get("https://eksisozluk.com")

time.sleep(1)

driver.maximize_window()

time.sleep(1)

arama_bari = driver.find_element_by_id("search-textbox")
arama_bari.send_keys(baslik)
arama_bari.send_keys(Keys.ENTER)

time.sleep(1)

baslik_uzunlugu = driver.find_element_by_class_name("last")
baslik_uzunlugu = int(baslik_uzunlugu.text)

l = 1

while l <= baslik_uzunlugu:
            
    time.sleep(1)

    entries = driver.find_elements_by_css_selector(".content")

    for entry in entries:
        entry = entry.text
        entry_texts.append(entry)

    time.sleep(1)

    dates = driver.find_elements_by_class_name("entry-date")
                
    for date in dates:
        date = date.text
        date_texts.append(date)

    time.sleep(1)

    authors = driver.find_elements_by_class_name("entry-author")

    for author in authors:
        author = author.text 
        author_texts.append(author)

    l += 1

    try:
        reklami_gec = driver.find_element_by_id("interstitial-close-link-tag")
        reklami_gec.click()
        time.sleep(1)

    except:

        sonraki = driver.find_element_by_class_name("next")
        sonraki.click()

driver.close()

df = pd.DataFrame({"Entryler": entry_texts})

if scrape_date:
    df["Tarihler"] = date_texts

if scrape_author:
    df["Yazarlar"] = author_texts

df.to_excel(dosya_adi, header = True, index = False)

x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
print(x)