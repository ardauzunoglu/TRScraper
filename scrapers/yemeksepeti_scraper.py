import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def initialize():

    print("""
        ---------------------------------------------------------
        -         Yemeksepeti Scraper'a hoş geldiniz!           -
        -         Geliştirici: Arda Uzunoğlu                    -
        ---------------------------------------------------------
    """)

    global restoran_info, username_info, password_info, sehir, dosya_adi, delay, yorum_texts, author_texts, date_texts, speed_ratings, service_ratings, flavour_ratings, scrape_author, scrape_date, scrape_speed, scrape_service, scrape_flavour, path

    restoran_info = input("Yorumların Çekileceği Restoran: ")
    username_info = "ardauzunogluarda@gmail.com"
    password_info = "ardaardaarda1"
    sehir = input("Yemeksepeti Şehir: ")
    dosya_adi = input("Oluşturulacak Excel dosyasının adı: ")
    dosya_adi = dosya_adi + ".xlsx"
    delay = int(input("Bekleme süresi: "))

    yorum_texts = []
    author_texts = []
    date_texts = []
    speed_ratings = []
    service_ratings = []
    flavour_ratings = []

    scrape_author_input = input("Müşteri isimleri çekilsin mi(y/n): ")
    while (scrape_author_input.lower() != "y") or (scrape_author_input.lower() != "n"):
        if scrape_author_input.lower() == "y":
            scrape_author = True
            break

        elif scrape_author_input.lower() == "n":
            scrape_author = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_author_input = input("Müşteri isimleri çekilsin mi(y/n): ")
            print("\n")

    scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
    while (scrape_date_input.lower() != "y") or (scrape_date_input.lower() != "n"):
        if scrape_date_input.lower() == "y":
            scrape_date = True
            break

        elif scrape_date_input.lower() == "n":
            scrape_date = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_date_input = input("İnceleme tarihleri çekilsin mi(y/n): ")
            print("\n")

    scrape_speed_input = input("İncelemedeki hız puanı çekilsin mi(y/n): ")
    while (scrape_speed_input.lower() != "y") or (scrape_speed_input.lower() != "n"):
        if scrape_speed_input.lower() == "y":
            scrape_speed = True
            break

        elif scrape_speed_input.lower() == "n":
            scrape_speed = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_speed_input = input("İncelemedeki hız puanı çekilsin mi(y/n): ") 
            print("\n")

    scrape_service_input = input("İncelemedeki servis puanı çekilsin mi(y/n): ")
    while (scrape_service_input.lower() != "y") or (scrape_service_input.lower() != "n"):
        if scrape_service_input.lower() == "y":
            scrape_service = True
            break

        elif scrape_service_input.lower() == "n":
            scrape_service = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_service_input = input("İncelemedeki servis puanı çekilsin mi(y/n): ")
            print("\n")

    scrape_flavour_input = input("İncelemedeki lezzet puanı çekilsin mi(y/n): ")
    while (scrape_flavour_input.lower() != "y") or (scrape_flavour_input.lower() != "n"):
        if scrape_flavour_input.lower() == "y":
            scrape_flavour = True
            break

        elif scrape_flavour_input.lower() == "n":
            scrape_flavour = False
            break

        else:
            print("Geçersiz yanıt.")
            scrape_flavour_input = input("İnceleme lezzet puanı çekilsin mi(y/n): ")
            print("\n")
    
    path = "C:\Program Files (x86)\chromedriver.exe"

    tr_chars = ["ğ", "ş", "ı", "ü", "ö", "ç"]
    tr2eng = {
        "ğ":"g",
        "ş":"s",
        "ı":"i",
        "ü":"u",
        "ö":"o",
        "ç":"c"
    }

    sehir = sehir.lower()
    for harf in sehir:
        if harf in tr_chars:
            sehir = sehir.replace(harf, tr2eng[harf])

        else:
            pass

def scrape():
    try:
        driver = webdriver.Chrome(path)
        time.sleep(delay)

    except:
        print("Chromedriver kullanılamıyor.")
        sys.exit()

    try:
        url = "https://www.yemeksepeti.com/" + sehir
        driver.get(url)
        driver.maximize_window()
        time.sleep(delay)

    except:
        print("Yemeksepeti'ne ulaşılamıyor.")
        sys.exit()

    try:
        username = driver.find_element_by_id("UserName")
        username.send_keys(username_info) 

        password = driver.find_element_by_id("password")
        password.send_keys(password_info)
        password.send_keys(Keys.ENTER)
        time.sleep(delay)

    except:
        print("Kullanıcı adı ve/veya parola hatalı.")
        sys.exit()

    try:
        address_area = driver.find_element_by_class_name("address-area")
        address_area.click()
        time.sleep(delay)

    except:
        print("Kayıtlı adres bulunamadı.")
        sys.exit()

    try:
        search_box = driver.find_element_by_class_name("search-box")
        search_box.send_keys(restoran_info)
        search_box.send_keys(Keys.ENTER)
        time.sleep(delay+3)

        restoran = driver.find_element_by_class_name("restaurantName")
        restoran.click()
        time.sleep(delay)

    except:
        print("Restoran bulunamadı.")
        sys.exit()

    try:
        yorumlar_section = driver.find_element_by_xpath("//*[@id='restaurantDetail']/div[2]/div[1]/ul/li[4]/a")
        yorumlar_section.click()
        time.sleep(delay)

    except:
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
            yorum_texts.append(yorum)

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

    kisa_liste = [len(yorum_texts), len(author_texts), len(date_texts), len(speed_ratings), len(service_ratings), len(flavour_ratings)]
    kisa = min(kisa_liste)
    kisa -= 1

    yorum_texts_fin = yorum_texts[:kisa]
    df = pd.DataFrame({"Yorumlar": yorum_texts_fin})

    if scrape_author:
        author_texts_fin = author_texts[:kisa]
        df["Müşteriler"] = author_texts_fin

    if scrape_date:
        date_texts_fin = date_texts[:kisa]
        df["Yorum Tarihi"] = date_texts_fin

    if scrape_speed:
        speed_ratings_fin = speed_ratings[:kisa]
        df["Hız Değerlendirmesi"] = speed_ratings_fin

    if scrape_service:
        service_ratings_fin = service_ratings[:kisa]
        df["Servis Değerlendirmesi"] = service_ratings_fin

    if scrape_flavour:
        flavour_ratings_fin = flavour_ratings[:kisa]
        df["Lezzet Değerlendirmesi"] = flavour_ratings_fin

    df.to_excel(dosya_adi, header = True, index = False)

    x = "Çektiğiniz veriler "+ dosya_adi + " adlı excel dosyasına kaydedildi."
    print(x)

    print("""
        --------------------------------------------------------------------------
        -  Projeden memnun kaldıysanız Github üzerinden yıldızlamayı unutmayın.  -
        -  Github Hesabım: ardauzunoglu                                          -
        --------------------------------------------------------------------------
    """)

    time.sleep(3)

if __name__ == "__main__":
    initialize()
    scrape()