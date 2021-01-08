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

            return delay

        print("""
                ---------------------------------------------------------
                -         Gittigidiyor Scraper'a hoş geldiniz!          -
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
            print("Gittigidiyor adresine gidiliyor...")
            driver.get("https://www.gittigidiyor.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Gittigidiyor adresine gidildi.")

        except:
            print("Gittigidiyor'a erişilemiyor.")
            sys.exit()

        try:
            print("Ürün aranıyor...")
            search_bar = driver.find_element_by_xpath("//*[@id='__next']/header/div[3]/div/div/div/div[2]/form/div/div[1]/div[2]/input")
            search_bar.send_keys(product_name)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(delay)

            product = driver.find_element_by_class_name("srp-item-list")
            product.click()
            time.sleep(delay)
            print("Ürün bulundu.")

        except NoSuchElementException:
            print("Ürün bulunamadı.")
            sys.exit()

        url = driver.current_url
        root = url.index("_")
        url = url[:root]
        url = url + "/yorumlari"
        driver.get(url)

        review_counts = driver.find_element_by_class_name("catalog-point-content").text
        review_counts = int(review_counts.replace("Kullanıcı Değerlendirmesi", ""))

        if review_counts % 10 == 0:
            length_of_page = review_counts // 10
        else:
            length_of_page = (review_counts // 10) + 1

        l = 1 

        while l <= length_of_page:
            
            print("İncelemeler çekiliyor...")
            print("Sayfa: " + str(l))
            
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False

            while match == False:
                lastCount = lenOfPage
                time.sleep(delay)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

            time.sleep(delay)

            reviews = driver.find_elements_by_class_name("user-catalog-review-comment-detail")
            for review in reviews:
                review = review.text
                if review == "":
                    review = "BOŞ"
                review_texts.append(review)

                print("Veriler çekiliyor...")
                print("İnceleme: " + str(len(review_texts)))

            time.sleep(delay)

            usefuls = driver.find_elements_by_class_name("point-count")
            for useful in usefuls:
                useful = useful.text
                if useful == "":
                    useful = "0"
                review_useful.append(useful)
            
            headlines = driver.find_elements_by_class_name("user-catalog-review-header")
            for headline in headlines:
                headline = headline.text 
                if headline == "":
                    headline = "BOŞ"
                review_headlines.append(headline)
            
            customers = driver.find_elements_by_class_name("user-detail-container")
            for customer in customers:
                customer = customer.text
                customer = customer.split()

                customer_name = customer[0]
                customer_name_texts.append(customer_name)

                date = customer[1]
                date_texts.append(date)
            
            try:
                next_button = driver.find_element_by_class_name("next-link")
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
            df["Yorum Beğeni Sayısı"] = df["Yorum Beğeni Sayısı"]

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

        time.sleep(3)
    initialize()
    scrape()

if __name__ == "__main__":
    gittigidiyor_scrape()