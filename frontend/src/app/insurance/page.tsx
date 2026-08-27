"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { ShieldCheck, Plus, CheckCircle2, FileText, DollarSign } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function InsurancePage() {
  const [claims, setClaims] = useState<any[]>([]);
  const [providers, setProviders] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showClaimModal, setShowClaimModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedProvider, setSelectedProvider] = useState("");
  const [policyNo, setPolicyNo] = useState("POL-BCBS-99120");
  const [preAuthNo, setPreAuthNo] = useState("AUTH-2026-881");
  const [claimAmount, setClaimAmount] = useState("1500.00");

  const loadData = async () => {
    try {
      const [cRes, pRes, patRes] = await Promise.all([
        ApiClient.get("/insurance/claims"),
        ApiClient.get("/insurance/providers"),
        ApiClient.get("/patients"),
      ]);
      setClaims(cRes.items || []);
      setProviders(pRes || []);
      setPatients(patRes.items || []);
      if (patRes.items?.length) setSelectedPatient(patRes.items[0].id);
      if (pRes?.length) setSelectedProvider(pRes[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateClaim = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/insurance/claims", {
        patient_id: selectedPatient,
        provider_id: selectedProvider,
        policy_number: policyNo,
        pre_auth_number: preAuthNo,
        total_claim_amount: parseFloat(claimAmount),
      });
      setShowClaimModal(false);
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
              Insurance, TPA & Electronic Claims Desk
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Payer contracts, pre-authorization requests, electronic EDI claim submissions, and settlement tracking.
            </p>
          </div>
          <Button
            onClick={() => setShowClaimModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Submit Insurance Claim
          </Button>
        </div>

        {/* Claims Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Claim #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Insurance Payer (TPA)</TableHead>
                <TableHead>Policy & Pre-Auth #</TableHead>
                <TableHead>Claimed Amount</TableHead>
                <TableHead>Approved Amount</TableHead>
                <TableHead>Co-Pay</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {claims.map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {c.claim_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{c.patient?.first_name} {c.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {c.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800 text-xs">{c.provider?.name || "BlueCross Shield"}</p>
                    <p className="text-[11px] text-slate-400">EDI 837</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs font-mono text-slate-700">{c.policy_number}</p>
                    <span className="text-[10px] text-teal-600 font-semibold">{c.pre_auth_number || "Pre-Auth Pending"}</span>
                  </TableCell>
                  <TableCell className="font-bold text-slate-800 text-xs">
                    {formatCurrency(c.total_claim_amount)}
                  </TableCell>
                  <TableCell className="text-xs text-emerald-700 font-bold">
                    {formatCurrency(c.approved_amount)}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatCurrency(c.patient_copay_amount)}
                  </TableCell>
                  <TableCell>
                    <Badge variant={c.status === "APPROVED" || c.status === "SETTLED" ? "success" : "brand"}>
                      {c.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Submit Claim Modal */}
        <Modal
          isOpen={showClaimModal}
          onClose={() => setShowClaimModal(false)}
          title="Submit Electronic Insurance Claim"
        >
          <form onSubmit={handleCreateClaim} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Insurance Payer / TPA</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedProvider} onChange={(e) => setSelectedProvider(e.target.value)}>
                {providers.map((pr) => (
                  <option key={pr.id} value={pr.id}>{pr.name} ({pr.code})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Insurance Policy Number" required value={policyNo} onChange={(e) => setPolicyNo(e.target.value)} />
              <Input label="Pre-Authorization #" value={preAuthNo} onChange={(e) => setPreAuthNo(e.target.value)} />
            </div>

            <Input label="Total Claim Amount ($)" type="number" step="0.01" required value={claimAmount} onChange={(e) => setClaimAmount(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowClaimModal(false)}>Cancel</Button>
              <Button type="submit">Submit Claim to Payer</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
