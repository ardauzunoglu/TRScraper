import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def beyazperde_scrape():
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
            -         Beyazperde Scraper'a hoş geldiniz!            -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global film, file, delay, review_texts, review_useful, review_not_useful, review_scores, member_name_texts, date_texts, scrape_useful, scrape_scores, scrape_member_name, scrape_date, path

        film = input("İncelemelerin Çekileceği Film: ")
        file = input("Oluşturulacak Excel dosyasının adı: ") + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        review_texts = []
        review_useful = []
        review_not_useful = []
        review_scores = []
        member_name_texts = []
        date_texts = []

        scrape_useful_input = input("İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): ")
        scrape_scores_input = input("Filme verilen puan çekilsin mi(y/n): ")
        scrape_member_name_input = input("Kullanıcı isimleri çekilsin mi(y/n): ")
        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        
        scrape_useful = preference(scrape_useful_input)
        scrape_scores = preference(scrape_scores_input)
        scrape_member_name = preference(scrape_member_name_input)
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
            print("Beyazperde adresine gidiliyor...")
            driver.get("http://www.beyazperde.com")
            time.sleep(delay)
            driver.maximize_window()
            time.sleep(delay)
            print("Beyazperde adresine gidildi.")

        except:
            print("Beyazperde'ye erişilemiyor.")
            sys.exit()

        try:
            print("Film aranıyor...")
            search = driver.find_element_by_class_name("header-search-input")
            search.send_keys(film)
            time.sleep(delay+3)

            auto_complete = driver.find_element_by_class_name("autocomplete-result-title")
            auto_complete.click()
            time.sleep(delay)
            print("Film bulundu.")
            
        except NoSuchElementException:
            print("Film bulunamadı.")
            sys.exit()

        try:
            member_reviews = driver.find_element_by_link_text("Üye Eleştirileri")
            member_reviews.click()
            time.sleep(delay)

            review_count = driver.find_element_by_class_name("titlebar-title.titlebar-title-md").text
            review_count = int(review_count.replace(" kullanıcı eleştirisi",""))
            time.sleep(delay)

        except NoSuchElementException:
            print("Film incelemeleri bulunamadı.")
            sys.exit()

        try:
            close_banner = driver.find_element_by_id("creativeClose")
            close_banner.click()
            time.sleep(delay)

        except NoSuchElementException:
            pass
    
        if (review_count % 20) == 0:
            review_page_count = review_count // 20

        else:
            review_page_count = (review_count // 20) + 1

        constant_url = driver.current_url

        l = 1
        while l <= review_page_count:

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

            reviews = driver.find_elements_by_class_name("review-card-content")
            for review in reviews:
                review = review.text
                review_texts.append(review)

            usefuls = driver.find_elements_by_class_name("reviews-users-comment-useful")
            for useful_unp in usefuls:
                useful_unp = useful_unp.text
                useful_unp = useful_unp.split()

                useful = useful_unp[0][0]
                not_useful = useful_unp[0][1]

                review_useful.append(useful)
                review_not_useful.append(not_useful)

            scores = driver.find_elements_by_class_name("stareval-note")
            for score in scores:
                score = score.text
                score = score.replace(",0","")
                review_scores.append(score)

            member_names = driver.find_elements_by_class_name("review-card-user-infos.cf")
            for member_name in member_names:
                member_name = member_name.text
                seperation = member_name.index("\n")
                member_name = member_name[:seperation]
                member_name_texts.append(member_name)

            dates = driver.find_elements_by_class_name("review-card-meta-date")
            for date in dates:
                date = date.text
                date = date.split()
                date = date[:3]
                date = " ".join(date)
                date_texts.append(date)

            l += 1
            url = constant_url + "?page=" + str(l)
            driver.get(url)

        driver.close()
        
        length_list = [review_texts, review_useful, review_not_useful, review_scores, member_name_texts, date_texts]
        limit = map(len, length_list)
        limit = min(list(limit))
        limit -= 1

        review_texts_fin = review_texts[:limit]
        df = pd.DataFrame({"İncelemeler":review_texts_fin})

        if scrape_useful:
            review_useful_fin = review_useful[:limit]
            review_not_useful_fin = review_not_useful[:limit]
            df["İncelemeyi Yararlı Bulanlar"] = review_useful_fin
            df["İncelemeyi Yararlı Bulmayanlar"] = review_not_useful_fin

        if scrape_scores:
            review_scores_fin = review_scores[:limit]
            df["İnceleme Puanları"] = review_scores_fin

        if scrape_member_name:
            member_name_texts_fin = member_name_texts[:limit]
            df["İncelemeyi Yayınlayan Kişi"] = member_name_texts_fin

        if scrape_date:
            date_texts_fin = date_texts[:limit]
            df["İncelemenin Yayınlanma Tarihi"] = date_texts_fin

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
    beyazperde_scrape()