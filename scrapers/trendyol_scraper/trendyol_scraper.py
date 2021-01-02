import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def trendyol_scrape():
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
            -         Trendyol Scraper'a hoş geldiniz!              -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, review_useful, customer_name_texts, date_texts, scrape_useful, scrape_customer_name, scrape_date, path

        product_name = input("İncelemelerin çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = delay_check(input("Bekleme süresi(sn): "))

        review_texts = []
        review_useful = []
        customer_name_texts = []
        date_texts = []

        scrape_useful_question = "İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): "
        scrape_useful_input = input(scrape_useful_question)
        scrape_useful = preference(scrape_useful_input, scrape_useful_question)

        scrape_customer_name_question = "Müşteri isimleri çekilsin mi(y/n): "
        scrape_customer_name_input = input(scrape_customer_name_question)
        scrape_customer_name = preference(scrape_customer_name_input, scrape_customer_name_question)

        scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
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
            print("Trendyol adresine gidiliyor...")
            driver.get("https://www.trendyol.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Trendyol adresine gidildi.")

        except:
            print("Trendyola'a erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_class_name("search-box")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("prdct-desc-cntnr")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        url = driver.current_url
        index_of_question_mark = url.index("?")
        url = url[:index_of_question_mark]
        url = url + "/yorumlar"
        driver.get(url)

        review_count = driver.find_element_by_class_name("pr-rnr-sm-p-s").text
        review_count = review_count.replace("Değerlendirme", "")
        review_count = review_count.replace("Yorum", "")
        review_count = review_count.split()
        review_count = int(review_count[1])

        while len(review_texts) < review_count:

            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False

            while match == False:
                lastCount = lenOfPage
                time.sleep(delay)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

            time.sleep(delay)

            reviews = driver.find_elements_by_class_name("rnr-com-tx")
            for review in reviews:
                review = review.text
                review_texts.append(review)

                print("Veriler çekiliyor...")
                print("İnceleme: " + str(len(review_texts)))

            usefuls = driver.find_elements_by_xpath("//*[@class='tooltip-wrp']//span[2]")
            for useful in usefuls:
                useful = useful.text
                useful = useful.strip("()")
                review_useful.append(useful)

            customers = driver.find_elements_by_xpath("//*[@class='rnr-com-bt']//span[@class = 'rnr-com-usr']")
            for customer in customers:
                customer = customer.text
                customer = customer.replace("|","")
                customer = customer.split()

                customer_name = customer[-3:]
                customer_name = " ".join(customer_name)
                customer_name_texts.append(customer_name)

                date = customer[:-3]
                date = " ".join(date)
                date_texts.append(date)

        driver.close()

        length_list = [review_texts, review_useful, customer_name_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1

        review_texts_fin = review_texts[:limit]
        df = pd.DataFrame({"Yorum": review_texts_fin})

        if scrape_useful:
            review_useful_fin = review_useful[:limit]
            df["Yorum Beğeni Sayısı"] = review_useful_fin

        if scrape_customer_name:
            customer_name_texts_fin = customer_name_texts[:limit]
            df["Yorum Yazan Müşteri"] = customer_name_texts_fin

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["Yorumun Yazıldığı Tarih"] = date_texts_fin

        df.to_excel(file, header = True, index = False)

        x = "Çektiğiniz veriler " + file + " adlı excel dosyasına kaydedildi."
        print(x)
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
    trendyol_scrape()