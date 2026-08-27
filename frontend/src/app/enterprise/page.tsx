"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Building2, Plus, Ambulance, ArrowRightLeft, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function EnterprisePage() {
  const [transfers, setTransfers] = useState<any[]>([]);
  const [branches, setBranches] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showTransferModal, setShowTransferModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [srcBranch, setSrcBranch] = useState("");
  const [dstBranch, setDstBranch] = useState("");
  const [reason, setReason] = useState("Higher Acuity ECMO Intensive Care required");

  const loadData = async () => {
    try {
      const [tRes, bRes, pRes] = await Promise.all([
        ApiClient.get("/enterprise/transfers"),
        ApiClient.get("/organization/branches"),
        ApiClient.get("/patients"),
      ]);
      setTransfers(tRes.items || []);
      setBranches(bRes || []);
      setPatients(pRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
      if (bRes?.length > 1) {
        setSrcBranch(bRes[0].id);
        setDstBranch(bRes[1].id);
      } else if (bRes?.length === 1) {
        setSrcBranch(bRes[0].id);
        setDstBranch(bRes[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateTransfer = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/enterprise/transfers", {
        patient_id: selectedPatient,
        source_branch_id: srcBranch,
        destination_branch_id: dstBranch,
        clinical_reason: reason,
        requires_advanced_life_support_ambulance: true,
      });
      setShowTransferModal(false);
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
              Multi-Branch Enterprise Network & Cross-Hospital Transfers
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Multi-facility rollup analytics, cross-branch electronic health record sharing, and critical ALS ambulance patient transfers.
            </p>
          </div>
          <Button
            onClick={() => setShowTransferModal(true)}
            leftIcon={<Ambulance className="w-4 h-4" />}
            size="sm"
          >
            Dispatch Inter-Branch Transfer
          </Button>
        </div>

        {/* Multi-Branch Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Apex Central Hospital</p>
              <p className="text-sm font-bold text-slate-800 mt-1">Main Academic Medical Center (Branch 01)</p>
            </div>
            <Badge variant="success">Operational</Badge>
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Apex City South Pavilion</p>
              <p className="text-sm font-bold text-slate-800 mt-1">Surgical & Oncology Center (Branch 02)</p>
            </div>
            <Badge variant="success">Operational</Badge>
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Apex North Children's Hospital</p>
              <p className="text-sm font-bold text-slate-800 mt-1">Pediatric & Maternal Care (Branch 03)</p>
            </div>
            <Badge variant="success">Operational</Badge>
          </Card>
        </div>

        {/* Transfers Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Transfer #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Origin Facility</TableHead>
                <TableHead>Destination Facility</TableHead>
                <TableHead>Clinical Transfer Reason</TableHead>
                <TableHead>Acuity Transport</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transfers.map((t) => (
                <TableRow key={t.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {t.transfer_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{t.patient?.first_name} {t.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {t.patient?.uhid}</p>
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-800">
                    {t.source_branch?.name || "Central Medical Branch"}
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-teal-700">
                    {t.destination_branch?.name || "Apex South Pavilion"}
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 max-w-xs">{t.clinical_reason}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="danger">ALS Ambulance</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{t.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Transfer Modal */}
        <Modal
          isOpen={showTransferModal}
          onClose={() => setShowTransferModal(false)}
          title="Dispatch Inter-Hospital Branch Transfer"
        >
          <form onSubmit={handleCreateTransfer} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Source Branch</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={srcBranch} onChange={(e) => setSrcBranch(e.target.value)}>
                  {branches.map((b) => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Destination Branch</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={dstBranch} onChange={(e) => setDstBranch(e.target.value)}>
                  {branches.map((b) => (
                    <option key={b.id} value={b.id}>{b.name}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Clinical Transfer Indication</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={3} required value={reason} onChange={(e) => setReason(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowTransferModal(false)}>Cancel</Button>
              <Button type="submit">Authorize & Dispatch Transport</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
