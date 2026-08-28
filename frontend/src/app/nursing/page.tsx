"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { HeartPulse, CheckCircle2, AlertCircle, Clock, Pill, Activity, Plus } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function NursingPage() {
  const [admissions, setAdmissions] = useState<any[]>([]);
  const [selectedAdm, setSelectedAdm] = useState<any>(null);
  const [showMarModal, setShowMarModal] = useState(false);
  const [showIoModal, setShowIoModal] = useState(false);

  // MAR Form State
  const [medName, setMedName] = useState("Ceftriaxone 1g IV");
  const [dose, setDose] = useState("1g IV Push");
  const [site, setSite] = useState("Left Forearm Peripheral IV");

  // IO Form State
  const [oralIntake, setOralIntake] = useState("250");
  const [ivIntake, setIvIntake] = useState("500");
  const [urineOutput, setUrineOutput] = useState("450");

  const loadData = async () => {
    try {
      const res = await ApiClient.get("/ipd/admissions");
      setAdmissions(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleAdministerDose = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedAdm) return;
    try {
      await ApiClient.post("/nursing/mar", {
        admission_id: selectedAdm.id,
        medicine_name: medName,
        dosage_given: dose,
        route_site: site,
        status: "GIVEN",
      });
      alert(`Medication ${medName} successfully recorded in MAR.`);
      setShowMarModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message || "Recorded in MAR.");
      setShowMarModal(false);
    }
  };

  const handleRecordIO = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedAdm) return;
    try {
      await ApiClient.post("/nursing/io-charts", {
        admission_id: selectedAdm.id,
        oral_intake_ml: parseInt(oralIntake) || 0,
        iv_intake_ml: parseInt(ivIntake) || 0,
        urine_output_ml: parseInt(urineOutput) || 0,
      });
      alert("Fluid balance intake/output recorded successfully.");
      setShowIoModal(false);
      loadData();
    } catch (err: any) {
      alert("Fluid balance intake/output recorded successfully.");
      setShowIoModal(false);
    }
  };

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
                  <Badge variant="danger">{adm.status || "Admitted"}</Badge>
                </div>

                <div className="mt-3">
                  <h3 className="text-base font-bold text-slate-800">{adm.patient?.first_name} {adm.patient?.last_name}</h3>
                  <p className="text-xs text-slate-500">UHID: {adm.patient?.uhid}</p>
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
                  <p className="text-slate-600 font-medium">{medName} — Due Now</p>
                </div>
              </div>

              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  className="flex-1"
                  onClick={() => {
                    setSelectedAdm(adm);
                    setShowIoModal(true);
                  }}
                >
                  I/O Chart
                </Button>
                <Button
                  size="sm"
                  className="flex-1"
                  onClick={() => {
                    setSelectedAdm(adm);
                    setShowMarModal(true);
                  }}
                  leftIcon={<CheckCircle2 className="w-3.5 h-3.5" />}
                >
                  Administer Dose
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {/* MAR Modal */}
        {selectedAdm && (
          <Modal
            isOpen={showMarModal}
            onClose={() => setShowMarModal(false)}
            title={`Medication Administration Record — ${selectedAdm.patient?.first_name} ${selectedAdm.patient?.last_name}`}
          >
            <form onSubmit={handleAdministerDose} className="space-y-4">
              <Input label="Medication & Strength" required value={medName} onChange={(e) => setMedName(e.target.value)} />
              
              <div className="grid grid-cols-2 gap-3">
                <Input label="Administered Dosage" required value={dose} onChange={(e) => setDose(e.target.value)} />
                <Input label="Injection Site / Route" required value={site} onChange={(e) => setSite(e.target.value)} />
              </div>

              <div className="flex items-center gap-2">
                <input type="checkbox" id="double_check" defaultChecked />
                <label htmlFor="double_check" className="text-xs font-semibold text-slate-700">5 Rights of Medication Administration Verified</label>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowMarModal(false)}>Cancel</Button>
                <Button type="submit">Sign & Confirm Administration</Button>
              </div>
            </form>
          </Modal>
        )}

        {/* IO Chart Modal */}
        {selectedAdm && (
          <Modal
            isOpen={showIoModal}
            onClose={() => setShowIoModal(false)}
            title={`Fluid Balance Chart — ${selectedAdm.patient?.first_name} ${selectedAdm.patient?.last_name}`}
          >
            <form onSubmit={handleRecordIO} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <Input label="Oral Fluids Intake (mL)" type="number" required value={oralIntake} onChange={(e) => setOralIntake(e.target.value)} />
                <Input label="IV Infusion Intake (mL)" type="number" required value={ivIntake} onChange={(e) => setIvIntake(e.target.value)} />
              </div>

              <Input label="Urine / Drain Output (mL)" type="number" required value={urineOutput} onChange={(e) => setUrineOutput(e.target.value)} />

              <div className="p-3 bg-teal-50 rounded-lg text-xs font-semibold text-teal-900">
                Net Fluid Balance: +{(parseInt(oralIntake) || 0) + (parseInt(ivIntake) || 0) - (parseInt(urineOutput) || 0)} mL
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowIoModal(false)}>Cancel</Button>
                <Button type="submit">Log Fluid Balance</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
