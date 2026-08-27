"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { CalendarDays, Plus, Clock, CheckCircle2, XCircle, ArrowRight, UserCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [apptDate, setApptDate] = useState(new Date().toISOString().split("T")[0]);
  const [startTime, setStartTime] = useState("10:00");
  const [complaint, setComplaint] = useState("");

  const loadData = async () => {
    try {
      const [apptsRes, docsRes, patsRes] = await Promise.all([
        ApiClient.get("/appointments"),
        ApiClient.get("/doctors"),
        ApiClient.get("/patients"),
      ]);
      setAppointments(apptsRes.items || []);
      setDoctors(docsRes.items || []);
      setPatients(patsRes.items || []);
      if (docsRes.items?.length) setSelectedDoctor(docsRes.items[0].id);
      if (patsRes.items?.length) setSelectedPatient(patsRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/appointments", {
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
        appointment_date: apptDate,
        start_time: startTime,
        end_time: "10:30",
        chief_complaint: complaint,
      });
      setShowAddModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleStatusChange = async (appointmentId: string, newStatus: string) => {
    try {
      await ApiClient.patch(`/appointments/${appointmentId}/status`, {
        status: newStatus,
      });
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const statusVariant = (status: string) => {
    switch (status) {
      case "CONFIRMED": return "brand";
      case "CHECKED_IN": return "info";
      case "IN_CONSULTATION": return "warning";
      case "COMPLETED": return "success";
      case "CANCELLED": return "danger";
      default: return "neutral";
    }
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Appointment Scheduling & Live Queue Desk
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Multi-channel booking, token allocation, patient check-in, and doctor consultation routing.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Book Appointment
          </Button>
        </div>

        {/* Appointments Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Token & Appt #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Doctor & Specialization</TableHead>
                <TableHead>Date & Time</TableHead>
                <TableHead>Chief Complaint</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {appointments.map((a) => (
                <TableRow key={a.id}>
                  <TableCell>
                    <span className="font-bold text-teal-800 text-sm block">#{a.token_number || "-"}</span>
                    <span className="font-mono text-[11px] text-slate-400">{a.appointment_number}</span>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{a.patient ? `${a.patient.first_name} ${a.patient.last_name}` : "Patient"}</p>
                    <p className="text-xs text-slate-400">UHID: {a.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">{a.doctor?.user?.first_name} {a.doctor?.user?.last_name}</p>
                    <p className="text-xs text-teal-600">{a.doctor?.specialization}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs font-semibold text-slate-700">{formatDate(a.appointment_date)}</p>
                    <p className="text-xs text-slate-400">{a.start_time}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-600 truncate max-w-xs">{a.chief_complaint || "Routine consultation"}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant={statusVariant(a.status)}>
                      {a.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {a.status === "CONFIRMED" && (
                      <Button
                        size="sm"
                        variant="primary"
                        onClick={() => handleStatusChange(a.id, "CHECKED_IN")}
                        leftIcon={<CheckCircle2 className="w-3.5 h-3.5" />}
                      >
                        Check In
                      </Button>
                    )}
                    {a.status === "CHECKED_IN" && (
                      <Badge variant="info">In Queue</Badge>
                    )}
                    {a.status === "COMPLETED" && (
                      <Badge variant="success">Completed</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Modal for Booking Appointment */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Book Patient Appointment"
        >
          <form onSubmit={handleCreate} className="space-y-4">
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
                    {p.uhid} — {p.first_name} {p.last_name} ({p.phone_number})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                Select Doctor & Specialization
              </label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 focus:border-teal-600 focus:outline-none"
                value={selectedDoctor}
                onChange={(e) => setSelectedDoctor(e.target.value)}
              >
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.user?.first_name} {d.user?.last_name} ({d.specialization}) — {formatCurrency(d.consultation_fee)}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Appointment Date"
                type="date"
                required
                value={apptDate}
                onChange={(e) => setApptDate(e.target.value)}
              />
              <Input
                label="Time Slot"
                type="time"
                required
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </div>

            <Input
              label="Chief Complaint / Reason for Visit"
              placeholder="e.g. Chest pain, High fever, Annual health check"
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
            />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>
                Cancel
              </Button>
              <Button type="submit">Confirm Booking</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
