import csv # 引入 csv 模組來處理 CSV 檔案
import requests # 引入 requests 模組來進行 HTTP 請求
import re # 引入 re 模組來處理正則表達式
from bs4 import BeautifulSoup # 從 bs4 模組引入 BeautifulSoup 類別來處理 HTML 網頁內容
from ShopCrawler import CrawlerShop # 從 ShopCrawler 模組中引入 CrawlerShop 類別


class PconeShop(CrawlerShop): # 定義一個名為 PconeShop 的類別，該類別繼承自 CrawlerShop
    def find_products(self) -> list: # 定義一個名為 find_products 的方法，該方法回傳一個串列
        "抓取產品頁頁面url"
        try: # 嘗試執行以下程式碼
            self.page = BeautifulSoup(self.res.text,"lxml") # 將 HTTP 請求回傳的網頁內容轉換為 BeautifulSoup 物件
            product_list_items = self.page.find_all("a", class_="product-list-item") # 尋找網頁中的所有 class 為 "product-list-item" 的 a 標籤
            return ["https://www.pcone.com.tw/" + item.get("href") for item in product_list_items] # 將所有 a 標籤的 href 屬性值取出，並加上 "https://www.pcone.com.tw/" 作為開頭，將結果串列回傳
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在尋找產品時發生錯誤: {e}") # 印出錯誤訊息
            return [] # 回傳一個空串列

    def get_product_info(self, product_url: str) -> dict: # 定義一個名為 get_product_info 的方法，該方法接收一個字串參數並回傳一個字典
        "抓取產品資訊"
        try: # 嘗試執行以下程式碼
            print(f"正在抓取{product_url}") # 印出當前正在抓取的產品網址
            product_page = requests.get(product_url, headers=self.header, verify=False) # 進行 HTTP GET 請求，取得產品網頁的內容
            soup = BeautifulSoup(product_page.text, "lxml") # 將網頁內容轉換為 BeautifulSoup 物件

            product_info = { # 建立一個字典來存放產品資訊
                'shop_name': soup.find("div", class_="merchant-name").text, # 找出 class 為 "merchant-name" 的 div 標籤，並取出其文字內容，存到 product_info 字典的 'shop_name' 鍵中
                'product_name': soup.find("h1", class_="name x-large-font").text, # 尋找網頁中的 class 為 "name x-large-font" 的 h1 標籤，並取出其文字內容
                'shop_info': soup.find_all("p", class_="data medium-font"), # 尋找網頁中的所有 class 為 "data medium-font" 的 p 標籤
                'product_money': soup.find("div", class_="site-color medium-font site-color").text, # 尋找網頁中的 class 為 "site-color medium-font site-color" 的 div 標籤，並取出其文字內容
                'product_score': soup.find("div", "review pointer").text, # 尋找網頁中的 class 為 "review pointer" 的 div 標籤，並取出其文字內容
                'buy_info': soup.find("div", class_="review-info d-flex justify-content-start").text, # 尋找網頁中的 class 為 "review-info d-flex justify-content-start" 的 div 標籤，並取出其文字內容
            }
            return product_info # 回傳產品資訊字典
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在抓取{product_url}時發生錯誤: {e}") # 印出錯誤訊息
            return None # 回傳 None

    def export_csv(self) -> None: # 定義一個名為 export_csv 的方法，該方法不回傳任何值
        """處理店家資訊，將列表中的每個元素的文字內容取出，並返回一個元組。"""
        try: # 嘗試執行以下程式碼
            with open('期末.csv', 'w', newline='', encoding='utf-8-sig') as f: # 開啟一個名為 '期末.csv' 的 CSV 檔案，以寫入模式開啟，並設定換行符為空字串，編碼為 'utf-8-sig'
                writer = csv.writer(f) # 建立一個 csv.writer 物件
                writer.writerow(["店家名稱", "產品名稱", "店家商品數量", "店家評價", "店家出貨天數", "店家回覆率", "特價", "折數", "商品評分", "購買人數"]) # 寫入 CSV 檔案的表頭

                for product_data in self.data: # 迭代 self.data 中的每一個元素
                    writer.writerow(product_data) # 將元素寫入 CSV 檔案
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在寫入CSV時發生錯誤: {e}") # 印出錯誤訊息

    def process_shop_info(self, shop_info: list) -> tuple: # 定義一個名為 process_shop_info 的方法，該方法接收一個串列參數並回傳一個元組
        """處理店家資訊，將列表中的每個元素的文字內容取出，並返回一個元組。"""
        try: # 嘗試執行以下程式碼
            return tuple(info.text for info in shop_info) # 將串列中的每一個元素的文字內容取出，建立一個元組並回傳
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在處理店家資訊時發生錯誤: {e}") # 印出錯誤訊息
            return () # 回傳一個空元組

    def process_product_money(self, product_money: str) -> int: # 定義一個名為 process_product_money 的方法，該方法接收一個字串參數並回傳一個整數
        """處理商品價格，將價格字串以 $ 為分隔符，取出第二個元素，並轉換為整數。"""
        try: # 嘗試執行以下程式碼
            return int(product_money.split('$')[1]) # 將字串以 $ 為分隔符進行切割，取出第二個元素，將其轉換為整數並回傳
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在處理商品價格{product_money}時發生錯誤: {e}") # 印出錯誤訊息
            return None # 回傳 None

    def process_product_score(self, product_score: str) -> str: # 定義一個名為 process_product_score 的方法，該方法接收一個字串參數並回傳一個字串
        """處理商品評分，將評分字串以左括號為分隔符，取出第一個元素。"""
        try: # 嘗試執行以下程式碼
            return product_score.split('(')[0] # 將字串以左括號為分隔符進行切割，取出第一個元素並回傳
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在處理商品評分{product_score}時發生錯誤: {e}") # 印出錯誤訊息
            return None # 回傳 None

    def calculate_discount(self, product_money: int, yuan: int) -> int: # 定義一個名為 calculate_discount 的方法，該方法接收兩個整數參數並回傳一個整數
        """計算商品的折數。"""
        try: # 嘗試執行以下程式碼
            return int(product_money / yuan * 100) # 將 product_money 除以 yuan，乘以 100，轉換為整數並回傳
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在計算商品折數時發生錯誤: {e}") # 印出錯誤訊息
            return None # 回傳 None

    def get_buy_count(self, buy_info: str) -> str: # 定義一個名為 get_buy_count 的方法，該方法接收一個字串參數並回傳一個字串
        """使用正規表示式，找出 'buy_info' 中的數字，並取出第三個元素，即購買人數。如果元素數量不足，則返回 '0'。"""
        try: # 嘗試執行以下程式碼
            buy = re.findall(r"\d+.?\d*", buy_info) # 使用正規表示式，找出字串中的數字
            return buy[2] if len(buy) > 2 else '0' # 如果數字的個數大於 2，則回傳第三個數字，否則回傳 '0'
        except Exception as e: # 如果在嘗試執行以上程式碼時發生異常
            print(f"在處理購買人數{buy_info}時發生錯誤: {e}") # 印出錯誤訊息
            return '0' # 回傳 '0'

    def script(self) -> None:
        """主要的流程控制方法。"""
        self.data = [] # 建立一個空的串列，用來存放產品資訊
        for product_url in self.find_products(): # 迭代 products 串列中的每一個元素
            product_info = self.get_product_info(product_url) # 呼叫 get_product_info 方法，並傳入 product_url 參數，取得產品資訊，存到 product_info 字典中
            shop_name = product_info['shop_name'] # 將 'shop_name' 的值存到 shop_name 變數中
            product_name = product_info['product_name'] # 將 'product_name' 的值存到 product_name 變數中
            shop_q, shop_s, shop_t, shop_r = self.process_shop_info(product_info['shop_info']) # 將 'shop_info' 中的每一個 p 標籤的文字內容，分別存到 shop_q、shop_s、shop_t、shop_r 四個變數中
            product_money = self.process_product_money(product_info['product_money']) # 將 'product_money' 中的價格字串，以 $ 為分隔符，取出第二個元素，即商品價格，存到 product_money 變數中
            product_score = self.process_product_score(product_info['product_score']) # 將 'product_score' 中的評分字串，以左括號為分隔符，取出第一個元素，即商品評分，存到 product_score 變數中
            yuan = product_money # product_money 的值存到 yuan 變數中

            zhe = self.calculate_discount(product_money, yuan) # 計算商品的折數，存到 zhe 變數中
            buy_count = self.get_buy_count(product_info['buy_info']) # 使用正規表示式，找出 'buy_info' 中的數字，存到 buy_count 變數中

            self.data.append([shop_name, product_name, shop_q, shop_s, shop_t, shop_r, product_money, zhe, product_score, buy_count]) # 將產品資訊加入 data 串列中
        print("抓取完畢") # 列出log顯示抓取完畢
