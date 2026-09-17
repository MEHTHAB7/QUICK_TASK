import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { motion } from 'framer-motion';
import { LogIn, LogOut, CheckCircle } from 'lucide-react';

const AttendanceLog = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const response = await api.get('/attendance/');
      setLogs(response.data);
    } catch (error) {
      console.error('Failed to fetch attendance', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckIn = async () => {
    setActionLoading(true);
    try {
      await api.post('/attendance/check-in');
      await fetchLogs();
    } catch (error) {
      console.error(error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCheckOut = async () => {
    setActionLoading(true);
    try {
      await api.post('/attendance/check-out');
      await fetchLogs();
    } catch (error) {
      console.error(error);
    } finally {
      setActionLoading(false);
    }
  };

  const todayLog = logs.find(log => new Date(log.date).toDateString() === new Date().toDateString());

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Attendance</h1>
        <p className="text-muted">Track your daily check-ins and check-outs</p>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel p-8"
      >
        <h2 className="text-xl font-semibold text-white mb-6">Today's Action</h2>
        <div className="flex gap-4">
          <button 
            onClick={handleCheckIn}
            disabled={todayLog || actionLoading}
            className={`flex-1 flex items-center justify-center gap-2 py-4 rounded-xl font-medium transition-all ${
              todayLog 
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700' 
                : 'bg-green-500/20 text-green-400 hover:bg-green-500/30 border border-green-500/30'
            }`}
          >
            {todayLog ? <CheckCircle className="w-5 h-5" /> : <LogIn className="w-5 h-5" />}
            {todayLog ? 'Checked In' : 'Check In Now'}
          </button>
          
          <button 
            onClick={handleCheckOut}
            disabled={!todayLog || todayLog.check_out || actionLoading}
            className={`flex-1 flex items-center justify-center gap-2 py-4 rounded-xl font-medium transition-all ${
              !todayLog || todayLog.check_out
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700' 
                : 'bg-red-500/20 text-red-400 hover:bg-red-500/30 border border-red-500/30'
            }`}
          >
            <LogOut className="w-5 h-5" />
            {todayLog?.check_out ? 'Checked Out' : 'Check Out Now'}
          </button>
        </div>
      </motion.div>

      <div className="glass-panel overflow-hidden">
        <div className="p-6 border-b border-white/5 bg-white/[0.02]">
          <h2 className="text-xl font-semibold text-white">Recent Logs</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/5 text-slate-400 text-sm">
                <th className="p-4 font-medium">Date</th>
                <th className="p-4 font-medium">Status</th>
                <th className="p-4 font-medium">Check In</th>
                <th className="p-4 font-medium">Check Out</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="4" className="p-4 text-center text-slate-400">Loading...</td></tr>
              ) : logs.map((log) => (
                <tr key={log.id} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                  <td className="p-4 text-white">{new Date(log.date).toLocaleDateString()}</td>
                  <td className="p-4">
                    <span className="bg-primary/20 text-primary px-3 py-1 rounded-full text-xs font-medium">
                      {log.status}
                    </span>
                  </td>
                  <td className="p-4 text-slate-300">{log.check_in ? new Date(log.check_in).toLocaleTimeString() : '-'}</td>
                  <td className="p-4 text-slate-300">{log.check_out ? new Date(log.check_out).toLocaleTimeString() : '-'}</td>
                </tr>
              ))}
              {!loading && logs.length === 0 && (
                <tr><td colSpan="4" className="p-8 text-center text-slate-500">No attendance records found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AttendanceLog;
