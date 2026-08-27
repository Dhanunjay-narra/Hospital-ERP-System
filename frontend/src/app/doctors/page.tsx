"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Stethoscope, Clock, DollarSign, Calendar, MapPin, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<any[]>([]);
  const [filterSpec, setFilterSpec] = useState("");

  const loadDoctors = async () => {
    try {
      const res = await ApiClient.get("/doctors", { specialization: filterSpec });
      setDoctors(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, [filterSpec]);

  const daysMap = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Doctor & Provider Management
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Consultant profiles, medical qualifications, consultation fees, and weekly OPD duty rosters.
            </p>
          </div>
        </div>

        {/* Doctor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {doctors.map((doc) => (
            <Card key={doc.id} className="p-5 flex flex-col justify-between space-y-4 hover:border-teal-500 transition">
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-800 font-bold text-base flex items-center justify-center">
                      <Stethoscope className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-800">
                        {doc.user ? `${doc.user.first_name} ${doc.user.last_name}` : "Doctor"}
                      </h3>
                      <p className="text-xs text-teal-700 font-semibold">{doc.specialization}</p>
                    </div>
                  </div>
                  <Badge variant={doc.is_on_duty ? "success" : "neutral"}>
                    {doc.is_on_duty ? "On Duty" : "Off Duty"}
                  </Badge>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 text-xs text-slate-600">
                  <div className="flex justify-between">
                    <span className="text-slate-400">License #</span>
                    <span className="font-mono font-medium">{doc.license_number}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Qualifications</span>
                    <span className="font-medium">{doc.qualification} ({doc.experience_years} yrs exp)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Consultation Room</span>
                    <span className="font-medium text-slate-800">{doc.consultation_room || "Room 101"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">OPD Fee</span>
                    <span className="font-bold text-emerald-700">{formatCurrency(doc.consultation_fee)}</span>
                  </div>
                </div>

                {/* Working Days */}
                <div className="mt-3">
                  <p className="text-[11px] font-semibold text-slate-500 uppercase mb-1.5">Weekly Schedule</p>
                  <div className="flex gap-1">
                    {doc.schedules?.map((s: any) => (
                      <span
                        key={s.id}
                        className="px-2 py-0.5 text-[10px] font-bold bg-slate-100 text-slate-700 rounded"
                      >
                        {daysMap[s.day_of_week]}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <Button size="sm" variant="outline" className="w-full">
                View Calendar & Slots
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
