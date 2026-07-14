"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  BriefcaseBusiness,
  Download,
  LogOut,
  RefreshCw,
  Send,
} from "lucide-react";
import { useRouter } from "next/navigation";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const REFRESH_INTERVAL_MS = 5000;

type LeadStatus = "PENDING" | "REACHED_OUT";
type StatusFilter = "ALL" | LeadStatus;

type Lead = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  resume_filename: string;
  status: LeadStatus;
  created_at: string;
  updated_at: string;
};

export default function LeadsPage() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [leads, setLeads] = useState<Lead[]>([]);
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("ALL");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastUpdatedAt, setLastUpdatedAt] = useState<string | null>(null);
  const [downloadingLeadId, setDownloadingLeadId] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const stats = useMemo(() => {
    const pending = leads.filter((lead) => lead.status === "PENDING").length;
    const reached = leads.filter((lead) => lead.status === "REACHED_OUT").length;
    return { total: leads.length, pending, reached };
  }, [leads]);

  const visibleLeads = useMemo(() => {
    if (statusFilter === "ALL") {
      return leads;
    }
    return leads.filter((lead) => lead.status === statusFilter);
  }, [leads, statusFilter]);

  const loadLeads = useCallback(async (authToken = token, options?: { silent?: boolean }) => {
    if (!authToken) return;
    if (options?.silent) {
      setIsRefreshing(true);
    } else {
      setIsLoading(true);
    }
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/leads`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          window.localStorage.removeItem("prospect_portal_internal_token");
          router.replace("/internal/login");
          return;
        }
        throw new Error(response.status === 403 ? "Invalid token" : "Unable to load leads");
      }
      setLeads(await response.json());
      setLastUpdatedAt(new Date().toISOString());
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : "Unable to load leads");
    } finally {
      if (options?.silent) {
        setIsRefreshing(false);
      } else {
        setIsLoading(false);
      }
    }
  }, [router, token]);

  useEffect(() => {
    const storedToken = window.localStorage.getItem("prospect_portal_internal_token");
    if (!storedToken) {
      router.replace("/internal/login");
      return;
    }
    setToken(storedToken);
  }, [router]);

  useEffect(() => {
    if (!token) return;
    void loadLeads(token);
  }, [loadLeads, token]);

  useEffect(() => {
    if (!token || !autoRefresh) return;
    const intervalId = window.setInterval(() => {
      void loadLeads(token, { silent: true });
    }, REFRESH_INTERVAL_MS);
    return () => window.clearInterval(intervalId);
  }, [autoRefresh, loadLeads, token]);

  async function markReachedOut(leadId: string) {
    if (!token) return;
    setNotice(null);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/leads/${leadId}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: "REACHED_OUT" }),
      });
      if (!response.ok) {
        throw new Error("Unable to update status");
      }
      const updatedLead: Lead = await response.json();
      setLeads((current) =>
        current.map((lead) => (lead.id === updatedLead.id ? updatedLead : lead)),
      );
    } catch (updateError) {
      setError(
        updateError instanceof Error ? updateError.message : "Unable to update status",
      );
    }
  }

  function signOut() {
    window.localStorage.removeItem("prospect_portal_internal_token");
    router.push("/internal/login");
  }

  async function downloadResume(lead: Lead) {
    if (!token) return;
    setNotice(null);
    setError(null);
    setDownloadingLeadId(lead.id);
    try {
      const response = await fetch(`${API_BASE_URL}/api/leads/${lead.id}/resume`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        throw new Error("Unable to download resume");
      }
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = objectUrl;
      anchor.download = lead.resume_filename;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
      setNotice(`Download started for ${lead.resume_filename}.`);
    } catch (downloadError) {
      setError(
        downloadError instanceof Error
          ? downloadError.message
          : "Unable to download resume",
      );
    } finally {
      setDownloadingLeadId(null);
    }
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
          <nav className="nav-actions">
            <button className="button button-secondary" onClick={() => loadLeads()}>
              <RefreshCw size={18} aria-hidden="true" />
              {isRefreshing ? "Refreshing" : "Refresh"}
            </button>
            <button className="button button-danger" onClick={signOut}>
              <LogOut size={18} aria-hidden="true" />
              Sign out
            </button>
          </nav>
        </div>
      </header>

      <section className="page">
        <div className="dashboard-header">
          <div>
            <h1>Lead dashboard</h1>
            <p>Review submissions, download resumes, and track attorney outreach.</p>
          </div>
        </div>

        <div className="stats" aria-label="Lead status summary">
          <div className="stat">
            <span>Total leads</span>
            <strong>{stats.total}</strong>
          </div>
          <div className="stat">
            <span>Pending</span>
            <strong>{stats.pending}</strong>
          </div>
          <div className="stat">
            <span>Reached out</span>
            <strong>{stats.reached}</strong>
          </div>
        </div>

        {error ? <div className="message error">{error}</div> : null}
        {notice ? <div className="message success">{notice}</div> : null}

        <div className="toolbar" aria-label="Lead filters">
          <div className="segmented-control">
            <button
              className={statusFilter === "ALL" ? "active" : ""}
              onClick={() => setStatusFilter("ALL")}
            >
              All
              <span>{stats.total}</span>
            </button>
            <button
              className={statusFilter === "PENDING" ? "active" : ""}
              onClick={() => setStatusFilter("PENDING")}
            >
              Pending
              <span>{stats.pending}</span>
            </button>
            <button
              className={statusFilter === "REACHED_OUT" ? "active" : ""}
              onClick={() => setStatusFilter("REACHED_OUT")}
            >
              Reached out
              <span>{stats.reached}</span>
            </button>
          </div>
          <div className="live-status">
            <label>
              <input
                checked={autoRefresh}
                onChange={(event) => setAutoRefresh(event.target.checked)}
                type="checkbox"
              />
              Live updates
            </label>
            <span>
              {lastUpdatedAt
                ? `Updated ${new Date(lastUpdatedAt).toLocaleTimeString()}`
                : "Waiting for first sync"}
            </span>
          </div>
        </div>

        <div className="panel table-wrap">
          {isLoading ? (
            <div className="empty-state">Loading leads...</div>
          ) : leads.length === 0 ? (
            <div className="empty-state">No leads submitted yet.</div>
          ) : visibleLeads.length === 0 ? (
            <div className="empty-state">No leads match this filter.</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Prospect</th>
                  <th>Email</th>
                  <th>Resume</th>
                  <th>Status</th>
                  <th>Submitted</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {visibleLeads.map((lead) => (
                  <tr key={lead.id}>
                    <td>
                      <strong>
                        {lead.first_name} {lead.last_name}
                      </strong>
                    </td>
                    <td>{lead.email}</td>
                    <td>{lead.resume_filename}</td>
                    <td>
                      <span
                        className={`status ${
                          lead.status === "PENDING" ? "pending" : "reached"
                        }`}
                      >
                        {lead.status === "PENDING" ? "Pending" : "Reached out"}
                      </span>
                    </td>
                    <td>{new Date(lead.created_at).toLocaleString()}</td>
                    <td>
                      <div className="row-actions">
                        <button
                          className="button button-secondary"
                          disabled={downloadingLeadId === lead.id}
                          onClick={() => downloadResume(lead)}
                        >
                          <Download size={17} aria-hidden="true" />
                          {downloadingLeadId === lead.id ? "Downloading..." : "Resume"}
                        </button>
                        <button
                          className="button button-primary"
                          disabled={lead.status === "REACHED_OUT"}
                          onClick={() => markReachedOut(lead.id)}
                        >
                          <Send size={17} aria-hidden="true" />
                          Mark reached
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>
    </main>
  );
}
