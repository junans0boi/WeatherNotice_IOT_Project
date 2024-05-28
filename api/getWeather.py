import requests
from datetime import datetime

# API Key와 기본 날짜 및 시간 설정
SERVICE_KEY = "Xnp%2BTViCCwNnf67xecZvXEnev8RZ3KVpPS3uPbB44Uk14TkI%2FYNkS0vOSbypnx2c%2BOhLX2zSXHI4sdCGyck0Mw%3D%3D"
BASE_DATE = datetime.today().strftime("%Y%m%d")
BASE_TIME = '0500'  # 매일 05:00시에 업데이트
NX = '55'
NY = '126'

# 날씨 코드 매핑 (강수 상태와 하늘 상태)
PTY_CODE = {0: '강수 없음', 1: '비', 2: '비/눈', 3: '눈', 5: '빗방울', 6: '진눈깨비', 7: '눈날림'}
SKY_CODE = {1: '맑음', 3: '구름많음', 4: '흐림'}

# API 요청 URL 구성
url = (
    f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    f"?serviceKey={SERVICE_KEY}&pageNo=1&numOfRows=1000&dataType=JSON"
    f"&base_date={BASE_DATE}&base_time={BASE_TIME}&nx={NX}&ny={NY}"
)

# API 요청 및 응답 데이터 파싱
response = requests.get(url, verify=False)
data = response.json()

# 날씨 데이터를 문자열로 포맷팅하는 함수
def get_weather_string(data):
    weather_data = {}
    for item in data['response']['body']['items']['item']:
        category = item['category']
        forecast_time = item['fcstTime']
        forecast_value = item['fcstValue']
        
        if forecast_time not in weather_data:
            weather_data[forecast_time] = {}
        
        weather_data[forecast_time][category] = forecast_value

    sorted_times = sorted(weather_data.keys()) # 시간 순서대로 정렬
    formatted_data = []
    for forecast_time in sorted_times:
        values = weather_data[forecast_time]
        update_time = f"{forecast_time[:2]}:{forecast_time[2:]}" # 시간 포맷 변경
        tmp = values.get('TMP', 'N/A')  # 기온
        wsd = values.get('WSD', 'N/A')  # 풍속
        sky = SKY_CODE.get(int(values.get('SKY', 0)), 'N/A')    # 하늘 상태
        pty = PTY_CODE.get(int(values.get('PTY', 0)), 'N/A')    # 강수 상태
        reh = values.get('REH', 'N/A')  # 습도

        # 포맷팅된 문자열 리스트에 추가
        formatted_data.append(
            f"{update_time} - {sky}, {pty}, 기온: {tmp}°C, "
            f", 습도: {reh}%, 바람: {wsd}m/s"
        )

    return "\n".join(formatted_data)    # 줄바꿈으로 연결된 문자열 반환

# 날씨 문자열 생성
weather_string = get_weather_string(data)

# 최종 출력 문자열 포맷
template = (
    f"{BASE_DATE[:4]}년 {BASE_DATE[4:6]}월 {BASE_DATE[6:]}일 {(int(NX), int(NY))}지역의 날씨는\n"
    f"{weather_string}"
)
print(template)
