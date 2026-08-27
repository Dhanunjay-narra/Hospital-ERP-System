"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAVIGATION_CONFIG } from "@/lib/constants";
import { cn } from "@/lib/utils";
import * as Icons from "lucide-react";

export const Sidebar: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const pathname = usePathname();
  const [collapsedSuites, setCollapsedSuites] = useState<Record<string, boolean>>({});

  const toggleSuite = (suite: string) => {
    setCollapsedSuites((prev) => ({ ...prev, [suite]: !prev[suite] }));
  };

  const renderIcon = (iconName: string) => {
    const IconComponent = (Icons as any)[iconName] || Icons.Circle;
    return <IconComponent className="w-4 h-4 flex-shrink-0" />;
  };

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          "fixed top-0 bottom-0 left-0 z-40 w-72 bg-slate-900 text-slate-200 flex flex-col border-r border-slate-800 transition-transform duration-300 lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-6 bg-slate-950/80 border-b border-slate-800">
          <Link href="/dashboard" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-900/30">
              <Icons.Activity className="w-5 h-5" />
            </div>
            <div>
              <span className="font-bold text-base text-white tracking-tight leading-none block">
                ApexCare
              </span>
              <span className="text-[10px] uppercase font-semibold tracking-wider text-teal-400">
                Hospital ERP + CRM
              </span>
            </div>
          </Link>
          <button
            onClick={onClose}
            className="lg:hidden p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
          >
            <Icons.X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation List */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-6">
          {NAVIGATION_CONFIG.map((group) => {
            const isCollapsed = collapsedSuites[group.suite];
            return (
              <div key={group.suite} className="space-y-1">
                <button
                  onClick={() => toggleSuite(group.suite)}
                  className="w-full flex items-center justify-between px-2 py-1 text-[11px] font-bold uppercase tracking-wider text-slate-400 hover:text-slate-200 transition"
                >
                  <span>{group.suite}</span>
                  <Icons.ChevronDown
                    className={cn(
                      "w-3.5 h-3.5 transition-transform",
                      isCollapsed && "-rotate-90"
                    )}
                  />
                </button>

                {!isCollapsed && (
                  <div className="space-y-0.5 mt-1">
                    {group.items.map((item) => {
                      const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
                      return (
                        <Link
                          key={item.href}
                          href={item.href}
                          onClick={() => {
                            if (window.innerWidth < 1024) onClose();
                          }}
                          className={cn(
                            "flex items-center justify-between px-3 py-2 text-xs font-medium rounded-lg transition-all group",
                            isActive
                              ? "bg-teal-700 text-white font-semibold shadow-sm"
                              : "text-slate-300 hover:bg-slate-800/80 hover:text-white"
                          )}
                        >
                          <div className="flex items-center gap-3">
                            <span className={cn(isActive ? "text-teal-200" : "text-slate-400 group-hover:text-slate-200")}>
                              {renderIcon(item.icon)}
                            </span>
                            <span>{item.title}</span>
                          </div>
                          {item.badge && (
                            <span className="px-1.5 py-0.5 text-[10px] font-bold bg-teal-500/20 text-teal-300 rounded">
                              {item.badge}
                            </span>
                          )}
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer info */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-[11px] font-medium text-slate-300">Apex Main Branch</span>
          </div>
          <span className="text-[10px] text-slate-500 font-mono">v1.0.0</span>
        </div>
      </aside>
    </>
  );
};
