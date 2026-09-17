import React, { useState, useEffect, useRef, useContext } from 'react';
import { Send, MessageSquare } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import { motion } from 'framer-motion';

const TeamChat = () => {
  const { user } = useContext(AuthContext);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/api/v1/ws/chat';
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      console.log('Connected to chat');
    };

    ws.current.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setMessages((prev) => [...prev, message]);
      } catch (e) {
        // Fallback for raw text
        setMessages((prev) => [...prev, { text: event.data, sender: 'System', timestamp: new Date().toISOString() }]);
      }
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim() && ws.current) {
      const msgData = {
        text: inputValue,
        sender: user?.email || 'Unknown User',
        timestamp: new Date().toISOString()
      };
      ws.current.send(JSON.stringify(msgData));
      setInputValue('');
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
          <MessageSquare className="w-8 h-8 text-primary" />
          Team Chat
        </h1>
        <p className="text-muted">Real-time communication with your team</p>
      </div>

      <div className="flex-1 glass-panel flex flex-col overflow-hidden relative">
        <div className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-slate-500">
              <MessageSquare className="w-12 h-12 mb-4 opacity-50" />
              <p>No messages yet. Start the conversation!</p>
            </div>
          )}
          {messages.map((msg, idx) => {
            const isMe = msg.sender === user?.email;
            return (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={idx} 
                className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}
              >
                {!isMe && <span className="text-xs text-slate-400 mb-1 ml-1">{msg.sender.split('@')[0]}</span>}
                <div 
                  className={`px-4 py-2 rounded-2xl max-w-[75%] shadow-lg ${
                    isMe 
                      ? 'bg-primary text-white rounded-br-sm' 
                      : 'bg-slate-800 text-slate-200 border border-white/10 rounded-bl-sm'
                  }`}
                >
                  <p className="text-sm">{msg.text}</p>
                </div>
                <span className="text-[10px] text-slate-500 mt-1">
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </motion.div>
            );
          })}
          <div ref={messagesEndRef} />
        </div>

        <div className="p-4 bg-slate-900/50 border-t border-white/5 backdrop-blur-md">
          <form onSubmit={sendMessage} className="flex gap-3">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 transition-colors"
            />
            <button 
              type="submit" 
              disabled={!inputValue.trim()}
              className="btn-primary p-3 rounded-xl disabled:opacity-50 flex items-center justify-center"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TeamChat;
