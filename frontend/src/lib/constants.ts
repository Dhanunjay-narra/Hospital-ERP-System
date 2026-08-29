export interface NavItem {
  title: string;
  href: string;
  icon: string;
  badge?: string;
  roles?: string[];
}

export interface NavGroup {
  suite: string;
  items: NavItem[];
}

export const NAVIGATION_CONFIG: NavGroup[] = [
  {
    suite: "Executive & Core",
    items: [
      { title: "Dashboard", href: "/dashboard", icon: "LayoutDashboard" },
      { title: "Organization", href: "/organization", icon: "Building2" },
      { title: "Users & RBAC", href: "/users", icon: "Users2" },
      { title: "Multi-Branch Enterprise", href: "/enterprise", icon: "Network" },
    ],
  },
  {
    suite: "Patient Operations",
    items: [
      { title: "Patients Registry", href: "/patients", icon: "UserCheck" },
      { title: "Doctors & Schedules", href: "/doctors", icon: "Stethoscope" },
      { title: "Appointments Queue", href: "/appointments", icon: "CalendarDays" },
      { title: "OPD Consultations", href: "/opd", icon: "ClipboardList" },
      { title: "IPD Bed Allocation", href: "/ipd", icon: "BedDouble" },
      { title: "EMR & Rx Clinical", href: "/clinical", icon: "FileHeart" },
      { title: "Nursing Station", href: "/nursing", icon: "HeartPulse" },
    ],
  },
  {
    suite: "Diagnostics & Acute Care",
    items: [
      { title: "Emergency & Trauma", href: "/emergency", icon: "ShieldAlert" },
      { title: "Operation Theatre", href: "/ot", icon: "Activity" },
      { title: "Pharmacy & Formulary", href: "/pharmacy", icon: "Pill" },
      { title: "Laboratory & Tests", href: "/laboratory", icon: "FlaskConical" },
      { title: "Radiology & Imaging", href: "/radiology", icon: "ScanLine" },
      { title: "Blood Bank", href: "/blood-bank", icon: "Droplets" },
    ],
  },
  {
    suite: "Finance & Supply Chain",
    items: [
      { title: "Billing & Cashier", href: "/billing", icon: "Receipt" },
      { title: "Insurance & Claims", href: "/insurance", icon: "ShieldCheck" },
      { title: "Inventory & Stores", href: "/inventory", icon: "Boxes" },
      { title: "Procurement & POs", href: "/procurement", icon: "ShoppingCart" },
    ],
  },
  {
    suite: "Staff, HR & Compliance",
    items: [
      { title: "Staff & HR", href: "/hr", icon: "UserCog" },
      { title: "Duty Roster", href: "/roster", icon: "CalendarClock" },
      { title: "Medical Records (MRD)", href: "/medical-records", icon: "Archive" },
      { title: "Document & Consents", href: "/documents", icon: "FolderArchive" },
      { title: "HIPAA Security & Audit", href: "/compliance", icon: "Lock" },
    ],
  },
  {
    suite: "Patient CRM & Telehealth",
    items: [
      { title: "Patient CRM Leads", href: "/crm", icon: "Contact" },
      { title: "Omnichannel Comms", href: "/communication", icon: "MessageSquare" },
      { title: "Marketing Campaigns", href: "/marketing", icon: "Megaphone" },
      { title: "Feedback & NPS", href: "/feedback", icon: "Star" },
      { title: "Virtual Telemedicine", href: "/telemedicine", icon: "Video" },
    ],
  },
  {
    suite: "Intelligence & Analytics",
    items: [
      { title: "Decision Support (CDSS)", href: "/cdss", icon: "BrainCircuit" },
      { title: "Executive BI Analytics", href: "/analytics", icon: "BarChart3" },
      { title: "Reporting Engine", href: "/reports", icon: "FileSpreadsheet" },
    ],
  },
];
