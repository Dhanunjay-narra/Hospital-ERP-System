"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { ShieldAlert, Plus, HeartPulse, Activity, AlertTriangle, UserCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function EmergencyPage() {
  const [triages, setTriages] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [priority, setPriority] = useState("RED");
  const [complaint, setComplaint] = useState("");
  const [bay, setBay] = useState("Resuscitation Bay 1");
  const [sbp, setSbp] = useState("90");
  const [dbp, setDbp] = useState("60");
  const [pulse, setPulse] = useState("120");
  const [spo2, setSpo2] = useState("91");

  const loadData = async () => {
    try {
      const [tRes, pRes] = await Promise.all([
        ApiClient.get("/emergency/triage"),
        ApiClient.get("/patients"),
      ]);
      setTriages(tRes.items || []);
      setPatients(pRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateTriage = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/emergency/triage", {
        patient_id: selectedPatient,
        priority_level: priority,
        chief_complaint: complaint,
        assigned_bay: bay,
        systolic_bp: parseInt(sbp),
        diastolic_bp: parseInt(dbp),
        pulse_rate: parseInt(pulse),
        spo2_percentage: parseFloat(spo2),
        airway_compromised: priority === "RED",
      });
      setShowAddModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const priorityColor = (p: string) => {
    switch (p) {
      case "RED": return "bg-red-600 text-white font-bold animate-pulse";
      case "AMBER": return "bg-amber-500 text-white font-bold";
      case "YELLOW": return "bg-yellow-400 text-slate-900 font-bold";
      case "GREEN": return "bg-emerald-500 text-white font-bold";
      default: return "bg-blue-500 text-white";
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Emergency & Acute Trauma Command Center
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Manchester / ESI 5-Level Triage, resuscitation bay tracking, rapid trauma intake, and crisis coordination.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            variant="danger"
            leftIcon={<ShieldAlert className="w-4 h-4" />}
            size="sm"
          >
            Rapid Emergency Intake
          </Button>
        </div>

        {/* Priority Counts */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-red-700">Level 1: Resuscitation</span>
            <p className="text-xl font-black text-red-700 mt-1">
              {triages.filter((t) => t.priority_level === "RED").length} Patients
            </p>
          </div>
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-amber-700">Level 2: Emergent</span>
            <p className="text-xl font-black text-amber-700 mt-1">
              {triages.filter((t) => t.priority_level === "AMBER").length} Patients
            </p>
          </div>
          <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-yellow-800">Level 3: Urgent</span>
            <p className="text-xl font-black text-yellow-800 mt-1">
              {triages.filter((t) => t.priority_level === "YELLOW").length} Patients
            </p>
          </div>
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-emerald-700">Level 4: Less Urgent</span>
            <p className="text-xl font-black text-emerald-700 mt-1">
              {triages.filter((t) => t.priority_level === "GREEN").length} Patients
            </p>
          </div>
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-blue-700">Level 5: Non-Urgent</span>
            <p className="text-xl font-black text-blue-700 mt-1">
              {triages.filter((t) => t.priority_level === "BLUE").length} Patients
            </p>
          </div>
        </div>

        {/* Triage Live Board */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ER Case #</TableHead>
                <TableHead>Triage Priority</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Assigned Trauma Bay</TableHead>
                <TableHead>Chief Complaint</TableHead>
                <TableHead>Triage Vitals</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {triages.map((t) => (
                <TableRow key={t.id}>
                  <TableCell className="font-mono font-bold text-xs text-rose-900">
                    {t.triage_number}
                  </TableCell>
                  <TableCell>
                    <span className={`px-2.5 py-1 text-xs rounded-full ${priorityColor(t.priority_level)}`}>
                      {t.priority_level}
                    </span>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{t.patient?.first_name} {t.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {t.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{t.assigned_bay}</Badge>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 font-medium">{t.chief_complaint}</p>
                  </TableCell>
                  <TableCell>
                    <span className="text-xs font-semibold text-rose-700">
                      BP {t.systolic_bp}/{t.diastolic_bp} | P: {t.pulse_rate} | SpO2: {t.spo2_percentage}%
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge variant="warning">{t.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Rapid Intake Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Emergency Trauma Registration & Triage"
        >
          <form onSubmit={handleCreateTriage} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
              >
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Triage Priority</label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 font-bold"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  <option value="RED">RED — Resuscitation (Immediate)</option>
                  <option value="AMBER">AMBER — Emergent (&lt; 10 min)</option>
                  <option value="YELLOW">YELLOW — Urgent (&lt; 60 min)</option>
                  <option value="GREEN">GREEN — Less Urgent</option>
                  <option value="BLUE">BLUE — Non-Urgent</option>
                </select>
              </div>

              <Input label="Assigned Bay" value={bay} onChange={(e) => setBay(e.target.value)} />
            </div>

            <Input
              label="Emergency Chief Complaint & Trauma Mechanism"
              required
              placeholder="e.g. Severe chest pain radiating to left arm, Motor vehicle accident"
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
            />

            <div className="grid grid-cols-4 gap-2">
              <Input label="Systolic BP" type="number" value={sbp} onChange={(e) => setSbp(e.target.value)} />
              <Input label="Diastolic BP" type="number" value={dbp} onChange={(e) => setDbp(e.target.value)} />
              <Input label="Pulse (bpm)" type="number" value={pulse} onChange={(e) => setPulse(e.target.value)} />
              <Input label="SpO2 (%)" type="number" value={spo2} onChange={(e) => setSpo2(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit" variant="danger">Dispatch to Trauma Bay</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
