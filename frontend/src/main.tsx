import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import './index.css';
import { AuthProvider } from './contexts/AuthContext'; // Import AuthProvider
import { Toaster } from '@/components/ui/sonner'; // Assuming you use sonner for toasts

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router>
      <AuthProvider> {/* Wrap App with AuthProvider */}
        <App />
        <Toaster /> {/* Add Toaster for notifications */}
      </AuthProvider>
    </Router>
  </React.StrictMode>
);

