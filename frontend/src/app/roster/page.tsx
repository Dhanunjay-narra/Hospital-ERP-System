"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { CalendarClock, Plus, ArrowRightLeft, ShieldCheck, UserCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function RosterPage() {
  const [slots, setSlots] = useState<any[]>([]);
  const [handovers, setHandovers] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [employees, setEmployees] = useState<any[]>([]);
  const [showSlotModal, setShowSlotModal] = useState(false);
  const [showHandoverModal, setShowHandoverModal] = useState(false);

  // Slot Form
  const [selectedDept, setSelectedDept] = useState("");
  const [selectedEmp, setSelectedEmp] = useState("");
  const [shiftDate, setShiftDate] = useState("2026-08-28");
  const [shiftType, setShiftType] = useState("MORNING");
  const [role, setRole] = useState("Primary Trauma On-Call");

  // Handover Form
  const [incomingEmp, setIncomingEmp] = useState("");
  const [criticalNotes, setCriticalNotes] = useState("Bed 204 requires hourly glucose checks. Bed 209 scheduled for CT non-contrast.");

  const loadData = async () => {
    try {
      const [sRes, hRes, dRes, eRes] = await Promise.all([
        ApiClient.get("/roster/slots"),
        ApiClient.get("/roster/handovers"),
        ApiClient.get("/organization/departments"),
        ApiClient.get("/hr/employees"),
      ]);
      setSlots(sRes || []);
      setHandovers(hRes || []);
      setDepartments(dRes || []);
      setEmployees(eRes.items || []);
      if (dRes?.length) setSelectedDept(dRes[0].id);
      if (eRes.items?.length) {
        setSelectedEmp(eRes.items[0].id);
        setIncomingEmp(eRes.items[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateSlot = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/roster/slots", {
        department_id: selectedDept,
        employee_id: selectedEmp,
        shift_date: shiftDate,
        shift_type: shiftType,
        assigned_role: role,
      });
      setShowSlotModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateHandover = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/roster/handovers", {
        department_id: selectedDept,
        incoming_employee_id: incomingEmp,
        shift_date: shiftDate,
        critical_patient_notes: criticalNotes,
      });
      setShowHandoverModal(false);
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
              Department Duty Roster & Clinical Shift Handover
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Physician & nursing shift rostering, 24/7 on-call schedules, digital SBAR handovers, and narcotics counts.
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowHandoverModal(true)} leftIcon={<ArrowRightLeft className="w-4 h-4" />}>
              Shift Handover SBAR
            </Button>
            <Button size="sm" onClick={() => setShowSlotModal(true)} leftIcon={<Plus className="w-4 h-4" />}>
              Assign Duty Slot
            </Button>
          </div>
        </div>

        {/* Duty Slots Grid */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Shift Date</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Assigned Staff Member</TableHead>
                <TableHead>Shift Type & Timings</TableHead>
                <TableHead>Clinical Duty Role</TableHead>
                <TableHead>Attendance</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {slots.map((s) => (
                <TableRow key={s.id}>
                  <TableCell className="font-mono font-bold text-xs text-slate-800">
                    {formatDate(s.shift_date)}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600 font-medium">
                    {s.department?.name || "Emergency Department"}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800 text-xs">
                      {s.employee?.user?.first_name} {s.employee?.user?.last_name}
                    </p>
                    <p className="text-[11px] text-slate-400">{s.employee?.designation}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{s.shift_type} ({s.start_time} - {s.end_time})</Badge>
                  </TableCell>
                  <TableCell className="text-xs text-slate-700 font-medium">
                    {s.assigned_role}
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">Present On-Duty</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Add Slot Modal */}
        <Modal
          isOpen={showSlotModal}
          onClose={() => setShowSlotModal(false)}
          title="Schedule Clinical Duty Roster"
        >
          <form onSubmit={handleCreateSlot} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Department</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedDept} onChange={(e) => setSelectedDept(e.target.value)}>
                  {departments.map((d) => (
                    <option key={d.id} value={d.id}>{d.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Staff Member</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedEmp} onChange={(e) => setSelectedEmp(e.target.value)}>
                  {employees.map((emp) => (
                    <option key={emp.id} value={emp.id}>{emp.user?.first_name} {emp.user?.last_name} ({emp.designation})</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Shift Date" type="date" required value={shiftDate} onChange={(e) => setShiftDate(e.target.value)} />
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Shift Window</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={shiftType} onChange={(e) => setShiftType(e.target.value)}>
                  <option value="MORNING">Morning (07:00 - 15:00)</option>
                  <option value="EVENING">Evening (15:00 - 23:00)</option>
                  <option value="NIGHT">Night (23:00 - 07:00)</option>
                  <option value="ON_CALL">24-Hour Emergency On-Call</option>
                </select>
              </div>
            </div>

            <Input label="Assigned Duty Role" required value={role} onChange={(e) => setRole(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowSlotModal(false)}>Cancel</Button>
              <Button type="submit">Publish Roster Slot</Button>
            </div>
          </form>
        </Modal>

        {/* Shift Handover Modal */}
        <Modal
          isOpen={showHandoverModal}
          onClose={() => setShowHandoverModal(false)}
          title="Clinical Shift Handover (SBAR Protocol)"
        >
          <form onSubmit={handleCreateHandover} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Incoming Relieving Staff</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={incomingEmp} onChange={(e) => setIncomingEmp(e.target.value)}>
                {employees.map((emp) => (
                  <option key={emp.id} value={emp.id}>{emp.user?.first_name} {emp.user?.last_name} ({emp.designation})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Critical Patient Alerts & Escalations</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={4} required value={criticalNotes} onChange={(e) => setCriticalNotes(e.target.value)} />
            </div>

            <div className="flex items-center gap-2">
              <input type="checkbox" id="narco" defaultChecked />
              <label htmlFor="narco" className="text-xs text-slate-700 font-bold">Narcotics Lockbox Count Reconciled & Verified</label>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowHandoverModal(false)}>Cancel</Button>
              <Button type="submit">Sign Off Shift Handover</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
