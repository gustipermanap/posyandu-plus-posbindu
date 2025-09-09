import React, { useState, useEffect } from 'react';
import api from '../api';

function ProfilePage({ loggedInUser, onProfileUpdate, isChangePasswordPage = false }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    profile_picture: null
  });
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (loggedInUser) {
      setFormData({
        username: loggedInUser.username || '',
        email: loggedInUser.email || '',
        first_name: loggedInUser.first_name || '',
        last_name: loggedInUser.last_name || '',
        profile_picture: loggedInUser.profile_picture || null
      });
    }
  }, [loggedInUser]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (isChangePasswordPage) {
      setPasswordData({
        ...passwordData,
        [name]: value
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleFileChange = (e) => {
    setFormData({
      ...formData,
      profile_picture: e.target.files[0]
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      if (isChangePasswordPage) {
        if (passwordData.new_password !== passwordData.confirm_password) {
          setError('Password baru dan konfirmasi password tidak cocok');
          return;
        }

        const formDataToSend = new FormData();
        formDataToSend.append('old_password', passwordData.old_password);
        formDataToSend.append('new_password', passwordData.new_password);

        await api.post('/auth/change-password/', formDataToSend);
        setMessage('Password berhasil diubah');
        setPasswordData({
          old_password: '',
          new_password: '',
          confirm_password: ''
        });
      } else {
        const formDataToSend = new FormData();
        formDataToSend.append('username', formData.username);
        formDataToSend.append('email', formData.email);
        formDataToSend.append('first_name', formData.first_name);
        formDataToSend.append('last_name', formData.last_name);
        
        if (formData.profile_picture) {
          formDataToSend.append('profile_picture', formData.profile_picture);
        }

        await api.put('/auth/user-info/', formDataToSend);
        setMessage('Profil berhasil diperbarui');
        
        // Refresh user data
        if (onProfileUpdate) {
          onProfileUpdate();
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Terjadi kesalahan saat memperbarui profil');
      console.error('Profile update error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (isChangePasswordPage) {
    return (
      <div className="profile-container">
        <h2>Ganti Password</h2>
        <form onSubmit={handleSubmit} className="profile-form">
          {error && <div className="error-message">{error}</div>}
          {message && <div className="success-message">{message}</div>}
          
          <div className="form-group">
            <label htmlFor="old_password">Password Lama:</label>
            <input
              type="password"
              id="old_password"
              name="old_password"
              value={passwordData.old_password}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="new_password">Password Baru:</label>
            <input
              type="password"
              id="new_password"
              name="new_password"
              value={passwordData.new_password}
              onChange={handleInputChange}
              required
              minLength="8"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="confirm_password">Konfirmasi Password Baru:</label>
            <input
              type="password"
              id="confirm_password"
              name="confirm_password"
              value={passwordData.confirm_password}
              onChange={handleInputChange}
              required
              minLength="8"
            />
          </div>
          
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Memproses...' : 'Ganti Password'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <h2>Profil Pengguna</h2>
      <form onSubmit={handleSubmit} className="profile-form">
        {error && <div className="error-message">{error}</div>}
        {message && <div className="success-message">{message}</div>}
        
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleInputChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="first_name">Nama Depan:</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleInputChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="last_name">Nama Belakang:</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleInputChange}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="profile_picture">Foto Profil:</label>
          <input
            type="file"
            id="profile_picture"
            name="profile_picture"
            accept="image/*"
            onChange={handleFileChange}
          />
          {formData.profile_picture && (
            <div className="current-image">
              <p>File terpilih: {formData.profile_picture.name}</p>
            </div>
          )}
        </div>
        
        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Memproses...' : 'Perbarui Profil'}
        </button>
      </form>
    </div>
  );
}

export default ProfilePage;
