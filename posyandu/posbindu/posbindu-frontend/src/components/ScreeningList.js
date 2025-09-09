import React, { useState, useEffect } from 'react';
import './ScreeningList.css';

function ScreeningList() {
  const [visits, setVisits] = useState([]);
  const [anamnesis, setAnamnesis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('visits');
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    participant_id: ''
  });

  useEffect(() => {
    fetchData();
  }, [activeTab, filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.participant_id) queryParams.append('participant_id', filters.participant_id);
      
      let response;
      if (activeTab === 'visits') {
        response = await fetch(`http://localhost:8080/api/screening/visit/?${queryParams}`);
      } else {
        response = await fetch(`http://localhost:8080/api/screening/anamnesis/?${queryParams}`);
      }
      
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      if (activeTab === 'visits') {
        setVisits(data.results || data);
      } else {
        setAnamnesis(data.results || data);
      }
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
      case 'Verified': return 'verified';
      case 'Completed': return 'completed';
      default: return 'draft';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) return <div className="loading">Loading data...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="screening-list">
      <div className="screening-header">
        <h2>Data Skrining POS BINDU PTM</h2>
        <div className="screening-actions">
          <button className="btn btn-primary">Tambah Kunjungan</button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'visits' ? 'active' : ''}`}
          onClick={() => setActiveTab('visits')}
        >
          Kunjungan
        </button>
        <button 
          className={`tab ${activeTab === 'anamnesis' ? 'active' : ''}`}
          onClick={() => setActiveTab('anamnesis')}
        >
          Anamnesis
        </button>
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
          
          <select 
            value={filters.status} 
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Status</option>
            <option value="Draft">Draft</option>
            <option value="Verified">Verified</option>
            <option value="Completed">Completed</option>
          </select>
          
          <input
            type="text"
            placeholder="ID Peserta"
            value={filters.participant_id}
            onChange={(e) => handleFilterChange('participant_id', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      {activeTab === 'visits' ? (
        <div className="visits-grid">
          {visits.map((visit) => (
            <div key={visit.id} className="visit-card">
              <div className="visit-card-header">
                <h3>Kunjungan #{visit.id}</h3>
                <span className={`status-badge ${getStatusColor(visit.status)}`}>
                  {visit.status}
                </span>
              </div>
              
              <div className="visit-card-body">
                <div className="visit-info">
                  <p><strong>Tanggal:</strong> {formatDate(visit.pos_date)}</p>
                  <p><strong>Lokasi:</strong> {visit.lokasi}</p>
                  <p><strong>Petugas ID:</strong> {visit.petugas_id}</p>
                  {visit.verified_by && (
                    <p><strong>Diverifikasi oleh:</strong> {visit.verified_by}</p>
                  )}
                </div>
                
                <div className="visit-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Edit</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="anamnesis-grid">
          {anamnesis.map((anamnesisItem) => (
            <div key={anamnesisItem.id} className="anamnesis-card">
              <div className="anamnesis-card-header">
                <h3>Anamnesis #{anamnesisItem.id}</h3>
                <span className="visit-badge">
                  Kunjungan #{anamnesisItem.visit}
                </span>
              </div>
              
              <div className="anamnesis-card-body">
                <div className="anamnesis-info">
                  <p><strong>Keluhan Utama:</strong> {anamnesisItem.keluhan_utama}</p>
                  {anamnesisItem.keluhan_tambahan && (
                    <p><strong>Keluhan Tambahan:</strong> {anamnesisItem.keluhan_tambahan}</p>
                  )}
                  {anamnesisItem.riwayat_penyakit && (
                    <p><strong>Riwayat Penyakit:</strong> {anamnesisItem.riwayat_penyakit}</p>
                  )}
                  {anamnesisItem.riwayat_keluarga && (
                    <p><strong>Riwayat Keluarga:</strong> {anamnesisItem.riwayat_keluarga}</p>
                  )}
                </div>
                
                <div className="anamnesis-lifestyle">
                  <h4>Gaya Hidup:</h4>
                  <div className="lifestyle-factors">
                    {anamnesisItem.pola_makan && (
                      <span className="lifestyle-factor">Pola Makan: {anamnesisItem.pola_makan}</span>
                    )}
                    {anamnesisItem.pola_olahraga && (
                      <span className="lifestyle-factor">Olahraga: {anamnesisItem.pola_olahraga}</span>
                    )}
                    {anamnesisItem.konsumsi_rokok && (
                      <span className="lifestyle-factor">Rokok: {anamnesisItem.konsumsi_rokok}</span>
                    )}
                    {anamnesisItem.konsumsi_alkohol && (
                      <span className="lifestyle-factor">Alkohol: {anamnesisItem.konsumsi_alkohol}</span>
                    )}
                  </div>
                </div>
                
                <div className="anamnesis-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Edit</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {(activeTab === 'visits' ? visits : anamnesis).length === 0 && (
        <div className="no-data">
          <p>Tidak ada data {activeTab === 'visits' ? 'kunjungan' : 'anamnesis'}</p>
        </div>
      )}
    </div>
  );
}

export default ScreeningList;
