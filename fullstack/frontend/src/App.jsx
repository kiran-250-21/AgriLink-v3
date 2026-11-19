import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import MobileBottomNav from './components/MobileBottomNav';
import ProtectedRoute from './components/ProtectedRoute';

// Auth Pages
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';

// Farmer Pages
import FarmerDashboard from './pages/farmer/FarmerDashboard';
import MarketIntelligence from './pages/farmer/MarketIntelligence';
import HarvestsList from './pages/farmer/HarvestsList';
import CreateHarvest from './pages/farmer/CreateHarvest';
import FarmerOrders from './pages/farmer/FarmerOrders';
import FarmerDeliveries from './pages/farmer/FarmerDeliveries';

// Buyer Pages
import BuyerDashboard from './pages/buyer/BuyerDashboard';
import AvailableHarvests from './pages/buyer/AvailableHarvests';
import SaleRequests from './pages/buyer/SaleRequests';
import BuyerRequirementsList from './pages/buyer/BuyerRequirementsList';
import CreateRequirement from './pages/buyer/CreateRequirement';
import BuyerOrders from './pages/buyer/BuyerOrders';

// Driver Pages
import DriverDashboard from './pages/driver/DriverDashboard';
import AvailableJobs from './pages/driver/AvailableJobs';
import ActiveDeliveries from './pages/driver/ActiveDeliveries';
import VehicleSetup from './pages/driver/VehicleSetup';

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard';
import UserManagement from './pages/admin/UserManagement';
import MarketManagement from './pages/admin/MarketManagement';
import OrderManagement from './pages/admin/OrderManagement';
import Analytics from './pages/admin/Analytics';
import AuditLogs from './pages/admin/AuditLogs';

// Layout wrapper for authenticated workspaces with responsive mobile drawer & bottom navigation
function MainLayout({ children }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <Navbar
        onToggleMobileMenu={() => setMobileMenuOpen((prev) => !prev)}
        isMobileMenuOpen={mobileMenuOpen}
      />
      <div className="flex flex-1 relative overflow-x-hidden">
        {/* Desktop Sidebar (hidden on mobile, visible on lg and up) */}
        <div className="hidden lg:block w-64 shrink-0">
          <Sidebar />
        </div>

        {/* Mobile / Tablet Drawer Sidebar (slide-out overlay) */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 z-50 lg:hidden flex">
            {/* Dark Backdrop */}
            <div
              className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity"
              onClick={() => setMobileMenuOpen(false)}
            />
            {/* Slide-out Drawer */}
            <div className="relative w-72 max-w-[85vw] h-full bg-slate-900 border-r border-slate-800 shadow-2xl flex flex-col z-10 animate-in slide-in-from-left duration-200">
              <Sidebar onCloseMobile={() => setMobileMenuOpen(false)} isMobile={true} />
            </div>
          </div>
        )}

        {/* Main Content Area */}
        <main className="flex-1 p-3.5 sm:p-5 md:p-6 lg:p-8 max-w-7xl mx-auto w-full pb-24 lg:pb-8 overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Mobile Bottom Navigation Bar (1-thumb fast switching for phones) */}
      <MobileBottomNav />
    </div>
  );
}

// Smart Root Redirect based on user role
function RootRedirect() {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;

  const routes = {
    FARMER: '/farmer/dashboard',
    BUYER: '/buyer/dashboard',
    DRIVER: '/driver/dashboard',
    ADMIN: '/admin/dashboard',
  };
  return <Navigate to={routes[user.role] || '/login'} replace />;
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Farmer Workspace */}
          <Route
            path="/farmer/*"
            element={
              <ProtectedRoute allowedRoles={['FARMER']}>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<FarmerDashboard />} />
                    <Route path="intelligence" element={<MarketIntelligence />} />
                    <Route path="harvests" element={<HarvestsList />} />
                    <Route path="harvests/new" element={<CreateHarvest />} />
                    <Route path="orders" element={<FarmerOrders />} />
                    <Route path="deliveries" element={<FarmerDeliveries />} />
                    <Route path="*" element={<Navigate to="dashboard" replace />} />
                  </Routes>
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Buyer Workspace */}
          <Route
            path="/buyer/*"
            element={
              <ProtectedRoute allowedRoles={['BUYER']}>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<BuyerDashboard />} />
                    <Route path="marketplace" element={<AvailableHarvests />} />
                    <Route path="requests" element={<SaleRequests />} />
                    <Route path="requirements" element={<BuyerRequirementsList />} />
                    <Route path="requirements/new" element={<CreateRequirement />} />
                    <Route path="orders" element={<BuyerOrders />} />
                    <Route path="*" element={<Navigate to="dashboard" replace />} />
                  </Routes>
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Driver Workspace */}
          <Route
            path="/driver/*"
            element={
              <ProtectedRoute allowedRoles={['DRIVER']}>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<DriverDashboard />} />
                    <Route path="jobs" element={<AvailableJobs />} />
                    <Route path="deliveries" element={<ActiveDeliveries />} />
                    <Route path="vehicle" element={<VehicleSetup />} />
                    <Route path="*" element={<Navigate to="dashboard" replace />} />
                  </Routes>
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Admin Workspace */}
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute allowedRoles={['ADMIN']}>
                <MainLayout>
                  <Routes>
                    <Route path="dashboard" element={<AdminDashboard />} />
                    <Route path="users" element={<UserManagement />} />
                    <Route path="markets" element={<MarketManagement />} />
                    <Route path="orders" element={<OrderManagement />} />
                    <Route path="analytics" element={<Analytics />} />
                    <Route path="audit-logs" element={<AuditLogs />} />
                    <Route path="*" element={<Navigate to="dashboard" replace />} />
                  </Routes>
                </MainLayout>
              </ProtectedRoute>
            }
          />

          {/* Default Catch-all */}
          <Route path="*" element={<RootRedirect />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
