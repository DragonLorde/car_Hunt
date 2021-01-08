import pymysql
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, CREDIT_SOFT_LIMIT, CREDIT_LIMIT
import datetime
import time


def create_connection():
    connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_NAME)
    return connection

def get_all_info():
    con = create_connection()
    with con.cursor() as cur:
        status = cur.execute('select * from users')
        if status == 0:
            print('base empty')
        else:
            res = cur.fetchall()
            for i in res:
                print(i)

def push_user(tgID, firstName, userName, lastName, phoneNumber):
    print(read_user_by_id(tgID))
    if read_user_by_id(tgID):
        return 0
    else:
        if write_user(tgID, firstName, userName, lastName, phoneNumber):
            return 1
        else:
            return 2

def read_user_by_id(tgid):
    con = create_connection()
    with con.cursor() as cur:
        status = cur.execute(f'select * from users where telegram_id = {tgid}')
        if status == 0:
            cur.close()
            con.close()
            return False
        else:
            res = cur.fetchone()
            cur.close()
            con.close()
            return res
            # 0 = tgid
            # 1 = first_name
            # 2 = username
            # 3 = last_name
            # 4 = phone_number
            # 5 = sub
            # 6 = last_call

def write_user(tgID, firstName, userName, lastName, phoneNumber):
    try:
        con = create_connection()
        with con.cursor() as cur:
            query = f"insert into users (telegram_id, first_name, username, last_name, phone_number, sub, last_call) values ('{tgID}', '{firstName}', '{userName}', '{lastName}', '{phoneNumber}', false, NOW());"
            print(query)
            status = cur.execute(query)
            con.commit()
        res = True
    except pymysql.err.Error:
        res = False
    finally:
        cur.close()
        con.close()
    return res

def update_time_user(tgID):
    try:
        con = create_connection()
        with con.cursor() as cur:
            query = f'SELECT * FROM users WHERE telegram_id = {tgID}'
            status = cur.execute(query)
            if status == 0:
                return 0
            else:
                res = cur.fetchone()
                if res[5]:
                    print('подпыска')
                else:
                    lastCall = res[6]
                    time = (datetime.datetime.now().timestamp() - res[6].timestamp()) / 60
                    if time > 45:
                        return True
                    else:
                        return round(45 - time)
    except pymysql.err.Error:
        return False
    finally:
        cur.close()
        con.close()



#write_user('425339450', 'Battle_in', 'evan_battle_in', 'None', '+79199371764')