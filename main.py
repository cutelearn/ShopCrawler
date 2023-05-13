from ShopCrawler import PconeShop

def main():
    pcone_crawler = PconeShop("https://www.pcone.com.tw/product/603#ref=d_nav") # 建立 PconeShop 物件，並傳入要爬蟲的網址
    pcone_crawler.script() # 呼叫 script 方法，開始爬蟲
    pcone_crawler.export_csv() # 呼叫 export_csv 方法，將資料寫入 CSV 檔案

if __name__ == "__main__":
    main()