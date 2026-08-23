from app.services.exasol_service import get_exasol_connection

conn = get_exasol_connection()

result = conn.execute("SELECT 1 AS test").fetchall()

print(result)

conn.close()