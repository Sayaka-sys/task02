import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime


LOG_FILE_PATH = "./log/log_###DATETIME###.log"
EXP_CSV_PATH="./exp_list_###SEARCH_KEYWORD###_###DATETIME###.csv"
log_file_path=LOG_FILE_PATH.replace("###DATETIME###",datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword=input("検索キーワードを入力してください：")
    print("検索キーワード:{}".format(search_keyword))
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_css_selector(".cassetteRecruit__copy")
    table_elms = driver.find_elements_by_class_name("tableCondition")
    

    # 1ページ分繰り返し
    # print(len(name_list))
    # print(len(content_list))
    # print(len(target_list))

    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)

    for table_elm in table_elms:
        print(table_elm.find_elements_by_class_name("tableCondition__body")[0].text)
        print(table_elm.find_elements_by_class_name("tableCondition__body")[1].text)
       

    next_link = driver.find_elements_by_class_name("iconFont--arrowLeft")
    driver.get(next_link[0].get_attribute('href'))

    name_list = driver.find_elements_by_css_selector(".cassetteRecruit__copy")
    table_elms = driver.find_elements_by_class_name("tableCondition")

    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)

    for table_elm in table_elms:
        print(table_elm.find_elements_by_class_name("tableCondition__body")[0].text)
        print(table_elm.find_elements_by_class_name("tableCondition__body")[1].text)


    df = pd.DataFrame({"名前":exp_name_list, "仕事内容":("tableCondition__body")[0], "対象":("tableCondition__body")[1]})
    df.to_csv("./sample.csv",encoding="utf_8-sig")
    print(df)


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
