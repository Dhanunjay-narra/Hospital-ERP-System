"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { StatsCard } from "@/components/ui/StatsCard";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import {
  Users,
  Bed,
  CalendarCheck2,
  DollarSign,
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Clock,
  CheckCircle2,
  HeartPulse,
  Pill,
} from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function DashboardPage() {
  const [beds, setBeds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
        if (!token) {
          setLoading(false);
          return;
        }
        const bedsData = await ApiClient.get("/organization/beds");
        if (Array.isArray(bedsData)) {
          setBeds(bedsData);
        } else if (bedsData?.items) {
          setBeds(bedsData.items);
        }
      } catch (e) {
        console.error("Failed to load dashboard data", e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const totalBeds = beds.length || 15;
  const availableBeds = beds.filter((b) => b.status === "AVAILABLE").length || 10;
  const occupiedBeds = totalBeds - availableBeds;
  const occupancyRate = Math.round((occupiedBeds / totalBeds) * 100);

  return (
    <AppLayout>
      <div className="space-y-6">
        {/* Welcome Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Hospital Operations Command Center
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Live multi-department metrics, patient flow, and clinical status.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" size="sm" leftIcon={<Clock className="w-4 h-4" />}>
              Live Status: Active
            </Button>
            <Button size="sm" leftIcon={<Activity className="w-4 h-4" />}>
              Emergency Intake
            </Button>
          </div>
        </div>

        {/* Top Operational Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard
            title="Total Active Patients"
            value="1,428"
            change="12.4%"
            isPositive={true}
            icon={<Users className="w-6 h-6 text-teal-700" />}
            iconBgColor="bg-teal-50"
          />
          <StatsCard
            title="Bed Occupancy"
            value={`${occupancyRate}%`}
            change="4.1%"
            isPositive={false}
            icon={<Bed className="w-6 h-6 text-blue-700" />}
            iconBgColor="bg-blue-50"
          />
          <StatsCard
            title="Today's Appointments"
            value="142"
            change="18%"
            isPositive={true}
            icon={<CalendarCheck2 className="w-6 h-6 text-indigo-700" />}
            iconBgColor="bg-indigo-50"
          />
          <StatsCard
            title="Daily Revenue"
            value="$42,850"
            change="8.5%"
            isPositive={true}
            icon={<DollarSign className="w-6 h-6 text-emerald-700" />}
            iconBgColor="bg-emerald-50"
          />
        </div>

        {/* Live Patient Flow & Department Queues */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* OPD Live Queue */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <div>
                <CardTitle>Live OPD Consultation Queue</CardTitle>
                <p className="text-xs text-slate-500 mt-0.5">Real-time outpatient tokens and waiting status</p>
              </div>
              <Badge variant="brand">8 Active Doctors</Badge>
            </CardHeader>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Token #</TableHead>
                  <TableHead>Patient</TableHead>
                  <TableHead>Doctor / Specialization</TableHead>
                  <TableHead>Wait Time</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell className="font-bold text-teal-700">#A-042</TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">Sarah Jenkins</p>
                    <p className="text-xs text-slate-400">UHID: APX-90812</p>
                  </TableCell>
                  <TableCell>Dr. Robert Vance (Cardiology)</TableCell>
                  <TableCell>12 mins</TableCell>
                  <TableCell>
                    <Badge variant="warning">In Consultation</Badge>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-bold text-teal-700">#A-043</TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">Michael Chen</p>
                    <p className="text-xs text-slate-400">UHID: APX-90815</p>
                  </TableCell>
                  <TableCell>Dr. Elena Rostova (Orthopedics)</TableCell>
                  <TableCell>4 mins</TableCell>
                  <TableCell>
                    <Badge variant="info">Waiting</Badge>
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell className="font-bold text-teal-700">#A-044</TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">Amanda Foster</p>
                    <p className="text-xs text-slate-400">UHID: APX-90820</p>
                  </TableCell>
                  <TableCell>Dr. Robert Vance (Cardiology)</TableCell>
                  <TableCell>Next</TableCell>
                  <TableCell>
                    <Badge variant="neutral">Checked In</Badge>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </Card>

          {/* Department Bed Occupancy Matrix */}
          <Card>
            <CardHeader>
              <CardTitle>Ward & Bed Matrix</CardTitle>
              <Badge variant="neutral">{availableBeds} Available</Badge>
            </CardHeader>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-700">General Ward A</span>
                  <span className="text-slate-500">8 / 10 Beds Occupied</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-teal-600 h-2.5 rounded-full" style={{ width: "80%" }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-700">Intensive Care Unit (ICU)</span>
                  <span className="text-slate-500">3 / 5 Beds Occupied</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-rose-500 h-2.5 rounded-full" style={{ width: "60%" }}></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-700">Pediatric Ward</span>
                  <span className="text-slate-500">2 / 6 Beds Occupied</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                  <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: "33%" }}></div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Emergency Rapid Triage</span>
                <span className="font-semibold text-emerald-600">3 Resuscitation Bays Open</span>
              </div>
            </div>
          </Card>
        </div>

        {/* Diagnostics & Operations Quick Health */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 bg-rose-50 text-rose-600 rounded-xl">
              <HeartPulse className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Emergency Load</p>
              <p className="text-base font-bold text-slate-800">4 Active Trauma</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Operation Theatres</p>
              <p className="text-base font-bold text-slate-800">2 In Surgery / 1 Ready</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl">
              <Pill className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Pharmacy Queue</p>
              <p className="text-base font-bold text-slate-800">18 Prescriptions Pending</p>
            </div>
          </Card>

          <Card className="p-4 flex items-center gap-3">
            <div className="p-3 bg-amber-50 text-amber-600 rounded-xl">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs text-slate-500">Critical Lab Findings</p>
              <p className="text-base font-bold text-slate-800">2 Panic Alerts</p>
            </div>
          </Card>
        </div>
      </div>
    </AppLayout>
  );
}
