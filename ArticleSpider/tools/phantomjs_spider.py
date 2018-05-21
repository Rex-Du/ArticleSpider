import time

from selenium import webdriver

# 很奇怪，使用chrom可以得到预期的结果，但是phantomjs却不行
# web = webdriver.PhantomJS(executable_path='C:\Program Files\\nodejs\\node_modules\phantomjs-prebuilt\lib\phantom\\bin\phantomjs.exe')
# web.set_window_size(1280, 2400)
web = webdriver.Chrome(executable_path='C:\Python\chromedriver.exe')

web.get('https://passport.lagou.com/login/login.html')
user_name_input = web.find_elements_by_css_selector('.input.input_white')[0]
print('得到用户名的输入框：', user_name_input)
user_name_input.send_keys('18627003837')
passwd_input = web.find_elements_by_css_selector('.input.input_white')[1]
print('得到密  码的输入框：', passwd_input)
passwd_input.send_keys('duqing512556')
submit_btn = web.find_elements_by_css_selector('.btn.btn_green.btn_active.btn_block.btn_lg')[0]
print('得到提交按钮：', submit_btn)
submit_btn.click()
time.sleep(2)
web.get('https://www.lagou.com/resume/myresume.html')
time.sleep(2)
print(web.page_source)