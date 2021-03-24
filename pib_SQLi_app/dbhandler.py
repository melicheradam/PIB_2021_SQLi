import psycopg2
import os
from django.conf import settings


def reload_db():
    fd = open(os.path.join(settings.BASE_DIR, 'db_reload.sql'), 'r')
    #fd = open(os.path.join(settings.BASE_DIR, 'sample_table.sql'), 'r')
    sqlfile = fd.read()
    fd.close()
    print("Reloading DB table to previous state")
    # all SQL commands (split on ';')
    sqlcommands = sqlfile.split(';')
    for command in sqlcommands:
        print(command)
        try:
            execute_db(command, [])
        except Exception as msg:
            print("Command skipped: ", msg)


def execute_db(query, params):
    hostname = os.environ['DBHOST']

    name = "pib_tables"
    host = hostname + ".postgres.database.azure.com"
    user = os.environ['DBUSER'] + "@" + hostname
    pw = os.environ['DBPASS']
    sslmode = "require"

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, name, pw, sslmode)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(query, params)

    if cursor.description is not None:
        returnval = cursor.fetchall()
    else:
        returnval = [[cursor.rowcount]]

    cursor.close()
    conn.close()

    return returnval
