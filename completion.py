from config import OPENAI_CONFIG
import openai
from openai.error import RateLimitError
import traceback
from typing import List
import time
import json
from promts import JSON_CORRECTION_PROMPT
from schemas.function_schemas import CORRECT_JSON

class Completion:
    def __init__(self):
        if OPENAI_CONFIG.API_TYPE == "azure":
            openai.api_type = OPENAI_CONFIG.API_TYPE
            openai.api_base = OPENAI_CONFIG.AZURE_ENDPOINT
            openai.api_version = OPENAI_CONFIG.AZURE_API_VERSION
            openai.api_key = OPENAI_CONFIG.AZURE_OPENAI_API_KEY
        else:
            openai.api_key = OPENAI_CONFIG.AZURE_OPENAI_API_KEY


    def __call__(self, messages: List[dict], model_name: str, load_json=True, cnt=0):
            
        try:
            

            ags = {
                "messages": messages
            }
            
            print("\033[95m Messages in completion:.\033[0m",messages)
            print("\033[95m ags in completion.\033[0m",ags)

            if OPENAI_CONFIG.API_TYPE == "azure":
                ags["engine"] = OPENAI_CONFIG.MODELS[model_name]
            else:
                ags["model"] = OPENAI_CONFIG.MODELS[model_name]

            response = openai.ChatCompletion.create(
                **ags
                )
            
            print("\033[95mresponse in completion:\033[0m",response)

            choices = response.get("choices")[0]
            content = choices.get("message").get("content")
            
            print("\033[95mcontent in completion\n:\033[0m",content)

            return content
            

        except RateLimitError:
            if cnt  > 2:
                raise Exception("RateLimit Error. Called OpenAI 3 times")
            cnt += 1
            time.sleep(5)
            print(f'RateLimit Error, Trying Again...')
            return self.__call__(messages, model_name, load_json, cnt)
        except ConnectionError:
            if cnt  > 2:
                raise Exception("ConnectionError. Called OpenAI 3 times")
            cnt += 1
            time.sleep(5)
            print(f'Connection Error, Trying Again...')
            return self.__call__(messages, model_name, load_json, cnt)
        except Exception as err:
            if cnt > 2:
                raise Exception(str(err))
            time.sleep(5)
            cnt += 1
            print(f'ERROR: {str(err)}')
            print(f'TRACEBACK: {traceback.format_exc()}')
            return self.__call__(messages, model_name, load_json, cnt)

class FunctionCall:

    def __init__(self):
        if OPENAI_CONFIG.API_TYPE == "azure":
            openai.api_type = OPENAI_CONFIG.API_TYPE
            openai.api_base = OPENAI_CONFIG.AZURE_ENDPOINT
            openai.api_version = OPENAI_CONFIG.AZURE_API_VERSION
            openai.api_key = OPENAI_CONFIG.AZURE_OPENAI_API_KEY
        else:
            openai.api_key = OPENAI_CONFIG.AZURE_OPENAI_API_KEY

    def __call__(self,
                 messages: List[dict],
                 model_name: str,
                 functions: List,
                 cnt: int = 0,
                 call_first: bool = True):
        
        try:
            
            ags = {
                "messages": messages,
                "functions": functions,
                "function_call": {
                    "name": functions[0].get("name")
                } if call_first else "auto",
                "temperature": 0.2
            }
            
            print("\033[95m messages in function call:\033[0m",messages)
            print("\033[95m ags in function call \n \033[0m",ags)
            if OPENAI_CONFIG.API_TYPE == "azure":
                ags["engine"] =OPENAI_CONFIG.MODELS[model_name]
            else:
                ags["model"] = OPENAI_CONFIG.MODELS[model_name]
            
            response = openai.ChatCompletion.create(
                **ags
                
            )
            print("\033[95m Response in function call\n: \033[0m ", response)
            # with open("func_call_resp.json", 'w') as fp:
            #     json.dump(response, fp)

            if response.choices[0]["message"].get("function_call", None):
                function = response.choices[0]["message"]["function_call"]
                function_name = function.get("name")
                try:
                    function_arguments = json.loads(function.get("arguments"), strict=False)
                except:
                    messages = [{
                        "role": "system",
                        "content": JSON_CORRECTION_PROMPT.system_prompt
                    }, {
                        "role": "user",
                        "content": JSON_CORRECTION_PROMPT.user_prompt.format(incorrect_json=function.get("arguments"))
                    }]

                    functions = [{
                        "name": "formatJson",
                        "description":
                        """This formats json.
                            """,
                        "parameters": CORRECT_JSON.schema()
                    }]
                    _, args = FunctionCall()(messages = messages, functions=functions, model_name='gpt-4-32k')
                    function_arguments = json.loads(args.get("corrected_json"), strict=False)
                return function_name, function_arguments
            else:
                function = response.choices[0]["message"]["content"]
                print("\033[95m Function in response if not none cond :\n \033[0m",function)
                try:
                    function_resp = json.loads(function, strict=False)
                except:
                    messages = [{
                        "role": "system",
                        "content": JSON_CORRECTION_PROMPT.system_prompt
                    }, {
                        "role": "user",
                        "content": JSON_CORRECTION_PROMPT.user_prompt.format(incorrect_json=function.get("arguments"))
                    }]

                    functions = [{
                        "name": "formatJson",
                        "description":
                        """This formats json.
                            """,
                        "parameters": CORRECT_JSON.schema()
                    }]
                    _, args = FunctionCall()(messages = messages, functions=functions, model_name='gpt-4-32k')
                    function_arguments = json.loads(args.get("corrected_json"), strict=False)
                return function_resp.get('function'), function_resp.get('arguments')
        except RateLimitError:
            if cnt > 2:
                raise Exception("RateLimit Error, called OpenAI 3 times.")
            time.sleep(5)
            print("RATE LIMIT ERROR...Trying AGAIN")
            cnt += 1
            return self.__call__(messages, model_name, functions,
                                 cnt, call_first)
        except ConnectionError:
            if cnt > 2:
                raise Exception("RateLimit Error, called OpenAI 3 times.")
            time.sleep(5)
            print("ConnectionError trying again")
            cnt += 1
            return self.__call__(messages, model_name, functions,
                                 cnt, call_first)
        except Exception as err:
            if cnt > 2:
                raise Exception(str(err))
            time.sleep(5)
            print("Got exception: ", str(err))
            cnt += 1
            return self.__call__(messages, model_name, functions,
                                 cnt, call_first)

if __name__ == "__main__":
    messages = [{
                "role": "system",
                "content": system_message
            }, {
                "role": "user",
                "content": user_message
            }]