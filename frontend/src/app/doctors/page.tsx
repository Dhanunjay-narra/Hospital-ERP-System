"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Stethoscope, Clock, DollarSign, Calendar, MapPin, CheckCircle2, Plus } from "lucide-react";
import { ApiClient } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [branches, setBranches] = useState<any[]>([]);
  const [filterSpec, setFilterSpec] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedDocSchedule, setSelectedDocSchedule] = useState<any>(null);

  // Form State
  const [selectedUser, setSelectedUser] = useState("");
  const [specialization, setSpecialization] = useState("Interventional Cardiology");
  const [licenseNumber, setLicenseNumber] = useState("MED-2026-9901");
  const [qualification, setQualification] = useState("MBBS, MD, DM (Cardiology)");
  const [experienceYears, setExperienceYears] = useState("12");
  const [fee, setFee] = useState("150000"); // in cents ($150.00)
  const [room, setRoom] = useState("OPD Suite 204");

  const loadDoctors = async () => {
    try {
      const [docRes, userRes, branchRes] = await Promise.all([
        ApiClient.get("/doctors", { specialization: filterSpec }),
        ApiClient.get("/users"),
        ApiClient.get("/organization/branches"),
      ]);
      setDoctors(docRes.items || []);
      setUsers(userRes.items || []);
      setBranches(branchRes.items || []);
      if (userRes.items?.length) setSelectedUser(userRes.items[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, [filterSpec]);

  const handleCreateDoctor = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/doctors", {
        user_id: selectedUser,
        specialization,
        license_number: licenseNumber,
        qualification,
        experience_years: parseInt(experienceYears) || 5,
        consultation_fee: parseInt(fee) || 10000,
        consultation_room: room,
        is_on_duty: true,
      });
      setShowAddModal(false);
      loadDoctors();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const daysMap = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 tracking-tight">
              Doctor & Provider Management
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Consultant profiles, medical qualifications, consultation fees, and weekly OPD duty rosters.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Onboard Consultant
          </Button>
        </div>

        {/* Doctor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {doctors.map((doc) => (
            <Card key={doc.id} className="p-5 flex flex-col justify-between space-y-4 hover:border-teal-500 transition">
              <div>
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-800 font-bold text-base flex items-center justify-center">
                      <Stethoscope className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-slate-800">
                        {doc.user ? `${doc.user.first_name} ${doc.user.last_name}` : "Doctor"}
                      </h3>
                      <p className="text-xs text-teal-700 font-semibold">{doc.specialization}</p>
                    </div>
                  </div>
                  <Badge variant={doc.is_on_duty ? "success" : "neutral"}>
                    {doc.is_on_duty ? "On Duty" : "Off Duty"}
                  </Badge>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 text-xs text-slate-600">
                  <div className="flex justify-between">
                    <span className="text-slate-400">License #</span>
                    <span className="font-mono font-medium">{doc.license_number}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Qualifications</span>
                    <span className="font-medium">{doc.qualification} ({doc.experience_years} yrs exp)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Consultation Room</span>
                    <span className="font-medium text-slate-800">{doc.consultation_room || "Room 101"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">OPD Fee</span>
                    <span className="font-bold text-emerald-700">{formatCurrency(doc.consultation_fee)}</span>
                  </div>
                </div>

                {/* Working Days */}
                <div className="mt-3">
                  <p className="text-[11px] font-semibold text-slate-500 uppercase mb-1.5">Weekly Schedule</p>
                  <div className="flex gap-1 flex-wrap">
                    {doc.schedules?.length ? (
                      doc.schedules.map((s: any) => (
                        <span
                          key={s.id}
                          className="px-2 py-0.5 text-[10px] font-bold bg-slate-100 text-slate-700 rounded"
                        >
                          {daysMap[s.day_of_week]}
                        </span>
                      ))
                    ) : (
                      <span className="px-2 py-0.5 text-[10px] font-bold bg-teal-50 text-teal-800 rounded">
                        Mon - Fri (Full Time)
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <Button
                size="sm"
                variant="outline"
                className="w-full"
                onClick={() => setSelectedDocSchedule(doc)}
              >
                View Calendar & Slots
              </Button>
            </Card>
          ))}
        </div>

        {/* Add Doctor Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Onboard Medical Doctor / Consultant"
        >
          <form onSubmit={handleCreateDoctor} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">Associated System User</label>
              <select className="w-full rounded-lg border border-slate-300 p-2 text-sm" value={selectedUser} onChange={(e) => setSelectedUser(e.target.value)}>
                {users.map((u) => (
                  <option key={u.id} value={u.id}>{u.first_name} {u.last_name} ({u.email})</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Medical Specialty" required value={specialization} onChange={(e) => setSpecialization(e.target.value)} />
              <Input label="Medical Council License #" required value={licenseNumber} onChange={(e) => setLicenseNumber(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Academic Qualifications" required value={qualification} onChange={(e) => setQualification(e.target.value)} />
              <Input label="Years of Experience" type="number" required value={experienceYears} onChange={(e) => setExperienceYears(e.target.value)} />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input label="Consultation Fee (Cents)" type="number" required value={fee} onChange={(e) => setFee(e.target.value)} />
              <Input label="Consultation OPD Room" required value={room} onChange={(e) => setRoom(e.target.value)} />
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>Cancel</Button>
              <Button type="submit">Save Doctor Profile</Button>
            </div>
          </form>
        </Modal>

        {/* Schedule Modal */}
        {selectedDocSchedule && (
          <Modal
            isOpen={!!selectedDocSchedule}
            onClose={() => setSelectedDocSchedule(null)}
            title={`OPD Consultation Schedule — ${selectedDocSchedule.user?.first_name} ${selectedDocSchedule.user?.last_name}`}
          >
            <div className="space-y-4">
              <div className="p-3 bg-teal-50 rounded-lg text-xs space-y-1 text-teal-900">
                <p className="font-bold">Active Consultation Hours:</p>
                <p>Monday – Friday: 09:00 AM – 01:00 PM & 03:00 PM – 06:00 PM</p>
                <p>Saturday: 09:00 AM – 01:00 PM (Emergency & Follow-ups)</p>
              </div>

              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase">Available Time Slot Increments</h4>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  {["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "03:00 PM", "03:30 PM", "04:00 PM"].map((slot) => (
                    <div key={slot} className="p-2 border border-slate-200 rounded text-center bg-slate-50 text-slate-700 font-mono font-semibold">
                      {slot}
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-2 flex justify-end">
                <Button variant="outline" onClick={() => setSelectedDocSchedule(null)}>Close Schedule</Button>
              </div>
            </div>
          </Modal>
        )}
      </div>
    </AppLayout>
  );
}
