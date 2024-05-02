import gradio as gr
import argparse
from utils.functioncalling import generate_hermes, loop_selfask, process_request
from vllm import LLM, SamplingParams
from configs import Config

def parse_args():
    parser = argparse.ArgumentParser(description="Functioncalling Chatbot")
    parser.add_argument("--model_name", type=str, default="mistralai/Mistral-7B-Instruct-v0.2", help="Name of the language model to use")
    parser.add_argument("--server_port", type=int, default=7868, help="Port number for launching the server")
    parser.add_argument("--server_name", type=str, default="localhost", help="Server name or IP address")
    return parser.parse_args()

def main():
    args = parse_args()
    
    _config = Config()

    SAMPLING_PARAMS = SamplingParams(temperature=_config.temperature, top_p=_config.top_p, top_k=_config.top_k)
    MAX_MODEL_LEN = _config.MAX_MODEL_LEN
    GPU_MEMORY_UTILIZATION = _config.GPU_MEMORY_UTILIZATION

    # Initialize language model
    llm = LLM(model=args.model_name, max_model_len=MAX_MODEL_LEN, gpu_memory_utilization=GPU_MEMORY_UTILIZATION, enforce_eager=True)

    # Chat interface function
    def chat_interface(message, history):
        completion = generate_hermes(message, llm, SAMPLING_PARAMS)
        response = loop_selfask(completion, message, llm, SAMPLING_PARAMS)
        result = process_request(response)
        if isinstance(response, dict):
            result_ = f""" 'Functioncall' : {response}
                         -------------------------
                         'Result : {result}"""
            return result_
        else:
            return result

    iface = gr.ChatInterface(
        fn=chat_interface,
        examples=[["Cho tôi biết thời tiết tại Danang hôm nay"], ["Bây giờ ở Hong Kong là mấy giờ"]],
        title="Functioncalling Chatbot"
    )
    iface.launch(share=True, server_port=args.server_port, server_name=args.server_name)

if __name__ == "__main__":
    main()
