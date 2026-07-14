"use client";

import { FormEvent, useState } from "react";
import { Send, Upload } from "lucide-react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export function LeadForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage(null);
    setError(null);

    const form = event.currentTarget;
    const formData = new FormData(form);

    try {
      const response = await fetch(`${API_BASE_URL}/api/leads`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.detail ?? "Unable to submit lead");
      }

      form.reset();
      setMessage("Submitted successfully. We sent confirmation emails.");
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Unable to submit lead",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <h2 className="panel-title">
        <Upload size={21} aria-hidden="true" />
        Lead form
      </h2>

      <div className="field">
        <label htmlFor="first_name">First name</label>
        <input id="first_name" name="first_name" required autoComplete="given-name" />
      </div>

      <div className="field">
        <label htmlFor="last_name">Last name</label>
        <input id="last_name" name="last_name" required autoComplete="family-name" />
      </div>

      <div className="field">
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required autoComplete="email" />
      </div>

      <div className="field">
        <label htmlFor="resume">Resume / CV</label>
        <input
          className="file-input"
          id="resume"
          name="resume"
          type="file"
          required
          accept=".pdf,.doc,.docx"
        />
      </div>

      <button
        className={`button button-primary full-width ${isSubmitting ? "is-loading" : ""}`}
        disabled={isSubmitting}
      >
        <Send size={18} aria-hidden="true" />
        {isSubmitting ? "Submitting..." : "Submit lead"}
      </button>

      {message ? <div className="message success">{message}</div> : null}
      {error ? <div className="message error">{error}</div> : null}
    </form>
  );
}
