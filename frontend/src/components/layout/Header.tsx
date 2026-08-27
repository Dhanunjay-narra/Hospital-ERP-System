"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Menu,
  Bell,
  Search,
  User as UserIcon,
  LogOut,
  Settings,
  Shield,
  Building,
  CheckCircle2,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";

export const Header: React.FC<{ onMenuToggle: () => void }> = ({ onMenuToggle }) => {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    const userInfo = localStorage.getItem("user_info");
    if (userInfo) {
      try {
        setUser(JSON.parse(userInfo));
      } catch (e) {}
    } else {
      setUser({
        first_name: "Super",
        last_name: "Admin",
        email: "admin@hospital.com",
        roles: [{ name: "Super Admin", code: "SUPER_ADMIN" }],
      });
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_info");
    router.push("/login");
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 sticky top-0 z-30 flex items-center justify-between px-4 lg:px-8 shadow-xs">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Global Search Bar */}
        <div className="hidden sm:flex items-center relative w-64 lg:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 pointer-events-none" />
          <input
            type="text"
            placeholder="Search patients (UHID/Name), appointments, doctors..."
            className="w-full pl-9 pr-4 py-1.5 text-xs bg-slate-100/80 hover:bg-slate-100 focus:bg-white border border-transparent focus:border-teal-600 rounded-lg text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-500/20 transition"
          />
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Branch / Tenant Selector */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 font-medium">
          <Building className="w-3.5 h-3.5 text-teal-600" />
          <span>Apex Central Hospital (Main)</span>
        </div>

        {/* Notification Bell */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-100 rounded-lg relative transition"
          >
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full ring-2 ring-white animate-ping" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-500 rounded-full ring-2 ring-white" />
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-slate-200 py-3 z-50 animate-in fade-in">
              <div className="px-4 pb-2 border-b border-slate-100 flex items-center justify-between">
                <span className="font-semibold text-xs text-slate-800">Notifications</span>
                <span className="text-[10px] text-teal-600 font-medium cursor-pointer hover:underline">Mark all read</span>
              </div>
              <div className="divide-y divide-slate-50 text-xs">
                <div className="px-4 py-3 hover:bg-slate-50/80 cursor-pointer">
                  <p className="font-semibold text-slate-800">Emergency Patient Admitted</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">ICU Bed #103 assigned to UHID-2026-0812</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">2 mins ago</span>
                </div>
                <div className="px-4 py-3 hover:bg-slate-50/80 cursor-pointer">
                  <p className="font-semibold text-slate-800">Lab Alert: Critical Potassium</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">Patient John Doe (K: 6.2 mmol/L)</p>
                  <span className="text-[10px] text-slate-400 mt-1 block">15 mins ago</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* User Profile Menu */}
        <div className="relative">
          <button
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="flex items-center gap-2.5 p-1.5 hover:bg-slate-100 rounded-xl transition"
          >
            <div className="w-8 h-8 rounded-full bg-teal-700 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              {user ? `${user.first_name[0]}${user.last_name[0]}` : "SA"}
            </div>
            <div className="hidden sm:block text-left">
              <p className="text-xs font-semibold text-slate-800 leading-tight">
                {user ? `${user.first_name} ${user.last_name}` : "Administrator"}
              </p>
              <p className="text-[10px] text-teal-600 font-medium uppercase tracking-wider">
                {user?.roles?.[0]?.name || "Super Admin"}
              </p>
            </div>
          </button>

          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-200 py-2 z-50 animate-in fade-in">
              <div className="px-4 py-2 border-b border-slate-100">
                <p className="text-xs font-bold text-slate-800">{user?.first_name} {user?.last_name}</p>
                <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
              </div>
              <div className="py-1 text-xs">
                <button
                  onClick={() => router.push("/settings")}
                  className="w-full px-4 py-2 text-left text-slate-700 hover:bg-slate-50 flex items-center gap-2.5"
                >
                  <Settings className="w-4 h-4 text-slate-400" />
                  Account Settings
                </button>
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-2 text-left text-rose-600 hover:bg-rose-50 flex items-center gap-2.5 font-medium"
                >
                  <LogOut className="w-4 h-4 text-rose-500" />
                  Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
