"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { HeartPulse, CheckCircle2, AlertCircle, Clock, Pill, Activity } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function NursingPage() {
  const [admissions, setAdmissions] = useState<any[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await ApiClient.get("/ipd/admissions", { status: "ADMITTED" });
        setAdmissions(res.items || []);
      } catch (e) {
        console.error(e);
      }
    };
    loadData();
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Nursing Station & Medication Administration (e-MAR)
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Active inpatients care roster, timed medication administration, fluid balance charts, and shift notes.
            </p>
          </div>
        </div>

        {/* Nursing Inpatient Roster */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {admissions.map((adm) => (
            <Card key={adm.id} className="p-5 flex flex-col justify-between space-y-4 hover:border-teal-500 transition">
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-teal-800 bg-teal-50 px-2.5 py-1 rounded-lg">
                    {adm.bed?.bed_number || "BED-ICU"}
                  </span>
                  <Badge variant="danger">Admitted</Badge>
                </div>

                <div className="mt-3">
                  <h3 className="text-base font-bold text-slate-800">{adm.patient?.first_name} {adm.patient?.last_name}</h3>
                  <p className="text-xs text-slate-500">UHID: {adm.patient?.uhid} • Age: {adm.patient?.age || "45"} yrs</p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Diagnosis</span>
                    <span className="font-semibold text-slate-800">{adm.admitting_diagnosis}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Attending Physician</span>
                    <span className="font-medium text-slate-700">{adm.primary_doctor?.user?.first_name} {adm.primary_doctor?.user?.last_name}</span>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-slate-50 rounded-lg space-y-1.5 text-xs">
                  <p className="font-semibold text-slate-700 flex items-center gap-1.5">
                    <Pill className="w-3.5 h-3.5 text-teal-700" />
                    Next Scheduled Dose
                  </p>
                  <p className="text-slate-600 font-medium">Metoprolol 25mg — Due at 14:00</p>
                </div>
              </div>

              <div className="flex gap-2">
                <Button size="sm" variant="outline" className="flex-1">
                  I/O Chart
                </Button>
                <Button size="sm" className="flex-1" leftIcon={<CheckCircle2 className="w-3.5 h-3.5" />}>
                  Administer Dose
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
