import React, { useState } from 'react';
import axios from 'axios';
import './LoginPage.css';

function LoginPage({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log("DEBUG: Attempting login with username:", formData.username);
      const response = await axios.post('/api/token/', {
        username: formData.username,
        password: formData.password,
      });
      console.log("DEBUG: Login response received:", { 
        hasAccess: !!response.data.access, 
        hasRefresh: !!response.data.refresh,
        status: response.status 
      });
      // Panggil onLogin dengan access dan refresh token yang diterima
      onLogin(response.data.access, response.data.refresh);
    } catch (err) {
      console.error("DEBUG: Login error details:", err);
      console.error("DEBUG: Error response:", err.response?.data);
      console.error("DEBUG: Error status:", err.response?.status);
      setError('Login gagal. Periksa username dan password Anda.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>POS BINDU PTM</h1>
          <p>Pos Binaan Terpadu Penyakit Tidak Menular</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Masukkan username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Masukkan password"
            />
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="login-button"
            disabled={loading}
          >
            {loading ? 'Memproses...' : 'Login'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Sistem POS BINDU PTM</p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
