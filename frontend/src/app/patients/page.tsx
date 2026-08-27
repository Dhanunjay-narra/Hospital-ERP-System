"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { UserCheck, Plus, Search, Eye, Calendar, HeartPulse, FileText, ShieldAlert, Activity } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function PatientsPage() {
  const [patients, setPatients] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [selectedPatient360, setSelectedPatient360] = useState<any>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [show360Modal, setShow360Modal] = useState(false);

  // Form State
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [dob, setDob] = useState("1990-01-01");
  const [gender, setGender] = useState("MALE");
  const [bloodGroup, setBloodGroup] = useState("O+");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [insurance, setInsurance] = useState("BlueCross");
  const [allergies, setAllergies] = useState("");

  const loadPatients = async () => {
    try {
      const res = await ApiClient.get("/patients", { search });
      setPatients(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadPatients();
  }, [search]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/patients", {
        first_name: firstName,
        last_name: lastName,
        date_of_birth: dob,
        gender,
        blood_group: bloodGroup,
        phone_number: phone,
        email,
        address,
        primary_insurance_provider: insurance,
        allergies_summary: allergies,
      });
      setShowAddModal(false);
      // Reset
      setFirstName("");
      setLastName("");
      setPhone("");
      setEmail("");
      loadPatients();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const openPatient360 = async (patientId: string) => {
    try {
      const res = await ApiClient.get(`/patients/${patientId}/360`);
      setSelectedPatient360(res);
      setShow360Modal(true);
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
              Master Patient Registry & 360° Command Center
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Search by UHID, Demographics, or Phone; view longitudinal clinical timelines and patient engagement.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Register New Patient
          </Button>
        </div>

        {/* Search Bar */}
        <Card className="p-4">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
            <input
              type="text"
              placeholder="Search by UHID (e.g. APX-2026-00001), Name, Phone number, or Email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:border-teal-600 focus:ring-2 focus:ring-teal-500/20 outline-none"
            />
          </div>
        </Card>

        {/* Patients Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>UHID</TableHead>
                <TableHead>Patient Demographics</TableHead>
                <TableHead>Contact & Address</TableHead>
                <TableHead>Blood Group</TableHead>
                <TableHead>Insurance</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {patients.map((p) => (
                <TableRow key={p.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {p.uhid}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{p.first_name} {p.last_name}</p>
                    <p className="text-xs text-slate-400">{p.age} yrs • {p.gender}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700">{p.phone_number}</p>
                    <p className="text-xs text-slate-400 truncate max-w-xs">{p.email || p.address || "-"}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{p.blood_group || "N/A"}</Badge>
                  </TableCell>
                  <TableCell>
                    <span className="text-xs text-slate-600 font-medium">
                      {p.primary_insurance_provider || "Self Pay"}
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge variant={p.status === "ACTIVE" ? "success" : "neutral"}>
                      {p.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => openPatient360(p.id)}
                      leftIcon={<Eye className="w-3.5 h-3.5" />}
                    >
                      Patient 360°
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Patient 360 Modal */}
        {selectedPatient360 && (
          <Modal
            isOpen={show360Modal}
            onClose={() => setShow360Modal(false)}
            title={`Patient 360° Profile — ${selectedPatient360.patient.first_name} ${selectedPatient360.patient.last_name}`}
            maxWidth="4xl"
          >
            <div className="space-y-6">
              {/* Header Info Banner */}
              <div className="p-4 bg-teal-50 border border-teal-200 rounded-xl flex flex-wrap items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-teal-900 bg-white px-2 py-0.5 rounded shadow-xs">
                      {selectedPatient360.patient.uhid}
                    </span>
                    <h2 className="text-lg font-bold text-slate-800">
                      {selectedPatient360.patient.first_name} {selectedPatient360.patient.last_name}
                    </h2>
                  </div>
                  <p className="text-xs text-slate-600 mt-1">
                    {selectedPatient360.patient.age} years • {selectedPatient360.patient.gender} • Blood Group: {selectedPatient360.patient.blood_group} • Phone: {selectedPatient360.patient.phone_number}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Badge variant="brand">Insurance: {selectedPatient360.patient.primary_insurance_provider || "Self Pay"}</Badge>
                </div>
              </div>

              {/* Statistics Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
                  <p className="text-[11px] text-slate-500 uppercase font-semibold">Total Appointments</p>
                  <p className="text-xl font-bold text-slate-800 mt-0.5">{selectedPatient360.total_appointments}</p>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
                  <p className="text-[11px] text-slate-500 uppercase font-semibold">OPD Consultations</p>
                  <p className="text-xl font-bold text-slate-800 mt-0.5">{selectedPatient360.total_opd_visits}</p>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
                  <p className="text-[11px] text-slate-500 uppercase font-semibold">Hospital Admissions</p>
                  <p className="text-xl font-bold text-slate-800 mt-0.5">{selectedPatient360.total_admissions}</p>
                </div>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-center">
                  <p className="text-[11px] text-slate-500 uppercase font-semibold">Active Prescriptions</p>
                  <p className="text-xl font-bold text-teal-700 mt-0.5">{selectedPatient360.active_prescriptions_count}</p>
                </div>
              </div>

              {/* Clinical Snapshot */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="p-4">
                  <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wide flex items-center gap-1.5 mb-3">
                    <HeartPulse className="w-4 h-4 text-rose-500" />
                    Latest Recorded Vitals
                  </h4>
                  {selectedPatient360.recent_vitals ? (
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="p-2 bg-slate-50 rounded">BP: <span className="font-bold">{selectedPatient360.recent_vitals.bp}</span></div>
                      <div className="p-2 bg-slate-50 rounded">Pulse: <span className="font-bold">{selectedPatient360.recent_vitals.pulse} bpm</span></div>
                      <div className="p-2 bg-slate-50 rounded">Temp: <span className="font-bold">{selectedPatient360.recent_vitals.temp} °C</span></div>
                      <div className="p-2 bg-slate-50 rounded">SpO2: <span className="font-bold">{selectedPatient360.recent_vitals.spo2} %</span></div>
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400">No recorded vitals yet.</p>
                  )}
                </Card>

                <Card className="p-4">
                  <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wide flex items-center gap-1.5 mb-3">
                    <ShieldAlert className="w-4 h-4 text-amber-500" />
                    Documented Allergies & Alerts
                  </h4>
                  <p className="text-xs text-slate-700 bg-amber-50 p-2 rounded border border-amber-100">
                    {selectedPatient360.patient.allergies_summary || "No known drug allergies reported."}
                  </p>
                </Card>
              </div>
            </div>
          </Modal>
        )}

        {/* Register Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Register Master Patient Record"
        >
          <form onSubmit={handleRegister} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="First Name" required value={firstName} onChange={(e) => setFirstName(e.target.value)} />
              <Input label="Last Name" required value={lastName} onChange={(e) => setLastName(e.target.value)} />
            </div>
            <div className="grid grid-cols-3 gap-3">
              <Input label="Date of Birth" type="date" required value={dob} onChange={(e) => setDob(e.target.value)} />
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Gender</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={gender} onChange={(e) => setGender(e.target.value)}>
                  <option value="MALE">Male</option>
                  <option value="FEMALE">Female</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Blood Group</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={bloodGroup} onChange={(e) => setBloodGroup(e.target.value)}>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Input label="Phone Number" required value={phone} onChange={(e) => setPhone(e.target.value)} />
              <Input label="Email Address" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <Input label="Residential Address" value={address} onChange={(e) => setAddress(e.target.value)} />
            <div className="grid grid-cols-2 gap-3">
              <Input label="Insurance Provider" value={insurance} onChange={(e) => setInsurance(e.target.value)} />
              <Input label="Allergies / Flags" placeholder="e.g. Penicillin" value={allergies} onChange={(e) => setAllergies(e.target.value)} />
            </div>
            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Create Patient File</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
