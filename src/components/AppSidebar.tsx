
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useAuth } from "@/contexts/AuthContext";
import { BarChart3, Package, TrendingUp, AlertTriangle, LogOut, User } from "lucide-react";

interface AppSidebarProps {
  currentView: string;
  onViewChange: (view: 'dashboard' | 'products' | 'forecasts' | 'alerts') => void;
}

const menuItems = [
  {
    title: "Dashboard",
    view: "dashboard" as const,
    icon: BarChart3,
  },
  {
    title: "Products",
    view: "products" as const,
    icon: Package,
  },
  {
    title: "Forecasts",
    view: "forecasts" as const,
    icon: TrendingUp,
  },
  {
    title: "Alerts",
    view: "alerts" as const,
    icon: AlertTriangle,
  },
];

export function AppSidebar({ currentView, onViewChange }: AppSidebarProps) {
  const { user, logout } = useAuth();

  return (
    <Sidebar>
      <SidebarHeader className="p-4">
        <div className="flex items-center space-x-2">
          <Package className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-lg font-bold">Stock Manager</h1>
            <p className="text-sm text-muted-foreground">AI-Powered Inventory</p>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton 
                    isActive={currentView === item.view}
                    onClick={() => onViewChange(item.view)}
                  >
                    <item.icon className="h-4 w-4" />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter className="p-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="w-full">
              <User className="h-4 w-4" />
              <span className="text-sm">{user?.email}</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={logout} className="w-full text-red-600 hover:text-red-700">
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
