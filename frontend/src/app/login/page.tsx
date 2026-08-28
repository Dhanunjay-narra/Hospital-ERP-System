"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Activity, Lock, Mail, ArrowRight, ShieldCheck, UserCheck, Stethoscope, HeartPulse, CreditCard, UserPlus, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ApiClient } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@hospital.com");
  const [password, setPassword] = useState("Admin@123456");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const performLogin = async (userEmail: string, userPass: string) => {
    setIsLoading(true);
    setError("");

    try {
      const res = await ApiClient.post("/auth/login", {
        username_or_email: userEmail,
        password: userPass,
      });

      localStorage.setItem("access_token", res.access_token);
      localStorage.setItem("user_info", JSON.stringify(res.user));
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Invalid email or password");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await performLogin(email, password);
  };

  const quickRoles = [
    {
      title: "Super Admin",
      role: "Full Platform Access",
      email: "admin@hospital.com",
      pass: "Admin@123456",
      icon: <UserCheck className="w-4 h-4 text-amber-600" />,
      bg: "hover:bg-amber-50 hover:border-amber-400 border-slate-200",
    },
    {
      title: "Chief Doctor",
      role: "EMR, OPD & Surgeries",
      email: "doctor@hospital.com",
      pass: "Doctor@123456",
      icon: <Stethoscope className="w-4 h-4 text-teal-600" />,
      bg: "hover:bg-teal-50 hover:border-teal-400 border-slate-200",
    },
    {
      title: "Nurse Station",
      role: "e-MAR, Vitals & Beds",
      email: "nurse@hospital.com",
      pass: "Nurse@123456",
      icon: <HeartPulse className="w-4 h-4 text-rose-600" />,
      bg: "hover:bg-rose-50 hover:border-rose-400 border-slate-200",
    },
    {
      title: "Billing Cashier",
      role: "POS Invoices & Claims",
      email: "billing@hospital.com",
      pass: "Billing@123456",
      icon: <CreditCard className="w-4 h-4 text-indigo-600" />,
      bg: "hover:bg-indigo-50 hover:border-indigo-400 border-slate-200",
    },
    {
      title: "Receptionist",
      role: "Appointments & Queue",
      email: "reception@hospital.com",
      pass: "Reception@123456",
      icon: <UserPlus className="w-4 h-4 text-blue-600" />,
      bg: "hover:bg-blue-50 hover:border-blue-400 border-slate-200",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Subtle Background Glow */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-teal-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-lg bg-white rounded-2xl shadow-2xl p-8 border border-slate-100 z-10">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-teal-700 text-white shadow-lg shadow-teal-900/30 mb-3">
            <Activity className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-slate-800">ApexCare Hospital ERP</h1>
          <p className="text-xs text-slate-500 mt-1 uppercase font-semibold tracking-wider">
            Clinical Operations & Patient CRM Portal
          </p>
        </div>

        {/* 1-Click Instant Quick Demo Login Bar */}
        <div className="mb-6 p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-teal-600 animate-pulse" />
              1-Click Instant Demo Login
            </span>
            <span className="text-[10px] text-teal-700 font-semibold bg-teal-50 px-2 py-0.5 rounded-full">
              Credentials Included
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {quickRoles.map((r) => (
              <button
                key={r.email}
                type="button"
                disabled={isLoading}
                onClick={() => {
                  setEmail(r.email);
                  setPassword(r.pass);
                  performLogin(r.email, r.pass);
                }}
                className={`flex flex-col items-start p-2 rounded-lg border bg-white text-left transition shadow-sm ${r.bg}`}
              >
                <div className="flex items-center gap-1.5 w-full">
                  {r.icon}
                  <span className="text-xs font-bold text-slate-800 truncate">{r.title}</span>
                </div>
                <span className="text-[10px] text-slate-500 truncate w-full mt-0.5">{r.role}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-3 text-xs bg-rose-50 border border-rose-200 text-rose-700 rounded-lg font-medium">
              {error}
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5 uppercase">
              Username or Email
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:border-teal-600 focus:ring-2 focus:ring-teal-500/20 outline-none transition"
                placeholder="admin@hospital.com"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-slate-700 uppercase">
                Password
              </label>
              <span className="text-[11px] text-teal-700 font-mono font-semibold">
                Pre-filled: {password}
              </span>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-lg focus:border-teal-600 focus:ring-2 focus:ring-teal-500/20 outline-none transition"
                placeholder="••••••••"
              />
            </div>
          </div>

          <div className="pt-2">
            <Button
              type="submit"
              isLoading={isLoading}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold text-sm shadow-md"
              rightIcon={<ArrowRight className="w-4 h-4 ml-1" />}
            >
              Sign In to System (1-Click)
            </Button>
          </div>
        </form>

        <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-center gap-2 text-slate-400 text-xs">
          <ShieldCheck className="w-4 h-4 text-teal-600" />
          <span>HIPAA & HL7 Compliant Multi-Tenant Platform</span>
        </div>
      </div>
    </div>
  );
}
