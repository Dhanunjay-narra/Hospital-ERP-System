"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Users, Plus, Calendar, DollarSign, Award, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function HRPage() {
  const [employees, setEmployees] = useState<any[]>([]);
  const [leaves, setLeaves] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [showEmpModal, setShowEmpModal] = useState(false);
  const [showLeaveModal, setShowLeaveModal] = useState(false);

  // Form State
  const [selectedUser, setSelectedUser] = useState("");
  const [selectedDept, setSelectedDept] = useState("");
  const [designation, setDesignation] = useState("Senior Clinical Specialist");
  const [salary, setSalary] = useState("8500");

  // Leave Form
  const [selectedEmp, setSelectedEmp] = useState("");
  const [leaveType, setLeaveType] = useState("CASUAL");
  const [startD, setStartD] = useState("2026-09-01");
  const [endD, setEndD] = useState("2026-09-03");
  const [reason, setReason] = useState("Annual family conference");

  const loadData = async () => {
    try {
      const [empRes, lRes, uRes, dRes] = await Promise.all([
        ApiClient.get("/hr/employees"),
        ApiClient.get("/hr/leaves"),
        ApiClient.get("/users"),
        ApiClient.get("/organization/departments"),
      ]);
      setEmployees(empRes.items || []);
      setLeaves(lRes || []);
      setUsers(uRes.items || []);
      setDepartments(dRes || []);
      if (uRes.items?.length) setSelectedUser(uRes.items[0].id);
      if (dRes?.length) setSelectedDept(dRes[0].id);
      if (empRes.items?.length) setSelectedEmp(empRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/hr/employees", {
        user_id: selectedUser,
        department_id: selectedDept,
        designation,
        employment_type: "FULL_TIME",
        joining_date: "2026-01-15",
        salary_amount: parseFloat(salary),
      });
      setShowEmpModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleApplyLeave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/hr/leaves", {
        employee_id: selectedEmp,
        leave_type: leaveType,
        start_date: startD,
        end_date: endD,
        reason,
      });
      setShowLeaveModal(false);
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
              Hospital Staff, Human Resources & Payroll
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Employee master profiles, department allocations, leave entitlement applications, and salary structure.
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowLeaveModal(true)} leftIcon={<Calendar className="w-4 h-4" />}>
              Apply Leave
            </Button>
            <Button size="sm" onClick={() => setShowEmpModal(true)} leftIcon={<Plus className="w-4 h-4" />}>
              Onboard Staff
            </Button>
          </div>
        </div>

        {/* Employee Directory */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee Code</TableHead>
                <TableHead>Staff Name</TableHead>
                <TableHead>Designation</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Employment Type</TableHead>
                <TableHead>Monthly Salary</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {employees.map((emp) => (
                <TableRow key={emp.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {emp.employee_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{emp.user?.first_name} {emp.user?.last_name}</p>
                    <p className="text-xs text-slate-400">{emp.user?.email}</p>
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-800">
                    {emp.designation}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {emp.department?.name || "General Administration"}
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{emp.employment_type}</Badge>
                  </TableCell>
                  <TableCell className="text-xs font-bold text-emerald-700">
                    {formatCurrency(emp.salary_amount)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">{emp.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Onboard Staff Modal */}
        <Modal
          isOpen={showEmpModal}
          onClose={() => setShowEmpModal(false)}
          title="Onboard Hospital Staff Member"
        >
          <form onSubmit={handleCreateEmployee} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">User Account</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedUser} onChange={(e) => setSelectedUser(e.target.value)}>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>{u.first_name} {u.last_name} ({u.email})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Department</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedDept} onChange={(e) => setSelectedDept(e.target.value)}>
                  {departments.map((d) => (
                    <option key={d.id} value={d.id}>{d.name}</option>
                  ))}
                </select>
              </div>
              <Input label="Designation / Role Title" required value={designation} onChange={(e) => setDesignation(e.target.value)} />
            </div>

            <Input label="Monthly Base Compensation ($)" type="number" required value={salary} onChange={(e) => setSalary(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowEmpModal(false)}>Cancel</Button>
              <Button type="submit">Complete Staff Onboarding</Button>
            </div>
          </form>
        </Modal>

        {/* Apply Leave Modal */}
        <Modal
          isOpen={showLeaveModal}
          onClose={() => setShowLeaveModal(false)}
          title="Submit Staff Leave Application"
        >
          <form onSubmit={handleApplyLeave} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Employee</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedEmp} onChange={(e) => setSelectedEmp(e.target.value)}>
                {employees.map((emp) => (
                  <option key={emp.id} value={emp.id}>{emp.user?.first_name} {emp.user?.last_name} ({emp.employee_code})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Leave Type</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={leaveType} onChange={(e) => setLeaveType(e.target.value)}>
                  <option value="CASUAL">Casual Leave</option>
                  <option value="SICK">Sick Leave</option>
                  <option value="ANNUAL">Annual Paid Leave</option>
                  <option value="MATERNITY">Maternity / Paternity</option>
                </select>
              </div>
              <Input label="Start Date" type="date" required value={startD} onChange={(e) => setStartD(e.target.value)} />
              <Input label="End Date" type="date" required value={endD} onChange={(e) => setEndD(e.target.value)} />
            </div>

            <Input label="Reason for Leave" required value={reason} onChange={(e) => setReason(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowLeaveModal(false)}>Cancel</Button>
              <Button type="submit">Submit Leave Request</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
