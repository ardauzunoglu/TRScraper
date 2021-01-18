import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

def beyazperde_scrape():
    def selenium():
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

            global film, file, delay, review_texts, review_useful, review_not_useful, review_scores, member_name_texts, date_texts, scrape_useful, scrape_scores, scrape_member_name, scrape_date, path

            film = input("İncelemelerin Çekileceği Film: ")
            file = input("Oluşturulacak Excel dosyasının adı: ") + ".xlsx"
            delay = delay_check(input("Bekleme süresi(sn): "))

            review_texts = []
            review_useful = []
            review_not_useful = []
            review_scores = []
            member_name_texts = []
            date_texts = []

            scrape_useful_question = "İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): "
            scrape_useful_input = input(scrape_useful_question)
            scrape_useful = preference(scrape_useful_input, scrape_useful_question)

            scrape_scores_question = "Filme verilen puan çekilsin mi(y/n): "
            scrape_scores_input = input(scrape_scores_question)
            scrape_scores = preference(scrape_scores_input, scrape_scores_question)

            scrape_member_name_question = "Kullanıcı isimleri çekilsin mi(y/n): "
            scrape_member_name_input = input(scrape_member_name_question)
            scrape_member_name = preference(scrape_member_name_input, scrape_member_name_question)

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
                    score = score.text.replace(",0","")
                    review_scores.append(score)

                member_names = driver.find_elements_by_class_name("review-card-user-infos.cf")
                for member_name in member_names:
                    seperation = member_name.index("\n")
                    member_name = member_name.text[:seperation]
                    member_name_texts.append(member_name)

                dates = driver.find_elements_by_class_name("review-card-meta-date")
                for date in dates:
                    date = date.text.split()[:3]
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
            review_count = int(soup.find("h2", {"class":"titlebar-title-md"}).text.split()[0])
            if review_count % 20 == 0:
                length_of_pages = review_count // 20
            else:
                length_of_pages = review_count // 20 + 1
            return length_of_pages

        def get_reviews(soup):
            reviews = soup.find_all("div", {"class":"hred.review-card.cf"})
            for review in reviews:
                usefuls_and_not_usefuls = review.find_all("span", {"class":"txt"})
                review_element = {
                    "İncelemeler":soup.find("div", {"class":"content-txt.review-card-content"}).text.replace("\n", ""),
                    "İncelemeyi Yararlı Bulanlar":usefuls_and_not_usefuls[0].text,
                    "İncelemeyi Yararlı Bulmayanlar":usefuls_and_not_usefuls[1].text,
                    "İnceleme Puanları":review.find("span", {"class":"stareval-note"}).text,
                    "İncelemeyi Yayınlayan Kişi":review.find("div", {"class":"meta-title"}).text,
                    "İncelemenin Yayınlanma Tarihi":review.find("span", {"class":"review-card-meta-date"}).text.split()[:3]
                }
                review_list.append(review_element)
                            
        def list_to_excel(list):
            df = pd.DataFrame(list)
            if not scrape_useful:
                df = df.drop(columns=["İncelemeyi Yararlı Bulanlar"])
                df = df.drop(columns=["İncelemeyi Yararlı Bulmayanlar"])

            if not scrape_scores:
                df = df.drop(columns=["İnceleme Puanları"])

            if not scrape_member_name:
                df = df.drop(columns=["İncelemeyi Yayınlayan Kişi"])

            if not scrape_date:
                df = df.drop(columns=["İncelemenin Yayınlanma Tarihi"])

            df.to_excel(file, header = True, index = False)
            print("Excele kaydedildi.")

        scrape_useful_question = "İncelemenin aldığı beğeni sayısı çekilsin mi(y/n): "
        scrape_useful_input = input(scrape_useful_question)
        scrape_useful = preference(scrape_useful_input, scrape_useful_question)

        scrape_scores_question = "Filme verilen puan çekilsin mi(y/n): "
        scrape_scores_input = input(scrape_scores_question)
        scrape_scores = preference(scrape_scores_input, scrape_scores_question)

        scrape_member_name_question = "Kullanıcı isimleri çekilsin mi(y/n): "
        scrape_member_name_input = input(scrape_member_name_question)
        scrape_member_name = preference(scrape_member_name_input, scrape_member_name_question)

        scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
        scrape_date_input = input(scrape_date_question)
        scrape_date = preference(scrape_date_input, scrape_date_question)

        review_list = []
        page_url = input("Film linki: ")
        file = input("Oluşturulacak Excel dosyasının adı: ") + ".xlsx"

        current_page = 1
        length_of_pages = get_length_of_pages()
        while current_page <= length_of_pages:
            page_url = page_url[:len(page_url)-1] + str(current_page)
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
                    -         Beyazperde Scraper'a hoş geldiniz!            -
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
    beyazperde_scrape()