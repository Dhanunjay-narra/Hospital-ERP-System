"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Archive, Plus, ShieldAlert, FolderKey, FileText } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function MedicalRecordsPage() {
  const [archives, setArchives] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showArchiveModal, setShowArchiveModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [rackNo, setRackNo] = useState("Rack-B4-Shelf-12");
  const [pages, setPages] = useState("32");
  const [retention, setRetention] = useState("10");

  const loadData = async () => {
    try {
      const [aRes, pRes] = await Promise.all([
        ApiClient.get("/medical-records/archives"),
        ApiClient.get("/patients"),
      ]);
      setArchives(aRes.items || []);
      setPatients(pRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateArchive = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/medical-records/archives", {
        patient_id: selectedPatient,
        physical_rack_number: rackNo,
        total_file_pages: parseInt(pages) || 20,
        retention_period_years: parseInt(retention) || 10,
      });
      setShowArchiveModal(false);
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
              Medical Records Department (MRD) Archives
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Physical file indexing, rack locators, legal retention policies, and HIPAA/GDPR disclosure audit tracking.
            </p>
          </div>
          <Button
            onClick={() => setShowArchiveModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Archive Medical Dossier
          </Button>
        </div>

        {/* Archives Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>MRD File #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Physical Storage Location</TableHead>
                <TableHead>Dossier Size</TableHead>
                <TableHead>Retention Window</TableHead>
                <TableHead>Archived Date</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {archives.map((a) => (
                <TableRow key={a.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {a.archive_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{a.patient?.first_name} {a.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {a.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{a.physical_rack_number}</Badge>
                  </TableCell>
                  <TableCell className="text-xs text-slate-700 font-medium">
                    {a.total_file_pages} Verified Pages
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {a.retention_period_years} Years Legal Retention
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(a.archived_date)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">{a.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Archive Modal */}
        <Modal
          isOpen={showArchiveModal}
          onClose={() => setShowArchiveModal(false)}
          title="Archive Patient Medical Dossier"
        >
          <form onSubmit={handleCreateArchive} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <Input label="Physical Rack / Compactor Location" required value={rackNo} onChange={(e) => setRackNo(e.target.value)} />

            <div className="grid grid-cols-2 gap-3">
              <Input label="Total Dossier Pages" type="number" required value={pages} onChange={(e) => setPages(e.target.value)} />
              <Input label="Retention Mandate (Years)" type="number" required value={retention} onChange={(e) => setRetention(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowArchiveModal(false)}>Cancel</Button>
              <Button type="submit">Complete Physical Archive</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
