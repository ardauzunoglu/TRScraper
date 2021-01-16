import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def yemeksepeti_scrape():
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

            global restaurant_info, username_info, password_info, city_info, file, delay, review_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings, scrape_author, scrape_date, scrape_speed, scrape_service, scrape_flavour, path

            restaurant_info = input("Yorumların Çekileceği Restoran: ")
            username_info = input("Yemeksepeti kullanıcı adı: ")
            password_info = input("Yemeksepeti parola: ")
            city_info = input("Yemeksepeti Şehir: ")
            file = input("Oluşturulacak Excel dosyasının adı: ")
            file = file + ".xlsx"
            delay = delay_check(input("Bekleme süresi(sn): "))

            review_texts = []
            author_texts = []
            date_texts = []
            speed_ratings = []
            service_ratings = []
            flavour_ratings = []

            scrape_author_question = "Müşteri isimleri çekilsin mi(y/n): "
            scrape_author_input = input(scrape_author_question)
            scrape_author = preference(scrape_author_input, scrape_author_question)

            scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
            scrape_date_input = input(scrape_date_question)
            scrape_date = preference(scrape_date_input, scrape_date_question)

            scrape_speed_question = "İncelemedeki hız puanı çekilsin mi(y/n): "
            scrape_speed_input = input(scrape_speed_question)
            scrape_speed = preference(scrape_speed_input, scrape_speed_question)

            scrape_service_question = "İncelemedeki servis puanı çekilsin mi(y/n): "
            scrape_service_input = input(scrape_service_question)
            scrape_service = preference(scrape_service_input, scrape_service_question)

            scrape_flavour_question = "İncelemedeki lezzet puanı çekilsin mi(y/n): "
            scrape_flavour_input = input(scrape_flavour_question)
            scrape_flavour = preference(scrape_flavour_input, scrape_flavour_question)
            
            path = "BURAYA CHROMEDRIVER KONUMUNU GİRİNİZ"

            tr_chars = ["ğ", "ş", "ı", "ü", "ö", "ç"]
            tr2eng = {
                "ğ":"g",
                "ş":"s",
                "ı":"i",
                "ü":"u",
                "ö":"o",
                "ç":"c"
            }

            city_info = city_info.lower()
            for harf in city_info:
                if harf in tr_chars:
                    city_info = city_info.replace(harf, tr2eng[harf])

                else:
                    pass

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
                print("Yemeksepeti adresine gidiliyor...")
                url = "https://www.yemeksepeti.com/" + city_info
                driver.get(url)
                time.sleep(delay)
                driver.maximize_window()
                time.sleep(delay)
                print("Yemeksepeti adresine gidildi.")

            except:
                print("Yemeksepeti'ne ulaşılamıyor.")
                sys.exit()

            try:
                print("Yemeksepeti hesabına giriş yapılıyor...")
                username = driver.find_element_by_id("UserName")
                username.send_keys(username_info) 
                time.sleep(delay)
            
                password = driver.find_element_by_id("password")
                password.send_keys(password_info)
                password.send_keys(Keys.ENTER)
                time.sleep(delay)
                print("Yemeksepeti hesabına giriş yapıldı.")

            except NoSuchElementException:
                print("Kullanıcı adı ve/veya parola hatalı.")
                sys.exit()

            try:
                address_area = driver.find_element_by_class_name("address-area")
                address_area.click()
                time.sleep(delay)

            except NoSuchElementException:
                print("Kayıtlı adres bulunamadı.")
                sys.exit()

            try:
                print("Restoran aranıyor...")
                search_box = driver.find_element_by_class_name("search-box")
                search_box.send_keys(restaurant_info)
                search_box.send_keys(Keys.ENTER)
                time.sleep(delay+3)

                restaurant = driver.find_element_by_class_name("restaurantName")
                restaurant.click()
                time.sleep(delay)
                print("Restoran bulundu.")

            except NoSuchElementException:
                print("Restoran bulunamadı.")
                sys.exit()

            try:
                yorumlar_section = driver.find_element_by_xpath("//*[@id='restaurantDetail']/div[2]/div[1]/ul/li[4]/a")
                yorumlar_section.click()
                time.sleep(delay)

            except NoSuchElementException:
                print("Yorum bulunamadı.")
                sys.exit()

            l = 1
            review_count = yorumlar_section.text
            review_count = review_count.replace("Yorumlar", "")
            review_count = review_count.replace("(","")
            review_count = review_count.replace(")","")
            review_count = int(review_count)

            if review_count % 30 == 0:
                review_count = review_count // 30

            else:
                review_count = (review_count // 30) + 1

            while l < review_count:

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

                yorumlar = driver.find_elements_by_class_name("comment.row")
                for yorum in yorumlar:
                    yorum = yorum.text  
                    yorum = yorum.replace("\n", " ")
                    yorum = yorum.split()

                    if "." in yorum[0]:
                        yorum = yorum[1:]

                    else:
                        pass
                        
                    yorum = " ".join(yorum)
                    review_texts.append(yorum)

                authors = driver.find_elements_by_class_name("userName")
                for author in authors:
                    author = author.text
                    author_texts.append(author)

                dates = driver.find_elements_by_class_name("commentDate")
                for date in dates:
                    date = date.text
                    date_texts.append(date)

                speeds = driver.find_elements_by_class_name("speed")
                for speed in speeds:
                    speed = speed.text
                    speed = speed.replace("Hız: ", "")
                    speed_ratings.append(speed)

                services = driver.find_elements_by_class_name("serving")
                for service in services:
                    service = service.text
                    service = service.replace("Servis: ", "")
                    service_ratings.append(service)

                flavours = driver.find_elements_by_class_name("flavour")
                for flavour in flavours:
                    flavour = flavour.text
                    flavour = flavour.replace("Lezzet: ", "")
                    flavour_ratings.append(flavour)

                l += 1
                next_page = driver.find_element_by_link_text(str(l))
                next_page.click()

            driver.close()

            def duplicates(lst, item):
                return [i for i, x in enumerate(lst) if x == item]

            if "Restoran Cevabı" in author_texts:
                girilecek_rating_indexleri = duplicates(author_texts,"Restoran Cevabı")
                for i in girilecek_rating_indexleri:
                    date_texts.insert(i, "Restoran Cevabı")
                    speed_ratings.insert(i, "Restoran Cevabı")
                    service_ratings.insert(i, "Restoran Cevabı")
                    flavour_ratings.insert(i, "Restoran Cevabı")

            elif "Yemeksepeti" in author_texts:
                girilecek_rating_indexleri = duplicates(author_texts,"Yemeksepeti")
                for i in girilecek_rating_indexleri:
                    date_texts.insert(i, "Yemeksepeti")
                    speed_ratings.insert(i, "Yemeksepeti")
                    service_ratings.insert(i, "Yemeksepeti")
                    flavour_ratings.insert(i, "Yemeksepeti")

            else:
                pass

            length_list = [review_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings]
            limit = map(len, length_list)
            limit = min(list(limit))
            limit -= 1

            review_texts = review_texts[:limit]
            df = pd.DataFrame({"Yorumlar": review_texts})

            if scrape_author:
                author_texts_fin = author_texts[:limit]
                df["Müşteriler"] = author_texts_fin

            if scrape_date:
                date_texts_fin = date_texts[:limit]
                df["Yorum Tarihi"] = date_texts_fin

            if scrape_speed:
                speed_ratings_fin = speed_ratings[:limit]
                df["Hız Değerlendirmesi"] = speed_ratings_fin

            if scrape_service:
                service_ratings_fin = service_ratings[:limit]
                df["Servis Değerlendirmesi"] = service_ratings_fin

            if scrape_flavour:
                flavour_ratings_fin = flavour_ratings[:limit]
                df["Lezzet Değerlendirmesi"] = flavour_ratings_fin

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
            review_count = int(soup.find("a", {"data-content-id":"restaurant_comments"}).text.split()[1].strip("()").replace(" ", ""))
            if review_count % 30 == 0:
                length_of_pages = review_count // 30
            else:
                length_of_pages = review_count // 30 + 1
            return length_of_pages

        def get_reviews(soup):
            reviews = soup.find_all("div", {"class":"comments-body"})
            for review in reviews:
                author = review.find("div", {"class":"userName"}).text.strip(" ")
                review_text = review.find("div", {"class":"comment"}).text.replace(author, "")
                date = review.find("div", {"class":"commentDate"}).text
                points = review.find("div", {"class":"row"}).text.split("|")
                
                if author == "Restoran Cevabı":
                    speed_rating = "Restoran Cevabı"
                    service_rating = "Restoran Cevabı"
                    flavour_rating = "Restoran Cevabı"

                elif author == "Yemeksepeti":
                    speed_rating = "Yemeksepeti"
                    service_rating = "Yemeksepeti"
                    flavour_rating = "Yemeksepeti"

                else:
                    speed_rating = points[0].replace("Hız: ", "")
                    service_rating = points[1].replace("Servis: ", "")
                    flavour_rating = points[2].split()[1]

                review_texts.append(review_text)
                author_texts.append(author)
                date_texts.append(date)
                speed_ratings.append(speed_rating)
                service_ratings.append(service_rating)
                flavour_ratings.append(flavour_rating)

        def list_to_excel(review_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings):
            df = pd.DataFrame({"Yorumlar": review_texts})

            if scrape_author:
                df["Müşteriler"] = author_texts

            if scrape_date:
                df["Yorum Tarihi"] = date_texts

            if scrape_speed:
                df["Hız Değerlendirmesi"] = speed_ratings

            if scrape_service:
                df["Servis Değerlendirmesi"] = service_ratings

            if scrape_flavour:
                df["Lezzet Değerlendirmesi"] = flavour_ratings

            df.to_excel(file, header = True, index = False)
            print("Excele kaydedildi.")

        scrape_author_question = "Müşteri isimleri çekilsin mi(y/n): "
        scrape_author_input = input(scrape_author_question)
        scrape_author = preference(scrape_author_input, scrape_author_question)

        scrape_date_question = "İnceleme tarihleri çekilsin mi(y/n): "
        scrape_date_input = input(scrape_date_question)
        scrape_date = preference(scrape_date_input, scrape_date_question)

        scrape_speed_question = "İncelemedeki hız puanı çekilsin mi(y/n): "
        scrape_speed_input = input(scrape_speed_question)
        scrape_speed = preference(scrape_speed_input, scrape_speed_question)

        scrape_service_question = "İncelemedeki servis puanı çekilsin mi(y/n): "
        scrape_service_input = input(scrape_service_question)
        scrape_service = preference(scrape_service_input, scrape_service_question)

        scrape_flavour_question = "İncelemedeki lezzet puanı çekilsin mi(y/n): "
        scrape_flavour_input = input(scrape_flavour_question)
        scrape_flavour = preference(scrape_flavour_input, scrape_flavour_question)

        review_texts = []
        author_texts = []
        date_texts = []
        speed_ratings = []
        service_ratings = []
        flavour_ratings = []

        page_url = input("Sayfa linki: ")
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

        if "Restoran Cevabı" in author_texts:
            girilecek_rating_indexleri = duplicates(author_texts,"Restoran Cevabı")
            for i in girilecek_rating_indexleri:
                date_texts.insert(i, "Restoran Cevabı")
                speed_ratings.insert(i, "Restoran Cevabı")
                service_ratings.insert(i, "Restoran Cevabı")
                flavour_ratings.insert(i, "Restoran Cevabı")

        list_to_excel(review_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings)
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
            -         Yemeksepeti Scraper'a hoş geldiniz!           -
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
    yemeksepeti_scrape()