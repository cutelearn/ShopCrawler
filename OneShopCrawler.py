import requests # 引入 requests 模組，可用來發送 HTTP 請求
from bs4 import BeautifulSoup # 引入 BeautifulSoup 模組，可用來解析 HTML 文件
import csv # 引入 csv 模組，可用來讀寫 CSV 檔案
import re # 引入 re 模組，可用來處理正規表示式

class CrawlerShop:
    def __init__(self, url: str) -> None:
        self.url = url # 初始化爬蟲的網址
        self.header = {'content-type': 'text/plain;charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'} # 設定 HTTP header，模擬使用者使用 Chrome 瀏覽器發送請求
        self.res=requests.get(url,headers=self.header) # 發送 GET 請求，並將回應儲存在 self.res 屬性中

class PconeShop(CrawlerShop):
    def find_products(self) -> list:
        "抓取產品頁頁面url" # 函式註解，說明此方法的功能
        self.page = BeautifulSoup(self.res.text,"lxml") # 解析網頁的 HTML 文件，並儲存到 self.page 屬性中
        product_list_items = self.page.find_all("a", class_="product-list-item") # 找出所有 class 為 "product-list-item" 的 a 標籤，並回傳結果的串列
        return ["https://www.pcone.com.tw/" + item.get("href") for item in product_list_items] #使用串列生成式生成url串列

    def get_product_info(self, product_url: str) -> dict:
        "抓取產品資訊"  # 函式註解，說明此方法的功能
        print(f"正在抓取{product_url}") #列出log顯示目前抓的產品頁面
        product_page = requests.get(product_url, headers=self.header) # 發送 GET 請求，並將回應儲存在 product_page 變數中
        soup = BeautifulSoup(product_page.text, "lxml") # 解析網頁的 HTML 文件，並儲存到 soup 變數中

        product_info = {
            'shop_name': soup.find("div", class_="merchant-name").text, # 找出 class 為 "merchant-name" 的 div 標籤，並取出其文字內容，存到 product_info 字典的 'shop_name' 鍵中
            'product_name': soup.find("h1", class_="name x-large-font").text, # 找出 class 為 "name x-large-font" 的 h1 標籤，並取出其文字內容，存到 product_info 字典的 'product_name' 鍵中
            'shop_info': soup.find_all("p", class_="data medium-font"), # 找出 class 為 "data medium-font" 的所有 p 標籤，存到 product_info 字典的 'shop_info' 鍵中
            'product_money': soup.find("div", class_="site-color medium-font site-color").text, # 找出 class 為 "site-color medium-font site-color" 的 div 標籤，並取出其文字內容，存到 product_info 字典的 'product_money' 鍵中
            'product_score': soup.find("div", "review pointer").text, # 找出 class 為 "review pointer" 的 div 標籤，並取出其文字內容，存到 product_info 字典的 'product_score' 鍵中
            'buy_info': soup.find("div", class_="review-info d-flex justify-content-start").text, # 找出 class 為 "review-info d-flex justify-content-start" 的 div 標籤，並取出其文字內容，存到 product_info 字典的 'buy_info' 鍵中
        }

        return product_info # 回傳 product_info 字典

    def export_csv(self) -> None:
        with open('期末.csv', 'w', newline='', encoding='utf-8-sig') as f: # 開啟 '期末.csv' 檔案，並設定編碼為 utf-8-sig，以避免中文亂碼
            writer = csv.writer(f) # 建立 csv.writer 物件，並傳入檔案物件
            writer.writerow(["店家名稱", "產品名稱", "店家商品數量", "店家評價", "店家出貨天數", "店家回覆率", "特價", "折數", "商品評分", "購買人數"]) # 寫入 CSV 檔案的欄位名稱

            for product_data in self.data: # 迭代 data 串列中的每一個元素
                writer.writerow(product_data) # 將每一個元素寫入 CSV 檔案中

    def process_shop_info(self, shop_info: list) -> tuple:
        """處理店家資訊，將列表中的每個元素的文字內容取出，並返回一個元組。"""
        return tuple(info.text for info in shop_info)

    def process_product_money(self, product_money: str) -> int:
        """處理商品價格，將價格字串以 $ 為分隔符，取出第二個元素，並轉換為整數。"""
        return int(product_money.split('$')[1])

    def process_product_score(self, product_score: str) -> str:
        """處理商品評分，將評分字串以左括號為分隔符，取出第一個元素。"""
        return product_score.split('(')[0]

    def calculate_discount(self, product_money: int, yuan: int) -> int:
        """計算商品的折數。"""
        return int(product_money / yuan * 100)

    def get_buy_count(self, buy_info: str) -> str:
        """使用正規表示式，找出 'buy_info' 中的數字，並取出第三個元素，即購買人數。如果元素數量不足，則返回 '0'。"""
        buy = re.findall(r"\d+.?\d*", buy_info)
        return buy[2] if len(buy) > 2 else '0'

    def script(self) -> None:
        """主要的流程控制方法。"""
        self.data = [] # 建立一個空的串列，用來存放產品資訊
        for product_url in self.find_products(): # 迭代 products 串列中的每一個元素
            product_info = self.get_product_info(product_url) # 呼叫 get_product_info 方法，並傳入 product_url 參數，取得產品資訊，存到 product_info 字典中

            shop_q, shop_s, shop_t, shop_r = self.process_shop_info(product_info['shop_info']) # 將 'shop_info' 中的每一個 p 標籤的文字內容，分別存到 shop_q、shop_s、shop_t、shop_r 四個變數中
            product_money = self.process_product_money(product_info['product_money']) # 將 'product_money' 中的價格字串，以 $ 為分隔符，取出第二個元素，即商品價格，存到 product_money 變數中
            product_score = self.process_product_score(product_info['product_score']) # 將 'product_score' 中的評分字串，以左括號為分隔符，取出第一個元素，即商品評分，存到 product_score 變數中

            try:
                yuan = self.process_product_money(product_info['product_money']) # 將 'product_money' 中的價格字串，以 $ 為分隔符，取出第二個元素，即商品價格，存到 yuan 變數中
            except:
                yuan = product_money # 如果無法取得商品價格，則將 product_money 的值存到 yuan 變數中

            zhe = self.calculate_discount(product_money, yuan) # 計算商品的折數，存到 zhe 變數中
            buy_count = self.get_buy_count(product_info['buy_info']) # 使用正規表示式，找出 'buy_info' 中的數字，存到 buy_count 變數中

            self.data.append([product_info['shop_name'], product_info['product_name'], shop_q, shop_s, shop_t, shop_r, product_money, zhe, product_score, buy_count]) # 將產品資訊加入 data 串列中
        print("抓取完畢") # 列出log顯示抓取完畢


def main():
    pcone_crawler = PconeShop("https://www.pcone.com.tw/product/603#ref=d_nav") # 建立 PconeShop 物件，並傳入要爬蟲的網址
    pcone_crawler.script() # 呼叫 script 方法，開始爬蟲
    pcone_crawler.export_csv() # 呼叫 export_csv 方法，將資料寫入 CSV 檔案


if __name__ == "__main__":
    main() # 如果此程式是直接執行的，則執行 main 函式
