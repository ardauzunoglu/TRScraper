import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Ekşi Sözlük Scraper'a hoş geldiniz!           -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)

    global path

    path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

def scrape():
    def spesific_initialize():

        global baslik, dosya_adi, delay, entry_texts, author_texts, date_texts, scrape_author_input, scrape_date_input, scrape_author, scrape_date

        baslik = input("Entrylerin çekileceği başlık: ")
        dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
        dosya_adi = dosya_adi + ".xlsx"
        delay = int(input("Bekleme süresi(sn): "))

        entry_texts = []
        author_texts = []
        date_texts = []

        scrape_author_input = input("Yazar isimleri çekilsin mi(y/n): ")
        while (scrape_author_input.lower() != "y") or (scrape_author_input.lower() != "n"):
            if scrape_author_input.lower() == "y":
                scrape_author = True
                break

            elif scrape_author_input.lower() == "n":
                scrape_author = False
                break

            else:
                print("Geçersiz yanıt.")
                scrape_author_input = input("Yazar isimleri çekilsin mi(y/n): ")
                print("\n")

        scrape_date_input = input("Entry tarihleri çekilsin mi(y/n): ")
        while (scrape_date_input.lower() != "y") or (scrape_date_input.lower() != "n"):
            if scrape_date_input.lower() == "y":
                scrape_date = True
                break

            elif scrape_date_input.lower() == "n":
                scrape_date = False
                break

            else:
                print("Geçersiz yanıt.")
                scrape_date_input = input("Entry tarihleri çekilsin mi(y/n): ")
                print("\n")

    def spesific_scrape():
        try:
            print("Chromedriver'a erişiliyor...")
            driver = webdriver.Chrome(path)
            time.sleep(delay)
            print("Chromedriver'a erişildi.")

        except:
            print("Chromedriver kullanılamıyor.")
            sys.exit()

        try:
            print("Ekşi Sözlük adresine gidiliyor...")
            driver.get("https://eksisozluk.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Ekşi Sözlük adresine gidildi.")

        except:
            print("Ekşi Sözlük'e erişilemiyor.")
            sys.exit()

        try:
            print("Başlık aranıyor...")
            arama_bari = driver.find_element_by_id("search-textbox")
            arama_bari.send_keys(baslik)
            arama_bari.send_keys(Keys.ENTER)
            time.sleep(delay)
            print("Başlık bulundu.")

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

            print("Veriler çekiliyor...")
            print("Sayfa: " + str(l)) 
            
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
        kisa = [len(entry_texts), len(author_texts), len(date_texts)]
        kisa = min(kisa)
        kisa -= 1

        entry_texts_fin = entry_texts[:kisa]
        df = pd.DataFrame({"Entryler": entry_texts_fin})

        if scrape_date:
            date_texts_fin = date_texts[:kisa]
            df["Tarihler"] = date_texts_fin

        if scrape_author:
            author_texts_fin = author_texts[:kisa]
            df["Yazarlar"] = author_texts_fin

        df.to_excel(dosya_adi, header = True, index = False)

        print("Başlık kazıması tamamlandı.")
        print("Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi.")

    spesific_initialize()
    spesific_scrape()

def end():

    print("""
        --------------------------------------------------------------------------
        -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
        -  Github Hesabım: ardauzunoglu                                          -
        --------------------------------------------------------------------------
    """)

    time.sleep(3)

if __name__ == "__main__":
    initialize()
    scrape()
    end()