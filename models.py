from sqlalchemy import Table, Column, Integer, String

from config import metadata_obj, engine

user = Table(
     "users",
     metadata_obj,
     Column("id", Integer, primary_key=True),
     Column("api_id", Integer),
     Column("api_hash", Integer),
    )


group = Table(
     "groups",
     metadata_obj,
     Column("id", Integer, primary_key=True),
     Column("link", String),
    )

metadata_obj.create_all(engine)

