import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Header from './components/Header';
import Home from './pages/Home';
import ItineraryPlanner from './pages/ItineraryPlanner';
import About from './pages/About';
import { apiService } from './services/api';

function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(false);
  const [healthCheckLoading, setHealthCheckLoading] = useState(true);

  useEffect(() => {
    // Check backend health on app load
    const checkBackendHealth = async () => {
      try {
        await apiService.health();
        setIsBackendHealthy(true);
      } catch (error) {
        console.error('Backend health check failed:', error);
        setIsBackendHealthy(false);
      } finally {
        setHealthCheckLoading(false);
      }
    };

    checkBackendHealth();
  }, []);

  if (healthCheckLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking backend connection...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header isBackendHealthy={isBackendHealthy} />
        
        {!isBackendHealthy && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mx-4 mt-4 rounded">
            <strong className="font-bold">Backend Connection Issue:</strong>
            <span className="block sm:inline"> Unable to connect to the backend API. Some features may not work properly.</span>
          </div>
        )}

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/planner" element={<ItineraryPlanner />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
