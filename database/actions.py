from sqlalchemy.engine import Connection
from sqlalchemy.dialects import sqlite

from database import schema


def insert(img_urls: list[dict], connection: Connection) -> None:
    query = sqlite.insert(schema.images_table)

    query = query.on_conflict_do_nothing(
        index_elements=[schema.images_table.c.id_uuid]
    )

    # query = query.on_conflict_do_update(
    #     index_elements=[schema.images_table.c.id_uuid],
    #     set_=dict(query.excluded)
    # )
    connection.execute(query, img_urls)


def get_all(connection: Connection) -> list[dict]:
    query = schema.images_table.select()
    return [dict(row) for row in connection.execute(query)]


def get_many(start_id: int, end_id: int, connection: Connection) -> list[dict]:
    query = schema.images_table.select().where((schema.images_table.c.id_number >= start_id) &
                                               (schema.images_table.c.id_number <= end_id))
    return [dict(row) for row in connection.execute(query)]


def get_info(connection: Connection) -> int:
    query = schema.images_table.select()
    return len(list(connection.execute(query)))


def get_user(username: str, connection: Connection) -> list[dict]:
    query = schema.users_table.select().where(schema.users_table.c.username == username)
    return [dict(row) for row in connection.execute(query)]
