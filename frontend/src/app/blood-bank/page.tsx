"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Droplets, Plus, UserCheck, ShieldCheck, HeartPulse } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function BloodBankPage() {
  const [units, setUnits] = useState<any[]>([]);
  const [donors, setDonors] = useState<any[]>([]);
  const [showUnitModal, setShowUnitModal] = useState(false);
  const [showDonorModal, setShowDonorModal] = useState(false);

  // Unit Form
  const [bloodGroup, setBloodGroup] = useState("O+");
  const [component, setComponent] = useState("PRBC");
  const [volume, setVolume] = useState("350");
  const [expiry, setExpiry] = useState("2026-10-15");

  // Donor Form
  const [donorName, setDonorName] = useState("");
  const [donorPhone, setDonorPhone] = useState("");
  const [donorBg, setDonorBg] = useState("O+");
  const [donorHb, setDonorHb] = useState("14.0");

  const loadData = async () => {
    try {
      const [uRes, dRes] = await Promise.all([
        ApiClient.get("/blood-bank/units"),
        ApiClient.get("/blood-bank/donors"),
      ]);
      setUnits(uRes || []);
      setDonors(dRes || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateUnit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/blood-bank/units", {
        blood_group: bloodGroup,
        component_type: component,
        volume_ml: parseFloat(volume),
        collection_date: new Date().toISOString().split("T")[0],
        expiry_date: expiry,
      });
      setShowUnitModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleRegisterDonor = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/blood-bank/donors", {
        full_name: donorName,
        phone_number: donorPhone,
        gender: "MALE",
        date_of_birth: "1992-05-15",
        blood_group: donorBg,
        hemoglobin_level: parseFloat(donorHb),
      });
      setShowDonorModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Hospital Blood Bank & Component Inventory
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Component separation (PRBC, FFP, Platelets), donor registry, cold-chain storage status, and cross-matching.
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowDonorModal(true)} leftIcon={<UserCheck className="w-4 h-4" />}>
              Register Donor
            </Button>
            <Button size="sm" onClick={() => setShowUnitModal(true)} leftIcon={<Plus className="w-4 h-4" />}>
              Add Blood Unit
            </Button>
          </div>
        </div>

        {/* Group Inventory Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          {groups.map((bg) => {
            const count = units.filter((u) => u.blood_group === bg && u.status === "AVAILABLE").length;
            return (
              <div key={bg} className="p-3 bg-white rounded-xl border border-slate-200 text-center space-y-1 shadow-xs">
                <span className="text-xs font-black text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">{bg}</span>
                <p className="text-lg font-bold text-slate-800">{count} Units</p>
                <span className="text-[10px] text-slate-400 font-medium uppercase">Available</span>
              </div>
            );
          })}
        </div>

        {/* Units Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Unit Barcode #</TableHead>
                <TableHead>Blood Group</TableHead>
                <TableHead>Component Type</TableHead>
                <TableHead>Volume</TableHead>
                <TableHead>Cold-Chain Storage</TableHead>
                <TableHead>Expiry Date</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {units.map((u) => (
                <TableRow key={u.id}>
                  <TableCell className="font-mono font-bold text-xs text-rose-800">
                    {u.unit_number}
                  </TableCell>
                  <TableCell>
                    <Badge variant="danger">{u.blood_group}</Badge>
                  </TableCell>
                  <TableCell className="font-semibold text-slate-800 text-xs">
                    {u.component_type}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">{u.volume_ml} mL</TableCell>
                  <TableCell className="text-xs text-slate-600">{u.storage_refrigerator_id}</TableCell>
                  <TableCell className="text-xs text-slate-600">{formatDate(u.expiry_date)}</TableCell>
                  <TableCell>
                    <Badge variant={u.status === "AVAILABLE" ? "success" : "neutral"}>
                      {u.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Add Unit Modal */}
        <Modal
          isOpen={showUnitModal}
          onClose={() => setShowUnitModal(false)}
          title="Add Tested Blood Unit to Inventory"
        >
          <form onSubmit={handleCreateUnit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Blood Group</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm font-bold" value={bloodGroup} onChange={(e) => setBloodGroup(e.target.value)}>
                  {groups.map((g) => <option key={g} value={g}>{g}</option>)}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Component Type</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={component} onChange={(e) => setComponent(e.target.value)}>
                  <option value="PRBC">PRBC (Packed Red Cells)</option>
                  <option value="WHOLE_BLOOD">Whole Blood</option>
                  <option value="FFP">FFP (Fresh Frozen Plasma)</option>
                  <option value="PLATELETS">Platelet Concentrate</option>
                  <option value="CRYOPRECIPITATE">Cryoprecipitate</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Volume (mL)" type="number" required value={volume} onChange={(e) => setVolume(e.target.value)} />
              <Input label="Expiry Date" type="date" required value={expiry} onChange={(e) => setExpiry(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowUnitModal(false)}>Cancel</Button>
              <Button type="submit">Store in Cold Storage</Button>
            </div>
          </form>
        </Modal>

        {/* Register Donor Modal */}
        <Modal
          isOpen={showDonorModal}
          onClose={() => setShowDonorModal(false)}
          title="Register Voluntary Blood Donor"
        >
          <form onSubmit={handleRegisterDonor} className="space-y-4">
            <Input label="Donor Full Name" required value={donorName} onChange={(e) => setDonorName(e.target.value)} />
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Blood Group</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={donorBg} onChange={(e) => setDonorBg(e.target.value)}>
                  {groups.map((g) => <option key={g} value={g}>{g}</option>)}
                </select>
              </div>
              <Input label="Phone Number" required value={donorPhone} onChange={(e) => setDonorPhone(e.target.value)} />
              <Input label="Hemoglobin (g/dL)" type="number" step="0.1" value={donorHb} onChange={(e) => setDonorHb(e.target.value)} />
            </div>
            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowDonorModal(false)}>Cancel</Button>
              <Button type="submit">Register Donor</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
