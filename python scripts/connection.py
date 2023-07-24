# connecting to SQL server
import pymysql
import pandas as pd


def sql_con():
    # connect to db
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Gamer0077Dark!',
        database='airbnb'
    )

    # read into pandas dataframe
    sql_query = pd.read_sql(
        """
        SELECT * FROM ab_nyc_2019
        """,
        con=connection
    )
    pd.set_option("display.max_columns", None)

    connection.close()
    return sql_query

