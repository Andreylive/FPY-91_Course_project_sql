import psycopg2


def create_db(cur):
    # Функция для создания структуры базы данных и отладки

    # Запрос для тестирования, чтобы не создавать новые элементы
    cur.execute("""
                DROP TABLE phones, clients;
                """)

    # Запрос на создание таблицы Clients
    cur.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                client_id SERIAL PRIMARY KEY,
                client_name VARCHAR(80) UNIQUE NOT NULL,
                client_surname VARCHAR(80) UNIQUE NOT NULL,
                client_email VARCHAR(80) UNIQUE NOT NULL
                );
                """)

    # Запрос на создание таблицы Phones
    cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                phone_id SERIAL PRIMARY KEY,
                phone_number VARCHAR(80) UNIQUE,
                client_id INTEGER NOT NULL REFERENCES clients(client_id)
                );
                """)
    conn.commit()


def add_client(cur, first_name, last_name, email, phone=None):
    # Функция для добавления нового клиента

    # Запрос на добавление основной информации о клиенте в таблицу Clients
    cur.execute("""
                INSERT INTO clients(client_name, client_surname, client_email)
                VALUES(%s, %s, %s) RETURNING client_id;
                """, (first_name, last_name, email))
    client_id = cur.fetchone()[0]
    conn.commit()

    # Запрос на добавление телефона клиента в таблицу Phones
    cur.execute("""
                INSERT INTO phones(client_id, phone_number)
                VALUES(%s, %s);""", (client_id, phone))
    conn.commit()


def add_phone(cur, client_id, phone):
    # Функция для добавления телефона к существующему клиенту
    cur.execute("""
                INSERT INTO phones(client_id, phone_number)
                VALUES(%s, %s);
                """, (client_id, phone))
    conn.commit()


def change_client(cur,
                  client_id,
                  client_name=None,
                  client_surname=None,
                  client_email=None,
                  old_phone=None,
                  new_phone=None
                  ):
    # Функция для изменения информации о существующем клиента
    if client_name is not None:
        cur.execute("""
                    UPDATE clients
                    SET client_name = %s
                    WHERE client_id = %s;
                    """, (client_name, client_id))

    if client_surname is not None:
        cur.execute("""
                    UPDATE clients
                    SET client_surname = %s
                    WHERE client_id = %s;
                    """, (client_surname, client_id))

    if client_email is not None:
        cur.execute("""
                    UPDATE clients
                    SET client_email = %s
                    WHERE client_id = %s;
                    """, (client_email, client_id))

    if old_phone is not None:
        cur.execute("""
                    UPDATE phones
                    SET phone_number = %s
                    WHERE client_id = %s and phone_number = %s;
                    """, (new_phone, client_id, old_phone))


def delete_phone(cur, client_id, phone_number):
    # Функция для удаления телефона существующего клиента
    cur.execute("""
                DELETE FROM phones
                WHERE client_id=%s AND phone_number=%s;
                """, (client_id, phone_number))
    conn.commit()


def delete_client(cur, client_id):
    # Функция для удаления существующего клиента
    # Удаляем сначала связанные с клиентом телефоны
    cur.execute("""
                DELETE FROM phones
                WHERE client_id=%s;
                """, (client_id,))
    # Удаляем самого клиента
    cur.execute("""
                DELETE FROM clients
                WHERE client_id=%s;
                """, (client_id,))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    # Функция поиска клиента по его данным
    if first_name is None and last_name is None and email is None:
        cur.execute("""
                    SELECT clients.client_id,
                            clients.client_name,
                            clients.client_surname,
                            clients.client_email
                    FROM phones
                    LEFT JOIN clients ON phones.client_id = clients.client_id
                    WHERE phone_number LIKE %s;
                    """, (phone,))
        client_info = cur.fetchall()[0]
        print(f'Основная информация о клиенте:\n'
              f'  id клиента: {client_info[0]}\n'
              f'  Имя: {client_info[1]}\n'
              f'  Фамилия: {client_info[2]}\n'
              f'  Электронная почта: {client_info[3]}')

        id_info = client_info[0]
        cur.execute("""
                    SELECT phone_number
                    FROM phones
                    WHERE client_id=%s;
                    """, (id_info,))
        phone_info = cur.fetchall()
        count = 0
        for i in phone_info:
            count += 1
            print(f'  Телефон {count}: {i[0]}')

    else:
        cur.execute("""
                    SELECT *
                    FROM clients
                    WHERE client_name LIKE %s
                        AND client_surname LIKE %s
                        AND client_email LIKE %s;
                    """, (first_name, last_name, email))
        client_info = cur.fetchall()[0]

        print(f'Основная информация о клиенте:\n'
              f'  id клиента: {client_info[0]}\n'
              f'  Имя: {client_info[1]}\n'
              f'  Фамилия: {client_info[2]}\n'
              f'  Электронная почта: {client_info[3]}')

        id_info = client_info[0]
        cur.execute("""
                    SELECT phone_number
                    FROM phones
                    WHERE client_id=%s;
                    """, (id_info,))
        phone_info = cur.fetchall()
        count = 0
        for i in phone_info:
            count += 1
            print(f'  Телефон {count}: {i[0]}')


# Проверка функций на данных
if __name__ == "__main__":
    with psycopg2.connect(database="clients", user="postgres") as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Andrei',
                            'Pshenichnyi',
                            'andrey.pshenichniy@gmail.com',
                            '+79855743133')
            add_client(cur, 'Yana',
                            'Pshenichnaia',
                            'osipenko.yana@gmail.com',
                            '+79831785314')
            add_client(cur, 'Viktor',
                            'Ivanov',
                            'ivanov.viktor@gmail.com',
                            '+79249003333')
            add_phone(cur, '1', '+79996783133')
            add_phone(cur, '1', '+79248882121')
            add_phone(cur, '3', '+78882223131')
            change_client(cur, '1',
                               'Andrei',
                               'Pshenichnyi',
                               'andrey.pshenichniy@gmail.com',
                               '+79855743133',
                               '+79998882190')
            delete_phone(cur, '1', '+79998882190')
            delete_client(cur, '1')
            find_client(cur, None, None, None, '+79249003333')
            find_client(cur, 'Viktor',
                             'Ivanov',
                             'ivanov.viktor@gmail.com',
                             '+79249003333')
    conn.close()
