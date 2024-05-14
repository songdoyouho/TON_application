from datetime import datetime
import pytz

# ISO 8601 格式的時間字符串
iso_time_str = "2024-05-13T22:23:27Z"

def get_local_time(iso_time_str):
    # 解析時間字符串為 UTC 時區的 datetime 對象
    utc_time = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%SZ")

    # 定義本地時區，例如 'Asia/Taipei'
    local_tz = pytz.timezone('Asia/Taipei')

    # 將 UTC 時間轉換成本地時間
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

    return local_time