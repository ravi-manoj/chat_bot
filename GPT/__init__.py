from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import os
import sys
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('API_KEY')

class GPT:
    def construct_index(self,directory_path):
        max_input_size = 4096
        num_outputs = 256
        max_chunk_overlap = 20
        chunk_size_limit = 600
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_outputs))
        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        documents = SimpleDirectoryReader(
            directory_path, recursive=True).load_data()
        print(documents)
        return 2

    def ask_bot(self,query):
        try:
            index = GPTSimpleVectorIndex.load_from_disk(os.getcwd()+'\server\index.json')
            response = index.query(query, response_mode="compact", verbose=False)
        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            return {'status':"failed",'error': ex_value.__cause__}, 401
        else:
            return {'status': "success", 'response': response.response}, 201
        
