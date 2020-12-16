import beyazperde_scraper as bp
import eksi_scraper as es
import hepsiburada_scraper as hb 
import kitapyurdu_scraper as ky 
import trendyol_scraper as ty 
import yemeksepeti_scraper as ys 
import youtube_scraper as yt

secenekler = {"beyazperde":bp, "ekşi sözlük":es, "hepsiburada":hb, "kitapyurdu":ky, "trendyol":ty, "yemeksepeti":ys, "youtube":yt}

secenek = input("Kullanacağınız scraper: ")
secenek = secenek.lower()

if secenek in secenekler:
    
    secenek = secenekler[secenek]
    secenek.initialize()
    secenek.scrape()

else:
    print("Geçersiz yanıt.")
    secenek = input("Kullanacağınız scraper: ")
    print("\n")