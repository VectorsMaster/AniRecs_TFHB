from environs import env

env.read_env()


class DataBaseSettings:
    DataBase_User: str = env.str("DATABASE_USER", "sample")
    DataBase_Password: str = env.str("DATABASE_PASSWORD", "sample")
    DataBase_Name: str = env.str("DATABASE_NAME", "sample")
    DataBase_URL: str = env.str("DATABASE_URL", "sample")


class JWTSettings:
    OPEN_SSL_RAND = env.str("OPEN_SSL_Rand", "sample")
    ALGORITHM = env.str("ALGORITHM", "sample")
    ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


database_settings = DataBaseSettings()
jwt_settings = JWTSettings()

ROOT_PASSWORD = env.str("ROOT_PASSWORD", "root_password")
CLIENT_ID = env.str("CLIENT_ID", "client_id")
