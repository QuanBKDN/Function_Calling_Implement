class Config(object):
    API_WEATHER_KEY = 'f1fb7258160ee918200f4f04e6a7421e'
    URL_WEATHER = "http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}&units=metric"
    API_ANSWERSUGGEST_URL = 'http://103.119.132.170:8002/test/v2.0/answer_suggestion'
    HEADERS_API_ANSWERSUGGEST = '{"Accept": "application/json", "Content-Type": "application/json"}'
    #config for vllm
    MAX_MODEL_LEN = 2048
    GPU_MEMORY_UTILIZATION = 0.7
    temperature = 0.2
    top_p = 0.9
    top_k = 1