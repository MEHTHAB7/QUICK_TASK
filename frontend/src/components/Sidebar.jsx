import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, CheckSquare, Clock, LogOut, Brain, MessageSquare } from 'lucide-react';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const Sidebar = () => {
  const { logout, user } = useContext(AuthContext);

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, roles: ['admin', 'manager', 'employee'] },
    { name: 'Analytics (AI)', path: '/analytics', icon: Brain, roles: ['admin', 'manager'] },
    { name: 'Tasks', path: '/tasks', icon: CheckSquare, roles: ['admin', 'manager', 'employee'] },
    { name: 'Attendance', path: '/attendance', icon: Clock, roles: ['admin', 'manager', 'employee'] },
    { name: 'Team Chat', path: '/chat', icon: MessageSquare, roles: ['admin', 'manager', 'employee'] },
  ];

  const filteredNavItems = navItems.filter(item => !item.roles || item.roles.includes(user?.role || 'employee'));

  return (
    <div className="w-64 glass-panel border-r border-white/5 flex flex-col m-4 rounded-3xl overflow-hidden h-[calc(100vh-2rem)]">
      <div className="p-6 border-b border-white/5">
        <h1 className="text-xl font-bold text-white flex items-center gap-2">
          <span className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-sm">AI</span>
          Productivity
        </h1>
      </div>
      
      <nav className="flex-1 p-4 space-y-2">
        {filteredNavItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive
                  ? 'bg-primary/20 text-primary font-medium'
                  : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-white/5">
        <button
          onClick={logout}
          className="flex items-center gap-3 px-4 py-3 w-full rounded-xl text-slate-400 hover:bg-red-500/10 hover:text-red-400 transition-all duration-200"
        >
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
