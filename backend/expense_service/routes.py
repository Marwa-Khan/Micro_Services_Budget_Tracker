from fastapi import APIRouter, HTTPException
from shared.database import get_db_connection, release_db_connection

expense_router = APIRouter()

@expense_router.post("/add-expense")
def add_expense(account_id: int, amount: float, description: str, expense_type: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO expenses (account_id, expense_des, expsense_amount, expense_type)
            VALUES (%s, %s, %s, %s)
            """,
            (account_id, description, amount, expense_type)
        )
        conn.commit()
        
        # Notification
        from shared.mqtt_client import publish_message
        publish_message("notifications", f"Expense added: {description}, Amount: {amount}.")
        
        return {"message": "Expense added successfully"}
    finally:
        cursor.close()
        release_db_connection(conn)
