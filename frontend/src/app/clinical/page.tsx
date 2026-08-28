"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { FileHeart, Pill, Stethoscope, Clock, ShieldAlert, Plus } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function ClinicalPage() {
  const [prescriptions, setPrescriptions] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [showRxModal, setShowRxModal] = useState(false);

  // Form
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [medName, setMedName] = useState("Amoxicillin 500mg");
  const [dosage, setDosage] = useState("500mg");
  const [frequency, setFrequency] = useState("TID (Three times daily)");
  const [duration, setDuration] = useState("7");
  const [instructions, setInstructions] = useState("Take after meals with full glass of water");

  const loadData = async () => {
    try {
      const [rxRes, patRes, docRes] = await Promise.all([
        ApiClient.get("/clinical/prescriptions"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
      ]);
      setPrescriptions(rxRes.items || []);
      setPatients(patRes.items || []);
      setDoctors(docRes.items || []);
      if (patRes.items?.length) setSelectedPatient(patRes.items[0].id);
      if (docRes.items?.length) setSelectedDoctor(docRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreatePrescription = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/clinical/prescriptions", {
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
        issued_date: new Date().toISOString(),
        items: [
          {
            medicine_name: medName,
            dosage: dosage,
            frequency: frequency,
            duration_days: parseInt(duration) || 7,
            instructions: instructions,
          },
        ],
      });
      setShowRxModal(false);
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
              Clinical Records & Electronic Medical Records (EMR)
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Longitudinal electronic health records, active electronic prescriptions, and diagnostic timeline.
            </p>
          </div>
          <Button
            onClick={() => setShowRxModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Issue Electronic Prescription
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Issued Electronic Prescriptions</CardTitle>
            <Badge variant="brand">{prescriptions.length} Active Prescriptions</Badge>
          </CardHeader>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Rx Number</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Doctor</TableHead>
                <TableHead>Issued Date</TableHead>
                <TableHead>Medications Prescribed</TableHead>
                <TableHead>Dispense Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {prescriptions.map((rx) => (
                <TableRow key={rx.id}>
                  <TableCell className="font-mono font-bold text-teal-800 text-xs">
                    {rx.prescription_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{rx.patient?.first_name} {rx.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {rx.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">{rx.doctor?.user?.first_name} {rx.doctor?.user?.last_name}</p>
                    <p className="text-xs text-teal-600">{rx.doctor?.specialization}</p>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(rx.issued_date)}
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      {rx.items?.map((item: any) => (
                        <div key={item.id} className="text-xs">
                          <span className="font-semibold text-slate-800">{item.medicine_name}</span>
                          <span className="text-slate-500"> — {item.dosage} ({item.frequency}, {item.duration_days} days)</span>
                        </div>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={rx.status === "DISPENSED" ? "success" : "warning"}>
                      {rx.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Prescription Modal */}
        <Modal
          isOpen={showRxModal}
          onClose={() => setShowRxModal(false)}
          title="Issue Electronic Prescription (e-Rx)"
        >
          <form onSubmit={handleCreatePrescription} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Prescribing Physician</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedDoctor} onChange={(e) => setSelectedDoctor(e.target.value)}>
                  {doctors.map((d) => (
                    <option key={d.id} value={d.id}>{d.user?.first_name} {d.user?.last_name} ({d.specialization})</option>
                  ))}
                </select>
              </div>
            </div>

            <Input label="Medicine Name & Formulation" required value={medName} onChange={(e) => setMedName(e.target.value)} />

            <div className="grid grid-cols-3 gap-3">
              <Input label="Dosage" required value={dosage} onChange={(e) => setDosage(e.target.value)} />
              <Input label="Frequency" required value={frequency} onChange={(e) => setFrequency(e.target.value)} />
              <Input label="Duration (Days)" type="number" required value={duration} onChange={(e) => setDuration(e.target.value)} />
            </div>

            <Input label="Patient Instructions & Dietary Notes" required value={instructions} onChange={(e) => setInstructions(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowRxModal(false)}>Cancel</Button>
              <Button type="submit">Sign & Authorize e-Rx</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
