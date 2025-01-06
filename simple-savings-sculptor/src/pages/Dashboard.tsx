
import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useSearchParams } from "react-router-dom";

const Dashboard = () => {
  const { user, logout } = useAuth();
  const { toast } = useToast();
  const [newExpense, setNewExpense] = useState({ description: "", amount: "", category: "food" });
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [expenses, setExpenses] = useState([]);
  const [totalExpenses, setTotalExpenses] = useState(0);
  const [savingsGoal, setSavingsGoal] = useState<number | null>(null);
  const [monthlyIncome, setMonthlyIncome] = useState<number | null>(null);
  const [monthlyExpensesData, setMonthlyExpensesData] = useState([]);
  const [searchParams] = useSearchParams();
  let getAccountData = {};
  const userId = searchParams.get("userId");

  // const userId = searchParams.get("userId");
  const userEmail = searchParams.get("userEmail");
  console.log("useremaeda",userEmail)

  const apiUrl = "http://127.0.0.1:8002";
  const apiUrlIncome = "http://127.0.0.1:8003";


  useEffect(() => {
    const fetchExpensesAndSavings = async () => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        if (!user || !user.id) {
          console.error("User ID not found in local storage.");
          return;
        }

        // Fetch expenses data
        const expensesResponse = await fetch(`${apiUrl}/get-expenses/${user.id}`);
        if (!expensesResponse.ok) {
          throw new Error(`Failed to fetch expenses: ${expensesResponse.statusText}`);
        }
        const expensesData = await expensesResponse.json();
        setExpenses(expensesData.expenses);
        setTotalExpenses(expensesData.total_expenses);

        // Fetch savings goal data
        const savingsResponse = await fetch(`${apiUrlIncome}/get-savings-goal/${user.id}`);
        if (!savingsResponse.ok) {
          throw new Error(`Failed to fetch savings goal: ${savingsResponse.statusText}`);
        }
        const savingsData = await savingsResponse.json();
        console.log("Savings data:", savingsData);

        setSavingsGoal(savingsData.saving_goal)
        getAccountData['savingGoal'] = savingsData.saving_goal

        getAccountData['percentage'] = savingsData.percentage
        getAccountData['spent'] = savingsData.spent
        getAccountData['remaining'] = savingsData.remaining
        getAccountData['monthly_income'] = savingsData.monthly_income
        setMonthlyIncome(savingsData.monthly_income)
        //   console.log('getAccountData', savingsData.monthly_income)
        // percentage: savingsData.percentage,
        // spent: savingsData.spent,

        // remaining: savingsData.remaining,
        // monthlyIncome: savingsData.monthly_income,
        // });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchExpensesAndSavings();
  }, []);

  const handleAddExpense = async () => {
    console.log("newExpense",newExpense)
    if (!newExpense.description || !newExpense.amount) {
      toast({
        title: "Error",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }

    const expenseData = {
      user_id: parseInt(userId),
      user_email:userEmail,
      expense_description: newExpense.description,
      expense_amount: parseFloat(newExpense.amount),
      expense_type: "Food",
    };

    setIsDialogOpen(false);

    try {
      const response = await fetch(`${apiUrl}/add-expense`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(expenseData),
      });

      const result = await response.json();

      if (response.ok) {
        setExpenses(result.expenses);
        setTotalExpenses(result.total_expenses);
        toast({
          title: "Success",
          description:` Added ${newExpense.amount} for ${newExpense.description}`,
        });
        setNewExpense({ description: "", amount: "", category: "food" });
        setIsDialogOpen(false);
      } else {
        toast({
          title: "Error",
          description: result.message || "Something went wrong.",
        });
      }
    } catch (error) {
      console.error("Error adding expense:", error);
      toast({
        title: "Error",
        description: "Failed to connect to the backend.",
      });
    }
  };


  const handleAddSavingsGoal = async () => {
    console.log("monthlyIncome",monthlyIncome)
    if (
      savingsGoal == null || savingsGoal <= 0 ||
      monthlyIncome == null || monthlyIncome <= 0
    ) {
      toast({
        title: "Error",
        description: "Please set valid savings goal and income.",
        variant: "destructive",
      });
      return;
    }

    try {
      const response = await fetch(`${apiUrlIncome}/set-savings-goal`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          saving_goal: savingsGoal,
          monthly_income: monthlyIncome,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        toast({
          title: "Savings Goal Updated",
          description: `
            Goal: $${data.saving_goal}, 
            Spent: $${data.spent}, 
            Remaining: $${data.remaining}, 
            Saved: ${data.percentage.toFixed(2)}%`,
        });
      } else {
        const errorData = await response.json();
        console.log("error data", errorData)
        toast({
          title: "Error",
          description: `Failed to update savings goal: ${errorData.detail || "Unknown error"}`,
        });
      }
    } catch (error) {
      console.error("Error updating savings goal:", error);
      toast({
        title: "Error",
        description: "Failed to connect to the backend.",
      });
    }
  };


  const remainingAmount = monthlyIncome && savingsGoal ? monthlyIncome - savingsGoal : 0;
  const progressBarPercentage = totalExpenses && savingsGoal ? (totalExpenses / savingsGoal) * 100 : 0;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome, {user?.email}{userId}</h1>
          <Button onClick={logout} variant="outline">Logout</Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Expenses Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex justify-between items-center">
                <span>Recent Expenses</span>
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button className="bg-money hover:bg-money-dark">Add Expense</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Add New Expense</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 mt-4">
                      <Input
                        placeholder="Description"
                        value={newExpense.description}
                        onChange={(e) =>
                          setNewExpense({ ...newExpense, description: e.target.value })
                        }
                      />
                      <Input
                        type="number"
                        placeholder="Amount"
                        value={newExpense.amount}
                        onChange={(e) =>
                          setNewExpense({ ...newExpense, amount: e.target.value })
                        }
                      />
                      <Button onClick={handleAddExpense} className="w-full">
                        Add Expense
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {expenses.length === 0 ? (
                  <span>No expenses added yet.</span>
                ) : (
                  expenses.map((expense, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span>{expense.description}</span>
                      <span className="text-money">${expense.amount}</span>
                    </div>
                  ))
                )}
                <div className="flex justify-between items-center font-bold">
                  <span>Total</span>
                  <span className="text-money">${totalExpenses}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Savings Goals Card */}
          <Card>
            <CardHeader>
              <CardTitle>Savings Goal</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Input
                  type="number"
                  placeholder="Enter your monthly income"
                  value={monthlyIncome || ""}
                  onChange={(e) => setMonthlyIncome(Number(e.target.value))}
                />
                <Input
                  type="number"
                  placeholder="Enter your savings goal"
                  value={savingsGoal || ""}
                  onChange={(e) => setSavingsGoal(Number(e.target.value))}
                />
                <Button onClick={handleAddSavingsGoal} className="w-full">
                  Set Savings Goal
                </Button>
                <div className="mt-4">
                  <div className="text-sm">Progress: {progressBarPercentage.toFixed(2)}%</div>
                  <div className="relative pt-1">
                    <div className="flex mb-2 items-center justify-between">
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-teal-600 bg-teal-200">
                          Spent: ${totalExpenses}
                        </span>
                      </div>
                      <div>
                        <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-teal-600 bg-teal-200">
                          Remaining: ${remainingAmount}
                        </span>
                      </div>
                    </div>
                    <div className="flex mb-2 items-center justify-between">
                      <div>
                        <ResponsiveContainer width="100%" height={50}>
                          <BarChart data={monthlyExpensesData}>
                            <Bar dataKey="expenses" fill="#009688" />
                            <XAxis dataKey="month" />
                            <YAxis />
                            <Tooltip />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
