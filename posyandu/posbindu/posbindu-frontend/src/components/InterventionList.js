import React, { useState, useEffect } from 'react';
import './InterventionList.css';

function InterventionList() {
  const [interventions, setInterventions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    jenis_intervensi: '',
    status: '',
    visit_id: ''
  });

  useEffect(() => {
    fetchInterventions();
  }, [filters]);

  const fetchInterventions = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.jenis_intervensi) queryParams.append('jenis_intervensi', filters.jenis_intervensi);
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.visit_id) queryParams.append('visit_id', filters.visit_id);
      
      const response = await fetch(`http://localhost:8080/api/intervention/intervention/?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch interventions');
      
      const data = await response.json();
      setInterventions(data.results || data);
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
      case 'Aktif': return 'active';
      case 'Selesai': return 'completed';
      case 'Dibatalkan': return 'cancelled';
      default: return 'draft';
    }
  };

  const getInterventionTypeColor = (jenis) => {
    switch (jenis) {
      case 'Edukasi': return 'education';
      case 'Konseling': return 'counseling';
      case 'Terapi': return 'therapy';
      case 'Monitoring': return 'monitoring';
      default: return 'other';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatDuration = (durasi) => {
    if (!durasi) return 'Tidak ditentukan';
    return `${durasi} minggu`;
  };

  if (loading) return <div className="loading">Loading interventions...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="intervention-list">
      <div className="intervention-header">
        <h2>Data Intervensi POS BINDU PTM</h2>
        <div className="intervention-actions">
          <button className="btn btn-primary">Tambah Intervensi</button>
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
          
          <select 
            value={filters.jenis_intervensi} 
            onChange={(e) => handleFilterChange('jenis_intervensi', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Jenis</option>
            <option value="Edukasi">Edukasi</option>
            <option value="Konseling">Konseling</option>
            <option value="Terapi">Terapi</option>
            <option value="Monitoring">Monitoring</option>
            <option value="Lainnya">Lainnya</option>
          </select>
          
          <select 
            value={filters.status} 
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Status</option>
            <option value="Draft">Draft</option>
            <option value="Aktif">Aktif</option>
            <option value="Selesai">Selesai</option>
            <option value="Dibatalkan">Dibatalkan</option>
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

      <div className="interventions-grid">
        {interventions.map((intervention) => {
          const statusColor = getStatusColor(intervention.status);
          const typeColor = getInterventionTypeColor(intervention.jenis_intervensi);
          
          return (
            <div key={intervention.id} className="intervention-card">
              <div className="intervention-card-header">
                <h3>{intervention.jenis_intervensi}</h3>
                <div className="intervention-badges">
                  <span className={`status-badge ${statusColor}`}>
                    {intervention.status}
                  </span>
                  <span className={`type-badge ${typeColor}`}>
                    {intervention.jenis_intervensi}
                  </span>
                </div>
              </div>
              
              <div className="intervention-card-body">
                <div className="intervention-info">
                  <p><strong>Kunjungan:</strong> #{intervention.visit}</p>
                  <p><strong>Tanggal:</strong> {formatDate(intervention.created_at)}</p>
                  <p><strong>Durasi:</strong> {formatDuration(intervention.durasi)}</p>
                  <p><strong>Frekuensi:</strong> {intervention.frekuensi || 'Tidak ditentukan'}</p>
                </div>
                
                <div className="intervention-description">
                  <h4>Deskripsi:</h4>
                  <p>{intervention.deskripsi}</p>
                </div>
                
                {intervention.target && (
                  <div className="intervention-target">
                    <h4>Target:</h4>
                    <p>{intervention.target}</p>
                  </div>
                )}
                
                {intervention.metode && (
                  <div className="intervention-method">
                    <h4>Metode:</h4>
                    <p>{intervention.metode}</p>
                  </div>
                )}
                
                {intervention.hasil && (
                  <div className="intervention-result">
                    <h4>Hasil:</h4>
                    <p>{intervention.hasil}</p>
                  </div>
                )}
                
                {intervention.evaluasi && (
                  <div className="intervention-evaluation">
                    <h4>Evaluasi:</h4>
                    <p>{intervention.evaluasi}</p>
                  </div>
                )}
                
                {intervention.tindak_lanjut && (
                  <div className="intervention-followup">
                    <h4>Tindak Lanjut:</h4>
                    <p>{intervention.tindak_lanjut}</p>
                  </div>
                )}
                
                <div className="intervention-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Edit</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {interventions.length === 0 && (
        <div className="no-data">
          <p>Tidak ada data intervensi</p>
        </div>
      )}
    </div>
  );
}

export default InterventionList;
