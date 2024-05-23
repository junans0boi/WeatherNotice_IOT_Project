from gtts import gTTS
import os

# 변환할 텍스트를 입력하세요.
text = "안녕하세요, 여기는 ChatGPT입니다."

# 텍스트를 변환할 언어를 지정하세요. 예: 'ko'는 한국어입니다.
language = 'ko'

# gTTS 객체를 생성합니다.
speech = gTTS(text=text, lang=language)

# 변환된 음성을 저장할 파일명을 지정하세요.
output_file = "output.mp3"

# 음성 파일을 저장합니다.
speech.save(output_file)

# 저장된 음성 파일을 재생합니다. (옵션)
os.system(f"start {output_file}")

print(f"음성 파일이 '{output_file}'로 저장되었습니다.")
