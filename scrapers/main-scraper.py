import beyazperde_scraper as bp
from beyazperde_scraper import beyazperde_scrape
import eksi_scraper as es
from eksi_scraper import eksisozluk_scrape
import hepsiburada_scraper as hb 
from hepsiburada_scraper import hepsiburada_scrape
import kitapyurdu_scraper as ky 
from kitapyurdu_scraper import kitapyurdu_scrape
import trendyol_scraper as ty 
from trendyol_scraper import trendyol_scrape
import yemeksepeti_scraper as ys 
from yemeksepeti_scraper import yemeksepeti_scrape
import youtube_scraper as yt
from youtube_scraper import youtube_scrape

choices = ["beyazperde", "ekşi sözlük", "hepsiburada", "kitapyurdu", "trendyol", "yemeksepeti", "youtube"]
libs = {"beyazperde":beyazperde_scrape, "ekşi sözlük":eksisozluk_scrape, "hepsiburada":hepsiburada_scrape, "kitapyurdu":kitapyurdu_scrape, "trendyol":trendyol_scrape, "yemeksepeti":yemeksepeti_scrape, "youtube":youtube_scrape}

choice = input("Kullanacağınız scraper: ")
choice = choice.lower()

if choice in choices:
    scraper = libs[choice]
    scraper()
else:
    print("Geçersiz yanıt.")
    secenek = input("Kullanacağınız scraper: ")