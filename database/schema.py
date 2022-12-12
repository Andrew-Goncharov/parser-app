from sqlalchemy import (
    Column, DateTime,  ForeignKey, Integer,
    MetaData, String, Table,
    UniqueConstraint
)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

images_table = Table(
    "images",
    metadata,
    Column("id_number", Integer, primary_key=True),
    Column("id_uuid", String, nullable=False),
    Column("img_url", String, nullable=False),
    UniqueConstraint("id_uuid", sqlite_on_conflict="IGNORE", name="uuid_unique")
)

users_table = Table(
    "users",
    metadata,
    Column("username", String, primary_key=True),
    Column("password", String, nullable=False)
)