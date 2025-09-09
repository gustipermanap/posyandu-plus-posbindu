import React, { useState, useEffect } from 'react';
import './ParticipantList.css';

function ParticipantList() {
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    jenis_kelamin: '',
    status_merokok: '',
    riwayat_dm: ''
  });

  useEffect(() => {
    fetchParticipants();
  }, [filters]);

  const fetchParticipants = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.jenis_kelamin) queryParams.append('jenis_kelamin', filters.jenis_kelamin);
      if (filters.status_merokok) queryParams.append('status_merokok', filters.status_merokok);
      if (filters.riwayat_dm) queryParams.append('riwayat_dm', filters.riwayat_dm);
      
      const response = await fetch(`http://localhost:8080/api/participant/participant/?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch participants');
      
      const data = await response.json();
      setParticipants(data.results || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const getRiskLevel = (participant) => {
    let riskScore = 0;
    if (participant.status_merokok === 'Aktif') riskScore += 2;
    if (participant.status_alkohol === 'Ya') riskScore += 1;
    if (participant.riwayat_dm) riskScore += 3;
    if (participant.riwayat_hipertensi) riskScore += 3;
    if (participant.riwayat_stroke) riskScore += 4;
    if (participant.riwayat_jantung) riskScore += 4;
    if (participant.riwayat_keluarga_ptm) riskScore += 2;
    
    if (riskScore >= 6) return { level: 'Tinggi', color: 'high' };
    if (riskScore >= 3) return { level: 'Sedang', color: 'medium' };
    return { level: 'Rendah', color: 'low' };
  };

  const calculateAge = (birthDate) => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  if (loading) return <div className="loading">Loading participants...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="participant-list">
      <div className="participant-header">
        <h2>Daftar Peserta POS BINDU PTM</h2>
        <div className="participant-actions">
          <button className="btn btn-primary">Tambah Peserta</button>
        </div>
      </div>

      <div className="filters-section">
        <div className="filters">
          <input
            type="text"
            placeholder="Cari nama atau NIK..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          <select 
            value={filters.jenis_kelamin} 
            onChange={(e) => handleFilterChange('jenis_kelamin', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Jenis Kelamin</option>
            <option value="Laki-laki">Laki-laki</option>
            <option value="Perempuan">Perempuan</option>
          </select>
          
          <select 
            value={filters.status_merokok} 
            onChange={(e) => handleFilterChange('status_merokok', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Status Merokok</option>
            <option value="Tidak">Tidak</option>
            <option value="Aktif">Aktif</option>
            <option value="Eks">Eks</option>
          </select>
          
          <select 
            value={filters.riwayat_dm} 
            onChange={(e) => handleFilterChange('riwayat_dm', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Riwayat DM</option>
            <option value="true">Ada Riwayat DM</option>
            <option value="false">Tidak Ada Riwayat DM</option>
          </select>
        </div>
      </div>

      <div className="participant-grid">
        {participants.map((participant) => {
          const riskLevel = getRiskLevel(participant);
          const age = calculateAge(participant.tanggal_lahir);
          
          return (
            <div key={participant.id} className="participant-card">
              <div className="participant-card-header">
                <h3>{participant.nama_lengkap}</h3>
                <div className="participant-badges">
                  <span className={`risk-badge ${riskLevel.color}`}>
                    Risiko {riskLevel.level}
                  </span>
                  <span className="age-badge">
                    {age} tahun
                  </span>
                </div>
              </div>
              
              <div className="participant-card-body">
                <div className="participant-info">
                  <p><strong>NIK:</strong> {participant.nik}</p>
                  <p><strong>Jenis Kelamin:</strong> {participant.jenis_kelamin}</p>
                  <p><strong>Alamat:</strong> {participant.alamat}</p>
                  <p><strong>RT/RW:</strong> {participant.rt}/{participant.rw}</p>
                  <p><strong>No. HP:</strong> {participant.no_hp || 'Tidak ada'}</p>
                  <p><strong>BPJS:</strong> {participant.bpjs ? 'Ya' : 'Tidak'}</p>
                </div>
                
                <div className="participant-health">
                  <h4>Faktor Risiko:</h4>
                  <div className="risk-factors">
                    {participant.status_merokok !== 'Tidak' && (
                      <span className="risk-factor smoking">
                        Merokok: {participant.status_merokok}
                      </span>
                    )}
                    {participant.status_alkohol === 'Ya' && (
                      <span className="risk-factor alcohol">
                        Konsumsi Alkohol
                      </span>
                    )}
                    {participant.riwayat_dm && (
                      <span className="risk-factor diabetes">
                        Riwayat DM
                      </span>
                    )}
                    {participant.riwayat_hipertensi && (
                      <span className="risk-factor hypertension">
                        Riwayat Hipertensi
                      </span>
                    )}
                    {participant.riwayat_stroke && (
                      <span className="risk-factor stroke">
                        Riwayat Stroke
                      </span>
                    )}
                    {participant.riwayat_jantung && (
                      <span className="risk-factor heart">
                        Riwayat Jantung
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="participant-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Skrining</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {participants.length === 0 && (
        <div className="no-data">
          <p>Tidak ada data peserta</p>
        </div>
      )}
    </div>
  );
}

export default ParticipantList;
