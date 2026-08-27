"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { FileCheck, Plus, CheckCircle2, ShieldCheck, Download, Eye } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showDocModal, setShowDocModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [docTitle, setDocTitle] = useState("General Informed Consent for Hospital Treatment");
  const [category, setCategory] = useState("CONSENT_FORM");
  const [signerName, setSignerName] = useState("Patient / Legal Guardian");

  const loadData = async () => {
    try {
      const [dRes, pRes] = await Promise.all([
        ApiClient.get("/documents"),
        ApiClient.get("/patients"),
      ]);
      setDocuments(dRes.items || []);
      setPatients(pRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateDocument = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/documents", {
        patient_id: selectedPatient,
        document_title: docTitle,
        category,
        file_path: "/secure-docs/consents/signed-consent-01.pdf",
        file_size_kb: 245,
        mime_type: "application/pdf",
        is_digitally_signed: true,
        signed_by_name: signerName,
      });
      setShowDocModal(false);
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
              Clinical Documents, Legal Consents & e-Signatures
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Informed surgical consent forms, patient identity scans, insurance verification cards, and digital signature logs.
            </p>
          </div>
          <Button
            onClick={() => setShowDocModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Attach Signed Consent / File
          </Button>
        </div>

        {/* Documents Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Document Title</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Digital Signature Verification</TableHead>
                <TableHead>File Specs</TableHead>
                <TableHead>Date Executed</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documents.map((d) => (
                <TableRow key={d.id}>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{d.document_title}</p>
                    <span className="text-[11px] font-mono text-slate-400">{d.file_path}</span>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{d.category}</Badge>
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{d.patient?.first_name} {d.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {d.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5 text-xs text-emerald-700 font-semibold">
                      <ShieldCheck className="w-4 h-4" /> Signed by {d.signed_by_name || "Patient"}
                    </div>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    PDF • {d.file_size_kb} KB
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(d.created_at)}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="outline" leftIcon={<Eye className="w-3.5 h-3.5" />}>
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Upload Document Modal */}
        <Modal
          isOpen={showDocModal}
          onClose={() => setShowDocModal(false)}
          title="Attach Digitally Signed Clinical Document"
        >
          <form onSubmit={handleCreateDocument} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <Input label="Document Title" required value={docTitle} onChange={(e) => setDocTitle(e.target.value)} />

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Document Category</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={category} onChange={(e) => setCategory(e.target.value)}>
                  <option value="CONSENT_FORM">Informed Consent Form</option>
                  <option value="IDENTITY_PROOF">Identity / ID Proof</option>
                  <option value="INSURANCE_CARD">Insurance Policy Card</option>
                  <option value="DISCHARGE_SUMMARY">Discharge Summary</option>
                </select>
              </div>

              <Input label="Signatory Name" required value={signerName} onChange={(e) => setSignerName(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowDocModal(false)}>Cancel</Button>
              <Button type="submit">Verify & Save Document</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
