import json
import requests

def get_jettons(account_id, currencies):
    url = f"https://tonapi.io/v2/accounts/{account_id}/jettons"
    params = {'currencies': ','.join(currencies)}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}
    
def get_account_transactions(account_id):
    url = f"https://tonapi.io/v2/blockchain/accounts/{account_id}/transactions"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data, status code: {response.status_code}"}


if __name__ == "__main__":
    # account_id = "UQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKZ"
    # account_id = "UQB7RQglXjFhNlIgGaAD-WDmrulKGXhH6HfKU_M4YPKWaxeZ"

    # account_id = "EQCN8TpPuQud6STd34j0R4DYySdr56KUO2SBnCxv7pdXwdJH"
    # currencies = ["usd", "ton"]
    
    # data = get_jettons(account_id, currencies)
    
    # # print(json.dumps(data, indent=4))
    # print(len(data['balances']))

    # for balance in data['balances']:
    #     if 'LP' in balance['jetton']['symbol']:
    #         print(json.dumps(balance['jetton'], indent=4))

    result = get_account_transactions("UQAKHdbLTBTYbgIeUzbcTuRnAiXkSwgHhiwzJfbKkowxjnXN")
    print(json.dumps(result['transactions'][1]['out_msgs'][0]['decoded_body']['destination'], indent=4))
    print(len(result['transactions'][1])) # 交易的排列順序是由新到舊
