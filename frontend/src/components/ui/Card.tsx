import React from "react";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className, hoverable, ...props }) => {
  return (
    <div
      className={cn(
        "bg-white rounded-xl border border-slate-200/80 shadow-sm p-5",
        hoverable && "transition hover:shadow-md hover:border-slate-300",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, className, ...props }) => (
  <div className={cn("flex items-center justify-between pb-4 mb-4 border-b border-slate-100", className)} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ children, className, ...props }) => (
  <h3 className={cn("text-base font-semibold text-slate-800", className)} {...props}>
    {children}
  </h3>
);
