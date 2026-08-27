"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Receipt, Plus, DollarSign, CreditCard, CheckCircle2, UserCheck, Printer } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function BillingPage() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [showInvoiceModal, setShowInvoiceModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState<any>(null);

  // Invoice Form
  const [selectedPatient, setSelectedPatient] = useState("");
  const [serviceName, setServiceName] = useState("Doctor Specialist Consultation");
  const [quantity, setQuantity] = useState("1");
  const [rate, setRate] = useState("120.00");

  // Payment Form
  const [payAmount, setPayAmount] = useState("120.00");
  const [payMethod, setPayMethod] = useState("CREDIT_CARD");
  const [reference, setReference] = useState("TXN-CARD-9921");

  const loadData = async () => {
    try {
      const [invRes, patRes] = await Promise.all([
        ApiClient.get("/billing/invoices"),
        ApiClient.get("/patients"),
      ]);
      setInvoices(invRes.items || []);
      setPatients(patRes.items || []);
      if (patRes.items?.length) setSelectedPatient(patRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateInvoice = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/billing/invoices", {
        patient_id: selectedPatient,
        items: [
          {
            service_name: serviceName,
            quantity: parseInt(quantity) || 1,
            unit_price: parseFloat(rate) || 100,
            discount_percent: 0,
            tax_amount: 0,
          },
        ],
      });
      setShowInvoiceModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleRecordPayment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedInvoice) return;
    try {
      await ApiClient.post("/billing/payments", {
        invoice_id: selectedInvoice.id,
        amount: parseFloat(payAmount),
        payment_method: payMethod,
        transaction_reference: reference,
      });
      setShowPaymentModal(false);
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
              Hospital Billing, Invoicing & Cashier Desk
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Centralized financial transactions, multi-department charges aggregation, split payments, and official receipts.
            </p>
          </div>
          <Button
            onClick={() => setShowInvoiceModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Create Invoice
          </Button>
        </div>

        {/* Financial Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Total Invoiced</p>
              <p className="text-xl font-bold text-slate-800 mt-1">
                {formatCurrency(invoices.reduce((a, b) => a + (b.total_amount || 0), 0))}
              </p>
            </div>
            <div className="p-3 bg-teal-50 text-teal-700 rounded-xl">
              <Receipt className="w-6 h-6" />
            </div>
          </Card>

          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Total Collected (Cash/Card)</p>
              <p className="text-xl font-bold text-emerald-700 mt-1">
                {formatCurrency(invoices.reduce((a, b) => a + (b.paid_amount || 0), 0))}
              </p>
            </div>
            <div className="p-3 bg-emerald-50 text-emerald-700 rounded-xl">
              <DollarSign className="w-6 h-6" />
            </div>
          </Card>

          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Outstanding Patient Balance</p>
              <p className="text-xl font-bold text-rose-600 mt-1">
                {formatCurrency(invoices.reduce((a, b) => a + (b.balance_amount || 0), 0))}
              </p>
            </div>
            <div className="p-3 bg-rose-50 text-rose-700 rounded-xl">
              <CreditCard className="w-6 h-6" />
            </div>
          </Card>
        </div>

        {/* Invoices List */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Invoice #</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Services Billed</TableHead>
                <TableHead>Total Amount</TableHead>
                <TableHead>Paid Amount</TableHead>
                <TableHead>Balance</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {invoices.map((inv) => (
                <TableRow key={inv.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {inv.invoice_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{inv.patient?.first_name} {inv.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {inv.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-0.5">
                      {inv.items?.map((item: any) => (
                        <p key={item.id} className="text-xs text-slate-700">
                          {item.service_name} ({item.quantity}x)
                        </p>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell className="font-bold text-slate-800 text-xs">
                    {formatCurrency(inv.total_amount)}
                  </TableCell>
                  <TableCell className="text-xs text-emerald-700 font-semibold">
                    {formatCurrency(inv.paid_amount)}
                  </TableCell>
                  <TableCell className="text-xs text-rose-600 font-bold">
                    {formatCurrency(inv.balance_amount)}
                  </TableCell>
                  <TableCell>
                    <Badge variant={inv.status === "PAID" ? "success" : inv.status === "PARTIALLY_PAID" ? "warning" : "neutral"}>
                      {inv.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    {inv.balance_amount > 0 && (
                      <Button
                        size="sm"
                        variant="primary"
                        onClick={() => {
                          setSelectedInvoice(inv);
                          setPayAmount(String(inv.balance_amount));
                          setShowPaymentModal(true);
                        }}
                        leftIcon={<CreditCard className="w-3.5 h-3.5" />}
                      >
                        Collect Pay
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Create Invoice Modal */}
        <Modal
          isOpen={showInvoiceModal}
          onClose={() => setShowInvoiceModal(false)}
          title="Generate Patient Invoice"
        >
          <form onSubmit={handleCreateInvoice} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Patient</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedPatient} onChange={(e) => setSelectedPatient(e.target.value)}>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.uhid} — {p.first_name} {p.last_name}</option>
                ))}
              </select>
            </div>

            <Input label="Billed Service / Item Name" required value={serviceName} onChange={(e) => setServiceName(e.target.value)} />

            <div className="grid grid-cols-2 gap-3">
              <Input label="Quantity" type="number" required value={quantity} onChange={(e) => setQuantity(e.target.value)} />
              <Input label="Unit Price ($)" type="number" step="0.01" required value={rate} onChange={(e) => setRate(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowInvoiceModal(false)}>Cancel</Button>
              <Button type="submit">Issue Official Invoice</Button>
            </div>
          </form>
        </Modal>

        {/* Collect Payment Modal */}
        {selectedInvoice && (
          <Modal
            isOpen={showPaymentModal}
            onClose={() => setShowPaymentModal(false)}
            title={`Collect Payment — ${selectedInvoice.invoice_number}`}
          >
            <form onSubmit={handleRecordPayment} className="space-y-4">
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs flex justify-between">
                <div>
                  <span className="font-semibold text-slate-700">Patient:</span> {selectedInvoice.patient?.first_name} {selectedInvoice.patient?.last_name}
                </div>
                <div>
                  <span className="font-semibold text-slate-700">Outstanding:</span> {formatCurrency(selectedInvoice.balance_amount)}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Input label="Payment Amount ($)" type="number" step="0.01" required value={payAmount} onChange={(e) => setPayAmount(e.target.value)} />
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Payment Method</label>
                  <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={payMethod} onChange={(e) => setPayMethod(e.target.value)}>
                    <option value="CREDIT_CARD">Credit / Debit Card</option>
                    <option value="CASH">Cash at Counter</option>
                    <option value="UPI">UPI / Digital Wallet</option>
                    <option value="BANK_TRANSFER">Bank Wire</option>
                    <option value="INSURANCE_CLAIM">Insurance Third-Party</option>
                  </select>
                </div>
              </div>

              <Input label="Reference / Authorization ID" value={reference} onChange={(e) => setReference(e.target.value)} />

              <div className="pt-2 flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowPaymentModal(false)}>Cancel</Button>
                <Button type="submit">Print Receipt & Complete</Button>
              </div>
            </form>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
