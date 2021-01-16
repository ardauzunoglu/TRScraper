import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def amazon_scraper():
    def selenium():
        def selenium_initialize():
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

        def selenium_scrape():
            try:
                print("Chromedriver'a erişiliyor...")
                driver = webdriver.Chrome(path)
                time.sleep(delay)
                print("Chromedriver'a erişildi.")

            except WebDriverException:
                print("Chromedriver kullanılamıyor.")            
                sys.exit()

            try:
                print("Amazon adresine gidiliyor...")
                driver.get("https://www.amazon.com.tr")
                time.sleep(delay)
                driver.maximize_window()
                time.sleep(delay)
                print("Amazon adresine gidildi.")

            except:
                print("Amazon'a erişilemiyor.")
                sys.exit()

            try:
                print("Ürün aranıyor...")
                search_bar = driver.find_element_by_id("twotabsearchtextbox")
                search_bar.send_keys(product_name)
                search_bar.send_keys(Keys.ENTER)
                time.sleep(delay)

                product = driver.find_element_by_class_name("s-result-item")
                product.click()
                time.sleep(delay)
                print("Ürün bulundu.")

            except NoSuchElementException:
                print("Ürün bulunamadı.")
                sys.exit()

            try:
                time.sleep(delay)
                review_count = driver.find_element_by_id("acrCustomerReviewText")
                review_count = int(review_count.text.replace("değerlendirme", ""))

            except NoSuchElementException:
                print("İnceleme bulunamadı.")
                sys.exit()

            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False

            while match == False:
                lastCount = lenOfPage
                time.sleep(delay)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

            see_all_reviews = driver.find_element_by_xpath("//*[@id='reviews-medley-footer']/div[2]/a")
            see_all_reviews.click()

            if review_count % 10 == 0:
                length_of_page = review_count // 10

            else:
                length_of_page = (review_count // 10) + 1 

            l = 1

            while l <= length_of_page:

                print("İncelemeler çekiliyor...")
                print("Sayfa: " + str(l))

                time.sleep(delay)
                
                reviews = driver.find_elements_by_class_name("review")
                for review in reviews:
                    review_text = review.find_element_by_class_name("review-text-content").text
                    review_texts.append(review_text)

                    try:
                        headline = review.find_element_by_class_name("review-title").text
                        review_headlines.append(headline)

                    except:
                        review_headlines.append("BOŞ")
                    
                    try:
                        useful = review.find_element_by_class_name("cr-vote-text")
                        useful = useful.text.split()[0]
                        if useful.lower == "bir":
                            useful = "1"
                        review_useful.append(useful)

                    except:
                        review_useful.append("0")

                    customer = review.find_element_by_class_name("a-profile-name").text
                    customer_name_texts.append(customer)

                    date = review.find_element_by_class_name("review-date")
                    date = date.text.split()
                    date = date[1:4]
                    date = " ".join(date)
                    date_texts.append(date)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                try:
                    next_page = driver.find_element_by_class_name("a-last")
                    next_page.click()

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
        selenium_initialize()
        selenium_scrape()

    def beautifulsoup():
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

        def get_soup(url):
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            return soup

        def get_length_of_pages():
            soup = get_soup(page_url)
            review_count = int(soup.find("div", {"data-hook":"cr-filter-info-review-rating-count"}).text.split()[4])
            if review_count % 10 == 0:
                length_of_pages = review_count // 10
            else:
                length_of_pages = review_count // 10 + 1
            return length_of_pages

        def get_reviews(soup):
            reviews = soup.find_all("div", {"data-hook":"review"})
            for review in reviews:
                review = {
                    "Yorum":review.find("span", {"data-hook":"review-body"}).text.replace("\n", ""),
                    "Yorumun Beğeni Sayısı":review.find("span", {"data-hook":"helpful-vote-statement"}).text.split()[0] if review.find("span", {"data-hook":"helpful-vote-statement"}).text.split()[0] != "Bir" else "1",
                    "Yorumun Başlığı":review.find("a", {"data-hook":"review-title"}).text,
                    "Yorum Yazan Müşteri":review.find("span", {"class":"a-profile-name"}).text.replace("\n", ""),
                    "Yorumun Yazıldığı Tarih":" ".join(review.find("span", {"data-hook":"review-date"}).text.split()[1:4])
                }
                review_list.append(review)
                    
        def list_to_excel(list):
            df = pd.DataFrame(list)
            if not scrape_useful:
                df = df.drop(columns=["Yorumun Beğeni Sayısı"])

            if not scrape_headlines:
                df = df.drop(columns=["Yorumun Başlığı"])

            if not scrape_customer_names:
                df = df.drop(columns=["Yorum Yazan Müşteri"])

            if not scrape_dates:
                df = df.drop(columns=["Yorumun Yazıldığı Tarih"])

            df.to_excel(file, header = True, index = False)
            print("Excele kaydedildi.")

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

        review_list = []
        page_url = input("Ürün linki: ")
        file = input("Oluşturulacak Excel dosyasının adı: ") + ".xlsx"

        current_page = 1
        length_of_pages = get_length_of_pages()

        while current_page <= length_of_pages:
            page_url = page_url[:len(page_url)-2] + str(current_page)
            soup = get_soup(page_url)
            print("Veriler çekiliyor...")
            print("Sayfa: " + str(current_page))
            get_reviews(soup)
            current_page += 1

        list_to_excel(review_list)
        x = "Çektiğiniz veriler " + file + " adlı excel dosyasına kaydedildi."
        print(x)
        print("""
                --------------------------------------------------------------------------
                -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
                -  Github Hesabım: ardauzunoglu                                          -
                --------------------------------------------------------------------------
        """)

    print("""
                    ---------------------------------------------------------
                    -         Amazon Scraper'a hoş geldiniz!                -
                    -         Geliştirici: Arda Uzunoğlu                    -
                    ---------------------------------------------------------
    """)

    s_or_bs = input("Kullanılacak kütüphane(s/bs): ")
    if s_or_bs.lower() == "bs":
        beautifulsoup()

    elif s_or_bs.lower() == "s":
        selenium()

    else:
        print("Geçersiz yanıt.")

if __name__ == "__main__":
    amazon_scraper()