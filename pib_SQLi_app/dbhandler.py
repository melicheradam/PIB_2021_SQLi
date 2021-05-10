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


def homepage_unprotected(request):
    username = request.GET.get('username', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    gender = request.GET.get('gender', '')
    order = request.GET.get('order', '')
    limit = request.GET.get('limit', '')
    sw = False
    query = "SELECT row_number() OVER () as number, username, first_name, last_name, gender FROM user_details"

    if username != "" or first_name != "" or last_name != "" or gender != "":
        query += " WHERE "

    if username != "":
        sw = True
        query += " username='" + username + "' "

    if first_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " first_name='" + first_name + "' "

    if last_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " last_name='" + last_name + "' "

    if gender != "":
        if sw:
            query += " OR "
        query += " gender='" + gender + "' "

    if order in ['number', 'username', 'first_name', 'last_name', 'gender']:
        query += " ORDER BY " + order

    try:
        int(limit)
        query += " LIMIT " + limit
    except ValueError:
        pass

    data = execute_db(query, [])
    return data


def homepage_prepared_all(request):
    username = request.GET.get('username', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    gender = request.GET.get('gender', '')
    order = request.GET.get('order', '')
    limit = request.GET.get('limit', '')
    sw = False
    params = []
    query = "SELECT row_number() OVER () as number, username, first_name, last_name, gender FROM user_details"

    if username != "" or first_name != "" or last_name != "" or gender != "":
        query += " WHERE "

    if username != "":
        sw = True
        query += " username=%s "
        params.append(username)

    if first_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " first_name=%s "
        params.append(first_name)

    if last_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " last_name=%s "
        params.append(last_name)

    if gender != "":
        if sw:
            query += " OR "
        query += " gender=%s "
        params.append(gender)

    if order != "":
        query += " ORDER BY %s "
        params.append(order)

    if limit != "":
        query += " LIMIT %s "
        params.append(limit)

    data = execute_db(query, params)
    return data


def homepage_prepared_some(request):
    username = request.GET.get('username', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')
    gender = request.GET.get('gender', '')
    order = request.GET.get('order', '')
    limit = request.GET.get('limit', '')
    sw = False
    params = []
    query = "SELECT row_number() OVER () as number, username, first_name, last_name, gender FROM user_details"

    if username != "" or first_name != "" or last_name != "" or gender != "":
        query += " WHERE "

    if username != "":
        sw = True
        query += " username=%s "
        params.append(username)

    if first_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " first_name=%s "
        params.append(first_name)

    if last_name != "":
        if sw:
            query += " OR "
        sw = True
        query += " last_name=%s "
        params.append(last_name)

    if gender != "":
        if sw:
            query += " OR "
        query += " gender=%s "
        params.append(gender)

    if order in ['number', 'username', 'first_name', 'last_name', 'gender']:
        query += " ORDER BY " + order

    try:
        int(limit)
        query += " LIMIT " + limit
    except ValueError:
        pass

    data = execute_db(query, params)
    return data


def execute_db(query, params):
    hostname = os.environ['DBHOST']

    name = "pib_tables"
    host = hostname
    user = os.environ['DBUSER']
    pw = os.environ['DBPASS']
    sslmode = "allow"

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


def execute_db_selector(query, params):
    hostname = os.environ['DBHOST']

    name = "pib_tables"
    host = hostname
    user = "selector"
    pw = "selector"
    sslmode = "allow"

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
