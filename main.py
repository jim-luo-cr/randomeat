import requests
import random
import logging


# 設定Log的顯示格式
logging.basicConfig(level=logging.INFO,
	format='[%(asctime)s %(levelname)-8s] %(message)s',
	datefmt='%Y%m%d %H:%M:%S',
	)


# Foodpanda api
def foodpanda(longitude, latitude, cuisine=''):
    url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
    query = {
        'longitude': longitude, # 經度
        'latitude': latitude, # 緯度
        'language_id': 6,
        'include': 'characteristics',
        'dynamic_pricing': 0,
        'configuration': 'Variant1',
        'country': 'tw',
        'budgets': '',
        'cuisine': cuisine, # 料理種類
        'sort': '',
        'food_characteristic': '',
        'use_free_delivery_label': False,
        'vertical': 'restaurants',
        'limit': 128, # 搜尋數量
        'offset': 0,
        'customer_type': 'regular',
        # 'opening_type': 'pickup' # 自取
    }
    headers = {
        'x-disco-client-id': 'web',
    }
    r = requests.get(url=url, params=query, headers=headers)
    if r.status_code == requests.codes.ok:
        data = r.json()
        restaurants = data['data']['items']
        return restaurants
    else:
        logging.error('Request failed.') # 請求失敗
        return []


# Line Notify api
def lineNotifyMessage(token, msg):
    headers = {
        'Authorization': 'Bearer ' + token, # Token
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {'message': msg}
    # Post to Line Notify
    r = requests.post(
        'https://notify-api.line.me/api/notify',
        headers=headers, 
        params=payload)
    return r.status_code


# 主程式開始
if __name__ == '__main__':
    # 雲馥數位的座標
    cloudriches_station = (121.486545, 25.0576383)

    # Line Notify 的 Token
    token = 'xxxxx'

    """
    cuisine:
    166     中港
    225     健康餐
    214     小吃
    165     披薩
    164     日韓
    252     東南亞
    175     歐式
    177     漢堡
    176     甜點
    183     異國
    186     素食
    179     美式
    181     飲料
    201     麵食
    """
    # 呼叫foodpanda的function
    restaurants = foodpanda(cloudriches_station[0], cloudriches_station[1], cuisine='181')
    logging.info('Find restaurants :{}'.format(len(restaurants)))

    # 如果有收到店家資訊
    if len(restaurants):
        msg = ''

        # 取隨機3家店家
        choose = 3
        if len(restaurants) < choose:
            choose = len(restaurants)
        random_index = random.sample(range(0, len(restaurants)), choose)

        # 讀取隨機index的店家資訊組成訊息
        for index in random_index:
            restaurant = restaurants[index]
            msg += '\n🥤【推薦】：{}\n'.format(restaurant['name'])
            msg += '🌟【評價】：{}\n'.format(restaurant['rating'])
            msg += '🔗【連結】：{}\n'.format(restaurant['redirection_url'])

        # 確認訊息有內容
        if len(msg):
            logging.info('Sending Line Notify . . . ')
            status_code = lineNotifyMessage(token, msg)
            if status_code == 200:
                logging.info('Success.')
            else:
                logging.error('Response: {}'.format(status_code))
        else:
            logging.error('msg is empty.')
