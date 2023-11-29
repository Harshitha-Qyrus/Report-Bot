
from completion import Completion, FunctionCall
from promts import GENERATE_GRAPH_PROMPT,CORRECT_GRAPH_PROMPT
from schemas.function_schemas import GenerateGraph

class GenerateGraphs:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, user_description, sample_data):
        messages = [{
            "role": "system",
            "content": GENERATE_GRAPH_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GENERATE_GRAPH_PROMPT.user_prompt.format(user_description=user_description, sample_data=sample_data)
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