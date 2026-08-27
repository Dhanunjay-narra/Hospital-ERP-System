"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { FlaskConical, Plus, AlertTriangle, CheckCircle2, QrCode, FileText } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function LaboratoryPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [catalog, setCatalog] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [doctors, setDoctors] = useState<any[]>([]);
  const [showOrderModal, setShowOrderModal] = useState(false);
  const [showResultModal, setShowResultModal] = useState(false);
  const [selectedResult, setSelectedResult] = useState<any>(null);

  // Order Form
  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [selectedTest, setSelectedTest] = useState("");
  const [priority, setPriority] = useState("ROUTINE");

  // Result Entry Form
  const [resultVal, setResultVal] = useState("");
  const [numericVal, setNumericVal] = useState("");

  const loadData = async () => {
    try {
      const [oRes, cRes, pRes, dRes] = await Promise.all([
        ApiClient.get("/laboratory/orders"),
        ApiClient.get("/laboratory/catalog"),
        ApiClient.get("/patients"),
        ApiClient.get("/doctors"),
      ]);
      setOrders(oRes.items || []);
      setCatalog(cRes || []);
      setPatients(pRes.items || []);
      setDoctors(dRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
      if (dRes.items?.length) setSelectedDoctor(dRes.items[0].id);
      if (cRes?.length) setSelectedTest(cRes[0].id);
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
      await ApiClient.post("/laboratory/orders", {
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
        priority: priority,
        test_ids: [selectedTest],
      });
      setShowOrderModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleSaveResult = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedResult) return;
    try {
      await ApiClient.post(`/laboratory/results/${selectedResult.id}`, {
        value: resultVal,
        numeric_value: numericVal ? parseFloat(numericVal) : undefined,
      });
      setShowResultModal(false);
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
              Diagnostic Laboratory & Pathology Workstation
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Specimen accessioning, barcode tracking, auto-evaluated reference ranges, and critical panic value alerts.
            </p>
          </div>
          <Button
            onClick={() => setShowOrderModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Create Lab Order
          </Button>
        </div>

        {/* Lab Orders Worklist */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Order # & Barcode</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Ordered Tests</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Order Time</TableHead>
                <TableHead>Findings & Values</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {orders.map((o) => (
                <TableRow key={o.id}>
                  <TableCell>
                    <span className="font-mono font-bold text-teal-800 text-xs block">{o.order_number}</span>
                    <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
                      <QrCode className="w-3 h-3" /> {o.sample_barcode}
                    </span>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{o.patient?.first_name} {o.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {o.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      {o.results?.map((r: any) => (
                        <div key={r.id} className="text-xs font-medium text-slate-800">
                          {r.parameter_name}
                        </div>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={o.priority === "STAT" ? "danger" : "neutral"}>
                      {o.priority}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDateTime(o.order_datetime)}
                  </TableCell>
                  <TableCell>
                    {o.results?.map((r: any) => (
                      <div key={r.id} className="text-xs flex items-center gap-2">
                        <span className="font-bold">{r.result_value} {r.unit_of_measure || ""}</span>
                        {r.is_critical && (
                          <Badge variant="danger" size="sm" className="animate-pulse">
                            CRITICAL PANIC
                          </Badge>
                        )}
                        {!r.is_critical && r.is_abnormal && (
                          <Badge variant="warning" size="sm">
                            Abnormal
                          </Badge>
                        )}
                      </div>
                    ))}
                  </TableCell>
                  <TableCell>
                    <Badge variant={o.status === "RESULTED" ? "success" : "brand"}>
                      {o.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {o.results?.length > 0 && o.status !== "RESULTED" && (
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedResult(o.results[0]);
                          setResultVal("");
                          setNumericVal("");
                          setShowResultModal(true);
                        }}
                      >
                        Enter Results
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Create Order Modal */}
        <Modal
          isOpen={showOrderModal}
          onClose={() => setShowOrderModal(false)}
          title="Create Diagnostic Lab Order"
        >
          <form onSubmit={handleCreateOrder} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
              >
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Ordering Physician</label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                value={selectedDoctor}
                onChange={(e) => setSelectedDoctor(e.target.value)}
              >
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>{d.user?.first_name} {d.user?.last_name} ({d.specialization})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Diagnostic Test Panel</label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                  value={selectedTest}
                  onChange={(e) => setSelectedTest(e.target.value)}
                >
                  {catalog.map((c) => (
                    <option key={c.id} value={c.id}>{c.test_code} — {c.test_name} (${c.price})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Priority</label>
                <select
                  className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  <option value="ROUTINE">Routine</option>
                  <option value="URGENT">Urgent</option>
                  <option value="STAT">STAT / Emergency</option>
                </select>
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowOrderModal(false)}>Cancel</Button>
              <Button type="submit">Generate Barcode & Order</Button>
            </div>
          </form>
        </Modal>

        {/* Enter Result Modal */}
        {selectedResult && (
          <Modal
            isOpen={showResultModal}
            onClose={() => setShowResultModal(false)}
            title={`Enter Laboratory Finding — ${selectedResult.parameter_name}`}
          >
            <form onSubmit={handleSaveResult} className="space-y-4">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs">
                <span className="font-semibold text-slate-700">Reference Range:</span> {selectedResult.reference_range} {selectedResult.unit_of_measure || ""}
              </div>

              <Input
                label="Result Text"
                required
                placeholder="e.g. 14.5, Normal, Positive"
                value={resultVal}
                onChange={(e) => setResultVal(e.target.value)}
              />

              <Input
                label="Numeric Value (for panic check)"
                type="number"
                step="0.01"
                placeholder="e.g. 14.5"
                value={numericVal}
                onChange={(e) => setNumericVal(e.target.value)}
              />

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowResultModal(false)}>Cancel</Button>
                <Button type="submit">Validate & Sign Lab Result</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
