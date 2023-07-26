import os
import time

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

import threading


CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
COOKIES_FILE_PATH = os.path.join(os.getcwd(), "cookies.txt")
DEFAULT_DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")

LIBRARY_MAPPING = {
    86: "ACS",
    100: "Elsevier-SD",
    64: "SpringerLink全文电子期刊",
    3: "ACM Digital Library全文数据库(国际)",
    51: "RSC（英国皇家化学学会）电子期刊及数据库(国际)",
    38: "IEEE/IET Electronic library(IEL全文数据库)",
    31: "EI Compendex（美国工程索引）"
}

def download_acs(driver, doi):
    # 点击快速搜索图标
    turn_off_checkbox = driver.find_element('id','turnOffNotification')
    if turn_off_checkbox.is_displayed():
        # 点击 "turn off" 的 checkbox
        turn_off_checkbox.click()
        # time.sleep(2)

    search_input = driver.find_element(By.CSS_SELECTOR, '.quick-search_all-field')
    search_input.send_keys(doi)
    try:
        # 点击搜索按钮
        search_button = driver.find_element(By.CSS_SELECTOR, '.quick-search_all-field ~ button')
        search_button.click()
    except Exception as e:
        turn_off_checkbox = driver.find_element('id', 'turnOffNotification')
        if turn_off_checkbox.is_displayed():
            # 点击 "turn off" 的 checkbox
            turn_off_checkbox.click()
        search_button = driver.find_element(By.CSS_SELECTOR, '.quick-search_all-field ~ button')
        search_button.click()


    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Download PDF')))
        pdf_button = driver.find_element(By.LINK_TEXT, 'Download PDF')
        driver.execute_script("arguments[0].click();", pdf_button)

    except Exception as e:
        print(f'Failed to click PDF download link. Error: {e}')

    # 停止代码运行，手动下载PDF
    time.sleep(60)

def download_els(driver, doi):
    # 寻找并填充 DOI 到搜索框

    time.sleep(3)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "qs")))
    search_box.send_keys(doi)
    search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".button.button-primary.button-icon-right")))
    search_button.click()
    # try:
    #     search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "qs")))
    #     search_box.send_keys(doi)
    #     search_box.send_keys(Keys.RETURN)
    #     # 尝试找到并点击 checkbox
    #     # checkbox.click()
    # except TimeoutException:
    #     pass
    #     # checkbox.click()

    # 在跳转页面等待并点击 checkbox
    # checkbox = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, "//input[@id='select-all-results']/following-sibling::span")))
    # checkbox.click()
    #
    # # 等待并点击下载按钮
    # download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    #     (By.CSS_SELECTOR, ".button-link.u-font-sans.button-link-secondary.download-all-link-button.active")))
    # download_button.click()

    # 等待 "View PDF" 链接出现
    try:
        pdf_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.DownloadPdf.download-link-item a.anchor.download-link"))
        )
    except Exception as e:
        search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "qs")))
        search_box.send_keys(doi)
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".button.button-primary.button-icon-right")))
        search_button.click()
        time.sleep(10)
        pdf_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.DownloadPdf.download-link-item a.anchor.download-link"))
        )

    # time.sleep(5)
    # 点击 "View PDF" 链接
    pdf_link.click()

    time.sleep(60)

def download_spr(driver, doi):
    # 1. 将 DOI 输入到搜索框
    time.sleep(3)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "query")))
    search_box.send_keys(doi)

    # 2. 点击提交按钮
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "search")))
    submit_button.click()

    # 在点击 PDF 下载链接前，先检查是否存在 cookie 接受按钮，如果存在则点击
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "button[data-cc-action='accept'].cc-button.cc-button--contrast.cc-banner__button.cc-banner__button-accept")))
        cookie_accept_button.click()
    except Exception as e:
        print("No cookie accept button found: ", str(e))

    # 3. 在新页面点击 PDF 下载链接
    pdf_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.webtrekk-track.pdf-link")))
    pdf_link.click()

    time.sleep(60)

def download_acm(driver, doi):
    # 1. 将 DOI 输入到搜索框
    time.sleep(3)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search'].autocomplete.quick-search__input.ui-autocomplete-input")))
    search_box.send_keys(doi)

    # 2. 点击提交按钮
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].btn.quick-search__button.icon-Icon_Search")))
    submit_button.click()

    # 在点击 PDF 下载链接前，先检查是否存在 cookie 通知，如果存在则点击 "Got it"
    try:
        cookie_close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a.btn.blue.cookiePolicy-popup__close.pull-right")))
        cookie_close_button.click()
    except Exception as e:
        print("No cookie notice found: ", str(e))

    # 3. 在新页面点击 PDF 下载链接
    pdf_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='PDF'].btn--icon.simple-tooltip__block--b.red.btn")))
    pdf_link.click()

    time.sleep(60)

