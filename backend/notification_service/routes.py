from fastapi import APIRouter
from shared.database import get_db_connection, release_db_connection

notification_router = APIRouter()

@notification_router.get("/notifications/{user_id}")
def get_notifications(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        notifications = cursor.fetchall()
        return {"notifications": notifications}
    finally:
        cursor.close()
        release_db_connection(conn)
