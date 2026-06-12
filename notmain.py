import psycopg2

class ClientDB:
    # Функция, создающая структуру БД (таблицы).
        def create_tables(cur):
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                surname VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL,
                phone VARCHAR(40) NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(id),
                phone VARCHAR(40) NOT NULL
            );
            """)

        # Функция, позволяющая добавить нового клиента.
        def add_client(cur, name, surname, email, phone):
            cur.execute("""
            INSERT INTO clients(name, surname, email, phone) VALUES(%s, %s, %s, %s) RETURNING id;
            """, (name, surname, email, phone))
            return cur.fetchone()[0]

        # Функция, позволяющая добавить телефон для существующего клиента.
        def add_phone(cur, client_id, phone):
            cur.execute("""INSERT INTO phones(client_id, phone) VALUES(%s, %s); """, (client_id, phone))

        # Функция, позволяющая изменить данные о клиенте.
        def update_client(cur, client_id, name=None, surname=None, email=None, phone=None):
            fields = {"name": name, "surname": surname, "email": email, "phone": phone}
            items = [(f"{field}=%s", value) for field, value in fields.items() if value is not None]
            if not items: return; conditions, params = list(zip(*items))
            query = f"UPDATE clients SET {", ".join(conditions)} HERE id=%s"
            params.append(client_id); cur.execute(query, params)


        # Функция, позволяющая удалить телефон для существующего клиента.
        def delete_phone(cur, client_id, phone):
            cur.execute("""
            DELETE FROM phones WHERE client_id=%s AND phone=%s;
            """, (client_id, phone))
            conn.commit()

        # Функция, позволяющая удалить существующего клиента.
        def delete_client(cur, client_id):
            cur.execute("""DELETE FROM clients WHERE id=%s; """, (client_id,))
            conn.commit()


        def find_client(cur, name=None, surname=None, email=None, phone=None):
            fields = {"name": name, "surname": surname, "email": email, "phone": phone}
            items = [(value, f"{field}=%s") for field, value in fields.items() if value is not None]
            if not items: return []; conditions, params = zip(*items)
            query = f"SELECT * FROM clients WHERE {' AND '.join(conditions)};"            
            cur.execute(query, params); return cur.fetchall()


if __name__ == "__main__":
    db = ClientDB()
    with psycopg2.connect(database="netology_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            db.create_tables(cur)
            client_id = db.add_client(cur, "Ivan", "Petrov", "ivan@mail.ru", "+79990000000")
            db.update_client(cur, client_id, email="new@mail.ru")
