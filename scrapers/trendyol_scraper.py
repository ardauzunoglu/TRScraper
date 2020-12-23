import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def trendyol_scrape():
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
            -         Trendyol Scraper'a hoş geldiniz!              -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)


        global product_name, file, delay, review_texts, review_useful, customer_name_texts, date_texts, scrape_useful, scrape_customer_name, scrape_date, path

        product_name = input("Yorumların çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        review_texts = []
        review_useful = []
        customer_name_texts = []
        date_texts = []

        scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ")
        scrape_useful = preference(scrape_useful_input)

        scrape_customer_name_input = input("Müşteri isimleri çekilsin mi(y/n): ")
        scrape_customer_name = preference(scrape_customer_name_input)

        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        scrape_date = preference(scrape_date_input)

        path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

    def scrape():
        try:
            driver = webdriver.Chrome(path)
            time.sleep(1)

        except:
            print("Chromedriver kullanılamıyor.")
            sys.exit()

        try:
            driver.get("https://www.trendyol.com")
            time.sleep(1)
            driver.maximize_window()
            time.sleep(1)

        except:
            print("Trendyola'a erişilemiyor.")
            sys.exit()

        try:
            arama_bari = driver.find_element_by_class_name("search-box")
            arama_bari.send_keys(product_name)
            arama_bari.send_keys(Keys.ENTER)
            time.sleep(1)

            urun = driver.find_element_by_class_name("prdct-desc-cntnr")
            urun.click()
            time.sleep(1)

        except:
            print("Ürün bulunamadı.")
            sys.exit()

        url = driver.current_url
        index_of_question_mark = url.index("?")
        url = url[:index_of_question_mark]
        url = url + "/yorumlar"
        driver.get(url)

        yorum_sayisi = driver.find_element_by_class_name("pr-rnr-sm-p-s")
        yorum_sayisi = yorum_sayisi.text
        yorum_sayisi = yorum_sayisi.replace("Değerlendirme", "")
        yorum_sayisi = yorum_sayisi.replace("Yorum", "")
        yorum_sayisi = yorum_sayisi.split()
        yorum_sayisi = int(yorum_sayisi[1])

        while len(review_texts) < yorum_sayisi:

            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False

            while match == False:
                lastCount = lenOfPage
                time.sleep(1)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

            time.sleep(1)

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

        x = "Çektiğiniz veriler "+ file + " adlı excel dosyasına kaydedildi."
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