from fastapi import APIRouter, HTTPException
from shared.database import get_db_connection, release_db_connection

account_router = APIRouter()

@account_router.post("/set-goal")
def set_goal(user_id: int, goal: float):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE accounts SET savings_goal = %s WHERE user_id = %s", (goal, user_id))
        conn.commit()
        
        # Notification
        from shared.mqtt_client import publish_message
        publish_message("notifications", f"User {user_id} set a savings goal of {goal}.")
        
        return {"message": "Savings goal set successfully"}
    finally:
        cursor.close()
        release_db_connection(conn)
