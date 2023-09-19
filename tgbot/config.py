from dataclasses import dataclass
from typing import Optional

from environs import Env

import sqlite3

paths_dict_rev = {
    "New to Arabic": "01",
    "Understand Arabic": "02",
    "10 Days Challenge": "0101",
    "Reading Fluency": "0102",
    "The Basics": "0201",
    "The Basics and Beyond": "0202",
    "Unit 1": "020101",
    "Unit 2": "020102",
    "Unit 3": "020103",
    "Unit 4": "020104",
    "Unit 5": "020105",
    "Unit 6": "020106",
    "Unit 7": "020107",
    "Unit 8": "020108",
    "Unit 9": "020109",
    "Unit 10": "020110",
    "Unit 11": "020111",
    "Unit 12": "020112",
    "Unit 13": "020113",
    "Unit 14": "020114",
    "Unit 15": "020115",
    "Dream": "020201",
    "Reading The Classics": "020202",
    "Basic Nahw": "02020101",
    "Basic Sarf": "02020102",
    "Advanced Sarf": "02020103",
    "Advanced Nahw & Structures": "02020104",
    "Balagha": "02020105",
    "Baqarah Beyond Translation": "02020106",
    "Dream BIG 2023": "02020107"
}
paths_dict = {
    "01": "New to Arabic",
    "02": "Understand Arabic",
    "0101": "10 Days Challenge",
    "0102": "Reading Fluency",
    "0201": "The Basics",
    "0202": "The Basics and Beyond",
    "020101": "Unit 1",
    "020102": "Unit 2",
    "020103": "Unit 3",
    "020104": "Unit 4",
    "020105": "Unit 5",
    "020106": "Unit 6",
    "020107": "Unit 7",
    "020108": "Unit 8",
    "020109": "Unit 9",
    "020110": "Unit 10",
    "020111": "Unit 11",
    "020112": "Unit 12",
    "020113": "Unit 13",
    "020114": "Unit 14",
    "020115": "Unit 15",
    "020201": "Dream",
    "020202": "Reading The Classics",
    "02020101": "Basic Nahw",
    "02020102": "Basic Sarf",
    "02020103": "Advanced Sarf",
    "02020104": "Advanced Nahw & Structures",
    "02020105": "Balagha",
    "02020106": "Baqarah Beyond Translation",
    "02020107": "Dream BIG 2023"
}
class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_videos(self, path):
        sql = """
        CREATE TABLE IF NOT EXISTS {path}_video (
            VideoID PRIMARY KEY NOT NULL,
            TFileID VARCHAR(255) NOT NULL
            );
""".format(path=path)
        self.execute(sql, commit=True)

    def create_table_files(self, path):
        sql = """
        CREATE TABLE IF NOT EXISTS {path}_file (
            VideoID NOT NULL ,
            FileID NOT NULL, 
            TFileID VARCHAR(255) NOT NULL
            );
""".format(path=path)
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_video(self, path, VideoID, TFileID):
        sql = """
        INSERT INTO {path}_video(VideoID, TFileID) VALUES(?, ?)
        """.format(path=path)
        self.execute(sql, parameters=(VideoID, TFileID), commit=True)

    def add_file(self, path,VideoID: str, FileID: str, TFileID: str):
        sql = """
        INSERT INTO {path}_file(VideoID, FileID, TFileID) VALUES(?, ?, ?)
        """.format(path=path)
        print(sql)
        self.execute(sql, parameters=(VideoID, FileID, TFileID), commit=True)

    def select_all_videos(self, pathID):
        sql = f"""
        SELECT * FROM {pathID}_video
        """
        return self.execute(sql, fetchall=True)
    def select_all_files(self, pathID):
        sql = f"""
        SELECT * FROM {pathID}
        """
        return self.execute(sql, fetchall=True)

    def select_video(self, path, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM {path}_video WHERE ".format(path=path)
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_file(self, pathID, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = f"SELECT * FROM {pathID}_file WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_video(self, pathID):
        return self.execute(f"SELECT COUNT(*) FROM {pathID}_video;", fetchone=True)

    def count_file(self, pathID):
        return self.execute(f"SELECT COUNT(*) FROM {pathID}_file;", fetchone=True)

    def delete_users(self, pathID, type):
        self.execute(f"DELETE FROM {pathID}_{type} WHERE TRUE", commit=True)

db = Database(path_to_db='main.db')

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")


@dataclass
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    # For SQLAlchemy
    def construct_sqlalchemy_url(self, driver="asyncpg", host=None, port=None) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        from sqlalchemy.engine.url import URL

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env):
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host, password=password, user=user, database=database, port=port
        )


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    admin_ids: list[int]
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        admin_ids = list(map(int, env.list("ADMINS")))
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, admin_ids=admin_ids, use_redis=use_redis)


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """
        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: str = None


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    db : Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    misc: Miscellaneous
    db: Optional[DbConfig] = None
    redis: Optional[RedisConfig] = None


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        # db=DbConfig.from_env(env),
        # redis=RedisConfig.from_env(env),
        misc=Miscellaneous(),
    )
