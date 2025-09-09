import React, { useState, useEffect } from 'react';
import './ReferralList.css';

function ReferralList() {
  const [referrals, setReferrals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    fasilitas_tujuan: '',
    status: '',
    prioritas: '',
    visit_id: ''
  });

  useEffect(() => {
    fetchReferrals();
  }, [filters]);

  const fetchReferrals = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.fasilitas_tujuan) queryParams.append('fasilitas_tujuan', filters.fasilitas_tujuan);
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.prioritas) queryParams.append('prioritas', filters.prioritas);
      if (filters.visit_id) queryParams.append('visit_id', filters.visit_id);
      
      const response = await fetch(`http://localhost:8080/api/referral/referral/?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch referrals');
      
      const data = await response.json();
      setReferrals(data.results || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Draft': return 'draft';
      case 'Pending': return 'pending';
      case 'Diterima': return 'accepted';
      case 'Selesai': return 'completed';
      case 'Ditolak': return 'rejected';
      default: return 'draft';
    }
  };

  const getPriorityColor = (prioritas) => {
    switch (prioritas) {
      case 'Rendah': return 'low';
      case 'Sedang': return 'medium';
      case 'Tinggi': return 'high';
      case 'Darurat': return 'emergency';
      default: return 'low';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getDaysSinceReferral = (tanggalRujukan) => {
    const today = new Date();
    const referralDate = new Date(tanggalRujukan);
    const diffTime = today - referralDate;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  if (loading) return <div className="loading">Loading referrals...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="referral-list">
      <div className="referral-header">
        <h2>Data Rujukan POS BINDU PTM</h2>
        <div className="referral-actions">
          <button className="btn btn-primary">Tambah Rujukan</button>
        </div>
      </div>

      <div className="filters-section">
        <div className="filters">
          <input
            type="text"
            placeholder="Cari peserta..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          <input
            type="text"
            placeholder="Fasilitas Tujuan"
            value={filters.fasilitas_tujuan}
            onChange={(e) => handleFilterChange('fasilitas_tujuan', e.target.value)}
            className="filter-input"
          />
          
          <select 
            value={filters.status} 
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Status</option>
            <option value="Draft">Draft</option>
            <option value="Pending">Pending</option>
            <option value="Diterima">Diterima</option>
            <option value="Selesai">Selesai</option>
            <option value="Ditolak">Ditolak</option>
          </select>
          
          <select 
            value={filters.prioritas} 
            onChange={(e) => handleFilterChange('prioritas', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Prioritas</option>
            <option value="Rendah">Rendah</option>
            <option value="Sedang">Sedang</option>
            <option value="Tinggi">Tinggi</option>
            <option value="Darurat">Darurat</option>
          </select>
          
          <input
            type="text"
            placeholder="ID Kunjungan"
            value={filters.visit_id}
            onChange={(e) => handleFilterChange('visit_id', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      <div className="referrals-grid">
        {referrals.map((referral) => {
          const statusColor = getStatusColor(referral.status);
          const priorityColor = getPriorityColor(referral.prioritas);
          const daysSince = getDaysSinceReferral(referral.tanggal_rujukan);
          
          return (
            <div key={referral.id} className="referral-card">
              <div className="referral-card-header">
                <h3>Rujukan #{referral.id}</h3>
                <div className="referral-badges">
                  <span className={`status-badge ${statusColor}`}>
                    {referral.status}
                  </span>
                  <span className={`priority-badge ${priorityColor}`}>
                    {referral.prioritas}
                  </span>
                </div>
              </div>
              
              <div className="referral-card-body">
                <div className="referral-info">
                  <p><strong>Kunjungan:</strong> #{referral.visit}</p>
                  <p><strong>Fasilitas Tujuan:</strong> {referral.fasilitas_tujuan}</p>
                  <p><strong>Tanggal Rujukan:</strong> {formatDate(referral.tanggal_rujukan)}</p>
                  <p><strong>Prioritas:</strong> {referral.prioritas}</p>
                  <p><strong>Status:</strong> {referral.status}</p>
                  {daysSince > 0 && (
                    <p><strong>Hari sejak rujukan:</strong> {daysSince} hari</p>
                  )}
                </div>
                
                <div className="referral-reason">
                  <h4>Alasan Rujukan:</h4>
                  <p>{referral.alasan_rujukan}</p>
                </div>
                
                {referral.tanggal_tindak_lanjut && (
                  <div className="referral-followup">
                    <h4>Tanggal Tindak Lanjut:</h4>
                    <p>{formatDate(referral.tanggal_tindak_lanjut)}</p>
                  </div>
                )}
                
                {referral.hasil_rujukan && (
                  <div className="referral-result">
                    <h4>Hasil Rujukan:</h4>
                    <p>{referral.hasil_rujukan}</p>
                  </div>
                )}
                
                {referral.catatan && (
                  <div className="referral-notes">
                    <h4>Catatan:</h4>
                    <p>{referral.catatan}</p>
                  </div>
                )}
                
                <div className="referral-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Edit</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {referrals.length === 0 && (
        <div className="no-data">
          <p>Tidak ada data rujukan</p>
        </div>
      )}
    </div>
  );
}

export default ReferralList;
