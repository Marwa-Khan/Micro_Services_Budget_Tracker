import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { console } from "inspector";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isLogin) {
      login(email, password);
    } else {
      register(email, password);
    }
    toast({
      title: isLogin ? "Welcome back!" : "Account created successfully!",
      description: "You are now logged in.",
    });
    navigate("/dashboard");
  };

  // const handleSubmit = async (e: React.FormEvent) => {
  //   // e.preventDefault();

  //   const apiUrl = isLogin
  //     ? "http://127.0.0.1:8001/auth"
  //     : "http://127.0.0.1:8001/register";
    


  //   try {
  //     const response = await fetch(apiUrl, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({ email: email, password: password }), // Sending email and password to the backend
  //     });

  //     const data = await response.json();

  //     if (response.ok) {
  //       toast({
  //         title: isLogin ? "Welcome back!" : "Account created successfully!",
  //         description: data.message,
  //       });
  //       navigate("/dashboard");
  //     } else {
  //       toast({
  //         title: "Error",
  //         description: data.detail || "Something went wrong.",
  //       });
  //     }
  //   } catch (error) {
  //     console.error("Error:", error);
  //     toast({
  //       title: "Error",
  //       description: "Failed to connect to the backend.",
  //     });
  //   }
  // };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-[400px]">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            {isLogin ? "Welcome Back" : "Create Account"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button
              type="submit"
              className="w-full bg-money hover:bg-money-dark"
            >
              {isLogin ? "Login" : "Register"}
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-gray-600">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-money hover:text-money-dark"
            >
              {isLogin ? "Register" : "Login"}
            </button>
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Auth;
