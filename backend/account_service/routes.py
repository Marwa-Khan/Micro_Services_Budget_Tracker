from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_account_db_connection, release_account_db_connection, get_expense_db_connection, release_expense_db_connection

router = APIRouter()

class SavingsGoalRequest(BaseModel):
    user_id: int
    saving_goal: float
    monthly_income: float

class SavingsGoalResponse(BaseModel):
    user_id: int
    saving_goal: float
    percentage: float
    spent: float
    remaining: float

from decimal import Decimal

@router.post("/set-savings-goal", response_model=SavingsGoalResponse)
def set_savings_goal(data: SavingsGoalRequest):
    account_conn = get_account_db_connection()
    account_cursor = account_conn.cursor()

    expense_conn = get_expense_db_connection()
    expense_cursor = expense_conn.cursor()

    try:
        # Fetch total expenses for the user from expense_service
        expense_cursor.execute(
            "SELECT COALESCE(SUM(expense_amount), 0) FROM expenses WHERE user_id = %s",
            (data.user_id,)
        )
        spent = expense_cursor.fetchone()[0]

        # Convert spent to float if it's Decimal
        spent = float(spent) if isinstance(spent, Decimal) else spent

        # Calculate remaining and percentage
        remaining = data.monthly_income - spent
        percentage = (spent / data.saving_goal) * 100 if data.saving_goal > 0 else 0

        # Check if the user exists in the accounts table
        account_cursor.execute(
            "SELECT user_id FROM accounts WHERE user_id = %s", (data.user_id,)
        )
        user_exists = account_cursor.fetchone()

        if not user_exists:
            # Insert user if not exists
            account_cursor.execute(
                """
                INSERT INTO accounts (user_id, saving_goal, monthly_income, spent, percentage)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id, saving_goal, percentage, spent
                """,
                (data.user_id, data.saving_goal, data.monthly_income, spent, percentage)
            )
        else:
            # Update the existing user's data
            account_cursor.execute(
                """
                UPDATE accounts
                SET saving_goal = %s, monthly_income = %s, spent = %s, percentage = %s
                WHERE user_id = %s
                RETURNING user_id, saving_goal, percentage, spent
                """,
                (data.saving_goal, data.monthly_income, spent, percentage, data.user_id)
            )

        # Fetch the updated or newly created record
        updated_account = account_cursor.fetchone()

        if not updated_account:
            raise HTTPException(status_code=404, detail="Failed to update or create savings goal")

        # Commit transaction in account_service database
        account_conn.commit()

        # Return the response
        return SavingsGoalResponse(
            user_id=updated_account[0],
            saving_goal=updated_account[1],
            percentage=updated_account[2],
            spent=updated_account[3],
            remaining=remaining
        )

    except Exception as e:
        account_conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating or creating savings goal: {str(e)}")

    finally:
        # Close cursors and release connections
        account_cursor.close()
        release_account_db_connection(account_conn)

        expense_cursor.close()
        release_expense_db_connection(expense_conn)


@router.get("/get-savings-goal/{user_id}", response_model=SavingsGoalResponse)
def get_savings_goal(user_id: int):
    account_conn = get_account_db_connection()
    account_cursor = account_conn.cursor()

    try:
        # Fetch savings goal details for the user
        account_cursor.execute(
            """
            SELECT saving_goal, percentage, spent, 
                   (monthly_income - spent) AS remaining,
                   monthly_income
            FROM accounts
            WHERE user_id = %s
            """,
            (user_id,)
        )
        result = account_cursor.fetchone()
        print("results ", result[4])

        if not result:
            raise HTTPException(status_code=404, detail="Savings goal not found for the user")

        # Return the savings goal data
        return SavingsGoalResponse(
            user_id=user_id,
            saving_goal=result[0],
            percentage=result[1],
            spent=result[2],
            remaining=result[3],
            monthly_income=result[4]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving savings goal: {str(e)}")

    finally:
        # Close cursor and release connection
        account_cursor.close()
        release_account_db_connection(account_conn)