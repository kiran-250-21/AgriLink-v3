import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  TrendingUp,
  PackageCheck,
  ShoppingBag,
  Truck,
  Store,
  PlusCircle,
  Users,
  ShieldAlert,
} from 'lucide-react';

export default function MobileBottomNav() {
  const { user } = useAuth();
  if (!user) return null;

  const roleBottomMenus = {
    FARMER: [
      { path: '/farmer/dashboard', label: 'Home', icon: LayoutDashboard },
      { path: '/farmer/intelligence', label: 'Intel', icon: TrendingUp, highlight: true },
      { path: '/farmer/harvests/new', label: 'Add', icon: PlusCircle },
      { path: '/farmer/harvests', label: 'Harvests', icon: PackageCheck },
      { path: '/farmer/orders', label: 'Orders', icon: ShoppingBag },
    ],
    BUYER: [
      { path: '/buyer/dashboard', label: 'Home', icon: LayoutDashboard },
      { path: '/buyer/marketplace', label: 'Market', icon: Store },
      { path: '/buyer/requests', label: 'Requests', icon: TrendingUp, highlight: true },
      { path: '/buyer/requirements/new', label: 'Post', icon: PlusCircle },
      { path: '/buyer/orders', label: 'Orders', icon: ShoppingBag },
    ],
    DRIVER: [
      { path: '/driver/dashboard', label: 'Home', icon: LayoutDashboard },
      { path: '/driver/jobs', label: 'Jobs', icon: Truck, highlight: true },
      { path: '/driver/deliveries', label: 'Transit', icon: PackageCheck },
      { path: '/driver/vehicle', label: 'Vehicle', icon: LayoutDashboard },
    ],
    ADMIN: [
      { path: '/admin/dashboard', label: 'Control', icon: LayoutDashboard },
      { path: '/admin/users', label: 'Users', icon: Users },
      { path: '/admin/markets', label: 'Markets', icon: Store },
      { path: '/admin/orders', label: 'Orders', icon: ShoppingBag },
      { path: '/admin/audit-logs', label: 'Audit', icon: ShieldAlert },
    ],
  };

  const navItems = roleBottomMenus[user.role] || [];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 lg:hidden bg-slate-950/95 backdrop-blur-md border-t border-slate-800 px-2 py-1.5 shadow-2xl safe-area-bottom">
      <div className="flex items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center py-1 px-2 rounded-xl text-[10px] font-semibold transition-all ${
                  isActive
                    ? item.highlight
                      ? 'text-amber-400 font-bold'
                      : 'text-emerald-400 font-bold'
                    : 'text-slate-400 hover:text-slate-200'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <div
                    className={`p-1 rounded-lg transition-all ${
                      isActive
                        ? item.highlight
                          ? 'bg-amber-500/20 text-amber-400'
                          : 'bg-emerald-500/20 text-emerald-400'
                        : 'text-slate-400'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="mt-0.5 tracking-tight">{item.label}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
}
