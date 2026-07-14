"use client";

import { FormEvent, useState } from "react";
import {
  BriefcaseBusiness,
  Clipboard,
  Eye,
  EyeOff,
  KeyRound,
  LogIn,
} from "lucide-react";
import { useRouter } from "next/navigation";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const DEMO_TOKEN = "dev-attorney-token";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showToken, setShowToken] = useState(false);
  const [copiedToken, setCopiedToken] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    const formData = new FormData(event.currentTarget);
    const token = String(formData.get("token") ?? "").trim();
    if (!token) {
      setError("Enter the internal token.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/leads`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        throw new Error("Invalid attorney token.");
      }

      window.localStorage.setItem("prospect_portal_internal_token", token);
      router.push("/internal/leads");
    } catch (loginError) {
      setError(
        loginError instanceof Error ? loginError.message : "Unable to verify token.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function copyDemoToken() {
    await navigator.clipboard.writeText(DEMO_TOKEN);
    setCopiedToken(true);
    window.setTimeout(() => setCopiedToken(false), 1800);
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark">
              <BriefcaseBusiness size={20} aria-hidden="true" />
            </span>
            <span>Prospect Portal</span>
          </div>
        </div>
      </header>

      <section className="page">
        <form className="panel form-panel login-wrap" onSubmit={handleSubmit}>
          <h1 className="panel-title">
            <KeyRound size={22} aria-hidden="true" />
            Internal access
          </h1>

          <div className="field">
            <label htmlFor="token">Attorney token</label>
            <p className="field-help">
              Use the attorney token assigned by your supervisor or workspace owner.
            </p>
            <div className="password-field">
              <input
                id="token"
                name="token"
                type={showToken ? "text" : "password"}
                required
                autoComplete="current-password"
                placeholder="dev-attorney-token"
              />
              <button
                aria-label={showToken ? "Hide token" : "Show token"}
                className="icon-button"
                onClick={() => setShowToken((current) => !current)}
                type="button"
              >
                {showToken ? (
                  <EyeOff size={19} aria-hidden="true" />
                ) : (
                  <Eye size={19} aria-hidden="true" />
                )}
              </button>
            </div>
          </div>

          <button className="button button-primary full-width" disabled={isSubmitting}>
            <LogIn size={18} aria-hidden="true" />
            {isSubmitting ? "Verifying..." : "Sign in"}
          </button>

          <div className="test-tip">
            <div>
              <strong>Testing tip</strong>
              <span>Use this demo token during local review.</span>
            </div>
            <button className="copy-token" onClick={copyDemoToken} type="button">
              <Clipboard size={16} aria-hidden="true" />
              {copiedToken ? "Copied" : DEMO_TOKEN}
            </button>
          </div>

          {error ? <div className="message error">{error}</div> : null}
        </form>
      </section>
    </main>
  );
}
