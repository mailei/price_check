from bs4 import BeautifulSoup
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from datetime import datetime
import re


def scraping(url):
  try:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    price = soup.find('span', class_='priceTxt').get_text()
    return int(re.sub('¥|,', '', price))
  except:
    print("価格取得エラー")
    raise Exception('価格取得エラー')


def is_low_price(price, threshold):
  if price < threshold:
    return True
  else:
    return False


def send_message(body):
  try:
    # mail account id/pw
    id = ""
    pw = ""
    to_add = ""

    message = MIMEText(body, "html")
    message["Subject"] = "価格コムチェック通知"
    message["To"] = to_add
    message["From"] = id

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
    server.login(id, pw)
    server.send_message(message)  # メールの送信
    print("送信完了")
  except:
    raise Exception("メール送信エラー")


if __name__ == '__main__':
  threshold_price = 200000
  target_page = 'https://kakaku.com/item/K0001210840/'
  while True:
    try:
      # １時間おきにチェック
      if datetime.now().strftime('%M')[0:2] != 00:
        price = scraping(target_page)
        if not is_low_price(price, threshold_price):
          send_message("値下がりしたよ！現在　{0}円だよ!".format(price))
    except Exception as e:
      send_message("エラーだよ！ {0}".format(e))