def download_rsc(driver, doi):
    # 1. 将 DOI 输入到搜索框
    time.sleep(3)
    search_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "JournalsSearchText")))
    search_box.send_keys(doi)

    # 2. 点击提交按钮
    # submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.input__search-submit[name='search']")))
    # submit_button.click()
    search_box.send_keys(Keys.RETURN)


    # 3. 在新页面点击 PDF 下载链接
    pdf_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn--primary.btn--tiny")))
    pdf_link.click()

    time.sleep(60)

    # while True:
    #     time.sleep(1)

def download_ieee(driver, doi):
    # 打开 IEEE Xplore 主页

    # 等待搜索框加载
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input.Typeahead-input'))
    )

    # 输入 DOI
    search_box.send_keys(doi)

    # 点击搜索按钮
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.fa.fa-search.stats-Global_Search_Icon'))
    )
    search_button.click()

    # 在新的页面上，等待并点击 PDF 下载链接
    pdf_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.stats_PDF_8963026.u-flex-display-flex'))
    )
    pdf_link.click()

    time.sleep(60)

def download_ei(driver, doi):
    # 打开 EI 主页
    # 等待搜索框加载

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input#search-word-1'))
    )

    # 输入 DOI
    search_box.send_keys(doi)

    # 点击搜索按钮
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#searchBtn'))
    )
    search_button.click()
    time.sleep(3)

    try:
        accept_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler'))
        )
        accept_cookies.click()
    except Exception as e:
        pass

    # 在新的页面上，选择所有结果
    # 点击页面上的"Select all results on this page"标签
    select_all_results = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="page-select"]'))
    )
    select_all_results.click()

    # 点击下载按钮
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#downloadlink'))
    )
    download_button.click()

    # 选择下载到本地
    download_to_pc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="outputMyPC"]'))
    )
    download_to_pc.click()

    # 选择 PDF 格式
    pdf_format = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="rdPdf"]'))
    )
    pdf_format.click()

    # 确认下载
    confirm_download = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#savePrefsButton'))
    )
    confirm_download.click()


USERNAME=""#sep账号
PASSWORD=""#sep密码

# 不同的库使用不同的下载函数
paper_downloader = {
    "ACS": download_acs,
    "Elsevier-SD":download_els,
    "SpringerLink全文电子期刊":download_spr,
    "ACM Digital Library全文数据库(国际)":download_acm,
    "RSC（英国皇家化学学会）电子期刊及数据库(国际)":download_rsc,
    "IEEE/IET Electronic library(IEL全文数据库)":download_ieee,
    "EI Compendex（美国工程索引）":download_ei
    # "其他库": 其他库的下载函数
    # ...
}

def load_cookies(driver):
    with open('cookies.txt', 'r') as f:
        cookies = eval(f.read())
        for cookie in cookies:
            driver.add_cookie(cookie)

def login_and_save_cookies(driver, username, password):
    driver.get("https://sep.ucas.ac.cn/")
    time.sleep(2)  # 等待页面加载

    user_input = driver.find_element("id","userName1")
    password_input = driver.find_element("id",'pwd1')

    user_input.send_keys(username)
    password_input.send_keys(password)

    try:
        # 检查验证码输入框是否存在，等待时间为5秒
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'certCode1')))
        # 如果找到了验证码输入框，提示用户输入验证码
        cert_code = input("请输入验证码：")
        cert_code_input = driver.find_element("id",'certCode1')
        cert_code_input.send_keys(cert_code)
    except:
        # 如果在规定时间内没有找到验证码输入框，说明不需要输入验证码，直接登录
        pass


    login_button = driver.find_element("id", 'sb1')
    login_button.click()
    time.sleep(2)  # 等待登录成功后的页面加载

    cookies = driver.get_cookies()
    with open('cookies.txt', 'w') as f:
        f.write(str(cookies))

