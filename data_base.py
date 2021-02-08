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

def write_fssp(messageID, userID, firstName, lastName, json, patronymic = ''):
    con = create_connection()
    with con.cursor() as cur:
        cur.execute(f"insert into fssp (message_id, user_id, first_name, last_name, patrinomic, json) values ({messageID}, {userID}, '{firstName}', '{lastName}', '{patronymic}','{json}');")
        con.commit()
        cur.close()
        con.close()

def read_fssp(messageId, userId):
    con = create_connection()
    with con.cursor() as cur:
        status = cur.execute(f'select * from fssp where (message_id = {messageId} and user_id = {userId});')
        if status == 0:
            cur.close()
            con.close()
            return False
        else:
            res = cur.fetchone()
            cur.close()
            con.close()
            return res


def read_reports_by_reg_number(regNumber):
    con = create_connection()
    with con.cursor() as cur:
        status = cur.execute(f"select url, date_generation from cars_reports where reg_number = '{regNumber}';")
        if status == 0:
            cur.close()
            con.close()
            return False
        else:
            res = cur.fetchall()
            cur.close()
            con.close()
            return res

def read_reports_by_vin(vin):
    con = create_connection()
    with con.cursor() as cur:
        status = cur.execute(f"select url, date_generation from cars_reports where vin = '{vin}';")
        if status == 0:
            cur.close()
            con.close()
            return False
        else:
            res = cur.fetchall()
            cur.close()
            con.close()
            return res

def write_report(vin, regNumber, bodyNumber, url, photo, easito, gibbd, rsa, taxi, reestr):
    con = create_connection()
    with con.cursor() as cur:
        query = "insert into cars_reports" \
                "(vin, reg_number, body_number, url, photo, date_generation, easito, gibbd, rsa, taxi, reestr)" \
                f" values (@{vin}@, @{regNumber}@, @{bodyNumber}@, @{url}@, @{photo}@, NOW(), @{easito}@, @{gibbd}@, @{rsa}@, @{taxi}@, @{reestr}@);".replace("'", "''").replace('@', "'")
        print(query)
        a = cur.execute(query)
        con.commit()
        print(a)

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
            # 7 = credit

def write_user(tgID, firstName, userName, lastName, phoneNumber):
    try:
        con = create_connection()
        with con.cursor() as cur:
            query = f"insert into users (telegram_id, first_name, username, last_name, phone_number, sub, last_call, credit)" \
                    f" values ('{tgID}', '{firstName}', '{userName}', '{lastName}', '{phoneNumber}', false, '2011-11-11', 0);"
            status = cur.execute(query)
            con.commit()
        res = True
    except pymysql.err.Error:
        res = False
    finally:
        cur.close()
        con.close()
    return res

def client_use(tgID):
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
                        cur.execute(f'update users set last_call = NOW() where telegram_id = {tgID};')
                        con.commit()
                        return True
                    else:
                        return round(45 - time)
    except pymysql.err.Error:
        return False
    finally:
        cur.close()
        con.close()



#write_user('425339450', 'Battle_in', 'evan_battle_in', 'None', '+79199371764')
# read_dssp(123,321)