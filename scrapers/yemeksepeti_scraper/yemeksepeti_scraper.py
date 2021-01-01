import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

def yemeksepeti_scrape():
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
            -         Yemeksepeti Scraper'a hoş geldiniz!           -
            -         Geliştirici: Arda Uzunoğlu                    -
            ---------------------------------------------------------
        """)

        global restaurant_info, username_info, password_info, city_info, file, delay, review_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings, scrape_author, scrape_date, scrape_speed, scrape_service, scrape_flavour, path

        restaurant_info = input("Yorumların Çekileceği Restoran: ")
        username_info = input("Yemeksepeti kullanıcı adı: ")
        password_info = input("Yemeksepeti parola: ")
        password_info = "ardaardaarda1"
        city_info = input("Yemeksepeti Şehir: ")
        file = input("Oluşturulacak Excel dosyasının adı: ")
        file = file + ".xlsx"
        delay = int(input("Bekleme süresi: "))

        review_texts = []
        author_texts = []
        date_texts = []
        speed_ratings = []
        service_ratings = []
        flavour_ratings = []

        scrape_author_input = input("Müşteri isimleri çekilsin mi(y/n): ")
        scrape_author = preference(scrape_author_input)

        scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
        scrape_date = preference(scrape_date_input)

        scrape_speed_input = input("İncelemedeki hız puanı çekilsin mi(y/n): ")
        scrape_speed = preference(scrape_speed_input)

        scrape_service_input = input("İncelemedeki servis puanı çekilsin mi(y/n): ")
        scrape_service = preference(scrape_service_input)

        scrape_flavour_input = input("İncelemedeki lezzet puanı çekilsin mi(y/n): ")
        scrape_flavour = preference(scrape_flavour_input)
        
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

            restoran = driver.find_element_by_class_name("restaurantName")
            restoran.click()
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
        yorum_uzunlugu = yorumlar_section.text
        yorum_uzunlugu = yorum_uzunlugu.replace("Yorumlar", "")
        yorum_uzunlugu = yorum_uzunlugu.replace("(","")
        yorum_uzunlugu = yorum_uzunlugu.replace(")","")
        yorum_uzunlugu = int(yorum_uzunlugu)

        if yorum_uzunlugu % 30 == 0:
            yorum_uzunlugu = yorum_uzunlugu // 30

        else:
            yorum_uzunlugu = (yorum_uzunlugu // 30) + 1

        while l < yorum_uzunlugu:

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

if __name__ == "__main__":
    yemeksepeti_scrape()