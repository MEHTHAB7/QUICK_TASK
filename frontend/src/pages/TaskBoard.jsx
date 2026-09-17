import React, { useState, useEffect, useContext } from 'react';
import api from '../services/api';
import { motion } from 'framer-motion';
import { Plus, Clock, AlertCircle, Trash2 } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const TaskBoard = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useContext(AuthContext);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '', priority: 'Medium', assigned_to_id: '', due_date: '' });
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchTasks();
    if (user?.role === 'admin' || user?.role === 'manager') {
      fetchUsers();
    }
  }, [user]);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users/');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users', error);
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await api.get('/tasks/');
      setTasks(response.data);
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...newTask };
      if (!payload.assigned_to_id) delete payload.assigned_to_id;
      if (!payload.due_date) delete payload.due_date;
      else payload.due_date = new Date(payload.due_date).toISOString();

      await api.post('/tasks/', payload);
      setNewTask({ title: '', description: '', priority: 'Medium', assigned_to_id: '', due_date: '' });
      setIsModalOpen(false);
      fetchTasks();
    } catch (error) {
      console.error('Failed to create task', error);
    }
  };

  const handleUpdateStatus = async (taskId, newStatus) => {
    try {
      await api.put(`/tasks/${taskId}`, { status: newStatus });
      fetchTasks();
    } catch (error) {
      console.error('Failed to update task status', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await api.delete(`/tasks/${taskId}`);
      fetchTasks();
    } catch (error) {
      console.error('Failed to delete task', error);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High': return 'text-red-400 bg-red-400/10 border-red-400/20';
      case 'Medium': return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
      case 'Low': return 'text-green-400 bg-green-400/10 border-green-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  const columns = ['Pending', 'In Progress', 'Completed'];

  if (loading) return <div className="text-white">Loading tasks...</div>;

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Task Board</h1>
          <p className="text-muted">Manage your tasks and projects</p>
        </div>
        {(user?.role === 'admin' || user?.role === 'manager') && (
          <button onClick={() => setIsModalOpen(true)} className="btn-primary flex items-center gap-2">
            <Plus className="w-5 h-5" />
            New Task
          </button>
        )}
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
        {columns.map(status => (
          <div key={status} className="flex flex-col h-full bg-surface/30 rounded-2xl border border-white/5 p-4 overflow-hidden">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${status === 'Completed' ? 'bg-green-500' : status === 'In Progress' ? 'bg-primary' : 'bg-slate-400'}`}></div>
              {status}
              <span className="ml-auto text-sm text-slate-500 bg-slate-800/50 px-2 py-0.5 rounded-full">
                {tasks.filter(t => t.status === status).length}
              </span>
            </h3>
            
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
              {tasks.filter(t => t.status === status).map((task, idx) => (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  key={task.id}
                  className="glass-panel p-4 cursor-pointer hover:border-white/20 transition-all group"
                >
                  <div className="flex justify-between items-start mb-3">
                    <span className={`text-xs px-2 py-1 rounded-md border ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                    {user?.role === 'admin' && (
                      <button 
                        onClick={(e) => { e.stopPropagation(); handleDeleteTask(task.id); }}
                        className="text-slate-500 hover:text-red-400 transition-colors"
                        title="Delete Task"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                  <h4 className="text-white font-medium mb-2 group-hover:text-primary transition-colors">{task.title}</h4>
                  <p className="text-sm text-slate-400 mb-4 line-clamp-2">{task.description}</p>
                  
                  <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {task.due_date ? new Date(task.due_date).toLocaleDateString() : 'No due date'}
                    </div>
                    {task.assignee && (
                      <div className="flex items-center gap-1 bg-white/5 px-2 py-1 rounded">
                        <span className="w-4 h-4 rounded-full bg-primary/20 flex items-center justify-center text-primary text-[10px]">
                          {task.assignee.full_name ? task.assignee.full_name.charAt(0).toUpperCase() : task.assignee.email.charAt(0).toUpperCase()}
                        </span>
                        <span>{task.assignee.full_name || task.assignee.email.split('@')[0]}</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="mt-3 pt-3 border-t border-white/5 flex justify-between items-center">
                    <span className="text-xs text-slate-400">Status</span>
                    <select
                      value={task.status}
                      onClick={(e) => e.stopPropagation()}
                      onChange={(e) => handleUpdateStatus(task.id, e.target.value)}
                      className="bg-slate-800 border border-white/10 rounded px-2 py-1 text-xs text-white outline-none focus:border-primary"
                    >
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Completed">Completed</option>
                    </select>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="glass-panel p-6 w-full max-w-md rounded-2xl border border-white/10">
            <h2 className="text-xl font-bold text-white mb-4">Create New Task</h2>
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Title</label>
                <input
                  type="text"
                  required
                  value={newTask.title}
                  onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Description</label>
                <textarea
                  value={newTask.description}
                  onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-primary h-24 resize-none"
                ></textarea>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1">Priority</label>
                <select
                  value={newTask.priority}
                  onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-primary"
                >
                  <option value="Low" className="bg-slate-800">Low</option>
                  <option value="Medium" className="bg-slate-800">Medium</option>
                  <option value="High" className="bg-slate-800">High</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1">Assign To</label>
                  <select
                    value={newTask.assigned_to_id}
                    onChange={(e) => setNewTask({ ...newTask, assigned_to_id: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-primary"
                  >
                    <option value="" className="bg-slate-800">Unassigned</option>
                    {users.map(u => (
                      <option key={u.id} value={u.id} className="bg-slate-800">{u.full_name || u.email}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1">Due Date</label>
                  <input
                    type="date"
                    value={newTask.due_date}
                    onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white outline-none focus:border-primary"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create Task
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskBoard;
