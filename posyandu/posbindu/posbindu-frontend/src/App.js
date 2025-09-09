import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ParticipantList from './components/ParticipantList';
import ScreeningList from './components/ScreeningList';
import ExaminationList from './components/ExaminationList';
import LabList from './components/LabList';
import RiskAssessmentList from './components/RiskAssessmentList';
import InterventionList from './components/InterventionList';
import ReferralList from './components/ReferralList';
import ReportList from './components/ReportList';
import LoginPage from './components/LoginPage';
import ProfilePage from './components/ProfilePage';
import useAuth from './hooks/useAuth';
import './App.css';

function App() {
  const { isLoggedIn, loggedInUser, handleLogin, handleLogout, fetchUserData } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  // Menutup dropdown ketika mengklik di luar area dropdown
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showDropdown && !event.target.closest('.profile-dropdown-menu') && !event.target.closest('[style*="float: right"]')) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

  return (
    <Router>
      <div className="App">
        {!isLoggedIn ? (
          <LoginPage onLogin={handleLogin} />
        ) : (
          <>
            <nav>
              <ul>
                <li>
                  <Link to="/">Dashboard</Link>
                </li>
                <li>
                  <Link to="/participant">Peserta</Link>
                </li>
                <li>
                  <Link to="/screening">Skrining</Link>
                </li>
                <li>
                  <Link to="/examination">Pemeriksaan</Link>
                </li>
                <li>
                  <Link to="/lab">Laboratorium</Link>
                </li>
                <li>
                  <Link to="/risk-assessment">Penilaian Risiko</Link>
                </li>
                <li>
                  <Link to="/intervention">Intervensi</Link>
                </li>
                <li>
                  <Link to="/referral">Rujukan</Link>
                </li>
                <li>
                  <Link to="/report">Laporan</Link>
                </li>
                {loggedInUser && 
                  <li style={{ float: 'right', marginRight: '20px', color: 'white', display: 'flex', alignItems: 'center', position: 'relative' }}>
                    <div onClick={toggleDropdown} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
                      {console.log("DEBUG: loggedInUser.profile_picture:", loggedInUser.profile_picture)} {/* Debug print */}
                      {loggedInUser.profile_picture && 
                        <img src={loggedInUser.profile_picture} alt="Profile" style={{ width: '30px', height: '30px', borderRadius: '50%', marginRight: '10px', objectFit: 'cover' }} />
                      } 
                      {!loggedInUser.profile_picture && 
                        <div style={{ width: '30px', height: '30px', borderRadius: '50%', marginRight: '10px', backgroundColor: '#007bff', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '14px', fontWeight: 'bold' }}>
                          {loggedInUser.username ? loggedInUser.username.charAt(0).toUpperCase() : 'U'}
                        </div>
                      } 
                      Selamat Datang, {loggedInUser.username}
                    </div>
                    {showDropdown && (
                      <div className="profile-dropdown-menu">
                        <Link to="/profile" className="profile-dropdown-item" onClick={toggleDropdown}>Profil</Link>
                        <Link to="/change-password" className="profile-dropdown-item" onClick={toggleDropdown}>Ganti Password</Link>
                        <Link to="/" onClick={() => { setIsLoading(true); handleLogout(); toggleDropdown(); }} className="profile-dropdown-item">
                          {isLoading ? 'Logging out...' : 'Logout'}
                        </Link>
                      </div>
                    )}
                  </li>
                }
              </ul>
            </nav>

            <Routes>
              <Route path="/" element={<Dashboard loggedInUser={loggedInUser} />} />
              <Route path="/participant" element={<ParticipantList />} />
              <Route path="/screening" element={<ScreeningList />} />
              <Route path="/examination" element={<ExaminationList />} />
              <Route path="/lab" element={<LabList />} />
              <Route path="/risk-assessment" element={<RiskAssessmentList />} />
              <Route path="/intervention" element={<InterventionList />} />
              <Route path="/referral" element={<ReferralList />} />
              <Route path="/report" element={<ReportList />} />
              <Route path="/profile" element={<ProfilePage loggedInUser={loggedInUser} onProfileUpdate={fetchUserData} />} />
              <Route path="/change-password" element={<ProfilePage loggedInUser={loggedInUser} onProfileUpdate={fetchUserData} isChangePasswordPage={true} />} />
            </Routes>
          </>
        )}
      </div>
    </Router>
  );
}

export default App;
