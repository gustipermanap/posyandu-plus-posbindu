import React, { useState, useEffect } from 'react';
import './LabList.css';

function LabList() {
  const [labResults, setLabResults] = useState([]);
  const [stock, setStock] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('results');
  const [filters, setFilters] = useState({
    search: '',
    jenis_pemeriksaan: '',
    status: '',
    visit_id: ''
  });

  useEffect(() => {
    fetchData();
  }, [activeTab, filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.jenis_pemeriksaan) queryParams.append('jenis_pemeriksaan', filters.jenis_pemeriksaan);
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.visit_id) queryParams.append('visit_id', filters.visit_id);
      
      let response;
      if (activeTab === 'results') {
        response = await fetch(`http://localhost:8080/api/lab/result/?${queryParams}`);
      } else {
        response = await fetch(`http://localhost:8080/api/lab/stock/?${queryParams}`);
      }
      
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      if (activeTab === 'results') {
        setLabResults(data.results || data);
      } else {
        setStock(data.results || data);
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

  const getResultStatus = (hasil, nilaiNormal) => {
    if (!hasil || !nilaiNormal) return { status: 'Tidak Diketahui', color: 'unknown' };
    
    const resultValue = parseFloat(hasil);
    const normalRange = nilaiNormal.split('-').map(v => parseFloat(v.trim()));
    
    if (normalRange.length === 2) {
      if (resultValue >= normalRange[0] && resultValue <= normalRange[1]) {
        return { status: 'Normal', color: 'normal' };
      } else if (resultValue < normalRange[0]) {
        return { status: 'Rendah', color: 'low' };
      } else {
        return { status: 'Tinggi', color: 'high' };
      }
    }
    
    return { status: 'Tidak Diketahui', color: 'unknown' };
  };

  const getStockStatus = (stokTersisa, stokAwal) => {
    const percentage = (stokTersisa / stokAwal) * 100;
    if (percentage <= 10) return { status: 'Kritis', color: 'critical' };
    if (percentage <= 30) return { status: 'Rendah', color: 'low' };
    if (percentage <= 70) return { status: 'Sedang', color: 'medium' };
    return { status: 'Aman', color: 'safe' };
  };

  const isExpiringSoon = (tanggalKadaluarsa) => {
    const today = new Date();
    const expiryDate = new Date(tanggalKadaluarsa);
    const diffTime = expiryDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays <= 30 && diffDays >= 0;
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
    <div className="lab-list">
      <div className="lab-header">
        <h2>Data Laboratorium POS BINDU PTM</h2>
        <div className="lab-actions">
          <button className="btn btn-primary">Tambah Hasil Lab</button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'results' ? 'active' : ''}`}
          onClick={() => setActiveTab('results')}
        >
          Hasil Lab
        </button>
        <button 
          className={`tab ${activeTab === 'stock' ? 'active' : ''}`}
          onClick={() => setActiveTab('stock')}
        >
          Stok Alat & Bahan
        </button>
      </div>

      <div className="filters-section">
        <div className="filters">
          <input
            type="text"
            placeholder="Cari..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          {activeTab === 'results' ? (
            <>
              <select 
                value={filters.jenis_pemeriksaan} 
                onChange={(e) => handleFilterChange('jenis_pemeriksaan', e.target.value)}
                className="filter-select"
              >
                <option value="">Semua Jenis</option>
                <option value="Gula Darah">Gula Darah</option>
                <option value="Kolesterol">Kolesterol</option>
                <option value="Fungsi Ginjal">Fungsi Ginjal</option>
                <option value="Fungsi Hati">Fungsi Hati</option>
                <option value="Lainnya">Lainnya</option>
              </select>
              
              <select 
                value={filters.status} 
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="filter-select"
              >
                <option value="">Semua Status</option>
                <option value="Normal">Normal</option>
                <option value="Abnormal">Abnormal</option>
                <option value="Perlu Tindak Lanjut">Perlu Tindak Lanjut</option>
              </select>
            </>
          ) : (
            <select 
              value={filters.jenis_pemeriksaan} 
              onChange={(e) => handleFilterChange('jenis_pemeriksaan', e.target.value)}
              className="filter-select"
            >
              <option value="">Semua Jenis</option>
              <option value="Alat">Alat</option>
              <option value="Bahan">Bahan</option>
              <option value="Reagen">Reagen</option>
            </select>
          )}
          
          <input
            type="text"
            placeholder="ID Kunjungan"
            value={filters.visit_id}
            onChange={(e) => handleFilterChange('visit_id', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      {activeTab === 'results' ? (
        <div className="lab-results-grid">
          {labResults.map((result) => {
            const resultStatus = getResultStatus(result.hasil, result.nilai_normal);
            
            return (
              <div key={result.id} className="lab-result-card">
                <div className="lab-result-card-header">
                  <h3>{result.jenis_pemeriksaan}</h3>
                  <span className={`result-status ${resultStatus.color}`}>
                    {resultStatus.status}
                  </span>
                </div>
                
                <div className="lab-result-card-body">
                  <div className="lab-result-info">
                    <p><strong>Hasil:</strong> {result.hasil}</p>
                    <p><strong>Nilai Normal:</strong> {result.nilai_normal}</p>
                    <p><strong>Status:</strong> {result.status}</p>
                    <p><strong>Tanggal Pemeriksaan:</strong> {formatDate(result.tanggal_pemeriksaan)}</p>
                    {result.catatan && (
                      <p><strong>Catatan:</strong> {result.catatan}</p>
                    )}
                  </div>
                  
                  <div className="lab-result-actions">
                    <button className="btn btn-outline">Lihat Detail</button>
                    <button className="btn btn-primary">Edit</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="stock-grid">
          {stock.map((item) => {
            const stockStatus = getStockStatus(item.stok_tersisa, item.stok_awal);
            const expiringSoon = isExpiringSoon(item.tanggal_kadaluarsa);
            
            return (
              <div key={item.id} className={`stock-card ${expiringSoon ? 'expiring' : ''}`}>
                <div className="stock-card-header">
                  <h3>{item.nama_item}</h3>
                  <div className="stock-badges">
                    <span className={`stock-status ${stockStatus.color}`}>
                      {stockStatus.status}
                    </span>
                    {expiringSoon && (
                      <span className="expiring-badge">
                        Akan Kadaluarsa
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="stock-card-body">
                  <div className="stock-info">
                    <p><strong>Jenis:</strong> {item.jenis_item}</p>
                    <p><strong>Stok Awal:</strong> {item.stok_awal} {item.satuan}</p>
                    <p><strong>Stok Tersisa:</strong> {item.stok_tersisa} {item.satuan}</p>
                    <p><strong>Tanggal Kadaluarsa:</strong> {formatDate(item.tanggal_kadaluarsa)}</p>
                    <p><strong>Supplier:</strong> {item.supplier}</p>
                  </div>
                  
                  <div className="stock-progress">
                    <div className="progress-bar">
                      <div 
                        className={`progress-fill ${stockStatus.color}`}
                        style={{ width: `${(item.stok_tersisa / item.stok_awal) * 100}%` }}
                      ></div>
                    </div>
                    <span className="progress-text">
                      {Math.round((item.stok_tersisa / item.stok_awal) * 100)}%
                    </span>
                  </div>
                  
                  <div className="stock-actions">
                    <button className="btn btn-outline">Lihat Detail</button>
                    <button className="btn btn-primary">Update Stok</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {(activeTab === 'results' ? labResults : stock).length === 0 && (
        <div className="no-data">
          <p>Tidak ada data {activeTab === 'results' ? 'hasil lab' : 'stok'}</p>
        </div>
      )}
    </div>
  );
}

export default LabList;
