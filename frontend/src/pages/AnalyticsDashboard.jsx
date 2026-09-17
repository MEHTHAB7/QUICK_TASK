import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import { Users, CheckSquare, Brain, Activity, TrendingUp, Download } from 'lucide-react';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predictionData, setPredictionData] = useState({
    tasks_completed: 10,
    hours_worked: 40,
    lines_of_code: 500,
    bugs_fixed: 2,
    meetings_attended: 4
  });
  const [predictedScore, setPredictedScore] = useState(null);
  const { user } = React.useContext(AuthContext);

  useEffect(() => {
    if (user?.role !== 'employee') {
      fetchStats();
    }
  }, [user]);

  const fetchStats = async () => {
    try {
      const response = await api.get('/analytics/dashboard-stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    try {
      const response = await api.post('/analytics/predict-productivity', predictionData);
      setPredictedScore(response.data.productivity_score);
    } catch (error) {
      console.error('Prediction failed', error);
    }
  };

  const handleDownloadReport = async () => {
    try {
      // In a real app, you would use api.get('/reports/productivity-report', { responseType: 'blob' })
      // For simplicity, we just open it directly if auth is not strictly required for GET on report, or handle via blob.
      const response = await api.get('/reports/productivity-report', { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'productivity_report.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Download failed', error);
    }
  };

  if (user?.role === 'employee') {
    return <div className="text-red-400 text-xl font-bold p-8">Access Denied: You do not have permission to view analytics.</div>;
  }

  if (loading || !stats) {
    return <div className="text-white">Loading Analytics...</div>;
  }

  const statCards = [
    { title: 'Total Employees', value: stats.total_employees, icon: Users, color: 'text-blue-400' },
    { title: 'Active Tasks', value: stats.active_tasks, icon: Activity, color: 'text-indigo-400' },
    { title: 'Completed Tasks', value: stats.completed_tasks, icon: CheckSquare, color: 'text-green-400' },
    { title: 'Avg Productivity', value: `${stats.avg_productivity_score}%`, icon: TrendingUp, color: 'text-purple-400' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
            <Brain className="w-8 h-8 text-primary" />
            AI Analytics Engine
          </h1>
          <p className="text-muted">Intelligent insights and predictive productivity modeling</p>
        </div>
        <button 
          onClick={handleDownloadReport}
          className="btn-primary flex items-center gap-2 px-6 py-3"
        >
          <Download className="w-5 h-5" />
          Download PDF Report
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, idx) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="glass-panel p-6"
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-xl bg-white/5 ${card.color}`}>
                <card.icon className="w-6 h-6" />
              </div>
            </div>
            <h3 className="text-slate-400 text-sm font-medium mb-1">{card.title}</h3>
            <p className="text-3xl font-bold text-white">{card.value}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-panel p-6 lg:col-span-2"
        >
          <h2 className="text-xl font-semibold text-white mb-6">Weekly Productivity Trend</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats.weekly_trends}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" domain={[0, 100]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#fff' }}
                  itemStyle={{ color: '#3b82f6' }}
                />
                <Area type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorScore)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-6"
        >
          <h2 className="text-xl font-semibold text-white mb-6">AI Productivity Predictor</h2>
          <p className="text-sm text-slate-400 mb-6">
            Input expected employee metrics to predict their productivity score using our trained Random Forest model.
          </p>
          
          <div className="space-y-4 mb-6">
            {Object.entries(predictionData).map(([key, value]) => (
              <div key={key}>
                <label className="block text-xs font-medium text-slate-400 mb-1 capitalize">
                  {key.replace(/_/g, ' ')}
                </label>
                <input
                  type="number"
                  className="input-field py-1.5 text-sm"
                  value={value}
                  onChange={(e) => setPredictionData({...predictionData, [key]: Number(e.target.value)})}
                />
              </div>
            ))}
          </div>
          
          <button onClick={handlePredict} className="w-full btn-primary py-2 mb-4">
            Run AI Prediction
          </button>

          {predictedScore !== null && (
            <div className="p-4 rounded-xl bg-primary/10 border border-primary/20 text-center">
              <p className="text-sm text-primary mb-1">Predicted Score</p>
              <p className="text-3xl font-bold text-white">{predictedScore}<span className="text-lg text-slate-400">/100</span></p>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
