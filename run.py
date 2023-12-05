from db_utils.db_executor import MYSQL_ADAPTER
from db_utils.db_converter import SQL_CONVERTER, DB_SCHEMA_GENERATOR, CorrectQuery
from classify_action import ClassifyAction
from format_answer import FORMAT_RESPONSE
from numbered_card_answer import NUMBER_RESPONSE
from generate_graphs_and_insights import GenerateGraphs, CorrectCode
from generate_report_layout import GenerateReportLayout
from generate_report_lists import GenerateReportList
from io import StringIO
import pandas as pd
import concurrent.futures
import uuid
import tqdm



def classify_action(user_description):
    """
    Classifies the user_description to a function
    """
    classify_action = ClassifyAction()
    function_name, function_args =  classify_action(user_desc=user_description)
    # print("returning in run.py fun_name,func_args:\n",function_name,function_args)

    if function_name and function_args:
        return function_name, function_args
    
    else:
        if function_name:
            return function_name, {"user_description": user_description}
        return None, None

def answerQuestion(user_description: str,selected_team:str):
    queried_data_str = __get_data__(user_description=user_description,selected_team=selected_team)
    # print("\033[43m Raw answer:\033[0m",queried_data_str)
    formatted_answer = __format_answer__(question = user_description, answer = queried_data_str)
    print("\033[43m Formatted Answer:\033[0m",formatted_answer)
    return formatted_answer

def __format_answer__(question, answer):
    format_response = FORMAT_RESPONSE()
    formatted_answer = format_response(question=question, answer=answer)
    formatted_answer = formatted_answer.get('formatted_answer')
    if formatted_answer:
        return formatted_answer
    else:
        return None

def numberedcard(user_description:str,selected_team:str):
    queried_data_str = __get_data__(user_description=user_description,selected_team=selected_team)
    print("\033[43m Raw answer:\033[0m",queried_data_str)
    final_answer=_format_numberd_card(question = user_description, answer = queried_data_str)
    # print("\033[43m Formatted Answer:\033[0m",formatted_answer)
    return final_answer

def _format_numberd_card(question, answer):
    abstract_answers=NUMBER_RESPONSE()
    get_numbers=abstract_answers(question=question, answer=answer)
    extracted_number = get_numbers['formatted_answer']
    if extracted_number:
        return extracted_number
    else:
        return None
    
def generateGraph(user_description: str,selected_team:str):
    print("Generating Graph......")
    queried_data_str = __get_data__(user_description=user_description,selected_team=selected_team)
    graph_filename = __generate_graphs_and_insights__(user_description=user_description, queried_data_str=queried_data_str)
    print("Graph generated in ", graph_filename)
    return graph_filename


def __generate_graphs_and_insights__(user_description, queried_data_str):
    generate_graphs = GenerateGraphs()
    csv_buffer = StringIO(queried_data_str)
    df_from_str = pd.read_csv(csv_buffer)
    df_from_str.to_csv("complete_data.csv", index=False)
    graph_args = generate_graphs(user_description=user_description, sample_data=df_from_str[:2].to_csv(index=False))
    graph_code = graph_args.get("graph_code")
    with open("graph_code.txt", 'w') as fp:
        fp.write(graph_code)

    filename = __run_code__(graph_code=graph_code, df_from_str=df_from_str)
    print("Image saved in ",filename)
    return filename

def __run_code__(graph_code, df_from_str, attempt=0):
    if graph_code:
        global_vars = globals()
        try:
            exec(graph_code, global_vars)
            
            filename = str(uuid.uuid4())
            print("arguments ", type(df_from_str))
        
            plot_graph(data = df_from_str, save_filename=filename)
            return filename
        except Exception as e:
            if attempt > 5:
                return None
            correct_code = CorrectCode()
            graph_args = correct_code(graph_code, str(e))
            graph_code = graph_args.get("graph_code")
            print("CORRECTING CODE")
            return __run_code__(graph_code=graph_code, df_from_str=df_from_str, attempt=attempt+1)
        
    else:
        return None
    

def __get_data__(user_description,selected_team):
    sql_converter = SQL_CONVERTER()
    schema_generator = DB_SCHEMA_GENERATOR(selected_team=selected_team)
    
    db_schema,project_uuid,suite_uuid = schema_generator()
    args = sql_converter(user_description,db_schema,project_uuid,suite_uuid)
    query = args.get('mysql_command')

    #TODO LINT SQL
    print("\033[32m QUERY predicted is \033[0m", query)

    # if query and lint_sql_command(query):
    return __execute_query__(query, db_schema)

def __execute_query__(query, db_schema):
    mysql_adapter = MYSQL_ADAPTER()
    if query:
        try:
            result = mysql_adapter.execute_query(query)
            print("\033[32m RESULT IS \033[0;32m ", result)
        except Exception as e:
            correct_query = CorrectQuery()
            args = correct_query(query, str(e), db_schema)
            query = args.get('mysql_command')
            # print("\033[32m QUERY predicted is \033[0;32m ", query)
            return __execute_query__(query, db_schema)

        return result.to_csv(index=False)
    else:
        return None


def generateReport(user_description: str,selected_team:str):
    """
    1. gets the schema
    2. analyzes schema and user description and comes up with a list of graphs and content that can be on the report
    3. For each point, generate graph code and content
    4. Generates an HTML out of it
    """
    #Get schema
    schema_generator = DB_SCHEMA_GENERATOR(selected_team=selected_team)
    db_schema = schema_generator()

    #analyze schema and generate ideas
    graph_ideas = __generate_graph_ideas__(db_schema=db_schema, user_description=user_description
    )
    # insight_ideas
    
    insight_ideas =__generate_insight_ideas__(db_schema=db_schema, user_description=user_description
    )
    
    graphs = []
    response=[]
    questions_list=[]
    for question in tqdm.tqdm(insight_ideas):
        name_of_question=question.get("questions")
        details_on_question=question.get("detail")
        requesting_call=numberedcard(user_description=f"Generate an solution for following details: Question:{name_of_question},details:{details_on_question}",selected_team=selected_team)
        questions_list.append(name_of_question)
        response.append(requesting_call)
    print("\033[33mALL QUESTIONS:\033[0m")
    for question in questions_list:
        print(question)
    print("\033 Final RESPONSE OF NUMBERED CARD ARE\033[0m",response)
        
    for graph_idea in tqdm.tqdm(graph_ideas):
        graph_description = graph_idea.get("graph_description")
        graph_details = graph_idea.get("graph_details")
        graph_reason = graph_idea.get("graph_reason")

        graph_filename = generateGraph(user_description=f"Generate graph for following details. graph_description: {graph_description}, graph_details: {graph_details}",selected_team=selected_team)
        graph_idea['graph_filename'] = graph_filename

        graphs.append(graph_idea)

    return graphs


def __generate_graph_ideas__(db_schema, user_description):
    """gets the db_schema and user_description and gives it to gpt, and ask it to generate the list of graph description and graph content that can be generated to create the report"""
    generate_report_layout = GenerateReportLayout()
    args = generate_report_layout(db_schema=db_schema, user_description=user_description)
    graph_ideas = args.get("graphs")
    return graph_ideas

def __generate_insight_ideas__(db_schema,user_description):
    """gets the db_schema and user_description and gives it to gpt, and ask it to generate the list of insight description and insight content that can be generated to create the report"""
    generate_report_lists=GenerateReportList()
    args = generate_report_lists(db_schema=db_schema, user_description=user_description)
    questions_list=args.get("insight")
    return questions_list


