import { useState, useEffect, useCallback } from 'react';
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

  const fetchUserData = useCallback(async () => {
    const accessToken = localStorage.getItem('access_token');
    console.log("DEBUG: fetchUserData called, accessToken exists:", !!accessToken);
    if (accessToken) {
      try {
        const decodedToken = jwtDecode(accessToken);
        console.log("DEBUG: Token decoded successfully, user_id:", decodedToken.user_id);
        const response = await api.get(`/api/auth/user-info/`);
        console.log("DEBUG: User data fetched successfully:", response.data);
        setLoggedInUser(response.data);
      } catch (error) {
        console.error("DEBUG: Error fetching user data:", error);
        console.error("DEBUG: Error response:", error.response?.data);
        console.error("DEBUG: Error status:", error.response?.status);
        // If token is invalid, clear it and logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsLoggedIn(false);
        setLoggedInUser(null);
      }
    }
  }, []);

  useEffect(() => {
    if (isLoggedIn) {
      fetchUserData();
    } else {
      setLoggedInUser(null);
    }
  }, [isLoggedIn, fetchUserData]);

  const handleLogin = (accessToken, refreshToken) => {
    console.log("DEBUG: handleLogin called with tokens:", { accessToken: !!accessToken, refreshToken: !!refreshToken });
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    console.log("DEBUG: Tokens saved to localStorage");
    setIsLoggedIn(true);
    console.log("DEBUG: isLoggedIn set to true");
    
    // Immediately try to fetch user data
    setTimeout(() => {
      console.log("DEBUG: Fetching user data after login...");
      fetchUserData();
    }, 100);
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
