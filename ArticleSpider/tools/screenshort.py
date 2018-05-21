from selenium import webdriver

# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe', chrome_options=chrome_options)
browser = webdriver.PhantomJS()
browser.get('http://wh.58.com/qzzpshengchankaifa/?PGTID=0d202409-0009-ee92-4b24-659a71a2ce9d&ClickID=1')
browser.implicitly_wait(5)
# browser.save_screenshot('page.png')
age = browser.find_element_by_xpath('//*[@id="infolist"]/ul/li[1]/div[1]/dl/dd/div[1]/a/div/div/em[2]|//*[@id="infolist"]/dl[1]/dd[4]')
# print(age.location)
# print(age.size)
# left = age.location['x']
# top = age.location['y']
# right = age.location['x'] + age.size['width']
# bottom = age.location['y'] + age.size['height']
#
# im = Image.open('page.png')
# im = im.crop((left, top, right, bottom))
# im.save('age.png')
# 本来直接用下面这个命令是可以截取元素的，但是未知原因报错
print(age)
age.screenshot('heheda.png')
# browser.close()