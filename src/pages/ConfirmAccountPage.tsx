import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { CheckCircle2, Mail, RefreshCcw } from "lucide-react";

import SectionHeading from "@/components/SectionHeading";
import { usePageMeta } from "@/hooks/usePageMeta";
import { confirmAccount, resendConfirmation } from "@/lib/account";

const ConfirmAccountPage = () => {
  usePageMeta({
    title: "Confirm Account | Brazilian Sushi",
    description: "Confirm your Brazilian Sushi account to activate sign-in, order history, and customer account features.",
    robots: "noindex,nofollow",
  });

  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";
  const initialEmail = searchParams.get("email") ?? "";
  const [email, setEmail] = useState(initialEmail);

  const confirmMutation = useMutation({
    mutationFn: (confirmationToken: string) => confirmAccount(confirmationToken),
  });

  const resendMutation = useMutation({
    mutationFn: resendConfirmation,
  });

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container max-w-3xl">
        <SectionHeading
          label="Account Confirmation"
          title="Confirm Your Account"
          subtitle="Activate your Brazilian Sushi account to unlock sign-in, saved preferences, order history, and future customer benefits."
        />

        <div className="bg-card border border-border rounded-2xl p-8 space-y-6">
          {token ? (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Your confirmation link is ready. Finish the activation below to start using your account.
              </p>
              <button
                type="button"
                onClick={() => confirmMutation.mutate(token)}
                disabled={confirmMutation.isPending || confirmMutation.isSuccess}
                className="w-full bg-gradient-gold text-primary-foreground py-3.5 rounded-lg font-semibold disabled:opacity-70"
              >
                {confirmMutation.isPending ? "Confirming..." : confirmMutation.isSuccess ? "Account Confirmed" : "Confirm Account"}
              </button>
              {confirmMutation.isSuccess && (
                <div className="rounded-2xl border border-primary/25 bg-primary/5 p-5">
                  <p className="inline-flex items-center gap-2 text-sm font-semibold text-foreground">
                    <CheckCircle2 className="w-4 h-4 text-primary" />
                    {confirmMutation.data.detail}
                  </p>
                  <Link to="/login" className="inline-flex items-center gap-2 text-primary font-semibold mt-4 hover:underline underline-offset-4">
                    Continue to Sign In
                  </Link>
                </div>
              )}
              {confirmMutation.isError && (
                <p className="text-sm text-destructive">
                  {confirmMutation.error instanceof Error
                    ? confirmMutation.error.message
                    : "We couldn't confirm your account with this link."}
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-5">
              <div className="rounded-2xl border border-border bg-secondary/40 p-5">
                <p className="inline-flex items-center gap-2 text-sm font-semibold text-foreground">
                  <Mail className="w-4 h-4 text-primary" />
                  Check your inbox and, if selected, your SMS notifications for the confirmation link.
                </p>
                <p className="text-sm text-muted-foreground mt-2">
                  If you did not receive it yet, you can request a new confirmation message below.
                </p>
              </div>
              <div className="space-y-3">
                <label className="text-sm font-medium block">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@email.com"
                  className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm"
                />
              </div>
              <button
                type="button"
                onClick={() => resendMutation.mutate(email.trim())}
                disabled={!email.trim() || resendMutation.isPending}
                className="w-full border border-primary/30 py-3.5 rounded-lg font-semibold disabled:opacity-70 inline-flex items-center justify-center gap-2"
              >
                <RefreshCcw className="w-4 h-4" />
                {resendMutation.isPending ? "Sending..." : "Resend Confirmation"}
              </button>
              {resendMutation.isSuccess && (
                <p className="text-sm text-muted-foreground">{resendMutation.data.detail}</p>
              )}
              {resendMutation.isError && (
                <p className="text-sm text-destructive">
                  {resendMutation.error instanceof Error
                    ? resendMutation.error.message
                    : "We couldn't resend the confirmation message right now."}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ConfirmAccountPage;
