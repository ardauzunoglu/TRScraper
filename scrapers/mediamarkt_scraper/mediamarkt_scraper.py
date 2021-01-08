import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def mediamarkt_scraper():
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
                -         MediaMarkt Scraper'a hoş geldiniz!            -
                -         Geliştirici: Arda Uzunoğlu                    -
                ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, review_headlines, review_useful, customer_name_texts, date_texts, scrape_headlines, scrape_useful, scrape_customer_names, scrape_dates, path

        product_name = input("İncelemelerin çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = delay_check(input("Bekleme süresi(sn): "))    

        review_texts = []
        review_useful = []
        review_headlines = []
        customer_name_texts = []
        date_texts = []

        scrape_useful_question = "İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): "
        scrape_useful_input = input(scrape_useful_question)
        scrape_useful = preference(scrape_useful_input, scrape_useful_question)

        scrape_headlines_question = "İncelemenin başlığı çekilsin mi(y/n): "
        scrape_headlines_input = input(scrape_headlines_question)
        scrape_headlines = preference(scrape_headlines_input, scrape_headlines_question)

        scrape_customer_name_question = "Müşteri isimleri çekilsin mi(y/n): "
        scrape_customer_name_input = input(scrape_customer_name_question)
        scrape_customer_names = preference(scrape_customer_name_input, scrape_customer_name_question)

        scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
        scrape_date_input = input(scrape_date_question)
        scrape_dates = preference(scrape_date_input, scrape_date_question)

        path = "BURAYA CHROMEDRİVER KONUMUNU GİRİNİZ"

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
            print("MediaMarkt adresine gidiliyor...")
            driver.get("https://www.mediamarkt.com.tr")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("MediaMarkt adresine gidildi.")

        except:
            print("MediaMarkt'a erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_xpath("//*[@id='search-autocomplete']/form/input[1]")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("clickable")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        time.sleep(delay)
        review_count = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/div[1]/h2").text.replace("Yorumlar ", "")
        review_count = review_count.replace("(", "")
        review_count = review_count.replace(")", "")
        review_count = int(review_count)
        driver.execute_script("window.scrollTo(0, 1080)")

        while len(review_texts) < review_count:
            if len(review_texts) <= 2:
                try:
                    useful = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[1]/li["+str(len(review_texts) + 1)+"]/article/div[1]").text
                    useful_prep = useful.split()[0]
                    review_useful.append(useful_prep)

                    headline = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[1]/li["+str(len(review_texts) + 1)+"]/article/h3").text
                    review_headlines.append(headline)

                    customer_name = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[1]/li["+str(len(review_texts) + 1)+"]/aside/strong").text
                    customer_name_texts.append(customer_name)

                    date = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[1]/li["+str(len(review_texts) + 1)+"]/aside/small").text
                    date_texts.append(date)

                    review = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[1]/li["+str(len(review_texts) + 1)+"]/article").text
                    question = driver.find_element_by_class_name("review-rate").text

                    review = review.replace(useful, "").replace(headline, "").replace(question, "")
                    review_texts.append(review)
                    print("Veriler çekiliyor...")
                    print("İnceleme: " + str(len(review_texts)))

                except:
                    break

                try:
                    cookie_accept_button = driver.find_element_by_xpath("//*[@id='cookie-info-layer']/div[1]/div/div[2]/a")
                    cookie_accept_button.click()

                except:
                    pass
                
                try:
                    load_all_reviews = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/div[3]/a[1]")
                    load_all_reviews.click()
                
                except:
                    pass

                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                match = False

                while match == False:
                    lastCount = lenOfPage
                    time.sleep(delay)
                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                    if lastCount == lenOfPage:
                        match = True

                time.sleep(delay)
            
            else:
                try:
                    useful = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[2]/li["+str(len(review_texts) + 1)+"]/article/div[1]").text
                    useful_prep = useful.split()[0]
                    review_useful.append(useful_prep)

                    headline = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[2]/li["+str(len(review_texts) + 1)+"]/article/h3").text
                    review_headlines.append(headline)

                    customer_name = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[2]/li["+str(len(review_texts) + 1)+"]/aside/strong").text
                    customer_name_texts.append(customer_name)

                    date = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[2]/li["+str(len(review_texts) + 1)+"]/aside/small").text
                    date_texts.append(date)

                    review = driver.find_element_by_xpath("//*[@id='yorumlar-']/div/ul[2]/li["+str(len(review_texts) + 1)+"]/article").text
                    question = driver.find_element_by_class_name("review-rate").text

                    review = review.replace(useful, "").replace(headline, "").replace(question, "")
                    review_texts.append(review)
                    print("Veriler çekiliyor...")
                    print("İnceleme: " + str(len(review_texts)))

                    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                    match = False

                    while match == False:
                        lastCount = lenOfPage
                        time.sleep(delay)
                        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                        if lastCount == lenOfPage:
                            match = True

                except:
                    break

                time.sleep(delay)

        driver.close()

        length_list = [review_texts, review_useful, review_headlines, customer_name_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1
            
        review_texts_fin = review_texts[:limit]
        df = pd.DataFrame({"Yorum": review_texts_fin})

        if scrape_useful:
            review_useful_fin = review_useful[:limit]
            df["Yorum Beğeni Sayısı"] = review_useful_fin

        if scrape_headlines:
            review_headlines_fin = review_headlines[:limit]
            df["Yorumun Başlığı"] = review_headlines_fin

        if scrape_customer_names:
            customer_name_texts_fin = customer_name_texts[:limit]
            df["Yorum Yazan Müşteri"] = customer_name_texts_fin

        if scrape_dates:
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
    initialize()
    scrape()

if __name__ == "__main__":
    mediamarkt_scraper()