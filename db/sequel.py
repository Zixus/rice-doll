import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv('.env')
DUMP_CHANNEL = int(os.getenv('DUMP_CHANNEL'))
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASS = os.getenv('MYSQL_PASS')
MYSQL_DB = os.getenv('MYSQL_DB')


class Database:
    def __init__(self) -> None:
        self.connect()

    def connect(self) -> None:
        self.connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB
        )
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()


class AvatarDB(Database):
    def get_avatar_after(self, avatar_before_url: str) -> str:
        select_query = "SELECT avatar_after FROM avatars WHERE avatar_before = %s"
        tuple_avatar_before_url = (avatar_before_url,)
        self.cursor.execute(select_query, tuple_avatar_before_url)
        return self.cursor.fetchone()

    def insert_avatar(self, avatar_bafore_url, avatar_after_url) -> None:
        insert_query = "INSERT INTO avatars (avatar_before, avatar_after) VALUES (%s, %s)"
        avatar_insert = (avatar_bafore_url, avatar_after_url)
        self.cursor.execute(insert_query, avatar_insert)
        self.connection.commit()


class AliasDB(Database):
    def select_user_alias(self, user_id: str) -> tuple:
        select_query = "SELECT name FROM user_alias WHERE user_id = %s ORDER BY name ASC"
        tuple_user_id = (user_id,)
        self.cursor.execute(select_query, tuple_user_id)
        return self.cursor.fetchall()

    def get_user_command(self, name: str, user_id: str) -> str:
        select_query = "SELECT command FROM user_alias WHERE name = %s AND user_id = %s"
        get_command_tuple = (name, user_id)
        self.cursor.execute(select_query, get_command_tuple)
        return self.cursor.fetchone()

    def upsert_user_alias(self, name: str, user_id: str, command: str) -> None:
        insert_query = """
            INSERT INTO user_alias (name, command, user_id) VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE command=%s;
        """
        alias_insert = (name, command, user_id, command)
        self.cursor.execute(insert_query, alias_insert)
        self.connection.commit()

    def delete_user_alias(self, name: str, user_id: str) -> None:
        delete_query = "DELETE FROM user_alias WHERE name = %s AND user_id = %s"
        alias_delete = (name, user_id)
        self.cursor.execute(delete_query, alias_delete)
        self.connection.commit()

    def select_server_alias(self, server_id: str) -> tuple:
        select_query = "SELECT name FROM server_alias WHERE server_id = %s ORDER BY name ASC"
        tuple_server_id = (server_id,)
        self.cursor.execute(select_query, tuple_server_id)
        return self.cursor.fetchall()

    def get_server_command(self, name: str, server_id: str) -> str:
        select_query = "SELECT command FROM server_alias WHERE name = %s AND server_id = %s"
        get_command_tuple = (name, server_id)
        self.cursor.execute(select_query, get_command_tuple)
        return self.cursor.fetchone()

    def upsert_server_alias(self, name: str, server_id: str, command: str) -> None:
        insert_query = """
            INSERT INTO server_alias (name, command, server_id) VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE command=%s;
        """
        alias_insert = (name, command, server_id, command)
        self.cursor.execute(insert_query, alias_insert)
        self.connection.commit()

    def delete_server_alias(self, name: str, server_id: str) -> None:
        delete_query = "DELETE FROM server_alias WHERE name = %s AND server_id = %s"
        alias_delete = (name, server_id)
        self.cursor.execute(delete_query, alias_delete)
        self.connection.commit()
