from dotenv import dotenv_values

__env = dotenv_values(".env")

DB = {
    'user': __env.get("DB_USER"),
    'password': __env.get("DB_PASSWORD"),
    'host': __env.get("DB_HOST"),
    'port': __env.get("DB_PORT"),
    'name': __env.get("DB_NAME"),
    'url': F"postgresql://{__env.get("DB_USER")}:{__env.get("DB_PASSWORD")}@{__env.get("DB_HOST")}:{__env.get("DB_PORT")}/{__env.get("DB_NAME")}",
    'conn_str':  F"host={__env.get("DB_HOST")} port={__env.get("DB_PORT")} user={__env.get("DB_USER")} dbname={__env.get("DB_NAME")} password={__env.get("DB_PASSWORD")} sslmode=disable"
}