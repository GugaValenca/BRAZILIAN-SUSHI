import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { UserPlus } from "lucide-react";
import { toast } from "sonner";

import SectionHeading from "@/components/SectionHeading";
import { useAuth } from "@/contexts/AuthContext";
import { usePageMeta } from "@/hooks/usePageMeta";

const RegisterPage = () => {
  usePageMeta({
    title: "Create Account | Brazilian Sushi",
    description: "Create a Brazilian Sushi customer account to save addresses, favorites, preferences, and order history.",
    robots: "noindex,nofollow",
  });

  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    phone_number: "",
    password: "",
    notification_preference: "both" as "sms" | "email" | "both",
    sms_opt_in: true,
    email_opt_in: true,
  });

  const mutation = useMutation({
    mutationFn: register,
    onSuccess: () => {
      toast.success("Account created successfully");
      navigate("/account");
    },
    onError: () => {
      toast.error("We could not create your account. Please review your details and try again.");
    },
  });

  const updateField = <K extends keyof typeof form>(field: K, value: (typeof form)[K]) => {
    setForm((current) => ({ ...current, [field]: value }));
  };

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container max-w-3xl">
        <SectionHeading
          label="Customer Access"
          title="Create Account"
          subtitle="Save addresses, track orders, manage favorites, and unlock verified customer benefits over time."
        />

        <form
          onSubmit={(event) => {
            event.preventDefault();
            mutation.mutate(form);
          }}
          className="bg-card border border-border rounded-2xl p-8 space-y-6"
        >
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium block mb-2">First name</label>
              <input required value={form.first_name} onChange={(e) => updateField("first_name", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
            <div>
              <label className="text-sm font-medium block mb-2">Last name</label>
              <input required value={form.last_name} onChange={(e) => updateField("last_name", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium block mb-2">Username</label>
              <input required value={form.username} onChange={(e) => updateField("username", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
            <div>
              <label className="text-sm font-medium block mb-2">Phone</label>
              <input required value={form.phone_number} onChange={(e) => updateField("phone_number", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium block mb-2">Email</label>
              <input required type="email" value={form.email} onChange={(e) => updateField("email", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
            <div>
              <label className="text-sm font-medium block mb-2">Password</label>
              <input required type="password" minLength={8} value={form.password} onChange={(e) => updateField("password", e.target.value)} className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm" />
            </div>
          </div>

          <div>
            <label className="text-sm font-medium block mb-2">Preferred notifications</label>
            <div className="grid sm:grid-cols-3 gap-3">
              {([
                ["sms", "SMS"],
                ["email", "Email"],
                ["both", "SMS + Email"],
              ] as const).map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => updateField("notification_preference", value)}
                  className={`rounded-xl border px-4 py-3 text-sm font-medium ${form.notification_preference === value ? "border-primary bg-primary/5" : "border-border"}`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-3 text-sm">
            <label className="inline-flex items-center gap-2">
              <input type="checkbox" checked={form.sms_opt_in} onChange={(e) => updateField("sms_opt_in", e.target.checked)} /> SMS updates
            </label>
            <label className="inline-flex items-center gap-2">
              <input type="checkbox" checked={form.email_opt_in} onChange={(e) => updateField("email_opt_in", e.target.checked)} /> Email updates
            </label>
          </div>

          <button type="submit" disabled={mutation.isPending} className="w-full bg-gradient-gold text-primary-foreground py-3.5 rounded-lg font-semibold disabled:opacity-70">
            <span className="inline-flex items-center gap-2"><UserPlus className="w-4 h-4" /> {mutation.isPending ? "Creating account..." : "Create Account"}</span>
          </button>
          <p className="text-sm text-muted-foreground text-center">
            Already registered? <Link to="/login" className="text-primary font-semibold">Sign in</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
