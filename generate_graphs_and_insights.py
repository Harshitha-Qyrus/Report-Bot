
import re
from completion import Completion, FunctionCall,AsyncCompletion
from promts import GENERATE_GRAPH_PROMPT,CORRECT_GRAPH_PROMPT
from schemas.function_schemas import GenerateGraph
import asyncio
import json

class GenerateGraphs:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()
        self.async_function = AsyncCompletion()

    async def __call__(self, user_description, sample_data):
        messages = [[{
            "role": "system",
            "content": GENERATE_GRAPH_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GENERATE_GRAPH_PROMPT.user_prompt.format(user_description=user_message, sample_data=df_data)
        }] for user_message,df_data in zip(user_description,sample_data) ]

        functions = [{
            "name": "generateGraph",
            "description":
            """This generates graph.
                """,
            "parameters": GenerateGraph.schema()
        }]
        
        # _, args=await self.async_function(
        #         message=messages,
        #         model="gpt-4-32k",
        #         functions=functions,
        #         function_call={"name": functions[0].get("name")})
        
        results = await asyncio.gather(*[
            self.async_function(
                message=msg,
                model="gpt-4-32k",
                functions=functions,
                function_call={"name": functions[0].get("name")})
            for msg in messages
        ])
        
        graph_codes = []
        for r in results:
            function_call_code = r['choices'][0]['message']['function_call']['arguments']
            match = re.search(r'"graph_code": "(.*?)"', function_call_code)
            if match:
                graph_code = match.group(1)
                graph_codes.append(graph_code)
        print("Total code for Graphs:",graph_codes)
        
        
        # graph_codes = [
        #         r["choices"][0]["message"]["function_call"][
        #             "arguments"]["graph_code"] for r in results]
        # [response['choices'][0]['message']['function_call']['arguments']['graph_code'] for response in responses]
        # _, args =self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        return graph_codes
    
class CorrectCode:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, graph_code, error_message):
        messages = [{
            "role": "system",
            "content": CORRECT_GRAPH_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": CORRECT_GRAPH_PROMPT.user_prompt.format(code=graph_code, error_message=error_message)
        }]

        functions = [{
            "name": "generateGraph",
            "description":
            """This generates graph.
                """,
            "parameters": GenerateGraph.schema()
        }]

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        return args


if __name__ == "__main__":
    generate_graphs = GenerateGraphs()
    args = generate_graphs(user_description="plot executions vs result", sample_data="execution_id, result\n1, Pass\n, 2, Fail")
    graph_code = args.get("graph_code")
    with open("graph_code.txt", 'w') as fp:
        fp.write(graph_code)