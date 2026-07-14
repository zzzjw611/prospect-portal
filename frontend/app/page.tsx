import { BriefcaseBusiness } from "lucide-react";
import { LeadForm } from "./components/LeadForm";

export default function Home() {
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

      <section className="page hero-grid">
        <div>
          <div className="eyebrow">Prospect intake</div>
          <h1>Share your background with our team.</h1>
          <p className="lead-copy">
            Submit your contact information and resume. Our team will review your
            details and follow up directly when there is a fit.
          </p>

          <div className="steps" aria-label="Submission process">
            <div className="step">
              <strong>Submit</strong>
              <span>Send your contact details and resume securely.</span>
            </div>
            <div className="step">
              <strong>Review</strong>
              <span>An attorney receives the lead notification.</span>
            </div>
            <div className="step">
              <strong>Follow up</strong>
              <span>The internal team tracks outreach status.</span>
            </div>
          </div>
        </div>

        <LeadForm />
      </section>
    </main>
  );
}