def create_driver():
    download_path = DEFAULT_DOWNLOAD_PATH
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "download.default_directory": download_path,
        "plugins.always_open_pdf_externally": False,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-blink-features=AutomationControlled")  # 反反爬
    options.page_load_strategy = "eager"  # 加快运行速度，如果报错可以注释掉，如果还觉得慢换成“none”，none模式未经过测试
    driver = webdriver.Chrome(options=options)

    return driver

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("UCAS文献下载工具")
        self.geometry('500x500')

        # 加载两张图片
        self.bao_image1 = tk.PhotoImage(file='catt.png')
        self.bao_image2 = tk.PhotoImage(file='catt2.png')

        self.driver = None
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 12), foreground='black')
        self.style.configure('TLabel', font=('Arial', 14), foreground='black')

        self.create_widgets()

    def create_widgets(self):
        library_frame = ttk.Frame(self, padding="10")
        library_frame.pack(fill=tk.X)

        self.library_label = ttk.Label(library_frame, text="请选择一个库:")
        self.library_dropdown = ttk.Combobox(library_frame, values=list(LIBRARY_MAPPING.values()))
        self.library_label.pack(side=tk.LEFT)
        self.library_dropdown.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        doi_frame = ttk.Frame(self, padding="10")
        doi_frame.pack(fill=tk.X)

        self.doi_label = ttk.Label(doi_frame, text="请输入待下载的文献DOI:")
        self.doi_entry = ttk.Entry(doi_frame)
        self.doi_label.pack(side=tk.LEFT)
        self.doi_entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        button_frame = ttk.Frame(self, padding="10")
        button_frame.pack(fill=tk.X)

        # 创建按钮并使用第一张图片
        self.bao_button = tk.Label(button_frame, image=self.bao_image1, bd=0)
        self.bao_button.pack(side=tk.LEFT, padx=10)
        # 为 label 添加点击事件绑定
        self.bao_button.bind('<Button-1>', self.start_download_thread)

        self.download_label = ttk.Label(button_frame, text="点猫下载")
        self.download_label.pack(side=tk.LEFT)

        self.close_button = ttk.Button(button_frame, text="关闭浏览器", command=self.close_browser)
        self.close_button.pack(side=tk.RIGHT, padx=10)

        self.guide_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10)
        self.guide_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        guide_string = (
            "使用指南:\n"
            "1.输入doi后选择对应的数据库，点击猫头下载\n"
            "2.点击下载后网页会自动运行到pdf浏览页面，无需手动点击\n"
            "3.运行过程中如果遇到网页更新缓慢可手动刷新当前页面\n"
            "4.代码运行到pdf浏览页面时需要手动点击chrome下载键，"
            "如果显示下载失败可点击打印图标选择另存为pdf\n"
            "5.登录时如果需要输入验证码，在运行终端输入后回车键提交即可\n"
            "6.首次登陆会自动保存cookies文件在本地\n"
            "7.EI数据库下载pdf无需手动点击，会自动下载到DEFAULT_DOWNLOAD_PATH\n"
            "8.同一时间只能下载一篇文献，点击关闭浏览器/手动关闭浏览器后可以继续使用gui页面下载另一篇"
        )
        self.guide_text.insert(tk.INSERT, guide_string)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        else:
            messagebox.showinfo("提示", "浏览器已关闭或未开启")

    def start_download_thread(self, event):
        # 在点击事件中改变按钮的图片
        if self.bao_button['image'] == str(self.bao_image1):  # 如果当前是第一张图片
            self.bao_button.config(image=self.bao_image2)  # 就改为第二张
        else:
            self.bao_button.config(image=self.bao_image1)  # 否则改为第一张

        # 创建一个新线程来运行 download_paper 方法
        download_thread = threading.Thread(target=self.download_paper)
        # 启动新线程
        download_thread.start()

    def download_paper(self):
        library_name = self.library_dropdown.get()
        doi = self.doi_entry.get()

        if not library_name or not doi:
            messagebox.showerror("错误", "请填写所有字段")
            return

        download_func = paper_downloader.get(library_name)
        if not download_func:
            messagebox.showerror("错误", "找不到对应的下载函数，请检查库名称。")
            return

        self.driver = create_driver()
        if os.path.exists(COOKIES_FILE_PATH):
            self.driver.get("https://sep.ucas.ac.cn/")
            load_cookies(self.driver)
            self.driver.get("https://libyw.ucas.ac.cn/portal/site/377/1994")
        else:
            login_and_save_cookies(self.driver, USERNAME, PASSWORD)
            time.sleep(2)

        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            time.sleep(2)
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/portal/site/377/1994"]')))
            link.click()
        except Exception as e:
            pass

        try:
            library_id = [k for k, v in LIBRARY_MAPPING.items() if v == library_name][0]
            library_link = "https://libyw.ucas.ac.cn" + "/user/resource/visit?id=" + str(library_id)
            self.driver.get(library_link)
        except Exception as e:
            print(f"An error occurred: {e}")

        download_func(self.driver, doi)

        messagebox.showinfo("成功", "已自动关闭浏览器")


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
