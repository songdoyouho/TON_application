import time
import json
import datetime
import requests
from datetime import datetime
import pytz
import config

# 設定 API URL 和您的 API Key
API_URL = "https://api.geckoterminal.com/api/v2"

def get_local_time(iso_time_str):
    # 解析時間字符串為 UTC 時區的 datetime 對象
    utc_time = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")

    # 定義本地時區，例如 'Asia/Taipei'
    local_tz = pytz.timezone('Asia/Taipei')

    # 將 UTC 時間轉換成本地時間
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

    return local_time

def telegram_bot_sendtext(bot_message):
    bot_token = config.TELEGRAM_API
    MY_TELEGRAM_ID = config.MY_TELEGRAM_ID

    # 送訊息給我
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + MY_TELEGRAM_ID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()

def check_buy_number(pool):
    output_list = []

    if pool['attributes']['transactions']['m5']['buys'] > 10:
        print('m5 large buy ' + pool['attributes']['name'])
        # telegram_bot_sendtext('m5 large buy ' + pool['attributes']['name'])
        output_list.append('m5 large buy ' + pool['attributes']['name'])

    if pool['attributes']['transactions']['m15']['buys'] > 25:
        print('m15 large buy ' + pool['attributes']['name'])
        # telegram_bot_sendtext('m15 large buy ' + pool['attributes']['name'])
        output_list.append('m15 large buy ' + pool['attributes']['name'])

    if pool['attributes']['transactions']['m30']['buys'] > 50:
        print('m30 large buy ' + pool['attributes']['name'])
        # telegram_bot_sendtext('m30 large buy ' + pool['attributes']['name'])
        output_list.append('m30 large buy ' + pool['attributes']['name'])

    if pool['attributes']['transactions']['h1']['buys'] > 100:
        print('h1 large buy ' + pool['attributes']['name'])
        # telegram_bot_sendtext('h1 large buy ' + pool['attributes']['name'])
        output_list.append('h1 large buy ' + pool['attributes']['name'])

    if pool['attributes']['transactions']['h24']['buys'] > 500:
        print('h24 large buy ' + pool['attributes']['name'])
        # telegram_bot_sendtext('h24 large buy ' + pool['attributes']['name'])
        output_list.append('h24 large buy ' + pool['attributes']['name'])

    return output_list

class Geckoterminal_api():
    def get_current_price_of_a_token(self, network, token_address):
        """just get the current price of a token.
        network: 'ton' or 'bsc'
        token_address: the address of the token.
        example: get_current_price_of_a_token('ton', 'EQADDUhZbgi8wKaG7JkzEXAj2xH4O_CSlxzeJWQckKpm_Gin')
        """

        url = f"{API_URL}/simple/networks/{network}/token_price/{token_address}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None
        
    def list_networks(self):
        """
        list all the networks.
        """
        url = f"{API_URL}/networks"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None
        
    def list_dexes(self, network):
        """
        """
        url = f"{API_URL}/networks/{network}/dexes"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None
        
    def get_trending_pools_on_network(self, network):
        """
        """
        url = f"{API_URL}/networks/{network}/trending_pools"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None
        
    def get_latest_pool_on_network(self, network):
        """
        """
        url = f"{API_URL}/networks/{network}/new_pools?page=5"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None
        
    def get_specific_pool_on_network(self, network, pool_address):
        """
        """
        print("pool_address:", pool_address)
        url = f"{API_URL}/networks/{network}/pools/{pool_address}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data:", response.status_code, response.text)
            return None


if __name__ == "__main__":
    geckoterminal_api = Geckoterminal_api()
    telegram_bot_sendtext('scanning the new pools...')
    output_list = []

    while True:
        current_time = time.localtime()
        if current_time.tm_min % 1 == 0 and current_time.tm_sec == 0: # 每?分鐘執行一次
            latest_pools = geckoterminal_api.get_latest_pool_on_network('ton')
            for pool in latest_pools['data']:
                # print(json.dumps(pool, indent=4))
                tmp_output_list = check_buy_number(pool)
                for tmp_output in tmp_output_list:
                    if tmp_output not in output_list:
                        output_list.append(tmp_output)
                        telegram_bot_sendtext(tmp_output)

        time.sleep(1)

    # print(json.dumps(geckoterminal_api.get_latest_pool_on_network('ton')['data'][0], indent=4))
    # print(len(geckoterminal_api.get_latest_pool_on_network('ton')['data']))

    # latest_pools = geckoterminal_api.get_latest_pool_on_network('ton')
    # for pool in latest_pools['data']:
    #     # print(json.dumps(pool, indent=4))
    #     print(pool['attributes']['name'])
    #     # print(pool['attributes']['pool_created_at']) # 時間是 +0，換算過來要再 +8

    #     # 拿 pool_address 得到 pool 資訊0
    #     result = geckoterminal_api.get_specific_pool_on_network('ton', pool['id'].split('ton_')[1])
    #     print(result)