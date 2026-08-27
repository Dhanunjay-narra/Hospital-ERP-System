"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Megaphone, Plus, Target, Users, TrendingUp, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function MarketingPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [name, setName] = useState("World Heart Day Comprehensive Screening");
  const [code, setCode] = useState("CMP-2026-HEART");
  const [demographic, setDemographic] = useState("Adults 40+");
  const [budget, setBudget] = useState("3500");
  const [packageRate, setPackageRate] = useState("149");
  const [startD, setStartD] = useState("2026-09-01");
  const [endD, setEndD] = useState("2026-09-30");

  const loadData = async () => {
    try {
      const res = await ApiClient.get("/marketing/campaigns");
      setCampaigns(res || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/marketing/campaigns", {
        campaign_name: name,
        campaign_code: code,
        target_demographic: demographic,
        budget_allocated: parseFloat(budget),
        discount_package_rate: parseFloat(packageRate),
        start_date: startD,
        end_date: endD,
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
              Hospital Marketing & Wellness Packages
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Preventive health checkup camps, specialty outreach campaigns, audience demographic targeting, and ROI tracking.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Launch Campaign
          </Button>
        </div>

        {/* Campaigns Table */}
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Campaign Code</TableHead>
                <TableHead>Campaign Program Name</TableHead>
                <TableHead>Target Demographic</TableHead>
                <TableHead>Budget Allocated</TableHead>
                <TableHead>Package Price</TableHead>
                <TableHead>Active Window</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {campaigns.map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-mono font-bold text-xs text-teal-800">
                    {c.campaign_code}
                  </TableCell>
                  <TableCell>
                    <p className="font-bold text-slate-800 text-xs">{c.campaign_name}</p>
                  </TableCell>
                  <TableCell>
                    <Badge variant="brand">{c.target_demographic}</Badge>
                  </TableCell>
                  <TableCell className="text-xs font-semibold text-slate-700">
                    {formatCurrency(c.budget_allocated)}
                  </TableCell>
                  <TableCell className="text-xs font-bold text-emerald-700">
                    {formatCurrency(c.discount_package_rate)}
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(c.start_date)} - {formatDate(c.end_date)}
                  </TableCell>
                  <TableCell>
                    <Badge variant="success">{c.status}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>

        {/* Launch Campaign Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Launch Health Package Campaign"
        >
          <form onSubmit={handleCreateCampaign} className="space-y-4">
            <Input label="Campaign Name" required value={name} onChange={(e) => setName(e.target.value)} />
            
            <div className="grid grid-cols-2 gap-3">
              <Input label="Campaign Code" required value={code} onChange={(e) => setCode(e.target.value)} />
              <Input label="Target Demographic" required value={demographic} onChange={(e) => setDemographic(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Budget Allocated ($)" type="number" required value={budget} onChange={(e) => setBudget(e.target.value)} />
              <Input label="Discounted Package Price ($)" type="number" required value={packageRate} onChange={(e) => setPackageRate(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Start Date" type="date" required value={startD} onChange={(e) => setStartD(e.target.value)} />
              <Input label="End Date" type="date" required value={endD} onChange={(e) => setEndD(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Activate Campaign</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
