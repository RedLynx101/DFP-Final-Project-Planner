import axios from 'axios';

// Get the backend URL - secure production-ready logic
const getBackendUrl = () => {
  // Check if we're in production mode
  const isProduction = import.meta.env.MODE === 'production' || import.meta.env.PROD;
  
  // If VITE_API_BASE_URL is explicitly set, use it (for custom deployments)
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // In production without explicit API URL, use relative URLs (same-origin deployment)
  if (isProduction) {
    // When frontend and backend are served from the same origin (current deployment)
    return '';  // Relative URLs will work since FastAPI serves both frontend and backend
  }
  
  // Development fallback to localhost backend
  return 'http://localhost:8000';
};

// Initialize API base URL with error handling
let API_BASE_URL;
try {
  API_BASE_URL = getBackendUrl();
} catch (error) {
  console.error('API Configuration Error:', error.message);
  // In case of configuration error, we still need a URL for axios
  // This will cause API calls to fail gracefully
  API_BASE_URL = 'http://localhost:8000';
}

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const apiService = {
  // Health check
  health: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },

  // Create itinerary (with extended timeout for long processing)
  createItinerary: async (payload) => {
    const response = await api.post('/api/itinerary', payload, {
      timeout: 180000 // 3 minutes timeout for itinerary generation
    });
    return response.data;
  },

  // Create itinerary options (with extended timeout for long processing)
  createItineraryOptions: async (payload) => {
    const response = await api.post('/api/itinerary/options', payload, {
      timeout: 180000 // 3 minutes timeout for itinerary generation
    });
    return response.data;
  },

  // Search food
  searchFood: async (query, location = 'Pittsburgh, PA', limit = 5, price = null) => {
    const params = { query, location, limit };
    if (price) params.price = price;
    const response = await api.get('/api/food/search', { params });
    return response.data;
  },

  // Get events for this week
  getEventsThisWeek: async () => {
    const response = await api.get('/api/events/this-week');
    return response.data;
  },
};

export default api;