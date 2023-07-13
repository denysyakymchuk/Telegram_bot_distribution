from config import engine

with engine.connect() as conn:
    result = conn.execute()
    print(result.all())