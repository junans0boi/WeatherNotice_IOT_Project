import requests
from datetime import datetime, timedelta

SERVICE_KEY = "Xnp%2BTViCCwNnf67xecZvXEnev8RZ3KVpPS3uPbB44Uk14TkI%2FYNkS0vOSbypnx2c%2BOhLX2zSXHI4sdCGyck0Mw%3D%3D"
BASE_DATE = datetime.today().strftime("%Y%m%d") # 현재 날짜 뽑아옴
BASE_TIME = '0600'
NX = '55'
NY = '124'

# 각 데이터 항목 파싱
PTY_CODE = {0: '강수 없음', 1: '비', 2: '비/눈', 3: '눈', 5: '빗방울', 6: '진눈깨비', 7: '눈날림'}
SKY_CODE = {1: '맑음', 3: '구름많음', 4: '흐림'}

# API 요청 입력 시간 계산
input_d = datetime.strptime(BASE_DATE + BASE_TIME, "%Y%m%d%H%M") - timedelta(hours=1)
input_datetime = input_d.strftime("%Y%m%d%H%M")
input_time = input_datetime[-4:]

# URL
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={SERVICE_KEY}&pageNo=1&numOfRows=1000&dataType=JSON&base_date={BASE_DATE}&base_time={input_time}&nx={NX}&ny={NY}"

# 포맷팅
response = requests.get(url, verify=False)
data = response.json()

def get_weather_string(data):
    weather_data = {}
    for item in data['response']['body']['items']['item']:
        category = item['category']
        fcst_time = item['fcstTime']
        fcst_value = item['fcstValue']
        
        if fcst_time not in weather_data:
            weather_data[fcst_time] = {}
        
        weather_data[fcst_time][category] = fcst_value

    sorted_times = sorted(weather_data.keys())
    formatted_data = []
    for fcst_time in sorted_times:
        values = weather_data[fcst_time]
        current_time = f"{fcst_time[:2]}:{fcst_time[2:]}"
        tem = values.get('TMP', 'N/A')
        vec = values.get('WSD', 'N/A')
        sky = SKY_CODE.get(int(values.get('SKY', 0)), 'N/A')
        precipitation = PTY_CODE.get(int(values.get('PTY', 0)), 'N/A')
        REH = values.get('REH', 'N/A')

        formatted_data.append(
            f"{current_time} - {sky}, {precipitation}, 기온: {tem}°C, "
            f", 습도: {REH}%, 바람: {vec}m/s"
        )

    return "\n".join(formatted_data)

weather_string = get_weather_string(data)
template = f'''{(int(NX), int(NY))} 지역의 날씨는\n{weather_string}'''
print(template)
