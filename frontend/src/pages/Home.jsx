import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const Home = () => {
  const [eventsData, setEventsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await apiService.getEventsThisWeek();
        setEventsData(data);
      } catch (err) {
        setError('Failed to load events');
        console.error('Error fetching events:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-lg p-8 mb-8 text-white">
        <div className="max-w-3xl">
          <h2 className="text-4xl font-bold mb-4">Plan Your Perfect Pittsburgh Weekend</h2>
          <p className="text-xl mb-6 text-blue-100">
            Discover the best food, museums, events, and experiences the Steel City has to offer. 
            Get personalized itineraries based on your preferences, budget, and mobility needs.
          </p>
          <Link
            to="/planner"
            className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
          >
            Start Planning →
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-2xl">🍽️</span>
          </div>
          <h3 className="text-xl font-semibold mb-2">Food & Dining</h3>
          <p className="text-gray-600">
            Discover Pittsburgh's best restaurants, from famous Primanti Bros sandwiches to hidden local gems.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-2xl">🏛️</span>
          </div>
          <h3 className="text-xl font-semibold mb-2">Museums & Culture</h3>
          <p className="text-gray-600">
            Explore world-class museums, art galleries, and cultural attractions throughout the city.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <span className="text-2xl">🎭</span>
          </div>
          <h3 className="text-xl font-semibold mb-2">Events & Entertainment</h3>
          <p className="text-gray-600">
            Stay updated with the latest events, concerts, festivals, and entertainment options.
          </p>
        </div>
      </div>

      {/* This Week's Events */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-2xl font-semibold mb-6">This Week's Events</h3>
        
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading events...</span>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600 mb-4">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="text-blue-600 hover:text-blue-800"
            >
              Try Again
            </button>
          </div>
        ) : eventsData && eventsData.events && eventsData.events.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {eventsData.events.slice(0, 6).map((event, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h4 className="font-semibold text-lg mb-2 line-clamp-2">{event.title}</h4>
                {event.details && (
                  <p className="text-gray-600 text-sm mb-2 line-clamp-3">{event.details}</p>
                )}
                {event.date_hint && (
                  <p className="text-blue-600 text-sm mb-2">{event.date_hint}</p>
                )}
                {event.url && (
                  <a 
                    href={event.url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Learn More →
                  </a>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-600">No events found for this week.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;