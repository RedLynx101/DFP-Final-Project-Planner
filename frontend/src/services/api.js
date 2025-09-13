import axios from 'axios';

// Get the backend URL - use the Replit domain if available, otherwise localhost
const getBackendUrl = () => {
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    // In Replit, replace port in domain to get backend URL
    const hostname = window.location.hostname;
    const replitDomain = hostname.replace(/-.+\./, '-00-23tgmvbh4vn59.');
    return `https://${replitDomain}`;
  }
  return 'http://localhost:8000';
};

const API_BASE_URL = getBackendUrl();

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

  // Create itinerary
  createItinerary: async (payload) => {
    const response = await api.post('/api/itinerary', payload);
    return response.data;
  },

  // Create itinerary options
  createItineraryOptions: async (payload) => {
    const response = await api.post('/api/itinerary/options', payload);
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