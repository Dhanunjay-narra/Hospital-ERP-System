"use client";

import React, { useState, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from "@/components/ui/Table";
import { Users2, Shield, Plus, Key, Lock, CheckCircle2 } from "lucide-react";
import { ApiClient } from "@/lib/api";

export default function UsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<"users" | "roles">("users");
  const [showAddModal, setShowAddModal] = useState(false);

  // Form State
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [selectedRole, setSelectedRole] = useState("");

  const loadData = async () => {
    try {
      const [uRes, rData] = await Promise.all([
        ApiClient.get("/users"),
        ApiClient.get("/roles"),
      ]);
      setUsers(uRes?.items || []);
      setRoles(rData || []);
      if (rData?.length) setSelectedRole(rData[0].id);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ApiClient.post("/users", {
        email,
        username,
        first_name: firstName,
        last_name: lastName,
        password,
        role_ids: selectedRole ? [selectedRole] : [],
      });
      setShowAddModal(false);
      setEmail("");
      setUsername("");
      setFirstName("");
      setLastName("");
      setPassword("");
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
              User & Identity Management (RBAC)
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Manage system staff accounts, cryptographic passwords, role mappings, and granular permissions.
            </p>
          </div>
          <Button
            onClick={() => setShowAddModal(true)}
            leftIcon={<Plus className="w-4 h-4" />}
            size="sm"
          >
            Create Staff Account
          </Button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex gap-2 border-b border-slate-200 pb-2">
          <button
            onClick={() => setActiveTab("users")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition ${
              activeTab === "users"
                ? "bg-teal-700 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Active Users ({users.length})
          </button>
          <button
            onClick={() => setActiveTab("roles")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition ${
              activeTab === "roles"
                ? "bg-teal-700 text-white"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            System Roles & Permissions ({roles.length})
          </button>
        </div>

        {activeTab === "users" && (
          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Staff Name</TableHead>
                  <TableHead>Username / Email</TableHead>
                  <TableHead>Assigned Roles</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Security Flags</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((u) => (
                  <TableRow key={u.id}>
                    <TableCell className="font-semibold text-slate-800">
                      {u.first_name} {u.last_name}
                    </TableCell>
                    <TableCell>
                      <p className="text-xs font-mono text-slate-700">{u.username}</p>
                      <p className="text-xs text-slate-400">{u.email}</p>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {u.roles?.map((r: any) => (
                          <Badge key={r.id} variant="brand">
                            {r.name}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={u.is_active ? "success" : "danger"}>
                        {u.is_active ? "Active" : "Inactive"}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <span className="text-xs text-slate-500">
                        {u.is_verified ? "Verified" : "Pending"} | MFA: {u.is_mfa_enabled ? "ON" : "OFF"}
                      </span>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        )}

        {activeTab === "roles" && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {roles.map((r) => (
              <Card key={r.id} className="p-4 flex flex-col justify-between space-y-3">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded">
                      {r.code}
                    </span>
                    {r.is_system && <Badge variant="neutral">System Built-in</Badge>}
                  </div>
                  <h3 className="text-sm font-bold text-slate-800 mt-2">{r.name}</h3>
                  <p className="text-xs text-slate-500 mt-1">{r.description || "Hospital operational role"}</p>
                </div>
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                  <span>{r.permissions?.length || 0} granular permissions</span>
                  <Shield className="w-4 h-4 text-teal-600" />
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Create User Modal */}
        <Modal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          title="Create New Staff Account"
        >
          <form onSubmit={handleCreateUser} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="First Name"
                required
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
              <Input
                label="Last Name"
                required
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
            <Input
              label="Email Address"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Input
              label="Username"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <Input
              label="Initial Password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                Assign System Role
              </label>
              <select
                className="w-full rounded-lg border border-slate-300 p-2 text-sm text-slate-800 focus:border-teal-600 focus:outline-none"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                {roles.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name} ({r.code})
                  </option>
                ))}
              </select>
            </div>
            <div className="pt-2 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setShowAddModal(false)}>
                Cancel
              </Button>
              <Button type="submit">Create Account</Button>
            </div>
          </form>
        </Modal>
      </div>
    </AppLayout>
  );
}
