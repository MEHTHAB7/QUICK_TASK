import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import TaskBoard from './pages/TaskBoard';
import AttendanceLog from './pages/AttendanceLog';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import TeamChat from './pages/TeamChat';
import ProtectedLayout from './layouts/ProtectedLayout';

function App() {
  return (
    <AuthProvider>
      <Router basename={import.meta.env.BASE_URL}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route element={<ProtectedLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/tasks" element={<TaskBoard />} />
            <Route path="/attendance" element={<AttendanceLog />} />
            <Route path="/analytics" element={<AnalyticsDashboard />} />
            <Route path="/chat" element={<TeamChat />} />
          </Route>
          
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
