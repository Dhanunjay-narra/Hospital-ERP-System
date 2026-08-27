"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Pill, Plus, Search, AlertCircle, CheckCircle2, DollarSign, Package } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function PharmacyPage() {
  const [medicines, setMedicines] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [name, setName] = useState("");
  const [genericName, setGenericName] = useState("");
  const [sku, setSku] = useState("");
  const [category, setCategory] = useState("ANTIBIOTICS");
  const [strength, setStrength] = useState("500mg");
  const [price, setPrice] = useState("1.50");
  const [batchNo, setBatchNo] = useState("BATCH-2026-A");
  const [qty, setQty] = useState("100");
  const [expiry, setExpiry] = useState("2027-12-31");

  const loadMedicines = async () => {
    try {
      const res = await ApiClient.get("/pharmacy/medicines", { search });
      setMedicines(res.items || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadMedicines();
  }, [search]);

  const handleCreateMedicine = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/pharmacy/medicines", {
        name,
        generic_name: genericName,
        sku_code: sku,
        category,
        dosage_form: "TABLET",
        strength,
        unit_price: parseFloat(price),
        mrp: parseFloat(price) * 1.2,
        reorder_level: 50,
        batches: [
          {
            batch_number: batchNo,
            expiry_date: expiry,
            quantity_received: parseInt(qty),
            selling_price: parseFloat(price),
          },
        ],
      });
      setShowAddModal(false);
      loadMedicines();
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
              Hospital Pharmacy & Drug Formulary
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Medicine master catalog, batch-level stock quantities, shelf expiration alerts, and prescription dispensing.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Add New Medicine
          </Button>
        </div>

        {/* Search */}
        <Card className="p-4">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search medicine by brand name, generic formulation, or SKU..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:border-teal-600 focus:outline-none"
            />
          </div>
        </Card>

        {/* Medicines Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>SKU & Formulation</TableHead>
                <TableHead>Generic Active Compound</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Available Stock (Batches)</TableHead>
                <TableHead>Nearest Expiry</TableHead>
                <TableHead>Unit Price</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {medicines.map((m) => {
                const totalStock = m.batches?.reduce((acc: number, b: any) => acc + (b.quantity_available || 0), 0) || 0;
                const firstBatch = m.batches?.[0];
                return (
                  <TableRow key={m.id}>
                    <TableCell>
                      <p className="font-bold text-slate-800 text-sm">{m.name} ({m.strength})</p>
                      <span className="font-mono text-[11px] text-slate-400">{m.sku_code}</span>
                    </TableCell>
                    <TableCell className="text-xs text-slate-600 font-medium">
                      {m.generic_name}
                    </TableCell>
                    <TableCell>
                      <Badge variant="brand">{m.category}</Badge>
                    </TableCell>
                    <TableCell>
                      <span className={`font-bold text-xs ${totalStock < m.reorder_level ? "text-rose-600 font-bold" : "text-emerald-700"}`}>
                        {totalStock} Units ({m.batches?.length || 0} Batches)
                      </span>
                    </TableCell>
                    <TableCell className="text-xs text-slate-600">
                      {firstBatch ? formatDate(firstBatch.expiry_date) : "N/A"}
                    </TableCell>
                    <TableCell className="font-bold text-slate-800 text-xs">
                      {formatCurrency(m.unit_price)}
                    </TableCell>
                    <TableCell>
                      <Badge variant={totalStock > 0 ? "success" : "danger"}>
                        {totalStock > 0 ? "In Stock" : "Out of Stock"}
                      </Badge>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Card>

        {/* Add Medicine Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Add Medicine to Hospital Formulary"
        >
          <form onSubmit={handleCreateMedicine} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="Brand Name" required placeholder="e.g. Augmentin 625mg" value={name} onChange={(e) => setName(e.target.value)} />
              <Input label="Generic Formulation" required placeholder="e.g. Amoxicillin + Clavulanate" value={genericName} onChange={(e) => setGenericName(e.target.value)} />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <Input label="SKU Code" required placeholder="e.g. SKU-AUG-625" value={sku} onChange={(e) => setSku(e.target.value)} />
              <Input label="Strength" required value={strength} onChange={(e) => setStrength(e.target.value)} />
              <Input label="Unit Price ($)" type="number" step="0.01" value={price} onChange={(e) => setPrice(e.target.value)} />
            </div>

            <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
              <p className="text-xs font-bold text-slate-700 uppercase">Initial Batch Details</p>
              <div className="grid grid-cols-3 gap-3">
                <Input label="Batch Number" required value={batchNo} onChange={(e) => setBatchNo(e.target.value)} />
                <Input label="Quantity" type="number" required value={qty} onChange={(e) => setQty(e.target.value)} />
                <Input label="Expiry Date" type="date" required value={expiry} onChange={(e) => setExpiry(e.target.value)} />
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Add to Inventory</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
