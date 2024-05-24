from datetime import datetime, timedelta
import json
import requests

serviceKey = "Xnp%2BTViCCwNnf67xecZvXEnev8RZ3KVpPS3uPbB44Uk14TkI%2FYNkS0vOSbypnx2c%2BOhLX2zSXHI4sdCGyck0Mw%3D%3D" # API Key 입력
base_date = '20240525' # 발표 일자
base_time = '0100' # 발표 시간
nx = '55' # 예보 지점 x좌표
ny = '124' # 예보 지점 y좌표

# 각 데이터 항목 파싱
deg_code = {0 : 'N', 360 : 'N', 180 : 'S', 270 : 'W', 90 : 'E', 22.5 :'NNE',
           45 : 'NE', 67.5 : 'ENE', 112.5 : 'ESE', 135 : 'SE', 157.5 : 'SSE',
           202.5 : 'SSW', 225 : 'SW', 247.5 : 'WSW', 292.5 : 'WNW', 315 : 'NW',
           337.5 : 'NNW'}
pyt_code = {0 : '강수 없음', 1 : '비', 2 : '비/눈', 3 : '눈', 5 : '빗방울', 6 : '진눈깨비', 7 : '눈날림'}
sky_code = {1 : '맑음', 3 : '구름많음', 4 : '흐림'}

# 입력 시간 계산
input_d = datetime.strptime(base_date + base_time, "%Y%m%d%H%M" ) - timedelta(hours=1)
input_datetime = datetime.strftime(input_d, "%Y%m%d%H%M")
input_time = input_datetime[-4:]

# url
url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?serviceKey={serviceKey}&numOfRows=60&pageNo=1&dataType=json&base_date={base_date}&base_time={input_time}&nx={nx}&ny={ny}"

# url로 API return 값 요청
response = requests.get(url, verify=False)
res = json.loads(response.text)

# 날씨 정보 받아오기
informations = dict()
for items in res['response']['body']['items']['item'] :
    cate = items['category']
    fcstTime = items['fcstTime']
    fcstValue = items['fcstValue']
    temp = dict()
    temp[cate] = fcstValue
    
    if fcstTime not in informations.keys() :
        informations[fcstTime] = dict()
    informations[fcstTime][cate] = fcstValue

# 풍향
def deg_to_dir(deg) :
    close_dir = ''
    min_abs = 360
    if deg not in deg_code.keys() :
        for key in deg_code.keys() :
            if abs(key - deg) < min_abs :
                min_abs = abs(key - deg)
                close_dir = deg_code[key]
    else : 
        close_dir = deg_code[deg]
    return close_dir
deg_to_dir(0)

# 문자열 포맷팅
for key, val in zip(informations.keys(), informations.values()) :
    template = f"""{base_date[:4]}년 {base_date[4:6]}월 {base_date[-2:]}일 {key[:2]}시 {key[2:]}분 {(int(nx), int(ny))} 지역의 날씨는 """ 
    
    # 맑음(1), 구름많음(3), 흐림(4)
    if val['SKY'] :
        sky_temp = sky_code[int(val['SKY'])]
        template += sky_temp + " "
    
    # (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
    if val['PTY'] :
        pty_temp = pyt_code[int(val['PTY'])]
        template += pty_temp
        # 강수 있는 경우
        if val['RN1'] != '강수없음' :
            # RN1 1시간 강수량 
            rn1_temp = val['RN1']
            template += f"시간당 {rn1_temp}mm "
    
    # 기온
    if val['T1H'] :
        t1h_temp = float(val['T1H'])
        template += f" 기온 {t1h_temp}℃ "
        
    # 습도
    if val['REH'] :
        reh_temp = float(val['REH'])
        template += f"습도 {reh_temp}% "
    
    # 풍향/풍속
    if val['VEC'] and val['WSD']:
        vec_temp = deg_to_dir(float(val['VEC']))
        wsd_temp = val['WSD']
        
    template += f"풍속 {vec_temp} 방향 {wsd_temp}m/s"
    print(template)