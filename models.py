from sqlalchemy import Table, Column, Integer, String

from config import metadata_obj, engine

user = Table(
     "users",
     metadata_obj,
     Column("id", Integer, primary_key=True),
     Column("title", String(50)),
     Column("api_id", Integer),
     Column("api_hash", String(50)),
     Column("phone_number", String(30))
    )


group = Table(
     "groups",
     metadata_obj,
     Column("id", Integer, primary_key=True),
     Column("link", String(50)),
    )

metadata_obj.create_all(engine)

