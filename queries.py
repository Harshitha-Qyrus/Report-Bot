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
    
    teams_schema= """SELECT* FROM usermgmt.team WHERE id IN (SELECT team_id FROM usermgmt.team_user 
    WHERE user_id IN (SELECT id FROM usermgmt.normal_user WHERE login = "{user_email}")) """
     
    teams_id_schema= """SELECT* FROM usermgmt.team WHERE id IN (SELECT team_id FROM usermgmt.team_user 
    WHERE user_id IN (SELECT id FROM usermgmt.normal_user WHERE login = "{user_email}" AND team_name = "{team_name}")) """
    
    joining_tables= """SELECT ts.uuid, ts.test_script_name 
    FROM webautomation.test_script AS ts
    JOIN webautomation.test_suite AS tss ON ts.test_suite_uuid = tss.uuid
    WHERE tss.project_uuid = '9bad3a17889d04' AND test_script_status = '1';"""

    find_teamid_query = """SELECT * FROM {database_name}.project WHERE team_id IN ({team_ids});"""  
    find_testsuite_id_query="""SELECT * FROM {database_name}.test_suite WHERE project_uuid IN ({project_ids});""" 
    
    
    
    #Query to get specified columns in specified tables
    select_all_from_table = """SELECT * FROM {database_name}.{table_name};"""
    # Query to get all Table names in a database
    get_all_table_names = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
                            WHERE TABLE_SCHEMA = '{database_name}' AND TABLE_TYPE = 'BASE TABLE';"""
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
                            




