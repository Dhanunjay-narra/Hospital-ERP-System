"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { FileHeart, Pill, Stethoscope, Clock, ShieldAlert } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function ClinicalPage() {
  const [prescriptions, setPrescriptions] = useState<any[]>([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await ApiClient.get("/clinical/prescriptions");
        setPrescriptions(res.items || []);
      } catch (e) {
        console.error(e);
      }
    };
    loadData();
  }, []);

  return (
    <AppLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
            Clinical Records & Electronic Medical Records (EMR)
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Longitudinal electronic health records, active electronic prescriptions, and diagnostic timeline.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Issued Electronic Prescriptions</CardTitle>
            <Badge variant="brand">{prescriptions.length} Active Prescriptions</Badge>
          </CardHeader>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Rx Number</TableHead>
                <TableHead>Patient Details</TableHead>
                <TableHead>Doctor</TableHead>
                <TableHead>Issued Date</TableHead>
                <TableHead>Medications Prescribed</TableHead>
                <TableHead>Dispense Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {prescriptions.map((rx) => (
                <TableRow key={rx.id}>
                  <TableCell className="font-mono font-bold text-teal-800 text-xs">
                    {rx.prescription_number}
                  </TableCell>
                  <TableCell>
                    <p className="font-semibold text-slate-800">{rx.patient?.first_name} {rx.patient?.last_name}</p>
                    <p className="text-xs text-slate-400">UHID: {rx.patient?.uhid}</p>
                  </TableCell>
                  <TableCell>
                    <p className="font-medium text-slate-800">{rx.doctor?.user?.first_name} {rx.doctor?.user?.last_name}</p>
                    <p className="text-xs text-teal-600">{rx.doctor?.specialization}</p>
                  </TableCell>
                  <TableCell className="text-xs text-slate-600">
                    {formatDate(rx.issued_date)}
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      {rx.items?.map((item: any) => (
                        <div key={item.id} className="text-xs">
                          <span className="font-semibold text-slate-800">{item.medicine_name}</span>
                          <span className="text-slate-500"> — {item.dosage} ({item.frequency}, {item.duration_days} days)</span>
                        </div>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant={rx.status === "DISPENSED" ? "success" : "warning"}>
                      {rx.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      </div>
    </AppLayout>
  );
}
