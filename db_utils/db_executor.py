from config import DB_CONFIG
import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from config import DB_CONFIG
import sqlfluff

class MYSQL_ADAPTER:
    
    def execute_query(self, query):
        # print("\033[41m QUERYYYYYYY \033[0m",query)
        with SSHTunnelForwarder((DB_CONFIG.SSH_HOST, 22), ssh_pkey=DB_CONFIG.SSH_PKEY_FILE, ssh_username=DB_CONFIG.SSH_UNAME,
            remote_bind_address=(DB_CONFIG.DB_HOST, 3306))  as tunnel:

            conn = pymysql.connect(host='127.0.0.1', user=DB_CONFIG.DB_UNAME, passwd=DB_CONFIG.DB_PASS, port=tunnel.local_bind_port, db='webautomation')
            data = pd.read_sql_query(query, conn)
            # print("\033[41m MYSQL ADAPTER DATA \033[0m",data)
            return data

    def __lint_sql_command__(self, query):
    
        # Lint the SQL string
        lint_result = sqlfluff.lint_string(query)

        if len(lint_result) > 0:
            for violation in lint_result.get_violations():
                print(f"Line {violation.line_no()}, Position {violation.line_pos()}: {violation.description()}")
            return False
        return True

if __name__ == "__main__":

    GET_SUITES = """
    SELECT test_suite.uuid as test_suite_uuid, test_suite.test_suite_name as test_suite_name, test_suite.description as test_suite_description, count(test_script.uuid) as num_testscripts
    FROM test_suite
    JOIN test_script ON test_suite.uuid = test_script.test_suite_uuid
    where test_suite.test_suite_status=1 and test_script.test_script_status=1
    group by test_suite.uuid;
    """
    mysql_adapter = MYSQL_ADAPTER()
    mysql_adapter.execute_query(GET_SUITES)

