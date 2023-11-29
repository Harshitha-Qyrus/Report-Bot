class Queries:
    schema1 = """SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME  
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_SCHEMA = '{database_name}' AND REFERENCED_TABLE_NAME IS NOT NULL;"""

    script_schema = """DESCRIBE {database_name}.test_script"""
    suite_schema = """DESCRIBE {database_name}.test_suite"""
    exec_schema = """DESCRIBE {database_name}.test_execution"""
    proj_schema = """DESCRIBE {database_name}.project"""
    step_schema = """DESCRIBE {database_name}.test_step"""
    sprint_schema = """DESCRIBE {database_name}.sprint"""
    
    # Usermgmt
    team_schema="""DESCRIBE {database_name}.team"""
    team_user_schema="""DESCRIBE {database_name}.team_user"""
    normal_user_schema="""DESCRIBE {database_name}.normal_user"""
    
    
    #Query to get specified columns in specified tables
    select_all_from_table = """SELECT * FROM {database_name}.{table_name};"""
    # Query to get all Table names in a database
    get_all_table_names = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                            WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_TYPE = 'BASE TABLE';"""



