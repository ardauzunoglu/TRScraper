import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def gittigidiyor_scrape():
    def initialize():
        def preference(scrape_input):
            while (scrape_input.lower() != "y") or (scrape_input.lower() != "n"):
                if scrape_input.lower() == "y":
                    output = True
                    break

                elif scrape_input.lower() == "n":
                    output = False
                    break

                else:
                    print("Geçersiz yanıt.")
                    scrape_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ") 

            return output
        print("""
                ---------------------------------------------------------
                -         Gittigidiyor Scraper'a hoş geldiniz!          -
                -         Geliştirici: Arda Uzunoğlu                    -
                ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, review_headlines, customer_name_texts, date_texts, scrape_headlines, scrape_customer_names, scrape_dates, path

        product_name = input("Yorumların çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))    

        review_texts = []
        review_headlines = []
        customer_name_texts = []
        date_texts = []

        scrape_useful_input = input("İncelemenin başlığı çekilsin mi(y/n): ")
        scrape_headlines = preference(scrape_useful_input)

        scrape_customer_name_input = input("Müşteri isimleri çekilsin mi(y/n): ")
        scrape_customer_names = preference(scrape_customer_name_input)

        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        scrape_dates = preference(scrape_date_input)

        path = "C:/chromedriver.exe"

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
            print("Gittigidiyor adresine gidiliyor...")
            driver.get("https://www.gittigidiyor.com")
            time.sleep(1)
            driver.maximize_window()
            time.sleep(1)
            print("Gittigidiyor adresine gidildi.")

        except:
            print("Gittigidiyor'a erişilemiyor.")
            sys.exit()

        

    initialize()
    scrape()

gittigidiyor_scrape()