import pymysql
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
import datetime

class database:
    con = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )



    def insert_client(self, tgID, firsName, lastName, phoneNumber):
        con = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
        )
        if self.about_client(tgID):
            print('tttttttt')
            return False
        else:
            print('hhhhhhhh')
            try:
                cur = con.cursor()
                cur.execute(f"insert into users (telegram_id, first_name, last_name, phone_number, sub, last_call)"
                            f" values ({tgID}, '{firsName}', '{lastName}', '{phoneNumber}', false, DATE '1999-1-1');")
                con.commit()
                return True
            except pymysql.err.Error:
                return True
            finally:
                con.close()


    def upd_time(self, tgID):
        con = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )

        try:
            print(f'update users set last_call = NOW() where telegram_id = {tgID}')
            cur = con.cursor()
            cur.execute(f'update users set last_call = NOW() where telegram_id = {tgID};')
            con.commit()
        except pymysql.err.Error:
            return True
        finally:
            con.close()


    def about_client(self, tgID):
        con = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )

        try:
            cur = con.cursor()
            res = cur.execute(f'SELECT * FROM users WHERE telegram_id = {tgID}')
            if res == 0:
                return False
            elif res == 1:
                return cur.fetchone()
        except pymysql.err.Error:
            return False
        finally:
            con.close()

    def about_client_subs(self, tgID):
        con = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )

        try:
            cur = con.cursor()
            status = cur.execute(f"SELECT * FROM users WHERE telegram_id = {tgID}")
            res = cur.fetchone()
            print(res)
            if res[4]:
                return True
            else:
                time = (datetime.datetime.now().timestamp() - res[5].timestamp()) / 60
                if time > 45:
                    return True
                else:
                    return round(45 - time)
        except pymysql.err.Error:
            return 0
        finally:
            con.close()

    def write_car_bygosnom(vin, gosnom, easito, ):
        con = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME
        )
        # +-----------------+-------------+------+-----+---------+-------+
        # | Field | Type | Null | Key | Default | Extra |
        # +-----------------+-------------+------+-----+---------+-------+
        # | vin | char(17) | YES | | NULL | |
        # | gosnom | char(9) | YES | | NULL | |
        # | body_number | varchar(40) | YES | | NULL | |
        # | photo | text | YES | | NULL | |
        # | url | text | YES | | NULL | |
        # | date_generation | date | YES | | NULL | |
        # | easito | text | YES | | NULL | |
        # | gibbd | text | YES | | NULL | |
        # | rsa | text | YES | | NULL | |
        # | taxi | text | YES | | NULL | |
        # | reestr | text | YES | | NULL | |
        try:
            cur = con.cursor()
            cur.execute('INSERT INTO cars (vin, gosnom)')
        except pymysql.err.Error:
            print('fuckd')
        finally:
            con.close()



#print(database().about_client_subs('425339450'))