"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Send, Plus, MessageSquare, Mail, Phone, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDateTime } from "@/lib/utils";

export default function CommunicationPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [templates, setTemplates] = useState<any[]>([]);
  const [showSendModal, setShowSendModal] = useState(false);
  const [showTplModal, setShowTplModal] = useState(false);

  // Send Form
  const [phone, setPhone] = useState("+1 (555) 998-1122");
  const [channel, setChannel] = useState("SMS");
  const [body, setBody] = useState("Your lab test results for CBC are ready for review on the patient portal.");

  // Template Form
  const [tplCode, setTplCode] = useState("TPL-LAB-READY");
  const [tplTitle, setTplTitle] = useState("Diagnostic Lab Results Alert");

  const loadData = async () => {
    try {
      const [mRes, tRes] = await Promise.all([
        ApiClient.get("/communication/messages"),
        ApiClient.get("/communication/templates"),
      ]);
      setMessages(mRes.items || []);
      setTemplates(tRes || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/communication/dispatch", {
        recipient_phone: phone,
        channel,
        message_body: body,
      });
      setShowSendModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateTemplate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/communication/templates", {
        template_code: tplCode,
        title: tplTitle,
        channel,
        body_content: body,
      });
      setShowTplModal(false);
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
              Hospital Communication Engine & Omnichannel Alerts
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Automated SMS, WhatsApp and Email dispatch for appointment reminders, lab results, and discharge follow-ups.
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowTplModal(true)} leftIcon={<Plus className="w-4 h-4" />}>
              Create Template
            </Button>
            <Button size="sm" onClick={() => setShowSendModal(true)} leftIcon={<Send className="w-4 h-4" />}>
              Dispatch Instant Message
            </Button>
          </div>
        </div>

        {/* Dispatched Messages Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Channel</TableHead>
                <TableHead>Recipient</TableHead>
                <TableHead>Message Content</TableHead>
                <TableHead>Dispatched Timestamp</TableHead>
                <TableHead>Delivery Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {messages.map((m) => (
                <TableRow key={m.id}>
                  <TableCell>
                    <Badge variant="brand">{m.channel}</Badge>
                  </TableCell>
                  <TableCell className="font-mono text-xs font-semibold text-slate-800">
                    {m.recipient_phone || m.recipient_email}
                  </TableCell>
                  <TableCell>
                    <p className="text-xs text-slate-700 font-medium max-w-md">{m.message_body}</p>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDateTime(m.sent_at)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">Delivered ✓</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Dispatch Modal */}
        <Modal
          isOpen={showSendModal}
          onClose={() => setShowSendModal(false)}
          title="Dispatch Omnichannel Notification"
        >
          <form onSubmit={handleSendMessage} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Communication Channel</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={channel} onChange={(e) => setChannel(e.target.value)}>
                  <option value="SMS">SMS Gateway</option>
                  <option value="WHATSAPP">WhatsApp Official API</option>
                  <option value="EMAIL">Transactional Email</option>
                </select>
              </div>

              <Input label="Recipient Phone / Email" required value={phone} onChange={(e) => setPhone(e.target.value)} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Message Body Content</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={4} required value={body} onChange={(e) => setBody(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowSendModal(false)}>Cancel</Button>
              <Button type="submit">Dispatch Message</Button>
            </div>
          </form>
        </Modal>

        {/* Template Modal */}
        <Modal
          isOpen={showTplModal}
          onClose={() => setShowTplModal(false)}
          title="Create Reusable Message Template"
        >
          <form onSubmit={handleCreateTemplate} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="Template Code" required value={tplCode} onChange={(e) => setTplCode(e.target.value)} />
              <Input label="Template Title" required value={tplTitle} onChange={(e) => setTplTitle(e.target.value)} />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Template Format with Placeholders</label>
              <textarea className="w-full rounded-lg border border-slate-300 p-2.5 text-xs" rows={4} required value={body} onChange={(e) => setBody(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowTplModal(false)}>Cancel</Button>
              <Button type="submit">Save Template</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
