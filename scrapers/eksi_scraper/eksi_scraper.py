import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys

def eksisozluk_scrape():
    def initialize():
        def preference(scrape_input, question):
            while (scrape_input.lower() != "y") or (scrape_input.lower() != "n"):
                if scrape_input.lower() == "y":
                    output = True
                    break

                elif scrape_input.lower() == "n":
                    output = False
                    break

                else:
                    print("Geçersiz yanıt.")
                    scrape_input = input(question) 

            return output

        def delay_check(delay):
            while type(delay) != int:
                try:
                    delay = int(delay)
                except ValueError:
                    print("Lütfen bir sayı değeri giriniz.")
                    delay = input("Bekleme süresi: ")
            
            return delay
            
        print("""
            ---------------------------------------------------------
            -         Ekşi Sözlük Scraper'a hoş geldiniz!           -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global title, file, delay, entry_texts, author_texts, date_texts, scrape_author_input, scrape_date_input, scrape_author, scrape_date, path

        title = input("Entrylerin çekileceği başlık: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = delay_check(input("Bekleme süresi(sn): "))

        entry_texts = []
        author_texts = []
        date_texts = []

        scrape_author_question = "Yazar isimleri çekilsin mi(y/n): "
        scrape_author_input = input(scrape_author_question)
        scrape_author = preference(scrape_author_input, scrape_author_question)

        scrape_date_question = "Entry tarihleri çekilsin mi(y/n): "
        scrape_date_input = input(scrape_date_question)
        scrape_date = preference(scrape_date_input, scrape_date_question)

        path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

    def scrape():
        try:
            print("Chromedriver'a erişiliyor...")
            driver = webdriver.Chrome(path)
            time.sleep(delay)
            print("Chromedriver'a erişildi.")

        except WebDriverException:
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
            search_bar = driver.find_element_by_id("search-textbox")
            search_bar.send_keys(title)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)
            print("Başlık bulundu.")

        except NoSuchElementException:
            print("Başlık bulunamadı.")
            sys.exit()

        try:
            length_of_title = driver.find_element_by_class_name("last")
            length_of_title = int(length_of_title.text)

        except NoSuchElementException:
            length_of_title = 1

        l = 1

        while l <= length_of_title:

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
                close_ad = driver.find_element_by_id("interstitial-close-link-tag")
                close_ad.click()
                time.sleep(delay)

            except NoSuchElementException:
                try:
                    next_page = driver.find_element_by_class_name("next")
                    next_page.click()

                except NoSuchElementException:
                    pass

        driver.close()

        length_list = [entry_texts, author_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1

        entry_texts_fin = entry_texts[:limit]
        df = pd.DataFrame({"Entryler": entry_texts_fin})

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["Tarihler"] = date_texts_fin

        if scrape_author:
            author_texts_fin = author_texts[:limit]
            df["Yazarlar"] = author_texts_fin

        df.to_excel(file, header = True, index = False)

        print("Başlık kazıması tamamlandı.")
        print("Çektiğiniz veriler "+ file + " adlı excel dosyasına kaydedildi.")
        print("""
            --------------------------------------------------------------------------
            -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
            -  Github Hesabım: ardauzunoglu                                          -
            --------------------------------------------------------------------------
        """)

        time.sleep(3)

    initialize()
    scrape()

if __name__ == "__main__":
    eksisozluk_scrape()