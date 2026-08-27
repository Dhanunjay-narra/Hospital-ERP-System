"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { ShoppingCart, Plus, Truck, Building, FileCheck } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function ProcurementPage() {
  const [pos, setPos] = useState<any[]>([]);
  const [vendors, setVendors] = useState<any[]>([]);
  const [items, setItems] = useState<any[]>([]);
  const [warehouses, setWarehouses] = useState<any[]>([]);
  const [showPOModal, setShowPOModal] = useState(false);
  const [showVendorModal, setShowVendorModal] = useState(false);

  // PO Form
  const [selectedVendor, setSelectedVendor] = useState("");
  const [selectedWh, setSelectedWh] = useState("");
  const [selectedItem, setSelectedItem] = useState("");
  const [orderQty, setOrderQty] = useState("100");
  const [unitRate, setUnitRate] = useState("12.00");

  // Vendor Form
  const [vName, setVName] = useState("");
  const [vCode, setVCode] = useState("");
  const [vEmail, setVEmail] = useState("");
  const [vPhone, setVPhone] = useState("");

  const loadData = async () => {
    try {
      const [poRes, vRes, itRes, whRes] = await Promise.all([
        ApiClient.get("/procurement/purchase-orders"),
        ApiClient.get("/procurement/vendors"),
        ApiClient.get("/inventory/items"),
        ApiClient.get("/inventory/warehouses"),
      ]);
      setPos(poRes.items || []);
      setVendors(vRes || []);
      setItems(itRes.items || []);
      setWarehouses(whRes || []);

      if (vRes?.length) setSelectedVendor(vRes[0].id);
      if (whRes?.length) setSelectedWh(whRes[0].id);
      if (itRes.items?.length) setSelectedItem(itRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreatePO = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const itemObj = items.find((i) => i.id === selectedItem);
      await ApiClient.post("/procurement/purchase-orders", {
        vendor_id: selectedVendor,
        warehouse_id: selectedWh,
        expected_delivery_date: "2026-09-15",
        items: [
          {
            item_id: selectedItem,
            item_name: itemObj?.item_name || "General Consumable",
            quantity_ordered: parseInt(orderQty) || 100,
            unit_price: parseFloat(unitRate) || 10,
          },
        ],
      });
      setShowPOModal(false);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateVendor = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/procurement/vendors", {
        name: vName,
        vendor_code: vCode,
        email: vEmail,
        phone: vPhone,
      });
      setShowVendorModal(false);
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
              Procurement & Vendor Supply Chain
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Purchase orders lifecycle, approved vendor directories, and 3-way matching goods receipts (GRN).
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowVendorModal(true)} leftIcon={<Building className="w-4 h-4" />}>
              Add Vendor
            </Button>
            <Button size="sm" onClick={() => setShowPOModal(true)} leftIcon={<Plus className="w-4 h-4" />}>
              Create Purchase Order
            </Button>
          </div>
        </div>

        {/* PO Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>PO #</TableHead>
                <TableHead>Vendor Details</TableHead>
                <TableHead>Ordered Line Items</TableHead>
                <TableHead>PO Total Amount</TableHead>
                <TableHead>Order Date</TableHead>
                <TableHead>Payment</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {pos.map((po) => (
                <TableRow key={po.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {po.po_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{po.vendor?.name}</p>
                    <p className="text-[11px] text-slate-400 font-mono">{po.vendor?.vendor_code} • {po.vendor?.phone}</p>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-0.5">
                      {po.items?.map((it: any) => (
                        <p key={it.id} className="text-xs text-slate-700">
                          {it.item_name} — {it.quantity_ordered} Qty
                        </p>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell className="font-bold text-slate-800 text-xs">
                    {formatCurrency(po.grand_total)}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(po.order_date)}
                  </TableCell>
                  <TableCell>
                    <Badge variant={po.payment_status === "PAID" ? "success" : "neutral"}>
                      {po.payment_status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={po.status === "APPROVED" || po.status === "GOODS_RECEIVED" ? "success" : "brand"}>
                      {po.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Create PO Modal */}
        <Modal
          isOpen={showPOModal}
          onClose={() => setShowPOModal(false)}
          title="Create Official Purchase Order (PO)"
        >
          <form onSubmit={handleCreatePO} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Select Vendor</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedVendor} onChange={(e) => setSelectedVendor(e.target.value)}>
                {vendors.map((v) => (
                  <option key={v.id} value={v.id}>{v.name} ({v.vendor_code})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Receiving Store</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedWh} onChange={(e) => setSelectedWh(e.target.value)}>
                  {warehouses.map((w) => (
                    <option key={w.id} value={w.id}>{w.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Item to Order</label>
                <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedItem} onChange={(e) => setSelectedItem(e.target.value)}>
                  {items.map((it) => (
                    <option key={it.id} value={it.id}>{it.item_name} ({it.item_code})</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Order Quantity" type="number" required value={orderQty} onChange={(e) => setOrderQty(e.target.value)} />
              <Input label="Negotiated Unit Price ($)" type="number" step="0.01" required value={unitRate} onChange={(e) => setUnitRate(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowPOModal(false)}>Cancel</Button>
              <Button type="submit">Approve & Dispatch PO</Button>
            </div>
          </form>
        </Modal>

        {/* Create Vendor Modal */}
        <Modal
          isOpen={showVendorModal}
          onClose={() => setShowVendorModal(false)}
          title="Register Hospital Vendor"
        >
          <form onSubmit={handleCreateVendor} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input label="Company Name" required value={vName} onChange={(e) => setVName(e.target.value)} />
              <Input label="Vendor Code" required value={vCode} onChange={(e) => setVCode(e.target.value)} />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Input label="Email" type="email" required value={vEmail} onChange={(e) => setVEmail(e.target.value)} />
              <Input label="Phone" required value={vPhone} onChange={(e) => setVPhone(e.target.value)} />
            </div>
            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowVendorModal(false)}>Cancel</Button>
              <Button type="submit">Save Vendor</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
