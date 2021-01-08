import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def incehesap_scraper():
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
                -         İncehesap Scraper'a hoş geldiniz!             -
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
            print("İncehesap adresine gidiliyor...")
            driver.get("https://www.incehesap.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("İncehesap adresine gidildi.")

        except:
            print("İncehesap'a erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_id("query")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("product-link")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        try:
            cancel_cookie_pop = driver.find_element_by_xpath("/html/body/div[4]/div/button")
            cancel_cookie_pop.click()
        except:
            pass

        try:
            time.sleep(delay)
            review_count = driver.find_element_by_xpath("/html/body/div[2]/div[1]/main/section[1]/div[2]/div[3]/div[4]/div[2]/a[2]")
            review_count.click()
            review_count = review_count.text.replace("(", "")
            review_count = review_count.replace(")", "")
            review_count = int(review_count.replace("Yorumlar", ""))

        except NoSuchElementException:
            print("İnceleme bulunamadı.")
            sys.exit()

        try:
            time.sleep(delay)
            load_all_comments = driver.find_element_by_class_name("all-comments")
            load_all_comments.click()

        except:
            pass

        while len(review_texts) <= review_count:
            
            time.sleep(delay)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")

            comments = driver.find_elements_by_class_name("item")
            for comment in comments:
                try:
                    customer = comment.find_element_by_xpath("//*[@id='comment-list']/div["+str(len(review_texts)+2)+"]/div[1]/strong").text
                    customer_name_texts.append(customer)

                    date = comment.find_element_by_xpath("//*[@id='comment-list']/div["+str(len(review_texts)+2)+"]/div[1]/span").text.split()
                    date = " ".join(date[:3])
                    date_texts.append(date)

                    headline = comment.find_element_by_xpath("//*[@id='comment-list']/div["+str(len(review_texts)+2)+"]/div[3]/b").text
                    if headline == "":
                        review_headlines.append("BOŞ")
                    else:
                        review_headlines.append(headline)

                    useful = comment.find_element_by_xpath("//*[@id='comment-list']/div["+str(len(review_texts)+2)+"]/div[4]/a[1]").text
                    useful = useful.replace("Evet", "").replace("(", "").replace(")", "")
                    review_useful.append(useful)

                    review = comment.find_element_by_xpath("//*[@id='comment-list']/div["+str(len(review_texts)+2)+"]/div[3]/span").text
                    review_texts.append(review)

                    print("İncelemeler çekiliyor...")
                    print("İnceleme: " + str(len(review_texts)))

                except:
                    break

            break

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
    incehesap_scraper()