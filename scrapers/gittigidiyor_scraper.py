import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def gittigidiyor_scrape():
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

        print("""
                ---------------------------------------------------------
                -         Gittigidiyor Scraper'a hoş geldiniz!          -
                -         Geliştirici: Arda Uzunoğlu                    -
                ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, review_headlines, customer_name_texts, date_texts, scrape_headlines, scrape_customer_names, scrape_dates, path

        product_name = input("İncelemelerin çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = delay_check(input("Bekleme süresi(sn): "))    

        review_texts = []
        review_headlines = []
        customer_name_texts = []
        date_texts = []

        scrape_headlines_question = "İncelemenin başlığı çekilsin mi(y/n): "
        scrape_headlines_input = input(scrape_headlines_question)
        scrape_headlines = preference(scrape_headlines_input, scrape_headlines_question)

        scrape_customer_name_question = "Müşteri isimleri çekilsin mi(y/n): "
        scrape_customer_name_input = input(scrape_customer_name_question)
        scrape_customer_names = preference(scrape_customer_name_input, scrape_customer_name_question)

        scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
        scrape_date_input = input(scrape_date_question)
        scrape_dates = preference(scrape_date_input, scrape_date_question)

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

        try:
            print("Ürün aranıyor...")
            arama_bari = driver.find_element_by_xpath("//*[@id='__next']/header/div[3]/div/div/div/div[2]/form/div/div[1]/div[2]/input")
            arama_bari.send_keys(product_name)
            arama_bari.send_keys(Keys.ENTER)
            time.sleep(1)

            urun = driver.find_element_by_class_name("srp-item-list")
            urun.click()
            time.sleep(1)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

    initialize()
    scrape()

gittigidiyor_scrape()