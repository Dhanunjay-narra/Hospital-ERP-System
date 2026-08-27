"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Video, Plus, ExternalLink, Calendar, Stethoscope, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function TelemedicinePage() {
  const [sessions, setSessions] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [startTime, setStartTime] = useState("2026-08-28T14:30");

  const loadData = async () => {
    try {
      const [sRes, pRes, dRes] = await Promise.all([
        ApiClient.get("/telemedicine/sessions"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
      ]);
      setSessions(sRes.items || []);
      setPatients(pRes.items || []);
      setDoctors(dRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
      if (dRes.items?.length) setSelectedDoctor(dRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateSession = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/telemedicine/sessions", {
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
        scheduled_start: new Date(startTime).toISOString(),
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
              Virtual Telemedicine & Remote Consultation Desk
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Encrypted WebRTC high-definition video rooms, digital waiting rooms, and integrated remote e-prescriptions.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Video className="w-4 h-4" />}
            size="sm"
          >
            Schedule Video Consultation
          </Button>
        </div>

        {/* Sessions Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Virtual Session #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Consulting Physician</TableHead>
                <TableHead>Scheduled Slot</TableHead>
                <TableHead>WebRTC Secure Room Link</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sessions.map((s) => (
                <TableRow key={s.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {s.session_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{s.patient?.first_name} {s.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {s.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800 text-xs">
                      {s.doctor?.user?.first_name} {s.doctor?.user?.last_name}
                    </p>
                    <p className="text-[11px] text-teal-600 font-medium">{s.doctor?.specialization}</p>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDateTime(s.scheduled_start)}
                  </TableCell>
                  <TableCell>
                    <a
                      href={s.meeting_room_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-mono text-xs text-teal-600 hover:underline flex items-center gap-1"
                    >
                      <ExternalLink className="w-3 h-3" /> Launch WebRTC Room
                    </a>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{s.status}</Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant="primary"
                      onClick={() => window.open(s.meeting_room_url, "_blank")}
                      leftIcon={<Video className="w-3.5 h-3.5" />}
                    >
                      Join Call
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Schedule Consultation Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Schedule Remote Video Teleconsultation"
        >
          <form onSubmit={handleCreateSession} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Consulting Doctor</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedDoctor} onChange={(e) => setSelectedDoctor(e.target.value)}>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>{d.user?.first_name} {d.user?.last_name} ({d.specialization})</option>
                ))}
              </select>
            </div>

            <Input label="Scheduled Start Time" type="datetime-local" required value={startTime} onChange={(e) => setStartTime(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Generate Video Meeting URL</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
