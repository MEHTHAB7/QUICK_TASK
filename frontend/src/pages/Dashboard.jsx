import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-muted">Welcome back, {user?.full_name || user?.email}</p>
        </div>
        <button onClick={logout} className="btn-secondary">
          Logout
        </button>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel p-6"
      >
        <h2 className="text-xl font-semibold text-white mb-4">Your Profile</h2>
        <div className="space-y-2 text-slate-300">
          <p><span className="font-medium text-slate-400">Email:</span> {user?.email}</p>
          <p><span className="font-medium text-slate-400">Role:</span> <span className="capitalize">{user?.role}</span></p>
          <p><span className="font-medium text-slate-400">Status:</span> {user?.is_active ? 'Active' : 'Inactive'}</p>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
