# AuthorName : DuQing
# CreateTime : 2017-10-17 16:27
import time
import datetime
from selenium import webdriver
from scrapy import Selector
import pymongo

# 注：这里的driver是从微软官网下载的，并且这个驱动是分版本的，要和本地的Edge版本一致才能用，我电脑上是14，所以得下载14393版本
"""
Release 16299
Version: 5.16299 | Edge version supported: 16.16299 | License terms
Insiders
Edge version Supported: Current Insiders Fast Ring Build License terms | Privacy Statement
Release 15063
Version: 4.15063 | Edge version supported: 15.15063 | License terms
Release 14393
Version: 3.14393 | Edge version supported: 14.14393 | License terms
"""
# browser = webdriver.Edge(executable_path='C:\Python\MicrosoftWebDriver.exe')
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('--user-data-dir=C:/Users/liush/AppData/Local/Google/Chrome/Application')
# browser = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe', chrome_options=options)
# browser = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe')

# 获取动态页面中的某个值
# browser.get('https://detail.tmall.com/item.htm?id=522680881881&spm=a223v.7835278.t0.1.1b188d4bLTyj6Z&pvid=f86cd266-4d61-4919-be70-a6476f545d1a&scm=1007.12144.69634.9011_8949&sku_properties=5919063:6536025')
# time.sleep(5)
# selector = Selector(text=browser.page_source)
# price = selector.css('.tm-promo-price .tm-price::text').extract_first()
# print(price)
# browser.quit()

# 在浏览器中下拉滚动条
# browser.get('https://www.oschina.net/blog')
# for i in range(3):
#     browser.execute_script('window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;')
#     time.sleep(3)
# 设置浏览器不加载图片
# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe', chrome_options=chrome_options)

# browser.get('https://detail.tmall.com/item.htm?id=522680881881&spm=a223v.7835278.t0.1.1b188d4bLTyj6Z&pvid=f86cd266-4d61-4919-be70-a6476f545d1a&scm=1007.12144.69634.9011_8949&sku_properties=5919063:6536025')
today = datetime.datetime.now().strftime('%Y-%m-%d')

client = pymongo.MongoClient('localhost', 27017)
walden = client['walden']
sheet_lines = walden['price']

# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(chrome_options=chrome_options)
browser = webdriver.PhantomJS()

for i in range(30):
    end_day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    url = 'http://flights.ctrip.com/booking/SHA-WUH-day-1.html?DDate1=%s#DDate1=%s'%(today, end_day)
    # 新标签页中打开

    time.sleep(1)
    browser.get(url)
    print(url)
    time.sleep(4)
    for i in range(2):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;')
        time.sleep(1)
    query_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    selector = Selector(text=browser.page_source)
    lower_price = selector.css('.current .base_price02::text').extract_first()
    table = selector.css('.search_box.search_box_tag.search_box_light')
    for flight in table:
        flight_name = flight.css('.clearfix.J_flight_no >strong::text').extract_first()
        flight_number = flight.css('.clearfix.J_flight_no >span::text').extract_first()
        start_time = flight.css('.right .time::text').extract_first()
        start_airport = flight.css('.right > div::text').extract_first()
        reach_time = flight.css('.left .time::text').extract_first()
        reach_airport = flight.css('.left > div::text').extract_first()
        price = flight.css('.price .base_price02::text').extract_first()
        if price == lower_price:
            print(query_time, end_day, flight_name, flight_number, start_time, start_airport, reach_time, reach_airport,
                  price)
            data = {
                'query_time': query_time,
                'flight_day': end_day,
                'flight_name': flight_name,
                'flight_number': flight_number,
                'start_time': start_time,
                'start_airport': start_airport,
                'reach_time': reach_time,
                'reach_airport': reach_airport,
                'price': int(price)
            }
            sheet_lines.insert_one(data)
    print('===============================================')
    time.sleep(1)
    browser.execute_script('window.open()')
    browser.close()
    # print(browser.window_handles)

    # if i % 2 == 0:
    #     browser.switch_to.window(browser.window_handles[1])
    # else:
    browser.switch_to.window(browser.window_handles[0])
