
from completion import Completion, FunctionCall
from promts import GENERATE_REPORT_LAYOUT_PROMPT
from schemas.function_schemas import GenerateReportLayoutSchema

class GenerateReportLayout:
    def __init__(self):
        self.completion = Completion()
        self.function_call = FunctionCall()

    def __call__(self, user_description, db_schema):
        messages = [{
            "role": "system",
            "content": GENERATE_REPORT_LAYOUT_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": GENERATE_REPORT_LAYOUT_PROMPT.user_prompt.format(user_description=user_description, db_schema=db_schema)
        }]
        
        # print("\033[31m Message in Generate report layout \033[0m", messages)

        functions = [{
            "name": "showReport",
            "description":
            """This function get the user description and database schema and generates the list of graphs and graph content that can be shown in the report.
                """,
            "parameters": GenerateReportLayoutSchema.schema()
        }]
        
        # print("\033[31m functions in Generate report layout \033[0m", functions)

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        # print("\033[31m ARGSSSSS IN REPORT \033[0m", args)
        return args