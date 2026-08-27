"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { BrainCircuit, Plus, ShieldAlert, AlertTriangle, CheckCircle2, Stethoscope } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function CDSSPage() {
  const [rules, setRules] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [code, setCode] = useState("CDSS-QSOFA-01");
  const [title, setTitle] = useState("qSOFA Bedside Sepsis Early Warning Protocol");
  const [category, setCategory] = useState("SEPSIS_ALERT");
  const [severity, setSeverity] = useState("HIGH_CRITICAL");
  const [desc, setDesc] = useState("Evaluates altered mental status, SBP <= 100 mmHg, and respiratory rate >= 22 breaths/min.");
  const [recAction, setRecAction] = useState("Order STAT blood cultures, serum lactate, and initiate broad-spectrum IV antimicrobials within 1 hour.");

  const loadData = async () => {
    try {
      const [rRes, aRes] = await Promise.all([
        ApiClient.get("/cdss/rules"),
        ApiClient.get("/cdss/alerts"),
      ]);
      setRules(rRes || []);
      setAlerts(aRes.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateRule = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/cdss/rules", {
        rule_code: code,
        title,
        category,
        severity,
        description: desc,
        recommended_action: recAction,
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
              Clinical Decision Support System (CDSS) & Safety Rules
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Drug-drug contraindication engine, allergy alerts, qSOFA sepsis indicators, and clinical guideline pathways.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Create Decision Rule
          </Button>
        </div>

        {/* Rules Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Rule Code</TableHead>
                <TableHead>Clinical Protocol Title</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Severity Level</TableHead>
                <TableHead>Evidence / Trigger Condition</TableHead>
                <TableHead>Recommended Action</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {rules.map((r) => (
                <TableRow key={r.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {r.rule_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{r.title}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{r.category}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={r.severity === "HIGH_CRITICAL" ? "danger" : "warning"}>
                      {r.severity}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-600 max-w-xs">{r.description}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-emerald-700 font-medium max-w-xs">{r.recommended_action}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">Active</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Create Rule Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Configure Clinical Decision Protocol"
        >
          <form onSubmit={handleCreateRule} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="Rule Code" required value={code} onChange={(e) => setCode(e.target.value)} />
              <Input label="Protocol Title" required value={title} onChange={(e) => setTitle(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Category</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm font-semibold" value={category} onChange={(e) => setCategory(e.target.value)}>
                  <option value="SEPSIS_ALERT">Sepsis / Shock Alert (qSOFA)</option>
                  <option value="DRUG_INTERACTION">Drug-Drug Interaction</option>
                  <option value="DRUG_ALLERGY">Drug-Allergy Contraindication</option>
                  <option value="RENAL_DOSAGE">Renal Clearance Adjustment</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Severity</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm font-bold" value={severity} onChange={(e) => setSeverity(e.target.value)}>
                  <option value="HIGH_CRITICAL">High Critical (Block Order)</option>
                  <option value="MODERATE">Moderate (Clinician Warning)</option>
                  <option value="LOW_INFORMATIONAL">Informational Advisory</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Trigger Clinical Condition</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={3} required value={desc} onChange={(e) => setDesc(e.target.value)} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Recommended Clinical Intervention</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={3} required value={recAction} onChange={(e) => setRecAction(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Activate Protocol Rule</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
