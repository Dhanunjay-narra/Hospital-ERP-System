"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { UserPlus, Plus, PhoneCall, MessageSquare, CheckCircle2, UserCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function CRMPage() {
  const [leads, setLeads] = useState<any[]>([]);
  const [showLeadModal, setShowLeadModal] = useState(false);
  const [showInteractModal, setShowInteractModal] = useState(false);
  const [selectedLead, setSelectedLead] = useState<any>(null);

  // Lead Form
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [specialty, setSpecialty] = useState("Cardiology");
  const [source, setSource] = useState("WEBSITE");

  // Interact Form
  const [channel, setChannel] = useState("PHONE_CALL");
  const [summary, setSummary] = useState("Informed about heart health checkup package. Scheduled consultation for Friday.");

  const loadData = async () => {
    try {
      const res = await ApiClient.get("/crm/leads");
      setLeads(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateLead = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/crm/leads", {
        full_name: name,
        phone_number: phone,
        email,
        inquiry_specialty: specialty,
        lead_source: source,
      });
      setShowLeadModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleAddInteraction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedLead) return;
    try {
      await ApiClient.post(`/crm/leads/${selectedLead.id}/interactions`, {
        channel,
        summary,
      });
      setShowInteractModal(false);
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
              Patient CRM, Inquiry Pipeline & Lead Tracking
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Multi-channel acquisition (Website, Calls, Camps), counselor interaction logs, and patient conversion.
            </p>
          </div>
          <Button
            onClick={() => setShowLeadModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Capture New Inquiry
          </Button>
        </div>

        {/* Pipeline Summary Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-blue-700">New Inquiries</span>
            <p className="text-xl font-bold text-blue-700 mt-1">{leads.filter((l) => l.status === "NEW").length}</p>
          </div>
          <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-amber-700">Contacted / In Progress</span>
            <p className="text-xl font-bold text-amber-700 mt-1">{leads.filter((l) => l.status === "CONTACTED").length}</p>
          </div>
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-emerald-700">Converted to Patient</span>
            <p className="text-xl font-bold text-emerald-700 mt-1">{leads.filter((l) => l.status === "CONVERTED").length}</p>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-center">
            <span className="text-[10px] font-bold uppercase text-slate-600">Total Leads Handled</span>
            <p className="text-xl font-bold text-slate-800 mt-1">{leads.length}</p>
          </div>
        </div>

        {/* Leads Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Lead Code</TableHead>
                <TableHead>Inquirer Details</TableHead>
                <TableHead>Clinical Interest</TableHead>
                <TableHead>Acquisition Source</TableHead>
                <TableHead>Interactions</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {leads.map((l) => (
                <TableRow key={l.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {l.lead_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{l.full_name}</p>
                    <p className="text-xs text-slate-400 font-mono">{l.phone_number} {l.email ? `• ${l.email}` : ""}</p>
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-800">
                    {l.inquiry_specialty}
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{l.lead_source}</Badge>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {l.interactions?.length || 0} Logged Touches
                  </TableCell>
                  <TableCell>
                    <Badge variant={l.status === "CONVERTED" ? "success" : l.status === "CONTACTED" ? "warning" : "neutral"}>
                      {l.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => {
                        setSelectedLead(l);
                        setShowInteractModal(true);
                      }}
                      leftIcon={<PhoneCall className="w-3.5 h-3.5" />}
                    >
                      Log Touch
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Capture Lead Modal */}
        <Modal
          isOpen={showLeadModal}
          onClose={() => setShowLeadModal(false)}
          title="Capture Patient Lead / Inquiry"
        >
          <form onSubmit={handleCreateLead} className="space-y-4">
            <Input label="Full Name" required value={name} onChange={(e) => setName(e.target.value)} />
            
            <div className="grid grid-cols-2 gap-3">
              <Input label="Phone Number" required value={phone} onChange={(e) => setPhone(e.target.value)} />
              <Input label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Inquiry Clinical Specialty" required value={specialty} onChange={(e) => setSpecialty(e.target.value)} />
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Acquisition Source</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={source} onChange={(e) => setSource(e.target.value)}>
                  <option value="WEBSITE">Website Portal</option>
                  <option value="PHONE_INQUIRY">Inbound Phone Call</option>
                  <option value="HEALTH_CAMP">Community Health Camp</option>
                  <option value="DOCTOR_REFERRAL">Doctor Referral</option>
                  <option value="SOCIAL_MEDIA">Social Media Campaign</option>
                </select>
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowLeadModal(false)}>Cancel</Button>
              <Button type="submit">Save Patient Lead</Button>
            </div>
          </form>
        </Modal>

        {/* Log Interaction Modal */}
        {selectedLead && (
          <Modal
            isOpen={showInteractModal}
            onClose={() => setShowInteractModal(false)}
            title={`Log Counselor Touchpoint — ${selectedLead.full_name}`}
          >
            <form onSubmit={handleAddInteraction} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Channel</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={channel} onChange={(e) => setChannel(e.target.value)}>
                  <option value="PHONE_CALL">Phone Call</option>
                  <option value="WHATSAPP">WhatsApp Message</option>
                  <option value="EMAIL">Email Follow-up</option>
                  <option value="IN_PERSON">In-Hospital Desk Visit</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Discussion Summary & Outcome</label>
                <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={3} required value={summary} onChange={(e) => setSummary(e.target.value)} />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowInteractModal(false)}>Cancel</Button>
                <Button type="submit">Record Interaction</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
