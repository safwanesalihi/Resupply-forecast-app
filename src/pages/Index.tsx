
import { useState } from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { Dashboard } from "@/components/Dashboard";
import { ProductManager } from "@/components/ProductManager";
import { ForecastView } from "@/components/ForecastView";
import { AlertCenter } from "@/components/AlertCenter";
import { LoginForm } from "@/components/auth/LoginForm";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";

type ViewType = 'dashboard' | 'products' | 'forecasts' | 'alerts';

function AppContent() {
  const [currentView, setCurrentView] = useState<ViewType>('dashboard');
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <LoginForm />
      </div>
    );
  }

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'products':
        return <ProductManager />;
      case 'forecasts':
        return <ForecastView />;
      case 'alerts':
        return <AlertCenter />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gray-50">
        <AppSidebar currentView={currentView} onViewChange={setCurrentView} />
        <main className="flex-1 overflow-auto">
          <div className="p-6">
            {renderView()}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}

const Index = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default Index;
