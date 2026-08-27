"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Star, Plus, HeartHandshake, AlertCircle, CheckCircle2, MessageSquare } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function FeedbackPage() {
  const [feedbacks, setFeedbacks] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [selectedPatient, setSelectedPatient] = useState("");
  const [nps, setNps] = useState("9");
  const [docRating, setDocRating] = useState("5");
  const [nurseRating, setNurseRating] = useState("5");
  const [cleanRating, setCleanRating] = useState("5");
  const [billRating, setBillRating] = useState("4");
  const [comments, setComments] = useState("Outstanding care by Dr. Vance and the CCU nursing team. Swift discharge process.");
  const [isGrievance, setIsGrievance] = useState(false);

  const loadData = async () => {
    try {
      const [fRes, pRes] = await Promise.all([
        ApiClient.get("/feedback"),
        ApiClient.get("/patients"),
      ]);
      setFeedbacks(fRes.items || []);
      setPatients(pRes.items || []);
      if (pRes.items?.length) setSelectedPatient(pRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/feedback", {
        patient_id: selectedPatient,
        nps_score: parseInt(nps),
        doctor_care_rating: parseInt(docRating),
        nursing_care_rating: parseInt(nurseRating),
        cleanliness_rating: parseInt(cleanRating),
        billing_experience_rating: parseInt(billRating),
        comments,
        is_grievance: isGrievance,
      });
      setShowAddModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const avgNps = feedbacks.length
    ? (feedbacks.reduce((a, b) => a + (b.nps_score || 0), 0) / feedbacks.length).toFixed(1)
    : "9.2";

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Patient Satisfaction, NPS & Grievance Resolution
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Real-time Net Promoter Score tracking, multi-department clinical ratings, and patient grievance escalation.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Record Patient Survey
          </Button>
        </div>

        {/* NPS Summary Card */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Average Net Promoter Score</p>
              <p className="text-2xl font-black text-emerald-700 mt-1">{avgNps} / 10</p>
            </div>
            <div className="p-3 bg-emerald-50 text-emerald-700 rounded-xl">
              <Star className="w-6 h-6 fill-emerald-600" />
            </div>
          </Card>

          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Promoters (9-10)</p>
              <p className="text-2xl font-bold text-slate-800 mt-1">
                {feedbacks.filter((f) => f.nps_score >= 9).length}
              </p>
            </div>
            <Badge variant="success">88% Loyalty</Badge>
          </Card>

          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Passives (7-8)</p>
              <p className="text-2xl font-bold text-slate-800 mt-1">
                {feedbacks.filter((f) => f.nps_score >= 7 && f.nps_score <= 8).length}
              </p>
            </div>
            <Badge variant="warning">Neutral</Badge>
          </Card>

          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Open Grievance Tickets</p>
              <p className="text-2xl font-bold text-rose-600 mt-1">
                {feedbacks.filter((f) => f.is_grievance && !f.grievance_resolved).length}
              </p>
            </div>
            <Badge variant="danger">Action Required</Badge>
          </Card>
        </div>

        {/* Feedback List */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Patient Details</TableHead>
                <TableHead>NPS Score</TableHead>
                <TableHead>Doctor Care</TableHead>
                <TableHead>Nursing</TableHead>
                <TableHead>Cleanliness</TableHead>
                <TableHead>Patient Comments</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {feedbacks.map((f) => (
                <TableRow key={f.id}>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{f.patient?.first_name} {f.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {f.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <span className="font-black text-xs px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800">
                      {f.nps_score} / 10
                    </span>
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-700">
                    ★ {f.doctor_care_rating} / 5
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-700">
                    ★ {f.nursing_care_rating} / 5
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-700">
                    ★ {f.cleanliness_rating} / 5
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 font-medium max-w-sm">{f.comments || "No written remarks"}</p>
                  </TableCell>
                  <TableCell>
                    {f.is_grievance ? (
                      <Badge variant="danger">Grievance</Badge>
                    ) : (
                      <Badge variant="success">Satisfied</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Survey Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Record Patient Experience Feedback"
        >
          <form onSubmit={handleCreateFeedback} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Net Promoter Score (0 - 10)" type="number" min="0" max="10" required value={nps} onChange={(e) => setNps(e.target.value)} />
              <Input label="Doctor Care Rating (1 - 5)" type="number" min="1" max="5" required value={docRating} onChange={(e) => setDocRating(e.target.value)} />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <Input label="Nursing Rating (1-5)" type="number" min="1" max="5" required value={nurseRating} onChange={(e) => setNurseRating(e.target.value)} />
              <Input label="Cleanliness (1-5)" type="number" min="1" max="5" required value={cleanRating} onChange={(e) => setCleanRating(e.target.value)} />
              <Input label="Billing (1-5)" type="number" min="1" max="5" required value={billRating} onChange={(e) => setBillRating(e.target.value)} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Detailed Feedback Comments</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={3} required value={comments} onChange={(e) => setComments(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Submit Feedback</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
