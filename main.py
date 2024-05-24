from WeatherNoticeLLM import set_api_key, get_llm_answer
from GTTS import text_to_speech

def main():
    # Set the API key for the LLM
    set_api_key()
    
    # Get the answer from the LLM
    prompt = "응~니얼굴~"
    answer = get_llm_answer(prompt)
    print(f"LLM Answer: {answer}")
    
    # Convert the answer to speech and save as MP3
    language = 'ko'
    output_file = "llm_output.mp3"
    text_to_speech(answer, language, output_file)

if __name__ == "__main__":
    main()
