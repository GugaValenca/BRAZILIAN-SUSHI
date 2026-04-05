import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { LogIn } from "lucide-react";
import { toast } from "sonner";

import SectionHeading from "@/components/SectionHeading";
import { useAuth } from "@/contexts/AuthContext";
import { usePageMeta } from "@/hooks/usePageMeta";

const LoginPage = () => {
  usePageMeta({
    title: "Sign In | Brazilian Sushi",
    description: "Access your Brazilian Sushi account to manage orders, addresses, favorites, and notification preferences.",
    robots: "noindex,nofollow",
  });

  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const mutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      toast.success("Signed in successfully");
      navigate((location.state as { from?: string } | null)?.from ?? "/account");
    },
    onError: () => {
      toast.error("We could not sign you in. Check your credentials and try again.");
    },
  });

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container max-w-2xl">
        <SectionHeading
          label="Customer Access"
          title="Sign In"
          subtitle="Access your orders, favorites, saved addresses, and verified customer benefits."
        />

        <form
          onSubmit={(event) => {
            event.preventDefault();
            mutation.mutate({ email, password });
          }}
          className="bg-card border border-border rounded-2xl p-8 space-y-5"
        >
          <div>
            <label className="text-sm font-medium block mb-2">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm"
              placeholder="you@email.com"
            />
          </div>
          <div>
            <label className="text-sm font-medium block mb-2">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm"
              placeholder="Your password"
            />
          </div>
          <button type="submit" disabled={mutation.isPending} className="w-full bg-gradient-gold text-primary-foreground py-3.5 rounded-lg font-semibold disabled:opacity-70">
            <span className="inline-flex items-center gap-2"><LogIn className="w-4 h-4" /> {mutation.isPending ? "Signing in..." : "Sign In"}</span>
          </button>
          <p className="text-sm text-muted-foreground text-center">
            New here? <Link to="/register" className="text-primary font-semibold">Create an account</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
