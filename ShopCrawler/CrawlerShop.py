import requests # 引入 requests 模組，可用來發送 HTTP 請求

class CrawlerShop:
    def __init__(self, url: str) -> None:
        self.url = url # 初始化爬蟲的網址
        self.header = {'content-type': 'text/plain;charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} # 設定 HTTP header，模擬使用者使用 Chrome 瀏覽器發送請求
        self.res=requests.get(url,headers=self.header) # 發送 GET 請求，並將回應儲存在 self.res 屬性中