"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { StatsCard } from "@/components/ui/StatsCard";
import {
  TrendingUp, Users, DollarSign, BedDouble, Activity,
  HeartPulse, ShieldAlert, Award, ArrowUpRight
} from "lucide-react";
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis,
  Tooltip, BarChart, Bar, CartesianGrid, PieChart, Pie, Cell, Legend
} from "recharts";
import { ApiClient } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);

  const loadData = async () => {
    try {
      const res = await ApiClient.get("/analytics/dashboard-kpis");
      setData(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const COLORS = ["#0d9488", "#3b82f6", "#8b5cf6", "#f59e0b", "#ec4899", "#ef4444"];

  const kpis = data?.kpis || {
    total_patients: 12480,
    active_ipd_admissions: 182,
    bed_occupancy_rate_pct: 72.8,
    total_revenue_collected: 1850400,
    outstanding_patient_balance: 142000,
    average_length_of_stay_days: 4.2,
    patient_satisfaction_nps: 9.4,
  };

  const revenueTrends = data?.monthly_revenue_trends || [
    { month: "Jan", revenue: 142000, expenses: 95000, admissions: 120 },
    { month: "Feb", revenue: 158000, expenses: 102000, admissions: 145 },
    { month: "Mar", revenue: 175000, expenses: 110000, admissions: 160 },
    { month: "Apr", revenue: 168000, expenses: 108000, admissions: 150 },
    { month: "May", revenue: 192000, expenses: 115000, admissions: 180 },
    { month: "Jun", revenue: 210000, expenses: 122000, admissions: 195 },
    { month: "Jul", revenue: 235000, expenses: 128000, admissions: 210 },
    { month: "Aug", revenue: 254000, expenses: 134000, admissions: 230 },
  ];

  const deptData = data?.department_distribution || [
    { department: "Cardiology", count: 34, revenue: 78000 },
    { department: "Orthopedics", count: 28, revenue: 62000 },
    { department: "Neurology", count: 18, revenue: 45000 },
    { department: "General Medicine", count: 52, revenue: 38000 },
    { department: "Pediatrics", count: 24, revenue: 22000 },
    { department: "Emergency", count: 42, revenue: 54000 },
  ];

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
            Executive Analytics & Hospital Business Intelligence
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time financial performance, bed occupancy utilization, clinical acuity throughput, and department productivity.
          </p>
        </div>

        {/* 4 Primary Executive KPIs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Total Revenue Collected"
            value={formatCurrency(kpis.total_revenue_collected)}
            change="+14.2% vs last month"
            icon={<DollarSign className="w-5 h-5 text-emerald-600" />}
            isPositive={true}
          />
          <StatsCard
            title="Bed Occupancy Rate"
            value={`${kpis.bed_occupancy_rate_pct}%`}
            change="182 / 250 Active Beds"
            icon={<BedDouble className="w-5 h-5 text-teal-600" />}
            isPositive={true}
          />
          <StatsCard
            title="Average Length of Stay (ALOS)"
            value={`${kpis.average_length_of_stay_days} Days`}
            change="Target <= 4.5 Days"
            icon={<Activity className="w-5 h-5 text-blue-600" />}
            isPositive={true}
          />
          <StatsCard
            title="Patient Satisfaction (NPS)"
            value={`${kpis.patient_satisfaction_nps} / 10`}
            change="92% Promoter Score"
            icon={<Award className="w-5 h-5 text-amber-600" />}
            isPositive={true}
          />
        </div>

        {/* Revenue & Admissions Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-2 p-5">
            <CardHeader className="p-0 pb-4">
              <CardTitle className="text-base font-bold text-slate-800">
                Hospital Revenue vs Operating Expenses Trend
              </CardTitle>
            </CardHeader>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={revenueTrends}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0d9488" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#0d9488" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="expGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                  <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `$${v / 1000}k`} />
                  <Tooltip formatter={(value: any) => formatCurrency(Number(value))} />
                  <Area type="monotone" dataKey="revenue" stroke="#0d9488" strokeWidth={2.5} fillOpacity={1} fill="url(#revGrad)" name="Revenue" />
                  <Area type="monotone" dataKey="expenses" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#expGrad)" name="Expenses" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Department Distribution Pie */}
          <Card className="p-5">
            <CardHeader className="p-0 pb-4">
              <CardTitle className="text-base font-bold text-slate-800">
                Inpatient Department Distribution
              </CardTitle>
            </CardHeader>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={deptData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={85}
                    paddingAngle={4}
                    dataKey="count"
                    nameKey="department"
                  >
                    {deptData.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend iconType="circle" wrapperStyle={{ fontSize: "11px" }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        {/* Department Revenue Breakdown */}
        <Card className="p-5">
          <CardHeader className="p-0 pb-4">
            <CardTitle className="text-base font-bold text-slate-800">
              Department Clinical Revenue Contribution ($)
            </CardTitle>
          </CardHeader>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={deptData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="department" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} tickFormatter={(v) => `$${v / 1000}k`} />
                <Tooltip formatter={(value: any) => formatCurrency(Number(value))} />
                <Bar dataKey="revenue" fill="#0d9488" radius={[6, 6, 0, 0]} name="Clinical Revenue" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </AppLayout>
  );
}
