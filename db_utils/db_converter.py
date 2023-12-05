from typing import Any
from completion import Completion, FunctionCall
from db_utils.db_executor import MYSQL_ADAPTER
from promts import MYSQL_CONVERTER_PROMPT,MYSQL_CORRECTOR_PROMPT
from queries import Queries
from schemas.function_schemas import MYSQL_MODEL
import pandas as pd
from pandas import DataFrame



class DB_SCHEMA_GENERATOR:
    def __init__(self,selected_team):
        self.mysql_adapter = MYSQL_ADAPTER()
        self.selected_team=selected_team
        print("PRINTING SELF.SELECTED TEAM",self.selected_team)
          
                         
    def __call__(self, database_name="webautomation",user_email="harshithan@quinnox.com"):
        table_schemas = """Table schemas: \n"""
        table_schema="There are 7 services.When a login is sucessfull each user will be a part of team where admin can create multiple teams as per their need and assign the services to that particular team. Admin can also invite the user from the Teams page. Also members can be added from the same page.To create a Team, enter Team Name, Team description, add member to the team."
        
        
        # table_names = self.get_all_table_names(database_name,username)
        # return table_names

        # Fetch and display the content of each table
        # result = {}
        # for table_name in table_names["TABLE_NAME"]:
        #     table_content = self.get_table_content(table_name, database_name,username)
        #     result[table_name] = table_content

        # return result
        
        table_schema = self.mysql_adapter.execute_query(Queries.proj_schema.format(database_name=database_name,user_email=user_email))
        table_schemas +="This is an Web Testing Service here are few key terms to be followed: Project : A project serves as a top-level hierarchy for structuring test suites, modules, scripts, and data which will be specified for its specific teams.Test Suite: A test suite is suite/collection of Test Scripts.Test Suites are a essential way of organising, maintaining test scenarios.Module:Modules are a collection of Test Scripts where each module can have multiple test scripts.Test Step:It can be defined in this case as single unit of a test script.Test Script:It is a collection of the Test Steps,Which are set of actions, validations and verifications that can be performed on the web application to ensure its functionality, performance, and reliability.Test Repository : It is a collection of Test Module, each comprising a collection of individual Test Scripts.Test Lab:The Test Lab serves as a versatile and efficient platform for rapidly creating and executing test suites within a Project. It also facilitates the process of importing test scripts into these suites, thereby enabling the efficient execution of test scripts.Sprints:Here it imports test scripts from both the Test Repository and Test Lab into the Sprints section."+"\n"+ "TABLE NAME : project "+ table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="So,in the above project table:1)Whenever a project is created it will have its team_id linked for which user belongs to.if an user as an subscription plus then it will have service_store_id 1 if not 0.If an project exist then project_status will be 1 if deleted on UI it will be 0."+ "\n"
        
        table_schema = self.mysql_adapter.execute_query(Queries.suite_schema.format(database_name=database_name,user_email=user_email))
        "Test suite is collection of test scripts.Test suite can be created from Sprint or Test Lab which is linked to a project.So there is another way of importing test scripts:i.e from Test repository(Modules) where only test scripts are present it can be imported to test suite in Sprint or Test Lab. "
        table_schemas += "TABLE NAME : test_suite " + table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="A test suite is suite/collection of Test Scripts.Test Suites are a essential way of organising, maintaining test scenarios. They are different from modules as the suite can contain imported scripts from multiple modules. The main use of test suites, however is for batch execution, where each suite containing multiple scripts can be executed at once.So,in the above test_suite table:1)test_suite_status columns indiactes whether the status of the suites (active or inactive),where suites exist it is 1 if deleted on UI will be 0."+ "\n"

        table_schema = self.mysql_adapter.execute_query(Queries.script_schema.format(database_name=database_name,user_email=user_email))
        table_schemas += "TABLE NAME : test_script " + table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="When an project is created ,Test Scripts can be created through test repository also called as modules or can be created with AI.A Test Script is a collection of the Test Steps.So,in the above test_script table: When test scripts are created it will have its unique id created in uuid column, if the test script contains any files or user has uploaded any kind of files the column has_upload_data reflects as 1 otherwise 0, if then scripts are created it can be cloned and cloned scripts will have is_original=0 and if else original scripts will have is_original=1.When the test script goes to execution and verify otp feature is enabled the column is_otp status would be set to 1 otherwise 0.when test_script is created imported from the module into the test_suite then only we can find the reference_script_id in the table.If the user created test_script and deleted then the column test_script_status will be 0 if not will be 1.Whenever the user imports the test_script into the test_Suite the test_scripts will be tagged with its specified test_suite_uuid.When an test_script is executed the test_script_status COLUMN will be set to 1 if not it will be 0.If the test_scripts are created from nova then the column is_ai_generated will be set to 1 otherwise if generated manuallyit will be 0. "+ "\n"

        table_schema = self.mysql_adapter.execute_query(Queries.step_schema.format(database_name=database_name,user_email=user_email))
        table_schemas += "TABLE NAME : test_step " + table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="Test step is a single unit of a test script which consists of many properties the main property being the 'User Action' which specifies user_action column from the table the nature of the action which will be performed on the web page (eg Click, Set, Go to url etc). So,in the above test_step table: Once the test_scripts are created , user can start creating the test_steps and its consecutive numbers will be associated with the step_number column .Each test_steps will contain an unique uuid.If the test_step wants to be executed repeatedly for number of data given by the user then the is_parametrized column will be set to 1 otherwise 0 and if the is_parametrized column is set to 1 then the data_column will be reflected on UI. When an user uploads any kind of file in test_steps the coulmn is_upload will be set to 1 otherwise 0.If the test_step is created and is present will have status as 1 if it is being deleted then it shall have 0.If an step is present in UI then step_status will be 1 otherwise if deleted will be 0"+ "\n"

        table_schema = self.mysql_adapter.execute_query(Queries.exec_schema.format(database_name=database_name,user_email=user_email))
        table_schemas += "TABLE NAME : test_execution " + table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="So,in the above test_execution table: Once all the test_scripts and test_steps are created we can execute the tests(test_execution).Each test_scripts can have many test_executions.The column execution_date refers to on which date the test has being executed.The column execution_time indicates the time taken by the test_script to be executed which depend on the execution_status.There are two runs basically performance and normal run if user opts performance run then is_performance_enabled,is_performance_run columns will have 1 otherwise 0 .Scenarios are basically scripts,when an script is failed the column fail_scenarios will be 1 otherwise 0.Like if an script is passed then column pass_scenarios will be 1 if not 0.Total pass/fail can be calculated in the column total_scenarios by its count.The status of the particular test_execution will be shown as pass or fail in the column status. If the user selects an dry run before execution then is_dry_run will be 1 if not 0.In a module when the dry run is enabled then is_module_run will have 1 else 0.When an test is executed from Test lab then is_test_lab_run will be 1 if not 0."+ "\n"
        
        table_schema = self.mysql_adapter.execute_query(Queries.sprint_schema.format(database_name=database_name,user_email=user_email))
        table_schemas += "TABLE NAME : sprint " + table_schema[['Field', 'Type']].to_csv(index=False) 
        table_schemas +="There wiil be a 'Sprints' section of the project,can associate any test scripts with ongoing sprint which can import test scripts from both the Test Repository and Test Lab into the 'Sprints' section. After importing, they can then arrange these scripts into Test Suites, enabling to conveniently execute the scripts as needed. So,in the above sprint table: This table has an sprint linked with multiple test_suites and each one of the sprint has an unique uuids.The column sprint_active will be enabled only when sprint is started which takes 1 if not 0. If the sprint is completed or not or ongoing can be viewed from the column sprint_execution_status."+"\n"
        
        # table_schema = self.mysql_adapter.execute_query(Queries.team_schema.format(database_name="usermgmt",user_email=user_email))
        # table_schemas += "TABLE NAME : Team " + table_schema.to_csv(index=False) + "\n"
        
        # table_schema = self.mysql_adapter.execute_query(Queries.team_user_schema.format(database_name="usermgmt",user_email=user_email))
        # table_schemas += "TABLE NAME : Team_user " + table_schema[['Field', 'Type']].to_csv(index=False) + "\n"
        
        # table_schema = self.mysql_adapter.execute_query(Queries.normal_user_schema.format(database_name="usermgmt",user_email=user_email))
        # table_schemas += "TABLE NAME : Normal_user " + table_schema[['Field', 'Type']].to_csv(index=False) + "\n"
        
        # table_schema= self.mysql_adapter.execute_query(Queries.team_schema.format(user_email=user_email))
        # table_schema+="User teamsssss"+table_schema.to_csv(index=False)+"\n"
        user_result=self.mysql_adapter.execute_query(Queries.teams_id_schema.format(user_email="vatsals@quinnox.com",team_name=self.selected_team))
        uuid_array = user_result['uuid'].tolist()
        print(uuid_array)
        with open("teamid_schema.txt","w") as fb:
            user_result[['uuid']].to_csv(fb, index=False) 
        sql_gen=self.mysql_adapter.execute_query(Queries.find_teamid_query.format(database_name=database_name, team_ids=', '.join(["'{}'".format(tid) for tid in uuid_array])))
        # print("MY DREAMMMM:",sql_gen)
        projectid_array=sql_gen['uuid'].tolist()
        with open("projectid_list.txt","w") as ab:
            sql_gen[['uuid']].to_csv(ab,index=False)
        suite_query=self.mysql_adapter.execute_query(Queries.find_testsuite_id_query.format(database_name=database_name, project_ids=', '.join(["'{}'".format(pid) for pid in projectid_array])))
        test_Suite_ids=suite_query['uuid'].tolist()
        with open("suite_id_list.txt","w") as ab:
            suite_query[['uuid']].to_csv(ab,index=False)
        

        db_schema = "Relations: \n"
        db_relations = self.mysql_adapter.execute_query(Queries.schema1.format(database_name=database_name))
        db_schema+= db_relations.to_csv(index=False)

        table_schemas += db_schema
        # print("\033[45m tABLE schemaaa last \033[0m",table_schemas)
        with open("tables_schema.txt","w") as fb:
            fb.write(table_schemas)
        return table_schemas,projectid_array,test_Suite_ids
    

