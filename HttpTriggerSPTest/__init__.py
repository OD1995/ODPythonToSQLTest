import logging
import azure.functions as func
import pyodbc


def get_connection_string():
    username = 'matt.shepherd'
    password = "4rsenal!PG01"
    driver = '{ODBC Driver 17 for SQL Server}'
    # driver = 'SQL Server Native Client 11.0'
    server = "fse-inf-live-uk.database.windows.net"
    database = 'AzureCognitive'
    ## Create connection string
    connectionString = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    
    return connectionString


def execute_sql_command(
    sp_string,
    sp_values
):
    connectionString = get_connection_string()
    print(connectionString)
    ## Connect to SQL server
    cursor = pyodbc.connect(connectionString).cursor()
    ## Execute command
    cursor.execute(sp_string, sp_values)
    ## Get returned values
    rc = cursor.fetchval()
    cursor.commit()

    return rc




def main(req: func.HttpRequest) -> func.HttpResponse:
    sp_string = """
    DECLARE	@return_value int

    EXEC	@return_value = [dbo].[spComputerVisionCloudProcessing_AddImages]
            @Sport = ?,
            @Event = ?,
            @Filename = ?

    SELECT	'Return Value' = @return_value
    """
    sp_values = (
                    "testing",
                    "MUFC_AFCB_Highlights",
                    '00002.jpeg'
                )

    od1 = execute_sql_command(
            sp_string=sp_string,
            sp_values=sp_values)

    return func.HttpResponse(od1)