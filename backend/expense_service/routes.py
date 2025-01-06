

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from database import get_db_connection, release_db_connection

# # Define models
# class Expense(BaseModel):
#     user_id: int
#     expense_description: str
#     expense_amount: float
#     expense_type: str

# class ExpenseResponse(BaseModel):
#     expenses: list
#     total_expenses: float

# # Router
# expense_router = APIRouter()

# @expense_router.post("/add-expense", response_model=ExpenseResponse)
# def add_expense(expense: Expense):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         # Insert new expense into the database
#         cursor.execute(
#             """
#             INSERT INTO expenses (user_id, expense_description, expense_amount, expense_type)
#             VALUES (%s, %s, %s, %s)
#             """,
#             (expense.user_id, expense.expense_description, expense.expense_amount, expense.expense_type)
#         )
#         conn.commit()

#         # Fetch updated expenses for the user
#         cursor.execute(
#             """
#             SELECT expense_description, expense_amount, expense_type FROM expenses
#             WHERE user_id = %s
#             """,
#             (expense.user_id,)
#         )
#         expenses = cursor.fetchall()

#         # Calculate the total expenses for the user
#         total_expenses = sum(exp[1] for exp in expenses)

#         # Format expenses for response
#         formatted_expenses = [
#             {"description": exp[0], "amount": exp[1], "category": exp[2]} for exp in expenses
#         ]

#         return {"expenses": formatted_expenses, "total_expenses": total_expenses}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error adding expense: {str(e)}")
#     finally:
#         cursor.close()
#         release_db_connection(conn)

# @expense_router.get("/get-expenses/{user_id}", response_model=ExpenseResponse)
# def get_expenses(user_id: int):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         # Fetch all expenses for the user
#         cursor.execute(
#             """
#             SELECT expense_description, expense_amount, expense_type FROM expenses
#             WHERE user_id = %s
#             """,
#             (user_id,)
#         )
#         expenses = cursor.fetchall()

#         if not expenses:
#             raise HTTPException(status_code=404, detail="No expenses found for this user.")

#         # Calculate the total expenses for the user
#         total_expenses = sum(exp[1] for exp in expenses)

#         # Format expenses for response
#         formatted_expenses = [
#             {"description": exp[0], "amount": exp[1], "category": exp[2]} for exp in expenses
#         ]

#         return {"expenses": formatted_expenses, "total_expenses": total_expenses}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching expenses: {str(e)}")
#     finally:
#         cursor.close()
#         release_db_connection(conn)




from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pika
import json
from expense_service.database import get_db_connection, release_db_connection
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")


# RabbitMQ connection settings
# RABBITMQ_HOST = "localhost"  # Change to RabbitMQ hostname in your deployment environment

def publish_to_rabbitmq(expense_data):
    """Publish expense data to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare a queue (idempotent)
    channel.queue_declare(queue='expense_notifications')

    # Publish the message
    channel.basic_publish(
        exchange='',
        routing_key='expense_notifications',
        body=json.dumps(expense_data),
    )
    connection.close()




# Define models
class Expense(BaseModel):
    user_id: int
    user_email:str
    expense_description: str
    expense_amount: float
    expense_type: str

class ExpenseResponse(BaseModel):
    expenses: list
    total_expenses: float

# Router
expense_router = APIRouter()





@expense_router.post("/add-expense", response_model=ExpenseResponse)
def add_expense(expense: Expense):
    conn = get_db_connection()
    cursor = conn.cursor()
    # print("expenses", expense.user_email)
    try:
        # Insert new expense into the database
        cursor.execute(
            """
            INSERT INTO expenses (user_id, expense_description, expense_amount, expense_type)
            VALUES (%s, %s, %s, %s)
            """,
            (expense.user_id, expense.expense_description, expense.expense_amount, expense.expense_type)
        )
        conn.commit()

        # Fetch updated expenses for the user
        cursor.execute(
            """
            SELECT expense_description, expense_amount, expense_type FROM expenses
            WHERE user_id = %s
            """,
            (expense.user_id,)
        )
        expenses = cursor.fetchall()


        # Calculate the total expenses for the user
        total_expenses = sum(exp[1] for exp in expenses)

        # Format expenses for response
        formatted_expenses = [
            {"description": exp[0], "amount": exp[1], "category": exp[2]} for exp in expenses
        ]

        print("expenses", expense.user_email)
        # Check if the expense exceeds the threshold
        if expense.expense_amount > 10:
            # Prepare message data for RabbitMQ
            # user_email = fetch_user_email(expense.user_id)
            expense_data = {
                "user_id": expense.user_id,
                "description": expense.expense_description,
                "amount": expense.expense_amount,
                "category": expense.expense_type,
                "email":expense.user_email,
            }
            publish_to_rabbitmq(expense_data)

        return {"expenses": formatted_expenses, "total_expenses": total_expenses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding expense: {str(e)}")
    finally:
        cursor.close()
        release_db_connection(conn)


@expense_router.get("/get-expenses/{user_id}", response_model=ExpenseResponse)
def get_expenses(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch all expenses for the user
        cursor.execute(
            """
            SELECT expense_description, expense_amount, expense_type FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )
        expenses = cursor.fetchall()

        if not expenses:
            raise HTTPException(status_code=404, detail="No expenses found for this user.")

        # Calculate the total expenses for the user
        total_expenses = sum(exp[1] for exp in expenses)

        # Format expenses for response
        formatted_expenses = [
            {"description": exp[0], "amount": exp[1], "category": exp[2]} for exp in expenses
        ]

        return {"expenses": formatted_expenses, "total_expenses": total_expenses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching expenses: {str(e)}")
    finally:
        cursor.close()
        release_db_connection(conn)