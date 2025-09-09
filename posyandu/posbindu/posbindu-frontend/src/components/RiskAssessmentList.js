import React, { useState, useEffect } from 'react';
import './RiskAssessmentList.css';

function RiskAssessmentList() {
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    jenis_penilaian: '',
    kategori_risiko: '',
    visit_id: ''
  });

  useEffect(() => {
    fetchAssessments();
  }, [filters]);

  const fetchAssessments = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.jenis_penilaian) queryParams.append('jenis_penilaian', filters.jenis_penilaian);
      if (filters.kategori_risiko) queryParams.append('kategori_risiko', filters.kategori_risiko);
      if (filters.visit_id) queryParams.append('visit_id', filters.visit_id);
      
      const response = await fetch(`http://localhost:8080/api/risk-assessment/assessment/?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch assessments');
      
      const data = await response.json();
      setAssessments(data.results || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const getRiskColor = (kategoriRisiko) => {
    switch (kategoriRisiko) {
      case 'Rendah': return 'low';
      case 'Sedang': return 'medium';
      case 'Tinggi': return 'high';
      default: return 'unknown';
    }
  };

  const getScoreColor = (skor) => {
    if (skor >= 8) return 'high';
    if (skor >= 5) return 'medium';
    return 'low';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) return <div className="loading">Loading assessments...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="risk-assessment-list">
      <div className="risk-assessment-header">
        <h2>Data Penilaian Risiko POS BINDU PTM</h2>
        <div className="risk-assessment-actions">
          <button className="btn btn-primary">Tambah Penilaian</button>
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
            value={filters.jenis_penilaian} 
            onChange={(e) => handleFilterChange('jenis_penilaian', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Jenis</option>
            <option value="Framingham">Framingham</option>
            <option value="WHO">WHO</option>
            <option value="Lokakarya">Lokakarya</option>
            <option value="Lainnya">Lainnya</option>
          </select>
          
          <select 
            value={filters.kategori_risiko} 
            onChange={(e) => handleFilterChange('kategori_risiko', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Kategori</option>
            <option value="Rendah">Rendah</option>
            <option value="Sedang">Sedang</option>
            <option value="Tinggi">Tinggi</option>
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

      <div className="assessments-grid">
        {assessments.map((assessment) => {
          const riskColor = getRiskColor(assessment.kategori_risiko);
          const scoreColor = getScoreColor(assessment.skor_total);
          
          return (
            <div key={assessment.id} className="assessment-card">
              <div className="assessment-card-header">
                <h3>{assessment.jenis_penilaian}</h3>
                <div className="assessment-badges">
                  <span className={`risk-badge ${riskColor}`}>
                    {assessment.kategori_risiko}
                  </span>
                  <span className={`score-badge ${scoreColor}`}>
                    Skor: {assessment.skor_total}
                  </span>
                </div>
              </div>
              
              <div className="assessment-card-body">
                <div className="assessment-info">
                  <p><strong>Kunjungan:</strong> #{assessment.visit}</p>
                  <p><strong>Tanggal:</strong> {formatDate(assessment.created_at)}</p>
                  <p><strong>Skor Total:</strong> {assessment.skor_total}</p>
                  <p><strong>Kategori Risiko:</strong> {assessment.kategori_risiko}</p>
                </div>
                
                <div className="assessment-recommendations">
                  <h4>Rekomendasi:</h4>
                  <p>{assessment.rekomendasi}</p>
                </div>
                
                {assessment.tindak_lanjut && (
                  <div className="assessment-followup">
                    <h4>Tindak Lanjut:</h4>
                    <p>{assessment.tindak_lanjut}</p>
                  </div>
                )}
                
                {assessment.catatan && (
                  <div className="assessment-notes">
                    <h4>Catatan:</h4>
                    <p>{assessment.catatan}</p>
                  </div>
                )}
                
                <div className="assessment-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Edit</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {assessments.length === 0 && (
        <div className="no-data">
          <p>Tidak ada data penilaian risiko</p>
        </div>
      )}
    </div>
  );
}

export default RiskAssessmentList;
