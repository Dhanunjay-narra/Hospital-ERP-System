"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { BedDouble, Plus, Bed, UserCheck, Stethoscope, LogOut, CheckCircle2, FileText } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function IPDPage() {
  const [admissions, setAdmissions] = useState<any[]>([]);
  const [beds, setBeds] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [wards, setWards] = useState<any[]>([]);
  const [showAdmitModal, setShowAdmitModal] = useState(false);
  const [showDischargeModal, setShowDischargeModal] = useState(false);
  const [selectedAdmission, setSelectedAdmission] = useState<any>(null);

  // Admission Form
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [selectedWard, setSelectedWard] = useState("");
  const [selectedBed, setSelectedBed] = useState("");
  const [diagnosis, setDiagnosis] = useState("");

  // Discharge Form
  const [dischargeDiag, setDischargeDiag] = useState("");
  const [summary, setSummary] = useState("");

  const loadData = async () => {
    try {
      const [admRes, bedRes, patRes, docRes, wardRes] = await Promise.all([
        ApiClient.get("/ipd/admissions"),
        ApiClient.get("/organization/beds"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
        ApiClient.get("/organization/wards"),
      ]);
      setAdmissions(admRes.items || []);
      setBeds(bedRes || []);
      setPatients(patRes.items || []);
      setDoctors(docRes.items || []);
      setWards(wardRes || []);

      if (patRes.items?.length) setSelectedPatient(patRes.items[0].id);
      if (docRes.items?.length) setSelectedDoctor(docRes.items[0].id);
      if (wardRes?.length) setSelectedWard(wardRes[0].id);
      const availBeds = (bedRes || []).filter((b: any) => b.status === "AVAILABLE");
      if (availBeds.length) setSelectedBed(availBeds[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAdmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/ipd/admissions", {
        patient_id: selectedPatient,
        primary_doctor_id: selectedDoctor,
        ward_id: selectedWard,
        bed_id: selectedBed,
        admitting_diagnosis: diagnosis,
        admission_type: "ELECTIVE",
      });
      setShowAdmitModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDischarge = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedAdmission) return;
    try {
      await ApiClient.post(`/ipd/admissions/${selectedAdmission.id}/discharge`, {
        discharge_diagnosis: dischargeDiag,
        discharge_summary: summary,
      });
      setShowDischargeModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Inpatient (IPD) & Bed Allocation Console
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Track inpatient admissions, real-time bed status, doctor daily rounds, and discharge summaries.
            </p>
          </div>
          <Button
            onClick={() => setShowAdmitModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Admit Inpatient
          </Button>
        </div>

        {/* Live Bed Matrix Visual */}
        <Card>
          <CardHeader>
            <CardTitle>Live Ward Bed Grid</CardTitle>
            <div className="flex gap-2 text-xs">
              <span className="flex items-center gap-1"><span className="w-3 h-3 bg-emerald-500 rounded-xs" /> Available</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 bg-rose-500 rounded-xs" /> Occupied</span>
            </div>
          </CardHeader>
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-3">
            {beds.map((bed) => (
              <div
                key={bed.id}
                className={`p-3 rounded-xl border flex flex-col items-center justify-center text-center space-y-1 transition ${
                  bed.status === "AVAILABLE"
                    ? "bg-emerald-50/50 border-emerald-200 text-emerald-900"
                    : "bg-rose-50/50 border-rose-200 text-rose-900"
                }`}
              >
                <Bed className={`w-6 h-6 ${bed.status === "AVAILABLE" ? "text-emerald-600" : "text-rose-600"}`} />
                <span className="font-bold text-xs">{bed.bed_number}</span>
                <span className="text-[10px] font-semibold uppercase">{bed.status}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Admissions Table */}
        <Card>
          <CardHeader>
            <CardTitle>Current Inpatient Records</CardTitle>
          </CardHeader>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Admission #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Attending Doctor</TableHead>
                <TableHead>Bed & Ward</TableHead>
                <TableHead>Admission Date</TableHead>
                <TableHead>Diagnosis</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {admissions.map((adm) => (
                <TableRow key={adm.id}>
                  <TableCell className="font-mono font-bold text-teal-800 text-xs">
                    {adm.admission_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{adm.patient?.first_name} {adm.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {adm.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">{adm.primary_doctor?.user?.first_name} {adm.primary_doctor?.user?.last_name}</p>
                    <p className="text-xs text-slate-400">{adm.primary_doctor?.specialization}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{adm.bed?.bed_number || "BED-ICU"}</Badge>
                    <span className="text-xs text-slate-500 block mt-0.5">{adm.ward?.name || "General Ward"}</span>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(adm.admission_date)}
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 truncate max-w-xs">{adm.admitting_diagnosis}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant={adm.status === "ADMITTED" ? "danger" : "success"}>
                      {adm.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {adm.status === "ADMITTED" && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedAdmission(adm);
                          setDischargeDiag(adm.admitting_diagnosis);
                          setShowDischargeModal(true);
                        }}
                        leftIcon={<LogOut className="w-3.5 h-3.5 text-rose-500" />}
                      >
                        Discharge
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Modal for Admitting Inpatient */}
        <Modal
          isOpen={showAdmitModal}
          onClose={() => setShowAdmitModal(false)}
          title="Admit Inpatient"
        >
          <form onSubmit={handleAdmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                Select Patient
              </label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 focus:border-teal-600 focus:outline-none"
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
              >
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.uhid} — {p.first_name} {p.last_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                Primary Attending Physician
              </label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 focus:border-teal-600 focus:outline-none"
                value={selectedDoctor}
                onChange={(e) => setSelectedDoctor(e.target.value)}
              >
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.user?.first_name} {d.user?.last_name} ({d.specialization})
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                  Ward
                </label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm"
                  value={selectedWard}
                  onChange={(e) => setSelectedWard(e.target.value)}
                >
                  {wards.map((w) => (
                    <option key={w.id} value={w.id}>{w.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                  Available Bed
                </label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm"
                  value={selectedBed}
                  onChange={(e) => setSelectedBed(e.target.value)}
                >
                  {beds.filter((b) => b.status === "AVAILABLE").map((b) => (
                    <option key={b.id} value={b.id}>{b.bed_number}</option>
                  ))}
                </select>
              </div>
            </div>

            <Input
              label="Admitting Diagnosis & Notes"
              required
              placeholder="e.g. Acute Appendicitis, Unstable Angina"
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
            />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAdmitModal(false)}>
                Cancel
              </Button>
              <Button type="submit">Complete Admission</Button>
            </div>
          </form>
        </Modal>

        {/* Modal for Discharge */}
        {selectedAdmission && (
          <Modal
            isOpen={showDischargeModal}
            onClose={() => setShowDischargeModal(false)}
            title={`Discharge Patient — ${selectedAdmission.patient?.first_name} ${selectedAdmission.patient?.last_name}`}
          >
            <form onSubmit={handleDischarge} className="space-y-4">
              <Input
                label="Final Discharge Diagnosis"
                required
                value={dischargeDiag}
                onChange={(e) => setDischargeDiag(e.target.value)}
              />
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                  Discharge Summary & Post-Hospitalization Care Plan
                </label>
                <textarea
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-xs"
                  rows={4}
                  required
                  placeholder="Patient recovered satisfactorily. Suture removal on day 10, oral analgesics as prescribed..."
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                />
              </div>
              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowDischargeModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" variant="danger">
                  Finalize Discharge & Release Bed
                </Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