class SQL_CONVERTER:
    def __init__(self) -> None:
        self.function_call = FunctionCall()
        self.completion = Completion()
        self.mysql_adapter = MYSQL_ADAPTER()

    def __get_user_prompt__(self, user_description, db_schema,project_uuid,suite_uuid):
        return MYSQL_CONVERTER_PROMPT.user_prompt.format(user_description=user_description, db_schema=db_schema,project_uuid=project_uuid,suite_uuid=suite_uuid)

        
    def __call__(self, user_description, db_schema,project_uuid,suite_uuid, database_name="webautomation"):
        

        messages = [{
            "role": "system",
            "content": MYSQL_CONVERTER_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": self.__get_user_prompt__(user_description, db_schema,project_uuid,suite_uuid)
        }]
        
        print("\033[46m Messages in SQL CONVERTER \033[0m",messages)


        functions = [{
            "name": "execute_mysql_command",
            "description":
            """This executes mysql commands.
                """,
            "parameters": MYSQL_MODEL.schema()
        }]
        

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        return args

class CorrectQuery:
    def __init__(self) -> None:
        self.function_call = FunctionCall()
        self.completion = Completion()
        self.mysql_adapter = MYSQL_ADAPTER()


    def __call__(self, query, error, db_schema, database_name="webautomation"):
        
        
        print("CORRECTING QUERY")
        messages = [{
            "role": "system",
            "content": MYSQL_CORRECTOR_PROMPT.system_prompt
        }, {
            "role": "user",
            "content": MYSQL_CORRECTOR_PROMPT.user_prompt.format(query=query, error=error, db_schema=db_schema)
        }]


        functions = [{
            "name": "execute_mysql_command",
            "description":
            """This executes mysql commands.
                """,
            "parameters": MYSQL_MODEL.schema()
        }]

        _, args = self.function_call(messages=messages, model_name="gpt-4-32k", functions=functions)
        return args
    