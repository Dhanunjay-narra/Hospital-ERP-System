"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Boxes, Plus, AlertTriangle, ArrowRightLeft, Warehouse } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function InventoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [warehouses, setWarehouses] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [code, setCode] = useState("ITM-GLV-LATEX");
  const [name, setName] = useState("Surgical Sterile Gloves Size 7.5");
  const [category, setCategory] = useState("CONSUMABLES");
  const [uom, setUom] = useState("BOX");
  const [selectedWh, setSelectedWh] = useState("");
  const [qty, setQty] = useState("250");
  const [reorder, setReorder] = useState("50");
  const [cost, setCost] = useState("12.50");

  const loadData = async () => {
    try {
      const [itRes, whRes] = await Promise.all([
        ApiClient.get("/inventory/items"),
        ApiClient.get("/inventory/warehouses"),
      ]);
      setItems(itRes.items || []);
      setWarehouses(whRes || []);
      if (whRes?.length) setSelectedWh(whRes[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/inventory/items", {
        item_code: code,
        item_name: name,
        category,
        unit_of_measure: uom,
        warehouse_id: selectedWh,
        quantity_on_hand: parseInt(qty),
        reorder_threshold: parseInt(reorder),
        unit_cost: parseFloat(cost),
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
              Hospital Central Inventory & Store Ledger
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Multi-store stock tracking, consumable thresholds, inter-store requisition transfers, and valuation.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Add Stock Item
          </Button>
        </div>

        {/* Warehouses Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Central Medical Store</p>
              <p className="text-sm font-bold text-slate-800 mt-1">14,200 Units (Level B1)</p>
            </div>
            <Warehouse className="w-6 h-6 text-teal-700" />
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">OT Surgical Sub-Store</p>
              <p className="text-sm font-bold text-slate-800 mt-1">3,850 Units (Floor 2)</p>
            </div>
            <Warehouse className="w-6 h-6 text-indigo-700" />
          </Card>
          <Card className="p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-500 uppercase font-semibold">Emergency Trauma Sub-Store</p>
              <p className="text-sm font-bold text-slate-800 mt-1">1,920 Units (Ground Floor)</p>
            </div>
            <Warehouse className="w-6 h-6 text-rose-700" />
          </Card>
        </div>

        {/* Items Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Item Code</TableHead>
                <TableHead>Item Name</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Assigned Store</TableHead>
                <TableHead>Current Stock</TableHead>
                <TableHead>Unit Cost</TableHead>
                <TableHead>Reorder Alert</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((i) => (
                <TableRow key={i.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {i.item_code}
                  </TableCell>
                  <TableCell className="font-semibold text-slate-800 text-xs">
                    {i.item_name}
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{i.category}</Badge>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {i.warehouse?.name || "Central Store"}
                  </TableCell>
                  <TableCell>
                    <span className="font-bold text-xs text-slate-800">
                      {i.quantity_on_hand} {i.unit_of_measure}
                    </span>
                  </TableCell>
                  <TableCell className="text-xs text-slate-700 font-semibold">
                    {formatCurrency(i.unit_cost)}
                  </TableCell>
                  <TableCell>
                    {i.quantity_on_hand <= i.reorder_threshold ? (
                      <Badge variant="danger" size="sm">
                        Low Stock (≤ {i.reorder_threshold})
                      </Badge>
                    ) : (
                      <Badge variant="success" size="sm">
                        Adequate
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Add Item Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Add General Hospital Stock Item"
        >
          <form onSubmit={handleCreateItem} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="Item Code" required value={code} onChange={(e) => setCode(e.target.value)} />
              <Input label="Item Name" required value={name} onChange={(e) => setName(e.target.value)} />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Category</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={category} onChange={(e) => setCategory(e.target.value)}>
                  <option value="CONSUMABLES">Consumables</option>
                  <option value="SURGICAL_INSTRUMENTS">Surgical Instruments</option>
                  <option value="PPE">PPE & Safety</option>
                  <option value="LINEN">Hospital Linen</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Store / Warehouse</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedWh} onChange={(e) => setSelectedWh(e.target.value)}>
                  {warehouses.map((w) => (
                    <option key={w.id} value={w.id}>{w.name}</option>
                  ))}
                </select>
              </div>

              <Input label="Unit of Measure" required value={uom} onChange={(e) => setUom(e.target.value)} />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <Input label="Quantity on Hand" type="number" required value={qty} onChange={(e) => setQty(e.target.value)} />
              <Input label="Reorder Alert Threshold" type="number" required value={reorder} onChange={(e) => setReorder(e.target.value)} />
              <Input label="Unit Cost ($)" type="number" step="0.01" required value={cost} onChange={(e) => setCost(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Save to Stock Catalog</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
