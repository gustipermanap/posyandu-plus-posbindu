import React, { useState, useEffect } from 'react';
import './Dashboard.css';

function Dashboard({ loggedInUser }) {
  const [dashboardData, setDashboardData] = useState({
    totalParticipants: 0,
    totalVisits: 0,
    totalExaminations: 0,
    totalLabResults: 0,
    totalRiskAssessments: 0,
    totalInterventions: 0,
    totalReferrals: 0,
    highRiskParticipants: 0,
    pendingReferrals: 0,
    activeInterventions: 0,
    recentActivities: []
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Simulasi data dashboard POS BINDU PTM
      setDashboardData({
        totalParticipants: 245,
        totalVisits: 156,
        totalExaminations: 142,
        totalLabResults: 89,
        totalRiskAssessments: 134,
        totalInterventions: 67,
        totalReferrals: 23,
        highRiskParticipants: 18,
        pendingReferrals: 8,
        activeInterventions: 45,
        recentActivities: [
          { id: 1, activity: 'Peserta baru terdaftar', participant: 'Ahmad Suryadi', time: '10:30' },
          { id: 2, activity: 'Skrining selesai', participant: 'Siti Nurhaliza', time: '11:15' },
          { id: 3, activity: 'Hasil lab diterima', participant: 'Budi Santoso', time: '11:45' },
          { id: 4, activity: 'Rujukan dibuat', participant: 'Dewi Kartika', time: '12:20' },
          { id: 5, activity: 'Intervensi dimulai', participant: 'Rudi Hartono', time: '13:10' }
        ]
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Selamat Datang di POS BINDU PTM</h1>
      <p>Halo {loggedInUser ? loggedInUser.username : 'Guest'}, berikut adalah ringkasan data POS BINDU PTM hari ini.</p>
      
      <div className="dashboard-grid">
        {/* Statistik Utama */}
        <div className="stats-section">
          <h2>Statistik Utama</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Peserta</h3>
              <div className="stat-number">{dashboardData.totalParticipants}</div>
            </div>
            <div className="stat-card">
              <h3>Kunjungan Hari Ini</h3>
              <div className="stat-number">{dashboardData.totalVisits}</div>
            </div>
            <div className="stat-card">
              <h3>Pemeriksaan Fisik</h3>
              <div className="stat-number">{dashboardData.totalExaminations}</div>
            </div>
            <div className="stat-card">
              <h3>Hasil Lab</h3>
              <div className="stat-number">{dashboardData.totalLabResults}</div>
            </div>
            <div className="stat-card">
              <h3>Penilaian Risiko</h3>
              <div className="stat-number">{dashboardData.totalRiskAssessments}</div>
            </div>
            <div className="stat-card">
              <h3>Intervensi Aktif</h3>
              <div className="stat-number">{dashboardData.activeInterventions}</div>
            </div>
          </div>
        </div>

        {/* Kategori Risiko */}
        <div className="risk-section">
          <h2>Kategori Risiko Peserta</h2>
          <div className="risk-grid">
            <div className="risk-card low">
              <h3>Risiko Rendah</h3>
              <div className="risk-number">{dashboardData.totalParticipants - dashboardData.highRiskParticipants - 45}</div>
            </div>
            <div className="risk-card medium">
              <h3>Risiko Sedang</h3>
              <div className="risk-number">45</div>
            </div>
            <div className="risk-card high">
              <h3>Risiko Tinggi</h3>
              <div className="risk-number">{dashboardData.highRiskParticipants}</div>
            </div>
          </div>
        </div>

        {/* Status Rujukan */}
        <div className="referral-section">
          <h2>Status Rujukan</h2>
          <div className="referral-grid">
            <div className="referral-card completed">
              <h3>Selesai</h3>
              <div className="referral-number">{dashboardData.totalReferrals - dashboardData.pendingReferrals}</div>
            </div>
            <div className="referral-card pending">
              <h3>Pending</h3>
              <div className="referral-number">{dashboardData.pendingReferrals}</div>
            </div>
          </div>
        </div>

        {/* Aktivitas Terbaru */}
        <div className="activity-section">
          <h2>Aktivitas Terbaru</h2>
          <div className="activity-list">
            {dashboardData.recentActivities.map((activity) => (
              <div key={activity.id} className="activity-item">
                <div className="activity-time">{activity.time}</div>
                <div className="activity-description">{activity.activity}</div>
                <div className="activity-participant">{activity.participant}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
