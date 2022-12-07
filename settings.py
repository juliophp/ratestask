# DATABASE SETTINGS
pg_db_username = 'postgres'
pg_db_password = 'ratestask'
pg_db_name = 'postgres'
pg_db_hostname = 'postgres_db'


DEBUG = False
PORT = 5432
HOST = "localhost"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
# PostgreSQL
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=pg_db_username,
                                                                                        DB_PASS=pg_db_password,
                                                                                        DB_ADDR=pg_db_hostname,
                                                                                        DB_NAME=pg_db_name)
