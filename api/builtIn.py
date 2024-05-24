import requests
import math
from datetime import datetime, timedelta
import json

# 격자 정보 변환을 위한 변수
RE = 6371.00877  # 지구 반경(km)
GRID = 5.0  # 격자 간격(km)
SLAT1 = 30.0  # 투영 위도1(degree)
SLAT2 = 60.0  # 투영 위도2(degree)
OLON = 126.0  # 기준점 경도(degree)
OLAT = 38.0  # 기준점 위도(degree)
XO = 43  # 기준점 X좌표(GRID)
YO = 136  # 기준점 Y좌표(GRID)

# 데이터 항목 매핑
DEG_CODE = {
    0: 'N', 360: 'N', 180: 'S', 270: 'W', 90: 'E',
    22.5: 'NNE', 45: 'NE', 67.5: 'ENE', 112.5: 'ESE',
    135: 'SE', 157.5: 'SSE', 202.5: 'SSW', 225: 'SW',
    247.5: 'WSW', 292.5: 'WNW', 315: 'NW', 337.5: 'NNW'
}

PTY_CODE = {
    0: '강수 없음', 1: '비', 2: '비/눈', 3: '눈',
    5: '빗방울', 6: '진눈깨비', 7: '눈날림'
}

SKY_CODE = {1: '맑음', 3: '구름많음', 4: '흐림'}

def get_geocode(address, api_key):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding response error: {data['status']}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Failed to get a valid response from the API. Error: {e}")
        return None, None

def dfs_xy_conv(code, v1, v2):
    DEGRAD = math.pi / 180.0

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    if code == "toXY":
        ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
        ra = re * sf / math.pow(ra, sn)
        theta = v2 * DEGRAD - olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn

        x = math.floor(ra * math.sin(theta) + XO + 0.5)
        y = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
        return x, y
    return None

def getWeather(service_key, base_date, base_time, nx, ny):
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={service_key}&numOfRows=60&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
    response = requests.get(url, verify=False)
    return json.loads(response.text)

def parse_to_weather(data):
    informations = {}
    for item in data['response']['body']['items']['item']:
        fcst_time = item['fcstTime']
        category = item['category']
        fcst_value = item['fcstValue']

        if fcst_time not in informations:
            informations[fcst_time] = {}
        informations[fcst_time][category] = fcst_value
    return informations

def deg_to_dir(deg):
    if deg not in DEG_CODE:
        closest_dir = min(DEG_CODE.keys(), key=lambda k: abs(k - deg))
        return DEG_CODE[closest_dir]
    return DEG_CODE[deg]

def format_to_weather(base_date, address, informations):
    report = []
    for time, values in informations.items():
        template = f"{base_date[:4]}년 {base_date[4:6]}월 {base_date[-2:]}일 {time[:2]}시 {time[2:]}분 {address} 지역의 날씨는 "
        if 'SKY' in values:
            template += f"{SKY_CODE[int(values['SKY'])]} "
        if 'PTY' in values:
            template += f"{PTY_CODE[int(values['PTY'])]} "
            if 'RN1' in values and values['RN1'] != '강수없음':
                template += f"시간당 {values['RN1']}mm "
        if 'T1H' in values:
            template += f"기온 {float(values['T1H'])}℃ "
        if 'REH' in values:
            template += f"습도 {float(values['REH'])}% "
        if 'VEC' in values and 'WSD' in values:
            template += f"풍속 {deg_to_dir(float(values['VEC']))} 방향 {values['WSD']}m/s"
        report.append(template)
    return report

def main():
    # Geocode API parameters
    address = "대한민국 인천광역시 미추홀구 경원대로 717"
    api_key = "AIzaSyDvzen4CZo2B7FOoK8n0EqYpdJSpFgEKjs"

    # 위경도 데이터 요청
    latitude, longitude = get_geocode(address, api_key)

    # 위경도 -> Grid
    grid_x, grid_y = dfs_xy_conv("toXY", latitude, longitude)

    # Weather API parameters
    service_key = "Xnp%2BTViCCwNnf67xecZvXEnev8RZ3KVpPS3uPbB44Uk14TkI%2FYNkS0vOSbypnx2c%2BOhLX2zSXHI4sdCGyck0Mw%3D%3D"
    base_date = '20240525'
    base_time = '0100'

    # 날씨 API에 요청할 시간 계산
    input_d = datetime.strptime(base_date + base_time, "%Y%m%d%H%M") - timedelta(hours=1)
    input_time = datetime.strftime(input_d, "%Y%m%d%H%M")[-4:]

    # 날씨 데이터 요청
    weather_data = getWeather(service_key, base_date, input_time, grid_x, grid_y)
    informations = parse_to_weather(weather_data)

    # Generate weather report
    weather_report = format_to_weather(base_date, address, informations)

    # Print the weather report
    for report in weather_report:
        print(report)

if __name__ == "__main__":
    main()
