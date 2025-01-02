
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from connection import get_db_connection, release_db_connection

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



from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection, release_db_connection

# Define models
class Expense(BaseModel):
    user_id: int
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
