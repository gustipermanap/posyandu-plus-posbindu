import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api';

const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        // Check if token is expired
        if (decodedToken.exp < currentTime) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          return false;
        }
        return true;
      } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return false;
      }
    }
    return false;
  });
  const [loggedInUser, setLoggedInUser] = useState(null);

  const fetchUserData = async () => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      try {
        const decodedToken = jwtDecode(accessToken);
        const userId = decodedToken.user_id;
        const response = await api.get(`/auth/user-info/`);
        console.log("DEBUG: User data fetched:", response.data); // Debug print
        setLoggedInUser(response.data);
      } catch (error) {
        console.error("Error decoding token or fetching user data:", error);
        // If token is invalid, clear it and logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsLoggedIn(false);
        setLoggedInUser(null);
      }
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchUserData();
    } else {
      setLoggedInUser(null);
    }
  }, [isLoggedIn]);

  const handleLogin = (accessToken, refreshToken) => {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    console.log("DEBUG: Logging out user"); // Debug print
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsLoggedIn(false);
    setLoggedInUser(null);
    // Force page reload to ensure clean state
    window.location.reload();
  };

  return { isLoggedIn, loggedInUser, handleLogin, handleLogout, fetchUserData };
};

export default useAuth;
