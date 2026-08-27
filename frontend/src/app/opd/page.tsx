"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { ClipboardList, Stethoscope, HeartPulse, Pill, CheckCircle2, UserCheck, Plus } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function OPDPage() {
  const [visits, setVisits] = useState<any[]>([]);
  const [selectedVisit, setSelectedVisit] = useState<any>(null);
  const [showConsultModal, setShowConsultModal] = useState(false);
  const [showVitalsModal, setShowVitalsModal] = useState(false);

  // Consultation Form
  const [diagnosis, setDiagnosis] = useState("");
  const [icd10, setIcd10] = useState("");
  const [notes, setNotes] = useState("");
  const [medicine, setMedicine] = useState("Amoxicillin 500mg");
  const [dosage, setDosage] = useState("1 tablet");
  const [frequency, setFrequency] = useState("1-0-1");
  const [duration, setDuration] = useState("5");

  // Vitals Form
  const [sbp, setSbp] = useState("120");
  const [dbp, setDbp] = useState("80");
  const [pulse, setPulse] = useState("72");
  const [temp, setTemp] = useState("37.0");
  const [spo2, setSpo2] = useState("99");

  const loadVisits = async () => {
    try {
      const res = await ApiClient.get("/opd/visits");
      setVisits(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadVisits();
  }, []);

  const openConsultation = (visit: any) => {
    setSelectedVisit(visit);
    setDiagnosis(visit.final_diagnosis || "");
    setNotes(visit.doctor_notes || "");
    setShowConsultModal(true);
  };

  const handleSaveConsultation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedVisit) return;
    try {
      // 1. Update Consultation
      await ApiClient.patch(`/opd/visits/${selectedVisit.id}/consultation`, {
        status: "COMPLETED",
        final_diagnosis: diagnosis,
        icd10_code: icd10,
        doctor_notes: notes,
      });

      // 2. Issue Electronic Prescription
      await ApiClient.post("/clinical/prescriptions", {
        patient_id: selectedVisit.patient_id,
        doctor_id: selectedVisit.doctor_id,
        opd_visit_id: selectedVisit.id,
        diagnosis_notes: diagnosis,
        items: [
          {
            medicine_name: medicine,
            dosage: dosage,
            frequency: frequency,
            duration_days: parseInt(duration) || 5,
            route: "ORAL",
            total_quantity: (parseInt(duration) || 5) * 2,
          },
        ],
      });

      setShowConsultModal(false);
      loadVisits();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleSaveVitals = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedVisit) return;
    try {
      await ApiClient.post("/opd/vitals", {
        patient_id: selectedVisit.patient_id,
        opd_visit_id: selectedVisit.id,
        systolic_bp: parseInt(sbp),
        diastolic_bp: parseInt(dbp),
        pulse_rate: parseInt(pulse),
        temperature_celsius: parseFloat(temp),
        spo2_percentage: parseFloat(spo2),
      });
      setShowVitalsModal(false);
      loadVisits();
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
              Doctor OPD Consultation Station
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Active patient consultation queue, clinical diagnosis, vitals capture, and digital prescription dispensing.
            </p>
          </div>
        </div>

        {/* OPD Queue List */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Queue Token</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Assigned Doctor</TableHead>
                <TableHead>Chief Complaint</TableHead>
                <TableHead>Vitals Recorded</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {visits.map((v) => (
                <TableRow key={v.id}>
                  <TableCell className="font-bold text-teal-800 text-sm">
                    #{v.queue_number || "1"}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{v.patient?.first_name} {v.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {v.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">{v.doctor?.user?.first_name} {v.doctor?.user?.last_name}</p>
                    <p className="text-xs text-teal-600">{v.doctor?.specialization}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 truncate max-w-xs">{v.chief_complaint || "Routine consultation"}</p>
                  </TableCell>
                  <TableCell>
                    {v.vitals?.length > 0 ? (
                      <span className="text-xs font-semibold text-emerald-700">
                        BP {v.vitals[0].systolic_bp}/{v.vitals[0].diastolic_bp} | P: {v.vitals[0].pulse_rate}
                      </span>
                    ) : (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedVisit(v);
                          setShowVitalsModal(true);
                        }}
                        leftIcon={<HeartPulse className="w-3 h-3 text-rose-500" />}
                      >
                        Add Vitals
                      </Button>
                    )}
                  </TableCell>
                  <TableCell>
                    <Badge variant={v.status === "COMPLETED" ? "success" : "warning"}>
                      {v.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant={v.status === "COMPLETED" ? "outline" : "primary"}
                      onClick={() => openConsultation(v)}
                      leftIcon={<Stethoscope className="w-3.5 h-3.5" />}
                    >
                      {v.status === "COMPLETED" ? "View EMR" : "Consult"}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Consultation Modal */}
        {selectedVisit && (
          <Modal
            isOpen={showConsultModal}
            onClose={() => setShowConsultModal(false)}
            title={`Clinical Encounter — ${selectedVisit.patient?.first_name} ${selectedVisit.patient?.last_name} (${selectedVisit.patient?.uhid})`}
            maxWidth="4xl"
          >
            <form onSubmit={handleSaveConsultation} className="space-y-5">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs flex justify-between">
                <div>
                  <span className="font-semibold text-slate-700">Chief Complaint:</span> {selectedVisit.chief_complaint || "Not specified"}
                </div>
                <div>
                  <span className="font-semibold text-slate-700">Allergies:</span> {selectedVisit.patient?.allergies_summary || "None reported"}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Input
                  label="Final Clinical Diagnosis"
                  required
                  placeholder="e.g. Acute Bronchitis, Essential Hypertension"
                  value={diagnosis}
                  onChange={(e) => setDiagnosis(e.target.value)}
                />
                <Input
                  label="ICD-10 Code"
                  placeholder="e.g. J20.9, I10"
                  value={icd10}
                  onChange={(e) => setIcd10(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                  Clinical Examination & Treatment Notes
                </label>
                <textarea
                  className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 focus:border-teal-600 focus:outline-none"
                  rows={3}
                  placeholder="Enter detailed physician notes, symptoms, physical examination..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </div>

              {/* Digital Prescription Builder */}
              <div className="p-4 bg-teal-50/50 border border-teal-200 rounded-xl space-y-3">
                <h4 className="text-xs font-bold text-teal-900 uppercase tracking-wide flex items-center gap-1.5">
                  <Pill className="w-4 h-4 text-teal-700" />
                  Electronic Prescription Pad
                </h4>
                <div className="grid grid-cols-4 gap-2">
                  <Input label="Medicine Name" value={medicine} onChange={(e) => setMedicine(e.target.value)} />
                  <Input label="Dosage" value={dosage} onChange={(e) => setDosage(e.target.value)} />
                  <Input label="Frequency" value={frequency} onChange={(e) => setFrequency(e.target.value)} />
                  <Input label="Duration (Days)" type="number" value={duration} onChange={(e) => setDuration(e.target.value)} />
                </div>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowConsultModal(false)}>
                  Cancel
                </Button>
                <Button type="submit" leftIcon={<CheckCircle2 className="w-4 h-4" />}>
                  Complete Encounter & Issue Rx
                </Button>
              </div>
            </form>
          </Modal>
        )}

        {/* Vitals Recording Modal */}
        {selectedVisit && (
          <Modal
            isOpen={showVitalsModal}
            onClose={() => setShowVitalsModal(false)}
            title="Record Patient Vitals"
          >
            <form onSubmit={handleSaveVitals} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <Input label="Systolic BP (mmHg)" type="number" required value={sbp} onChange={(e) => setSbp(e.target.value)} />
                <Input label="Diastolic BP (mmHg)" type="number" required value={dbp} onChange={(e) => setDbp(e.target.value)} />
              </div>
              <div className="grid grid-cols-3 gap-3">
                <Input label="Pulse (bpm)" type="number" required value={pulse} onChange={(e) => setPulse(e.target.value)} />
                <Input label="Temp (°C)" type="number" step="0.1" required value={temp} onChange={(e) => setTemp(e.target.value)} />
                <Input label="SpO2 (%)" type="number" required value={spo2} onChange={(e) => setSpo2(e.target.value)} />
              </div>
              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowVitalsModal(false)}>Cancel</Button>
                <Button type="submit">Save Vitals</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
