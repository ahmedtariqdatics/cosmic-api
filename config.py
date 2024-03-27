import os
import urllib.parse
from dotenv import load_dotenv

class ProductionConfig():
    load_dotenv(override=True)
    server = os.environ["SERVER_URL"]
    database = os.environ["DATABASE_NAME"]
    username = os.environ["DATABASE_USERNAME"]
    password = os.environ["DATABASE_PASSWORD"]
    conn = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';ENCRYPT=yes;UID=' + username + ';PWD=' + password)
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % conn
    SQLALCHEMY_TRACK_MODIFICATIONS = False
