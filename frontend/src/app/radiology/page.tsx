"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { ScanLine, Plus, Eye, FileCheck, CheckCircle2, Image as ImageIcon } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function RadiologyPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [showOrderModal, setShowOrderModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState<any>(null);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [modality, setModality] = useState("X_RAY");
  const [procedure, setProcedure] = useState("Chest X-Ray PA View");
  const [indication, setIndication] = useState("Suspected Pneumonia");

  // Report Form
  const [findings, setFindings] = useState("");
  const [impression, setImpression] = useState("");
  const [isCritical, setIsCritical] = useState(false);

  const loadData = async () => {
    try {
      const [rRes, pRes, dRes] = await Promise.all([
        ApiClient.get("/radiology/orders"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
      ]);
      setOrders(rRes.items || []);
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

  const handleCreateOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/radiology/orders", {
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
        modality,
        procedure_name: procedure,
        clinical_indication: indication,
      });
      setShowOrderModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleSaveReport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedOrder) return;
    try {
      await ApiClient.post(`/radiology/orders/${selectedOrder.id}/report`, {
        radiology_findings: findings,
        impression: impression,
        is_critical_finding: isCritical,
        pacs_image_url: "https://pacs.apexhealth.org/studies/99120",
      });
      setShowReportModal(false);
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
              Radiology & PACS Imaging Modality Desk
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Multi-modality imaging worklist (X-Ray, CT, MRI, Ultrasound), PACS viewer links, and radiologist diagnostic reporting.
            </p>
          </div>
          <Button
            onClick={() => setShowOrderModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Order Imaging Study
          </Button>
        </div>

        {/* Worklist Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Study #</TableHead>
                <TableHead>Modality</TableHead>
                <TableHead>Procedure & Indication</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Ordering Doctor</TableHead>
                <TableHead>Impression / Findings</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {orders.map((o) => (
                <TableRow key={o.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {o.order_number}
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{o.modality}</Badge>
                  </TableCell>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{o.procedure_name}</p>
                    <span className="text-[11px] text-slate-500">{o.clinical_indication}</span>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{o.patient?.first_name} {o.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {o.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs font-medium text-slate-700">{o.doctor?.user?.first_name} {o.doctor?.user?.last_name}</p>
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 font-medium truncate max-w-xs">{o.impression || "Awaiting Radiologist Read"}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant={o.status === "REPORTED" ? "success" : "neutral"}>
                      {o.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {o.status !== "REPORTED" && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedOrder(o);
                          setFindings("");
                          setImpression("");
                          setShowReportModal(true);
                        }}
                      >
                        Enter Report
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Order Imaging Modal */}
        <Modal
          isOpen={showOrderModal}
          onClose={() => setShowOrderModal(false)}
          title="Order Radiology / Imaging Study"
        >
          <form onSubmit={handleCreateOrder} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Ordering Doctor</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedDoctor} onChange={(e) => setSelectedDoctor(e.target.value)}>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>{d.user?.first_name} {d.user?.last_name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Modality</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm font-semibold" value={modality} onChange={(e) => setModality(e.target.value)}>
                  <option value="X_RAY">X-Ray (Digital)</option>
                  <option value="CT_SCAN">CT Scan</option>
                  <option value="MRI">MRI</option>
                  <option value="ULTRASOUND">Ultrasound / Sonography</option>
                </select>
              </div>
              <Input label="Procedure Name" required value={procedure} onChange={(e) => setProcedure(e.target.value)} />
            </div>

            <Input label="Clinical Indication" required value={indication} onChange={(e) => setIndication(e.target.value)} />

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowOrderModal(false)}>Cancel</Button>
              <Button type="submit">Schedule Study</Button>
            </div>
          </form>
        </Modal>

        {/* Enter Report Modal */}
        {selectedOrder && (
          <Modal
            isOpen={showReportModal}
            onClose={() => setShowReportModal(false)}
            title={`Sign Radiology Diagnostic Report — ${selectedOrder.procedure_name}`}
          >
            <form onSubmit={handleSaveReport} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Detailed Radiological Findings</label>
                <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={4} required placeholder="No acute focal consolidation. Heart size normal..." value={findings} onChange={(e) => setFindings(e.target.value)} />
              </div>
              <Input label="Diagnostic Impression / Summary" required placeholder="e.g. Normal baseline chest radiograph." value={impression} onChange={(e) => setImpression(e.target.value)} />
              <div className="flex items-center gap-2">
                <input type="checkbox" id="crit" checked={isCritical} onChange={(e) => setIsCritical(e.target.checked)} />
                <label htmlFor="crit" className="text-xs text-rose-700 font-bold">Flag as Critical Panic Finding (Alert Clinician)</label>
              </div>
              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowReportModal(false)}>Cancel</Button>
                <Button type="submit">Approve & Sign Report</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
