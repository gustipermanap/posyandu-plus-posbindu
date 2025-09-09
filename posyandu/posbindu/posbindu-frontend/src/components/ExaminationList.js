import React, { useState, useEffect } from 'react';
import './ExaminationList.css';

function ExaminationList() {
  const [vitalSigns, setVitalSigns] = useState([]);
  const [anthropometry, setAnthropometry] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('vital-signs');
  const [filters, setFilters] = useState({
    search: '',
    visit_id: '',
    sistol_min: '',
    sistol_max: ''
  });

  useEffect(() => {
    fetchData();
  }, [activeTab, filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.visit_id) queryParams.append('visit_id', filters.visit_id);
      if (filters.sistol_min) queryParams.append('sistol_min', filters.sistol_min);
      if (filters.sistol_max) queryParams.append('sistol_max', filters.sistol_max);
      
      let response;
      if (activeTab === 'vital-signs') {
        response = await fetch(`http://localhost:8080/api/examination/vital-sign/?${queryParams}`);
      } else {
        response = await fetch(`http://localhost:8080/api/examination/anthropometry/?${queryParams}`);
      }
      
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      if (activeTab === 'vital-signs') {
        setVitalSigns(data.results || data);
      } else {
        setAnthropometry(data.results || data);
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

  const getBloodPressureStatus = (sistol, diastol) => {
    if (sistol >= 180 || diastol >= 110) return { status: 'Krisis Hipertensi', color: 'critical' };
    if (sistol >= 140 || diastol >= 90) return { status: 'Hipertensi', color: 'high' };
    if (sistol >= 120 || diastol >= 80) return { status: 'Prehipertensi', color: 'medium' };
    return { status: 'Normal', color: 'normal' };
  };

  const getBMICategory = (bmi) => {
    if (bmi < 18.5) return { category: 'Kurus', color: 'underweight' };
    if (bmi < 25) return { category: 'Normal', color: 'normal' };
    if (bmi < 30) return { category: 'Gemuk', color: 'overweight' };
    return { category: 'Obesitas', color: 'obese' };
  };

  const calculateBMI = (berat, tinggi) => {
    const heightInMeters = tinggi / 100;
    return (berat / (heightInMeters * heightInMeters)).toFixed(1);
  };

  if (loading) return <div className="loading">Loading data...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="examination-list">
      <div className="examination-header">
        <h2>Data Pemeriksaan Fisik POS BINDU PTM</h2>
        <div className="examination-actions">
          <button className="btn btn-primary">Tambah Pemeriksaan</button>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'vital-signs' ? 'active' : ''}`}
          onClick={() => setActiveTab('vital-signs')}
        >
          Tanda Vital
        </button>
        <button 
          className={`tab ${activeTab === 'anthropometry' ? 'active' : ''}`}
          onClick={() => setActiveTab('anthropometry')}
        >
          Antropometri
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
          
          <input
            type="text"
            placeholder="ID Kunjungan"
            value={filters.visit_id}
            onChange={(e) => handleFilterChange('visit_id', e.target.value)}
            className="filter-input"
          />
          
          <input
            type="number"
            placeholder="Sistol Min"
            value={filters.sistol_min}
            onChange={(e) => handleFilterChange('sistol_min', e.target.value)}
            className="filter-input"
          />
          
          <input
            type="number"
            placeholder="Sistol Max"
            value={filters.sistol_max}
            onChange={(e) => handleFilterChange('sistol_max', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      {activeTab === 'vital-signs' ? (
        <div className="vital-signs-grid">
          {vitalSigns.map((vital) => {
            const bpStatus = getBloodPressureStatus(vital.sistol, vital.diastol);
            
            return (
              <div key={vital.id} className="vital-signs-card">
                <div className="vital-signs-card-header">
                  <h3>Tanda Vital #{vital.id}</h3>
                  <span className={`bp-status ${bpStatus.color}`}>
                    {bpStatus.status}
                  </span>
                </div>
                
                <div className="vital-signs-card-body">
                  <div className="vital-signs-grid">
                    <div className="vital-sign-item">
                      <h4>Tekanan Darah</h4>
                      <div className="vital-sign-value">
                        {vital.sistol}/{vital.diastol} mmHg
                      </div>
                    </div>
                    
                    <div className="vital-sign-item">
                      <h4>Nadi</h4>
                      <div className="vital-sign-value">
                        {vital.nadi} bpm
                      </div>
                    </div>
                    
                    <div className="vital-sign-item">
                      <h4>Suhu</h4>
                      <div className="vital-sign-value">
                        {vital.suhu}°C
                      </div>
                    </div>
                    
                    <div className="vital-sign-item">
                      <h4>Pernapasan</h4>
                      <div className="vital-sign-value">
                        {vital.pernapasan} /menit
                      </div>
                    </div>
                    
                    <div className="vital-sign-item">
                      <h4>SpO2</h4>
                      <div className="vital-sign-value">
                        {vital.spo2}%
                      </div>
                    </div>
                    
                    <div className="vital-sign-item">
                      <h4>Berat Badan</h4>
                      <div className="vital-sign-value">
                        {vital.berat_badan} kg
                      </div>
                    </div>
                  </div>
                  
                  <div className="vital-signs-actions">
                    <button className="btn btn-outline">Lihat Detail</button>
                    <button className="btn btn-primary">Edit</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="anthropometry-grid">
          {anthropometry.map((anthro) => {
            const bmi = calculateBMI(anthro.berat_badan, anthro.tinggi_badan);
            const bmiCategory = getBMICategory(parseFloat(bmi));
            
            return (
              <div key={anthro.id} className="anthropometry-card">
                <div className="anthropometry-card-header">
                  <h3>Antropometri #{anthro.id}</h3>
                  <span className={`bmi-category ${bmiCategory.color}`}>
                    BMI: {bmi} - {bmiCategory.category}
                  </span>
                </div>
                
                <div className="anthropometry-card-body">
                  <div className="anthropometry-grid">
                    <div className="anthropometry-item">
                      <h4>Berat Badan</h4>
                      <div className="anthropometry-value">
                        {anthro.berat_badan} kg
                      </div>
                    </div>
                    
                    <div className="anthropometry-item">
                      <h4>Tinggi Badan</h4>
                      <div className="anthropometry-value">
                        {anthro.tinggi_badan} cm
                      </div>
                    </div>
                    
                    <div className="anthropometry-item">
                      <h4>Lingkar Pinggang</h4>
                      <div className="anthropometry-value">
                        {anthro.lingkar_pinggang} cm
                      </div>
                    </div>
                    
                    <div className="anthropometry-item">
                      <h4>Lingkar Pinggul</h4>
                      <div className="anthropometry-value">
                        {anthro.lingkar_pinggul} cm
                      </div>
                    </div>
                    
                    <div className="anthropometry-item">
                      <h4>LILA</h4>
                      <div className="anthropometry-value">
                        {anthro.lingkar_lengan_atas} cm
                      </div>
                    </div>
                    
                    <div className="anthropometry-item">
                      <h4>Tebal Lemak Trisep</h4>
                      <div className="anthropometry-value">
                        {anthro.tebal_lemak_trisep} mm
                      </div>
                    </div>
                  </div>
                  
                  <div className="anthropometry-actions">
                    <button className="btn btn-outline">Lihat Detail</button>
                    <button className="btn btn-primary">Edit</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {(activeTab === 'vital-signs' ? vitalSigns : anthropometry).length === 0 && (
        <div className="no-data">
          <p>Tidak ada data {activeTab === 'vital-signs' ? 'tanda vital' : 'antropometri'}</p>
        </div>
      )}
    </div>
  );
}

export default ExaminationList;
