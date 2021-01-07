import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def n11_scraper():
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
                -         N11 Scraper'a hoş geldiniz!                   -
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
            print("N11 adresine gidiliyor...")
            driver.get("https://www.n11.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("N11 adresine gidildi.")

        except:
            print("N11'e erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_id("searchData")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("productName")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        review_count = driver.find_element_by_class_name("reviewNum").text
        review_count = int(review_count)

        go_to_reviews = driver.find_element_by_id("readReviews")
        go_to_reviews.click()

        if review_count % 10 == 0:
            length_of_page = review_count // 10
        else:
            length_of_page = (review_count // 10) + 1

        l = 1

        while l <= length_of_page:
            
            print("İncelemeler çekiliyor...")
            print("Sayfa: " + str(l))
            
            time.sleep(delay)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")

            comments = driver.find_elements_by_class_name("comment")
            for comment in comments:
                
                customer = comment.find_element_by_class_name("userName").text
                customer_name_texts.append(customer)

                date = comment.find_element_by_class_name("commentDate").text
                date_texts.append(date)

                try:
                    headline = comment.find_element_by_class_name("commentTitle").text
                    review_headlines.append(headline)

                except:
                    review_headlines.append("BOŞ")

                useful = comment.find_element_by_class_name("btnComment.yesBtn").text
                useful = useful.replace("Evet", "").replace("(", "").replace(")", "")
                review_useful.append(useful)

                replaced_useful = comment.find_element_by_class_name("btnComment.yesBtn").text
                review = comment.text
                review = review.replace(customer, "").replace(date, "").replace(replaced_useful, "").replace("Bu yorumu faydalı buldunuz mu?", "")
                review_texts.append(review)

            try:
                next_button = driver.find_element_by_xpath("//*[@id='tabPanelProComments']/div/div[2]/div[2]/a[11]")
                next_button.click()

            except:
                pass

            l += 1

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
    n11_scraper()