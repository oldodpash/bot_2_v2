import sqlite3
import json


def change_user_param_in_db(telegram_id, param, param_name):
    sqlite_connection = sqlite3.connect('telegram_bot_2.db')
    cursor = sqlite_connection.cursor()
    sql_update_query = f"""Update table_users set {param_name} = '{param}' where telegram_id = '{telegram_id}'"""
    cursor.execute(sql_update_query)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def read_records_from_db(telegram_id):
    sqlite_connection = sqlite3.connect('telegram_bot_2.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = """SELECT * from table_users"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    lang, hash_info, trans, wallet = '', '', '', ''
    for row in records:
        if str(telegram_id) == row[0]:
            lang, hash_info, trans, wallet = row[1], row[2], row[3], row[4]
    cursor.close()
    sqlite_connection.close()
    return lang, hash_info, trans, wallet


def registration_user_in_db(telegram_id, language):
    a, b, _, _ = read_records_from_db(telegram_id)
    if a == '' and b == '':
        sqlite_connection = sqlite3.connect('telegram_bot_2.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = f"""INSERT INTO table_users (telegram_id, user_language, hash, last_trans, last_wallet) VALUES ('{telegram_id}', '{language}', 'None', 'None', 'None');"""
        count = cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
    else:
        change_user_param_in_db(telegram_id, language, 'user_language')


def add_record_to_db(telegram_id, transaction_id, wallet):
    sqlite_connection = sqlite3.connect('telegram_bot_2.db')
    cursor = sqlite_connection.cursor()
    sqlite_insert_query = f"""INSERT OR REPLACE INTO table_transactions (telegram_id, transaction_id, wallet) VALUES ('{telegram_id}', '{transaction_id}', '{wallet}');"""
    count = cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()
    cursor.close()
    sqlite_connection.close()


def parse_txt_file(filename):
    return json.loads(open(filename, mode='r', encoding='UTF-8').read())


def get_lang(message, data):
    db_lang, _, _, _ = read_records_from_db(message)
    if db_lang == '':
        return 'None'
    idx = -1
    for i in data['lang']:
        idx += 1
        if i == db_lang:
            break
    return idx
