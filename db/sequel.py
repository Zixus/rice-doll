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


class Avatar(Database):
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
