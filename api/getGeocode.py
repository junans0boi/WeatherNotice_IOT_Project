import requests

def get_geocode(address, api_key):
    # URL
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'

    try:
        # API Request
        response = requests.get(url)
        response.raise_for_status()  # 요청이 성공했는지 확인
        
        data = response.json()  # Parse Json

        if data['status'] == 'OK':
            # 첫 번째 결과 추출
            result = data['results'][0]
            location = result['geometry']['location']
            lat, lng = location['lat'], location['lng']

            # 주소 및 위치 출력
            print(f"주소: {result['formatted_address']}")
            print(f"위도: {lat}")
            print(f"경도: {lng}")

            return lat, lng
        else:
            print(f"지오코딩 응답 오류: {data['status']}")
            return None, None
    
    except requests.exceptions.RequestException as e:
        print(f"API로부터 유효한 응답을 받지 못했습니다. 오류: {e}")
        return None, None

# address & API KEY
address = "대한민국 인천광역시 미추홀구 경원대로 717"
api_key = "AIzaSyDvzen4CZo2B7FOoK8n0EqYpdJSpFgEKjs"

# 함수 호출
latitude, longitude = get_geocode(address, api_key)