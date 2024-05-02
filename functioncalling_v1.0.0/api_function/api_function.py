import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from configs import Config

_config = Config()

class WeatherService:

    @staticmethod
    def get_weather_forecast(place):
        try:
            url = _config.URL_WEATHER.format(place=place, API_KEY=_config.API_WEATHER_KEY)
            response = requests.get(url)
            response.raise_for_status()  
            data = response.json()
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"Thời tiết tại {place} là {weather_description} với nhiệt độ là {temperature}"
        except requests.RequestException as e:
            return f"Không thể truy cập dữ liệu thời tiết: {e}"

class AnswerSuggestion:
    API_URL  = _config.API_ANSWERSUGGEST_URL
    HEADERS = _config.HEADERS_API_ANSWERSUGGEST
    @staticmethod
    
    def get_answer_suggestion(question):
        try:
            question_doc = {"id": "string", "guestId": "string", "question": question}
            search_result = requests.post(url=f'{AnswerSuggestion.API_URL}?subject=math&number_related_answers=5', json=question_doc, headers=AnswerSuggestion.HEADERS)
            search_result.raise_for_status()  
            search_result = search_result.json()
            if search_result.get("results"):
                answer = search_result['results']['answer']
                return f"Đây là đáp án của bài toán trên: {answer}"
            elif search_result.get("choices"):
                answer = search_result['choices'][0]['answer']
                question_content = search_result['choices'][0]['question_content']
                return f"Bạn có thể tham khảo bài toán cùng dạng này:\nQuestion: {question_content}\nAnswer: {answer}"
            else:
                return f"Không có thông tin cho bài toán {question}"
        except requests.RequestException as e:
            return f"Không thể lấy đề xuất câu trả lời: {e}"

class TimeService:
    @staticmethod
    
    def get_time(timezone: str) -> str:
        try:
            now = datetime.now(ZoneInfo(timezone))
            time = now.strftime("%H:%M")
            return f"Thời gian hiện tại với timezone: {timezone} : {time}"
        except Exception as e:
            return f"Không thể lấy thông tin thời gian: {e}"