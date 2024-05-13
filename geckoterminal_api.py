import time
import json
import datetime
import requests

# 設定 API URL 和您的 API Key
API_URL = "https://api.geckoterminal.com/api/v2"

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
        url = f"{API_URL}/networks/{network}/new_pools?page=1"
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

    new_pool_list = []

    while True:
        current_time = time.localtime()
        if current_time.tm_min % 1 == 0 and current_time.tm_sec == 0: # 每?分鐘執行一次
            latest_pools = geckoterminal_api.get_latest_pool_on_network('ton')
            for pool in latest_pools['data']:
                print(json.dumps(pool, indent=4))
                if pool not in new_pool_list:
                    new_pool_list.append(pool)

        time.sleep(0.5)

        if current_time.tm_min % 1 == 0 and current_time.tm_sec == 30:
            print(len(new_pool_list))