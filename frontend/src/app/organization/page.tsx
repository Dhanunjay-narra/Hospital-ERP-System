"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Building2, Plus, Bed, Layers, MapPin, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function OrganizationPage() {
  const [branches, setBranches] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [wards, setWards] = useState<any[]>([]);
  const [beds, setBeds] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<"departments" | "wards" | "beds">("departments");
  const [showAddModal, setShowAddModal] = useState(false);

  // New Department form state
  const [deptName, setDeptName] = useState("");
  const [deptCode, setDeptCode] = useState("");
  const [deptType, setDeptType] = useState("CLINICAL");

  const loadData = async () => {
    try {
      const [bData, dData, wData, bedData] = await Promise.all([
        ApiClient.get("/organization/branches"),
        ApiClient.get("/organization/departments"),
        ApiClient.get("/organization/wards"),
        ApiClient.get("/organization/beds"),
      ]);
      setBranches(bData || []);
      setDepartments(dData || []);
      setWards(wData || []);
      setBeds(bedData || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateDepartment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!branches.length) return;
    try {
      await ApiClient.post("/organization/departments", {
        branch_id: branches[0].id,
        name: deptName,
        code: deptCode,
        department_type: deptType,
        is_opd: true,
        is_ipd: true,
      });
      setShowAddModal(false);
      setDeptName("");
      setDeptCode("");
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
              Hospital & Facility Administration
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Configure branches, multi-specialty departments, inpatient wards, and clinical bed inventory.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Add Department
          </Button>
        </div>

        {/* Branch Info Banner */}
        {branches.length > 0 && (
          <Card className="bg-gradient-to-r from-teal-800 to-teal-950 text-white border-0">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-white/10 rounded-xl backdrop-blur-xs">
                  <Building2 className="w-7 h-7 text-teal-300" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-lg font-bold">{branches[0].name}</h2>
                    <Badge variant="brand" className="bg-teal-500/20 text-teal-200 border-teal-400/30">
                      Main Campus
                    </Badge>
                  </div>
                  <p className="text-xs text-teal-200 mt-1 flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5" />
                    {branches[0].address}, {branches[0].city}, {branches[0].country}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-6 text-xs border-t md:border-t-0 md:border-l border-white/10 pt-3 md:pt-0 md:pl-6">
                <div>
                  <p className="text-teal-300">Departments</p>
                  <p className="text-lg font-bold text-white">{departments.length}</p>
                </div>
                <div>
                  <p className="text-teal-300">Inpatient Wards</p>
                  <p className="text-lg font-bold text-white">{wards.length}</p>
                </div>
                <div>
                  <p className="text-teal-300">Total Beds</p>
                  <p className="text-lg font-bold text-white">{beds.length}</p>
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Navigation Tabs */}
        <div className="flex gap-2 border-b border-slate-200 pb-2">
          <button
            onClick={() => setActiveTab("departments")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition ${
              activeTab === "departments"
                ? "bg-teal-700 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Departments ({departments.length})
          </button>
          <button
            onClick={() => setActiveTab("wards")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition ${
              activeTab === "wards"
                ? "bg-teal-700 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Wards ({wards.length})
          </button>
          <button
            onClick={() => setActiveTab("beds")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition ${
              activeTab === "beds"
                ? "bg-teal-700 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Beds & Allocation ({beds.length})
          </button>
        </div>

        {/* Content Body */}
        {activeTab === "departments" && (
          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Code</TableHead>
                  <TableHead>Department Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>OPD / IPD Enabled</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {departments.map((dept) => (
                  <TableRow key={dept.id}>
                    <TableCell className="font-mono font-bold text-xs text-teal-800">{dept.code}</TableCell>
                    <TableCell className="font-semibold text-slate-800">{dept.name}</TableCell>
                    <TableCell>
                      <Badge variant={dept.department_type === "CLINICAL" ? "brand" : "neutral"}>
                        {dept.department_type}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-xs text-slate-600">
                        OPD: {dept.is_opd ? "Yes" : "No"} | IPD: {dept.is_ipd ? "Yes" : "No"}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge variant="success">Active</Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        )}

        {activeTab === "wards" && (
          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Ward Code</TableHead>
                  <TableHead>Ward Name</TableHead>
                  <TableHead>Ward Type</TableHead>
                  <TableHead>Gender Type</TableHead>
                  <TableHead>Capacity</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {wards.map((ward) => (
                  <TableRow key={ward.id}>
                    <TableCell className="font-mono font-bold text-teal-800">{ward.code}</TableCell>
                    <TableCell className="font-semibold text-slate-800">{ward.name}</TableCell>
                    <TableCell>
                      <Badge variant={ward.ward_type === "ICU" ? "danger" : "brand"}>
                        {ward.ward_type}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-xs text-slate-600">{ward.gender_type}</TableCell>
                    <TableCell className="text-xs font-semibold text-slate-700">
                      {beds.filter((b) => b.ward_id === ward.id).length} Beds
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        )}

        {activeTab === "beds" && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {beds.map((bed) => (
              <div
                key={bed.id}
                className="p-3 bg-white rounded-xl border border-slate-200 shadow-xs flex flex-col items-center justify-center text-center space-y-1.5 hover:border-teal-500 transition"
              >
                <Bed className={`w-6 h-6 ${bed.status === "AVAILABLE" ? "text-emerald-500" : "text-rose-500"}`} />
                <span className="font-bold text-xs text-slate-800">{bed.bed_number}</span>
                <Badge
                  variant={bed.status === "AVAILABLE" ? "success" : "danger"}
                  size="sm"
                >
                  {bed.status}
                </Badge>
              </div>
            ))}
          </div>
        )}

        {/* Modal for Adding Department */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Add New Department"
        >
          <form onSubmit={handleCreateDepartment} className="space-y-4">
            <Input
              label="Department Name"
              required
              placeholder="e.g. Neurology & Spine"
              value={deptName}
              onChange={(e) => setDeptName(e.target.value)}
            />
            <Input
              label="Department Code"
              required
              placeholder="e.g. NEURO"
              value={deptCode}
              onChange={(e) => setDeptCode(e.target.value)}
            />
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                Department Type
              </label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 focus:border-teal-600 focus:outline-none"
                value={deptType}
                onChange={(e) => setDeptType(e.target.value)}
              >
                <option value="CLINICAL">Clinical</option>
                <option value="DIAGNOSTIC">Diagnostic</option>
                <option value="SUPPORT">Support / Pharmacy</option>
                <option value="ADMINISTRATIVE">Administrative</option>
              </select>
            </div>
            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>
                Cancel
              </Button>
              <Button type="submit">Create Department</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
