import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def ciceksepeti_scraper():
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
                -         Çiçeksepeti Scraper'a hoş geldiniz!           -
                -         Geliştirici: Arda Uzunoğlu                    -
                ---------------------------------------------------------
        """)

        global product_name, file, delay, review_texts, customer_province_texts, customer_name_texts, date_texts, scrape_province, scrape_customer_names, scrape_dates, path

        product_name = input("İncelemelerin çekileceği ürün adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = delay_check(input("Bekleme süresi(sn): "))    

        review_texts = []
        customer_province_texts = []
        customer_name_texts = []
        date_texts = []

        scrape_province_question = "Müşterinin konumu çekilsin mi(y/n): "
        scrape_province_input = input(scrape_province_question)
        scrape_province = preference(scrape_province_input, scrape_province_question)

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
            print("Çiçeksepeti adresine gidiliyor...")
            driver.get("https://www.ciceksepeti.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Çiçeksepeti adresine gidildi.")

        except:
            print("Çiçeksepeti'ne erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_class_name("product-search__input")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("products__item-inner")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        see_all_reviews = driver.find_element_by_class_name("comments__all-comments")
        see_all_reviews.click()

        review_count = driver.find_element_by_class_name("page-comments__product-evaluation__comment-count").text.replace("Yorum", "")
        review_count = int(review_count.strip("()"))

        if review_count % 20 == 0:
            length_of_page = review_count // 20

        else:
            length_of_page = (review_count // 20) + 1 

        l = 1

        while l <= length_of_page:
            print("İncelemeler çekiliyor...")
            print("Sayfa: " + str(l))

            time.sleep(delay)

            reviews = driver.find_elements_by_class_name("page-comments__list__item")
            for review in reviews:
                review_text = review.find_element_by_class_name("page-comments__list__item__text").text
                if review_text == "":
                    review_text = "BOŞ"
                review_texts.append(review_text)
                
                customer_name = review.find_element_by_class_name("page-comments__list__item__name").text
                customer_name_texts.append(customer_name)

                try:
                    review = review.text.replace(review_text, "")

                except:
                    pass

                review = review.replace(customer_name, "")
                review = review.replace(" | ", "").split()
                customer_province = review[0]
                date = review[1]

                customer_province_texts.append(customer_province)
                date_texts.append(date)

            try:
                driver.execute_script("window.scrollTo(0, 2160)") 
                next_page = driver.find_element_by_class_name("cs-next")
                next_page.click()
                
            except:
                pass
        
            l += 1

        driver.close()

        length_list = [review_texts, customer_province_texts, customer_name_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1
            
        review_texts_fin = review_texts[:limit]
        df = pd.DataFrame({"Yorum": review_texts_fin})

        if scrape_province:
            customer_province_texts_fin = customer_province_texts[:limit]
            df["Yorum Beğeni Sayısı"] = customer_province_texts_fin
            df["Yorum Beğeni Sayısı"] = df["Yorum Beğeni Sayısı"]

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
    ciceksepeti_scraper()