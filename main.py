import os
import csv
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import locale
months = {
    'Янв': '01', 'Фев': '02', 'Мар': '03', 'Апр': '04',
    'Май': '05', 'Июн': '06', 'Июл': '07', 'Авг': '08',
    'Сен': '09', 'Окт': '10', 'Ноя': '11', 'Дек': '12'
}
def add_transaction(date, sender_img_url, send_amount, send_currency, receiver_img_url, receive_amount, receive_currency, source, inchane_id, usdt, file_path='transactions.csv'):
    # Проверка на существование файла
    file_exists = os.path.isfile(file_path)
    
    # Создание уникального идентификатора строки
    if 'alfabit.org' in source:
        transaction_id_2 = f"{sender_img_url},{send_amount},{send_currency},{receiver_img_url},{receive_amount},{receive_currency},{source},{inchane_id},{usdt}"
        transaction_id = f"{date},{sender_img_url},{send_amount},{send_currency},{receiver_img_url},{receive_amount},{receive_currency},{source},{inchane_id},{usdt}"

    else:
        transaction_id = f"{date},{sender_img_url},{send_amount},{send_currency},{receiver_img_url},{receive_amount},{receive_currency},{source},{inchane_id},{usdt}"
    
    # Чтение существующих строк и проверка на наличие текущей строки
    if file_exists:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if 'alfabit.org' in source:
                    if row[1:] == transaction_id_2.split(','):
                        return  # Если строка уже существует, выходим из функции
                else:
                    if row == transaction_id.split(','):
                        return  # Если строка уже существует, выходим из функции
    
    # Если файл не существует, создаем его и записываем заголовок
    if not file_exists:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Sender', 'Send Amount', 'Send Currency', 'Receiver', 'Receive Amount', 'Receive Currency', 'Source', 'Inchane_id', 'Usdt'])
    
    # Запись новой строки в файл
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)                                
        writer.writerow(transaction_id.split(','))
        print('записана новая строка')

urls = ['https://safelychange.com/#/ru/',
        'https://barry24.com',
        'https://i-obmen.bz/', 
        'https://keine-exchange.com', 
        'https://green-obmenka.ru', 
        'https://finex24.io', 
        'https://btchange.ru', 
        'https://pushpayer.net', 
        'https://buhtaobmena.me',
        'https://cripthub.ru/',
        'https://alfabit.org/ru/exchange',
        'https://obmenka.su',
        'https://changeexpert.io',
        'https://btcdeal.ru/',
        'https://avanchange.com/',
        'https://niceobmen.com',
        'https://yaobmen.cash',
        'https://nadex.io/',
        'https://bobr.exchange/',
        
        
       ]
def extract_in_brackets(text):
    match = re.search(r'\((.*?)\)', text)
    if match:
        return match.group(1)
    return None
