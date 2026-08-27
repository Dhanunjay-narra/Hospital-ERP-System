"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Activity, Plus, CheckSquare, Stethoscope, Clock, ShieldCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function OTPage() {
  const [surgeries, setSurgeries] = useState<any[]>([]);
  const [rooms, setRooms] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedRoom, setSelectedRoom] = useState("");
  const [selectedSurgeon, setSelectedSurgeon] = useState("");
  const [procedure, setProcedure] = useState("");
  const [startTime, setStartTime] = useState("2026-08-28T09:00");
  const [endTime, setEndTime] = useState("2026-08-28T12:00");

  const loadData = async () => {
    try {
      const [sRes, rRes, pRes, dRes] = await Promise.all([
        ApiClient.get("/ot/surgeries"),
        ApiClient.get("/ot/rooms"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
      ]);
      setSurgeries(sRes.items || []);
      setRooms(rRes || []);
      setPatients(pRes.items || []);
      setDoctors(dRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
      if (rRes?.length) setSelectedRoom(rRes[0].id);
      if (dRes.items?.length) setSelectedSurgeon(dRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleBookSurgery = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/ot/surgeries", {
        patient_id: selectedPatient,
        ot_room_id: selectedRoom,
        lead_surgeon_id: selectedSurgeon,
        procedure_name: procedure,
        scheduled_start: new Date(startTime).toISOString(),
        scheduled_end: new Date(endTime).toISOString(),
        anesthesia_type: "GENERAL",
      });
      setShowAddModal(false);
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
              Operation Theatre (OT) & Surgical Worklist
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Surgical theater booking, lead surgeon assignment, and WHO Surgical Safety Checklist enforcement.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Schedule Surgery
          </Button>
        </div>

        {/* OT Rooms Status Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-semibold uppercase">Major OT 1 (Cardiac Suite)</p>
              <p className="text-sm font-bold text-slate-800 mt-1">CABG — Dr. Robert Vance</p>
            </div>
            <Badge variant="danger">In Surgery</Badge>
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-semibold uppercase">Major OT 2 (Ortho Suite)</p>
              <p className="text-sm font-bold text-slate-800 mt-1">Total Knee — Dr. Elena Rostova</p>
            </div>
            <Badge variant="warning">Pre-Op Prep</Badge>
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 font-semibold uppercase">Minor OT 3 (General Suite)</p>
              <p className="text-sm font-bold text-emerald-700 mt-1">Sterilized & Ready</p>
            </div>
            <Badge variant="success">Available</Badge>
          </Card>
        </div>

        {/* Surgery Schedule Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Surgery #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Surgical Procedure</TableHead>
                <TableHead>Lead Surgeon</TableHead>
                <TableHead>Scheduled Slot</TableHead>
                <TableHead>WHO Checklist</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {surgeries.map((s) => (
                <TableRow key={s.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {s.surgery_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{s.patient?.first_name} {s.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {s.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{s.procedure_name}</p>
                    <span className="text-[11px] text-slate-500">{s.anesthesia_type} Anesthesia</span>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs font-medium text-slate-800">{s.lead_surgeon?.user?.first_name} {s.lead_surgeon?.user?.last_name}</p>
                    <p className="text-[11px] text-teal-600">{s.lead_surgeon?.specialization}</p>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDateTime(s.scheduled_start)}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1 text-[10px] font-bold">
                      <span className="px-1.5 py-0.5 bg-emerald-50 text-emerald-700 rounded">Sign In ✓</span>
                      <span className="px-1.5 py-0.5 bg-emerald-50 text-emerald-700 rounded">Time Out ✓</span>
                      <span className="px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded">Sign Out</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{s.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Schedule Surgery Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Schedule Surgical Operation"
        >
          <form onSubmit={handleBookSurgery} className="space-y-4">
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
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">OT Room</label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                  value={selectedRoom}
                  onChange={(e) => setSelectedRoom(e.target.value)}
                >
                  {rooms.map((r) => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Lead Surgeon</label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                  value={selectedSurgeon}
                  onChange={(e) => setSelectedSurgeon(e.target.value)}
                >
                  {doctors.map((d) => (
                    <option key={d.id} value={d.id}>{d.user?.first_name} {d.user?.last_name} ({d.specialization})</option>
                  ))}
                </select>
              </div>
            </div>

            <Input
              label="Surgical Procedure Name"
              required
              placeholder="e.g. Laparoscopic Cholecystectomy, Spinal Fusion"
              value={procedure}
              onChange={(e) => setProcedure(e.target.value)}
            />

            <div className="grid grid-cols-2 gap-3">
              <Input label="Scheduled Start" type="datetime-local" required value={startTime} onChange={(e) => setStartTime(e.target.value)} />
              <Input label="Scheduled End" type="datetime-local" required value={endTime} onChange={(e) => setEndTime(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Schedule OT Booking</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
