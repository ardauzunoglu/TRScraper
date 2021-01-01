import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys

def kitapyurdu_scrape():
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
            -         Kitapyurdu Scraper'a hoş geldiniz!            -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global book, file, delay, review_texts, review_useful, review_not_useful, author_texts, date_texts, scrape_useful, scrape_author, scrape_date, path

        book = input("İncelemelerin Çekileceği Kitap Adı: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        review_texts = []
        review_useful = []
        review_not_useful = []
        author_texts = []
        date_texts = []

        scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ")
        scrape_useful = preference(scrape_useful_input)

        scrape_author_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
        scrape_author = preference(scrape_author_input)

        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        scrape_date = preference(scrape_date_input)

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
            print("Kitapyurdu adresine gidiliyor...")
            driver.get("https://www.kitapyurdu.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Kitapyurdu adresine gidildi.")

        except:
            print("Kitapyurdu'na erişilemiyor.")
            sys.exit()

        try:
            print("Kitap aranıyor...")
            search = driver.find_element_by_id("search-input")
            search.send_keys(book)
            search.send_keys(Keys.ENTER)

            time.sleep(delay)

            try:
                close_notification = driver.find_element_by_class_name("opt-in-disallow-button")
                close_notification.click()

            except NoSuchElementException:
                pass

            time.sleep(delay)

            product = driver.find_element_by_class_name("name.ellipsis")
            product.click()
            time.sleep(delay)
            print("Kitap bulundu.")

        except NoSuchElementException:
            print("Kitap bulunamadı.")
            sys.exit()

        try:
            reviewsTab = driver.find_element_by_class_name("pr__htabs-review-text")
            reviewsTab.click()
            time.sleep(delay)

        except NoSuchElementException:
            print("Kitap incelemeleri bulunamadı.")
            sys.exit()

        l = 1
        review_length = reviewsTab.text.replace("Yorumlar","")
        
        try:
            review_length = review_length.replace(".","")
            review_length = int(review_length)

        except NoSuchElementException:
            review_length = int(review_length)

        if review_length % 5 == 0:
            review_length = review_length // 5
        else:
            review_length = (review_length // 5) + 1

        while l <= review_length:

            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
            match = False

            while match == False:
                lastCount = lenOfPage
                time.sleep(delay)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True

            print("Veriler çekiliyor...")
            print("Sayfa: " + str(l))

            try:
                reviews = driver.find_elements_by_class_name("review-text")
                for review in reviews:
                    review = review.text
                    review_texts.append(review)
                
                authors = driver.find_elements_by_xpath("//a[@class ='alt']//span[@itemprop='name']")
                for author in authors:
                    author = author.text 
                    author_texts.append(author)
                
                dates = driver.find_elements_by_class_name("review-date")
                for date in dates:
                    date = date.text
                    date_texts.append(date)

                usefuls = driver.find_elements_by_xpath("//div[@class ='agree']//span[@class='count']")
                for useful in usefuls:
                    useful = useful.text
                    review_useful.append(useful)

                not_usefuls = driver.find_elements_by_xpath("//div[@class ='disagree']//span[@class='count']")
                for not_useful in not_usefuls:
                    not_useful = not_useful.text
                    review_not_useful.append(not_useful)

            except NoSuchElementException:
                time.sleep(delay)

            l += 1

            try: 
                next_page = driver.find_element_by_link_text(str(l))
                next_page.click()

            except NoSuchElementException:
                time.sleep(delay)

        driver.close()

        length_list = [review_texts, review_useful, review_not_useful, author_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1

        review_texts_fin = review_texts[:limit]

        df = pd.DataFrame({"Yorumlar": review_texts_fin})

        if scrape_author:
            author_texts_fin = author_texts[:limit]
            df["Müşteriler"] = author_texts_fin

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["İnceleme Tarihi"] = date_texts_fin

        if scrape_useful:
            review_useful_fin = review_useful[:limit]
            review_not_useful_fin = review_not_useful[:limit]
            df["İncelemeyi Yararlı Bulan Kişi Sayısı"] = review_useful_fin
            df["İncelemeyi Yararlı Bulmayan Kişi Sayısı"] = review_not_useful_fin

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
    kitapyurdu_scrape()