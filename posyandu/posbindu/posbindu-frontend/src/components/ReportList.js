import React, { useState, useEffect } from 'react';
import './ReportList.css';

function ReportList() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    jenis_laporan: '',
    status: '',
    tanggal_mulai: '',
    tanggal_akhir: ''
  });

  useEffect(() => {
    fetchReports();
  }, [filters]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams();
      if (filters.search) queryParams.append('search', filters.search);
      if (filters.jenis_laporan) queryParams.append('jenis_laporan', filters.jenis_laporan);
      if (filters.status) queryParams.append('status', filters.status);
      if (filters.tanggal_mulai) queryParams.append('tanggal_mulai', filters.tanggal_mulai);
      if (filters.tanggal_akhir) queryParams.append('tanggal_akhir', filters.tanggal_akhir);
      
      const response = await fetch(`http://localhost:8080/api/reporting/report-log/?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch reports');
      
      const data = await response.json();
      setReports(data.results || data);
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
      case 'Final': return 'final';
      case 'Published': return 'published';
      case 'Archived': return 'archived';
      default: return 'draft';
    }
  };

  const getReportTypeColor = (jenis) => {
    switch (jenis) {
      case 'harian': return 'daily';
      case 'mingguan': return 'weekly';
      case 'bulanan': return 'monthly';
      case 'tahunan': return 'yearly';
      case 'khusus': return 'special';
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

  const formatDateRange = (tanggalMulai, tanggalAkhir) => {
    const start = formatDate(tanggalMulai);
    const end = formatDate(tanggalAkhir);
    return `${start} - ${end}`;
  };

  const getFileSize = (fileUrl) => {
    if (!fileUrl) return 'Tidak ada file';
    // Simulasi ukuran file
    return '2.5 MB';
  };

  const getFileExtension = (fileUrl) => {
    if (!fileUrl) return '';
    const extension = fileUrl.split('.').pop().toUpperCase();
    return extension;
  };

  if (loading) return <div className="loading">Loading reports...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="report-list">
      <div className="report-header">
        <h2>Data Laporan POS BINDU PTM</h2>
        <div className="report-actions">
          <button className="btn btn-primary">Buat Laporan Baru</button>
        </div>
      </div>

      <div className="filters-section">
        <div className="filters">
          <input
            type="text"
            placeholder="Cari laporan..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          <select 
            value={filters.jenis_laporan} 
            onChange={(e) => handleFilterChange('jenis_laporan', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Jenis</option>
            <option value="harian">Harian</option>
            <option value="mingguan">Mingguan</option>
            <option value="bulanan">Bulanan</option>
            <option value="tahunan">Tahunan</option>
            <option value="khusus">Khusus</option>
          </select>
          
          <select 
            value={filters.status} 
            onChange={(e) => handleFilterChange('status', e.target.value)}
            className="filter-select"
          >
            <option value="">Semua Status</option>
            <option value="Draft">Draft</option>
            <option value="Final">Final</option>
            <option value="Published">Published</option>
            <option value="Archived">Archived</option>
          </select>
          
          <input
            type="date"
            placeholder="Tanggal Mulai"
            value={filters.tanggal_mulai}
            onChange={(e) => handleFilterChange('tanggal_mulai', e.target.value)}
            className="filter-input"
          />
          
          <input
            type="date"
            placeholder="Tanggal Akhir"
            value={filters.tanggal_akhir}
            onChange={(e) => handleFilterChange('tanggal_akhir', e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      <div className="reports-grid">
        {reports.map((report) => {
          const statusColor = getStatusColor(report.status);
          const typeColor = getReportTypeColor(report.jenis_laporan);
          
          return (
            <div key={report.id} className="report-card">
              <div className="report-card-header">
                <h3>{report.nama_laporan}</h3>
                <div className="report-badges">
                  <span className={`status-badge ${statusColor}`}>
                    {report.status}
                  </span>
                  <span className={`type-badge ${typeColor}`}>
                    {report.jenis_laporan}
                  </span>
                </div>
              </div>
              
              <div className="report-card-body">
                <div className="report-info">
                  <p><strong>Jenis Laporan:</strong> {report.jenis_laporan}</p>
                  <p><strong>Periode:</strong> {formatDateRange(report.tanggal_mulai, report.tanggal_akhir)}</p>
                  <p><strong>Status:</strong> {report.status}</p>
                  <p><strong>Dibuat:</strong> {formatDate(report.created_at)}</p>
                  <p><strong>Diupdate:</strong> {formatDate(report.updated_at)}</p>
                </div>
                
                <div className="report-file">
                  <h4>File Laporan:</h4>
                  {report.file_laporan ? (
                    <div className="file-info">
                      <span className="file-icon">📄</span>
                      <span className="file-name">
                        {report.nama_laporan}.{getFileExtension(report.file_laporan)}
                      </span>
                      <span className="file-size">
                        {getFileSize(report.file_laporan)}
                      </span>
                    </div>
                  ) : (
                    <p className="no-file">Tidak ada file</p>
                  )}
                </div>
                
                <div className="report-data">
                  <h4>Data Laporan:</h4>
                  <div className="data-preview">
                    <p>Total Peserta: {report.data_laporan?.total_peserta || 0}</p>
                    <p>Total Kunjungan: {report.data_laporan?.total_kunjungan || 0}</p>
                    <p>Total Pemeriksaan: {report.data_laporan?.total_pemeriksaan || 0}</p>
                    <p>Total Rujukan: {report.data_laporan?.total_rujukan || 0}</p>
                  </div>
                </div>
                
                <div className="report-actions">
                  <button className="btn btn-outline">Lihat Detail</button>
                  <button className="btn btn-primary">Download</button>
                  <button className="btn btn-secondary">Edit</button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {reports.length === 0 && (
        <div className="no-data">
          <p>Tidak ada data laporan</p>
        </div>
      )}
    </div>
  );
}

export default ReportList;
