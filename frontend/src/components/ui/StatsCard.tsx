import React from "react";
import { cn } from "@/lib/utils";

export interface StatsCardProps {
  title: string;
  value: string | number;
  change?: string;
  isPositive?: boolean;
  icon: React.ReactNode;
  iconBgColor?: string;
  className?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  change,
  isPositive = true,
  icon,
  iconBgColor = "bg-teal-50 text-teal-700",
  className,
}) => {
  return (
    <div className={cn("bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm hover:shadow transition", className)}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-500">{title}</p>
          <p className="text-2xl font-bold text-slate-800 mt-1">{value}</p>
        </div>
        <div className={cn("p-3 rounded-xl", iconBgColor)}>
          {icon}
        </div>
      </div>
      {change && (
        <div className="mt-3 flex items-center gap-1.5 text-xs">
          <span className={cn("font-medium", isPositive ? "text-emerald-600" : "text-rose-600")}>
            {isPositive ? "+" : ""}{change}
          </span>
          <span className="text-slate-400">vs last period</span>
        </div>
      )}
    </div>
  );
};
