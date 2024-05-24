from gtts import gTTS
import os

def text_to_speech(text: str, language: str, output_file: str):
    speech = gTTS(text=text, lang=language)
    speech.save(output_file)
    os.system(f"start {output_file}")  # This is for Windows. Use 'open' for macOS or 'xdg-open' for Linux
    print(f"음성 파일이 '{output_file}'로 저장되었습니다.")

if __name__ == "__main__":
    text = "안녕하세요, 여기는 ChatGPT입니다."
    language = 'ko'
    output_file = "output.mp3"
    text_to_speech(text, language, output_file)