def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if url == urls[0]:
        elements = soup.find_all('div', class_='v-last-transactions-item last-transactions-list-item')
        for element in elements:
            print(element.get_text())
    elif url == urls[1]:  # https://barry24.com/
        inchane_id = '11204'
        usdt = 'trc erc bep'
        elements = soup.find_all('div', class_='home_lchange_one')
        for element in elements:
            img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
            sender = re.search(r'url\((.*?)\)', img_divs[0].get('style')).group(1)
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = re.search(r'url\((.*?)\)', img_divs[1].get('style')).group(1)
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[0]} {text[1]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[2]:  # i-obmen.bz
        elements = soup.find_all('div', class_='home_lchange_one')
        for element in elements:
            print(element.get_text())
    elif url == urls[3]:  # https://keine-exchange.com/
        inchane_id = '997'
        usdt = 'trc erc bep'
        elements = soup.find_all('div', class_='card-exchange box-panel')
        for element in elements:
            img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
            sender = re.search(r'url\((.*?)\)', img_divs[0].get('style')).group(1)
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = re.search(r'url\((.*?)\)', img_divs[1].get('style')).group(1)
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[0]} {text[1]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
            #(date, sender_img_url, send_amount, send_currency, receiver_img_url, receive_amount, receive_currency, source, inchane_id, usdt
    elif url == urls[4]:  # green-obmenka.ru  мск?
        usdt = 'trc'
        inchane_id = '11020'
        elements = soup.find_all('div', class_='home_lchange_one')
        for element in elements:
            img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
            sender = re.search(r'url\((.*?)\)', img_divs[0].get('style')).group(1)
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = re.search(r'url\((.*?)\)', img_divs[1].get('style')).group(1)
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[0]} {text[1]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[5]:  # https://finex24.io вероятно мск
        usdt = 'trc,erc,bep'
        inchane_id = '10943'
        elements = soup.find_all('div', class_='crypto')
        for element in elements[:3]:
            img_divs = element.find_all('div', class_='coin__logo')
            imgs = []
            for img_div in img_divs:
                imgs.append(img_div.find('img'))
            sender = imgs[0].get('src')
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = imgs[1].get('src')
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[3]} {text[4]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[5], text[6], receiver, text[7], text[8], url, inchane_id, usdt)
    elif url == urls[6]:  # https://btchange.ru вероятно мск
        usdt = 'trc erc'
        inchane_id = '11173'
        elements = soup.find_all('div', class_='home_lchange_one')
        for element in elements:
            img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
            sender = re.search(r'url\((.*?)\)', img_divs[0].get('style')).group(1)
            sender = re.search(r'uploads/(.*?)\.png', sender).group(1)
            receiver = re.search(r'url\((.*?)\)', img_divs[1].get('style')).group(1)
            receiver = re.search(r'uploads/(.*?)\.png', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[0]} {text[1]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[7]:  # https://pushpayer.net мск
        usdt = 'trc'
        inchane_id = '674'
        elements = soup.find_all('div', class_='swap__wrap')
        for element in elements:
            element = element.parent
            img_divs = element.find_all('div', class_='media')
            imgs = []
            for img_div in img_divs:
                imgs.append(img_div.find('img'))
            sender = imgs[0].get('src')
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg|svg)', sender).group(1)
            receiver = imgs[1].get('src')
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg|svg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[4]} {text[5]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[0], text[1], receiver, text[2], text[3], url, inchane_id, usdt)
    elif url == urls[8]:  # https://buhtaobmena.me вероятно мск
        usdt = 'trc bep'
        inchane_id = '11221'
        elements = soup.find_all('div', class_='crypto')
        for element in elements:
            img_divs = element.find_all('div', class_='coin__logo')
            imgs = []
            for img_div in img_divs:
                imgs.append(img_div.find('img'))
            sender = imgs[0].get('src')
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = imgs[1].get('src')
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[3]} {text[4]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
            add_transaction(dt, sender, text[5], text[6], receiver, text[7], text[8], url, inchane_id, usdt)
    elif url == urls[9]: #crypthub.ru
        usdt = 'trc erc bep'
        inchane_id = '1789'
        elements = soup.find_all('div', class_='lc_col')
        for element in elements:
            img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
            sender = re.search(r'url\((.*?)\)', img_divs[0].get('style')).group(1)
            sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
            receiver = re.search(r'url\((.*?)\)', img_divs[1].get('style')).group(1)
            receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
            text = element.get_text().split()
            date_str = f'{text[0]} {text[1]}'
            dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=8)
            add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[10]: #https://alfabit.org/ru/exchange
        inchane_id = '1682'
        usdt = 'trc erc'
        elements = soup.find_all('div', class_='exchange-item__content')
        for element in elements:
            coin_titles = element.find_all('span', class_='exchange-item__coin-title')
            sender = str(coin_titles[0].get_text()).replace(" ", "")
            sender_short = extract_in_brackets(sender)
            receiver = str(coin_titles[1].get_text()).replace(" ", "")
            receiver_short = extract_in_brackets(receiver)
            coin_amounts = element.find_all('span', class_='exchange-item__amount')
            send_amount = str(coin_amounts[0].get_text()).replace(",", ".")
            send_amount = "".join(send_amount.split())
            receive_amount = str(coin_amounts[1].get_text()).replace(",", ".")
            receive_amount = "".join(receive_amount.split())
            dt = datetime.now() - timedelta(hours=3)
            if sender == 'Bitcoin(BTC)':
                sender = 'BTC'
            if receiver == 'Bitcoin(BTC)':
                receiver = 'BTC'
            add_transaction(dt, sender, send_amount, sender_short, receiver, receive_amount, receiver_short, url, inchane_id, usdt)
            #(date, sender_img_url, send_amount, send_currency, receiver_img_url, receive_amount, receive_currency, source, inchane_id, usdt
    elif url == urls[11]: #https://obmenka.su/
            usdt = 'trc erc'
            inchane_id = '10341'
            elements = soup.find_all('div', class_='home_lchange_one')
            for element in elements:
                img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
                sender_style = img_divs[0].find('span').get('style')
                receiver_style = img_divs[1].find('span').get('style')
                sender = re.search(r'url\((.*?)\)', sender_style).group(1)
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
                receiver = re.search(r'url\((.*?)\)', receiver_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
                text = element.get_text().split()
                date_str = f'{text[0]} {text[1]}'
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[12]: #https://changeexpert.io/
            usdt = 'trc trx'
            inchane_id = '22783'
            elements = soup.find_all('div', class_='crypto')
            for element in elements:
                img_divs = element.find_all('div', class_='coin')
                sender_style = img_divs[0].find('img').get('src')
                receiver_style = img_divs[1].find('img').get('src')
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver_style).group(1)
                text = element.get_text().split()
                date_str = f'{text[3]} {text[4]}'
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                add_transaction(dt, sender, text[5], text[6], receiver, text[7], text[8], url, inchane_id, usdt)
    elif url == urls[13]: #https://btcdeal.ru/
            usdt = 'trc'
            inchane_id = '61587'
            elements = soup.find_all('div', class_='lastBlock-item swiper-slide')
            for element in elements[:10]:
                img_divs = element.find_all('div', class_='lastBlock-item__img')
                sender_style = img_divs[0].find('img').get('src')
                receiver_style = img_divs[1].find('img').get('src')
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver_style).group(1)
                text = element.get_text().split()
                dt = datetime.now() - timedelta(hours=3)
                add_transaction(dt, sender, text[0], text[1], receiver, text[2], text[3], url, inchane_id, usdt)
                #(date, sender_img_url, send_amount, send_currency, receiver_img_url, receive_amount, receive_currency, source, inchane_id, usdt,
    elif url == urls[14]: #https://avanchange.com/
            usdt = 'trc erc bep ton'
            inchane_id = '1808'
            elements = soup.find_all('div', class_='live-change')
            for element in elements:
                img_divs = element.find_all('div', class_='x')
                sender_style = img_divs[0].find('img').get('alt')
                receiver_style = img_divs[2].find('img').get('alt')
                text = element.get_text().split()
                if len(text) == 7:
                    date_str = f'{text[3]} {text[4]} {text[5]} {text[6]}'
                    date_str = date_str.replace(',', '')
                else:
                    date_str = f'{text[2]} {text[3]} {text[4]} {text[5]}'
                    date_str = date_str.replace(',', '')
                for ru_month, num_month in months.items():
                    date_str = date_str.replace(ru_month, num_month)
                dt = datetime.strptime(date_str, '%d %m %Y %H:%M') - timedelta(hours=3)
                if len(text) == 7:
                    receive_amount = f"{text[0]}{text[1]}"
                    add_transaction(dt, sender_style, '0', '?', receiver_style, receive_amount, text[2], url, inchane_id, usdt)
                else:
                    receive_amount = f"{text[0]}"
                    add_transaction(dt, sender_style, '0', '?', receiver_style, receive_amount, text[1], url, inchane_id, usdt)
    elif url == urls[15]: #https://niceobmen.com/
            usdt = 'trc erc bep'
            inchane_id = '10334'
            elements = soup.find_all('div', class_='home_lchange_one')
            for element in elements:
                img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
                sender_style = img_divs[0].get('style')
                receiver_style = img_divs[1].get('style')
                sender = re.search(r'url\((.*?)\)', sender_style).group(1)
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
                receiver = re.search(r'url\((.*?)\)', receiver_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
                text = element.get_text().split()
                date_str = f'{text[0]} {text[1]}'
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[16]: #https://yaobmen.cash/
            usdt = 'trc erc bep'
            inchane_id = '10913'
            elements = soup.find_all('div', class_='home_lchange_one')
            for element in elements:
                img_divs = element.find_all('div', class_='home_lchange_ico currency_logo')
                sender_style = img_divs[0].get('style')
                receiver_style = img_divs[1].get('style')
                sender = re.search(r'url\((.*?)\)', sender_style).group(1)
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender).group(1)
                receiver = re.search(r'url\((.*?)\)', receiver_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver).group(1)
                text = element.get_text().split()
                date_str = f'{text[0]} {text[1]}'
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                add_transaction(dt, sender, text[2], text[3], receiver, text[4], text[5], url, inchane_id, usdt)
    elif url == urls[17]: #https://nadex.io/
            usdt = 'trc erc bep'
            inchane_id = '19731'
            elements = soup.find_all('div', class_='crypto')
            for element in elements[:3]:
                img_divs = element.find_all('div', class_='coin__logo')
                sender_style = img_divs[0].find('img').get('src')
                receiver_style = img_divs[1].find('img').get('src')
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver_style).group(1)
                date_str = element.find('span', class_='time').get_text()
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                text = element.get_text().split()
                add_transaction(dt, sender, text[5], text[6], receiver, text[7], text[8], url, inchane_id, usdt)
    elif url == urls[18]: # https://bobr.exchange/
            usdt = 'trc erc bep'
            inchane_id = '0'
            elements = soup.find_all('div', class_='crypto')
            for element in elements:
                img_divs = element.find_all('div', class_='coin__logo')
                sender_style = img_divs[0].find('img').get('src')
                receiver_style = img_divs[1].find('img').get('src')
                sender = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', sender_style).group(1)
                receiver = re.search(r'uploads/(.*?)\.(png|jpg|jpeg)', receiver_style).group(1)
                date_str = element.find('span', class_='time').get_text()
                dt = datetime.strptime(date_str, '%d.%m.%Y, %H:%M') - timedelta(hours=3)
                text = element.get_text().split()
                add_transaction(dt, sender, text[5], text[6], receiver, text[7], text[8], url, inchane_id, usdt)
for url in urls:
    print(url)
    try:
        parse_page(url)
    except Exception as e:
        print(f'Ошибка при парсинге {url}: {e}')
