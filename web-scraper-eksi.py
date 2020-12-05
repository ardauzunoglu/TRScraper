import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    global baslik, dosya_adi, delay, entry_texts, author_texts, date_texts, scrape_author, scrape_date, path

    baslik = input("Entrylerin çekileceği başlık: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    entry_texts = []
    author_texts = []
    date_texts = []

    scrape_author = True
    scrape_date = True

    path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

def scrape():
    try:
        driver = webdriver.Chrome(path)
        time.sleep(delay)

    except:
        print("Chromedriver kullanılamıyor.")
        sys.exit()

    try:
        driver.get("https://eksisozluk.com")
        time.sleep(delay)
        driver.maximize_window()
        time.sleep(delay)

    except:
        print("Ekşi Sözlük'e erişilemiyor.")
        sys.exit()

    try:
        arama_bari = driver.find_element_by_id("search-textbox")
        arama_bari.send_keys(baslik)
        arama_bari.send_keys(Keys.ENTER)

        time.sleep(delay)

    except:
        print("Başlık bulunamadı.")
        sys.exit()

    try:
        baslik_uzunlugu = driver.find_element_by_class_name("last")
        baslik_uzunlugu = int(baslik_uzunlugu.text)

    except:
        baslik_uzunlugu = 1

    l = 1

    while l <= baslik_uzunlugu:
                
        time.sleep(delay)

        entries = driver.find_elements_by_css_selector(".content")

        for entry in entries:
            entry = entry.text
            entry_texts.append(entry)

        time.sleep(delay)

        dates = driver.find_elements_by_class_name("entry-date")
                    
        for date in dates:
            date = date.text
            date_texts.append(date)

        time.sleep(delay)

        authors = driver.find_elements_by_class_name("entry-author")

        for author in authors:
            author = author.text 
            author_texts.append(author)

        l += 1

        try:
            reklami_gec = driver.find_element_by_id("interstitial-close-link-tag")
            reklami_gec.click()
            time.sleep(delay)

        except:
            try:
                sonraki = driver.find_element_by_class_name("next")
                sonraki.click()

            except:
                pass

    driver.close()

    df = pd.DataFrame({"Entryler": entry_texts})

    if scrape_date:
        df["Tarihler"] = date_texts

    if scrape_author:
        df["Yazarlar"] = author_texts

    df.to_excel(dosya_adi, header = True, index = False)

    x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
    print(x)

if __name__ == "__main__":
    initialize()
    scrape()