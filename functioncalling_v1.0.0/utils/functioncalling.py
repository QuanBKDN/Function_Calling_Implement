import gc, inspect, json, re 
from functools import partial 
import typing 
import transformers
import torch 
import xml.etree.ElementTree as ET 
from typing import Dict, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
from vllm import LLM, SamplingParams
from api_function.api_function import WeatherService, AnswerSuggestion, TimeService


def loop_selfask(completion : str, prompt, llm, sampling_params) -> str: 
    """
    Uses the LLM's self-ask capability to improve performance.
    Args:
        completion (str): The LLM's previous completion.
        prompt (str): The user's request.
        llm (LLM): The LLM model.
        sampling_params (SamplingParams): The configuration for LLM sampling.

    Returns:
        str: The improved completion from the LLM.
    """
    if "Get_weather" in completion or "Get_time" in completion :
        weather = {"name" : "Get_weather", "place" : "Fill in the location where you want to get weather information"}
        time = {"name" : "Get_time", "timezone" :"Fill valid time zone from TZ identifier (example :Asia/Bangkok,America/Los_Angeles,...)"}
        prompt_ = f"""
        You are a supporter who can make function based on descriptions :
        <start> descriptions
        {weather}
        {time}
        <end> descriptions
        Requirement: Fill in the missing information similar to the given function based on the User's request
        User: {prompt}
        Describe the missing function :{completion} 
        """
        output = llm.generate(prompt_, sampling_params)
        output = output[0].outputs[0].text
        result = completion+output
        result = result.replace(" ","")
        match = re.search(r'\{.*?\}', result)
        if match :
            json_str = match.group()
            data = json.loads(json_str)
            return data
    return completion        

def process_request(data: Dict) -> Optional[str]:
    """
    Processes the data (potentially a function dictionary) using an API.

    Args:
        data (Dict): A dictionary representing a function.

    Returns:
        Optional[str]: The retrieved information from the API or None if data is invalid.
    """
    if isinstance(data, dict) and data.get('name') == 'Get_weather':
        weather_db = WeatherService()
        place = data['place']
        forecast = weather_db.get_weather_forecast(place)
        return forecast
    elif isinstance(data, dict) and data.get('name') == 'Get_time':
        time_db = TimeService()
        timezone = data['timezone']
        time = time_db.get_time(timezone)
        return time
    return data

def generate_hermes(prompt: str, llm: LLM, sampling_params: SamplingParams) -> str:
    """
    Generates a response to the user's prompt using the LLM.
    Args:
        prompt (str): The user's prompt.
        llm (LLM): The LLM model.
        sampling_params (SamplingParams): The configuration for LLM sampling.

    Return : 
        str : a answer of llm to create function
    """
    weather = {"name" : "Get_weather", "place" : "Fill in the location where you want to get weather information"}
    time = {"name" : "Get_time", "timezone" :"Fill valid time zone from TZ identifier (example :Asia/Bangkok,America/Los_Angeles,...)"}
    fn_1 = """{"name" : "Get_weather", "place" :}"""
    fn_2 = """{"name" : "Get_time", "timezone" :}"""
    prompts = f"""<|start|> System
    You are a helpful assistant and understand Vietnamese, with access to the following functions:    
    {weather}
    {time}
    To use functions, respond to user requests in the following form:    
    {fn_1}
    {fn_2}
    ...
    <|end|> System
    User question: {prompt} 
    It is mandatory to use the above function templates to fully answer the User's question. If it is not related to the function, then answer normally like an Assistant.    
    Assistant : 
    """
    output = llm.generate(prompts, sampling_params)
    output = output[0].outputs[0].text        
    return output
