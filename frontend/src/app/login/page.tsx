"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Activity, Lock, Mail, ArrowRight, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { ApiClient } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@hospital.com");
  const [password, setPassword] = useState("Admin@123456");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const res = await ApiClient.post("/auth/login", {
        username_or_email: email,
        password: password,
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

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Subtle Background Glow */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-teal-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 border border-slate-100 z-10">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-teal-700 text-white shadow-lg shadow-teal-900/30 mb-4">
            <Activity className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold text-slate-800">ApexCare Hospital ERP</h1>
          <p className="text-xs text-slate-500 mt-1 uppercase font-semibold tracking-wider">
            Clinical Operations & Patient CRM Portal
          </p>
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
              <a href="#" className="text-xs text-teal-700 hover:underline font-medium">
                Forgot?
              </a>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="password"
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
              Sign In to System
            </Button>
          </div>
        </form>

        <div className="mt-6 pt-6 border-t border-slate-100 flex items-center justify-center gap-2 text-slate-400 text-xs">
          <ShieldCheck className="w-4 h-4 text-teal-600" />
          <span>HIPAA & HL7 Compliant Multi-Tenant Platform</span>
        </div>
      </div>
    </div>
  );
}
