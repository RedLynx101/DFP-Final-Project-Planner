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
      <div className="relative bg-gradient-to-br from-yellow-400 via-yellow-500 to-black rounded-xl overflow-hidden p-0 mb-8 text-white shadow-2xl">
        {/* Pittsburgh-themed background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-full h-full bg-repeat-x" 
               style={{
                 backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
                 backgroundSize: '60px 60px'
               }}></div>
        </div>
        
        <div className="relative z-10 p-8 lg:p-12">
          <div className="max-w-4xl">
            {/* Steel City Badge */}
            <div className="inline-flex items-center bg-black bg-opacity-20 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-yellow-300 border-opacity-30">
              <span className="text-yellow-300 mr-2">🏭</span>
              <span className="text-sm font-semibold text-yellow-100 tracking-wide">THE STEEL CITY</span>
            </div>
            
            <h2 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              <span className="text-yellow-300">Pittsburgh</span>
              <br />
              <span className="text-white">Weekend</span>
              <br />
              <span className="text-black">Planner</span>
            </h2>
            
            <p className="text-xl lg:text-2xl mb-8 text-yellow-100 leading-relaxed max-w-2xl">
              From <span className="font-semibold text-yellow-300">Primanti Bros</span> to the 
              <span className="font-semibold text-yellow-300"> Carnegie Museums</span>, discover 
              personalized weekend adventures in America's most livable city.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                to="/planner"
                className="inline-flex items-center justify-center bg-black text-yellow-300 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-900 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <span className="mr-2">⚡</span>
                Start Planning Now
                <span className="ml-2">→</span>
              </Link>
              
              <div className="inline-flex items-center text-yellow-200">
                <div className="flex -space-x-2 mr-4">
                  <div className="w-10 h-10 rounded-full bg-yellow-500 border-2 border-white flex items-center justify-center">🍔</div>
                  <div className="w-10 h-10 rounded-full bg-yellow-600 border-2 border-white flex items-center justify-center">🏛️</div>
                  <div className="w-10 h-10 rounded-full bg-yellow-700 border-2 border-white flex items-center justify-center">🎭</div>
                </div>
                <div className="text-sm">
                  <div className="font-semibold">500+ Activities</div>
                  <div className="opacity-75">Ready to explore</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        {/* Food & Dining */}
        <div className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <span className="text-3xl">🍽️</span>
          </div>
          <h3 className="text-2xl font-bold mb-4 text-gray-800">Iconic Eats</h3>
          <p className="text-gray-600 leading-relaxed mb-4">
            From legendary <span className="font-semibold text-yellow-600">Primanti Bros</span> sandwiches 
            to award-winning <span className="font-semibold text-yellow-600">Strip District</span> markets. 
            Experience Pittsburgh's unique culinary scene.
          </p>
          <div className="flex items-center text-sm text-yellow-600 font-medium">
            <span className="mr-2">🍔</span>
            500+ Restaurants & Cafés
          </div>
        </div>
        
        {/* Museums & Culture */}
        <div className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100">
          <div className="w-16 h-16 bg-gradient-to-br from-black to-gray-700 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <span className="text-3xl">🏛️</span>
          </div>
          <h3 className="text-2xl font-bold mb-4 text-gray-800">World-Class Culture</h3>
          <p className="text-gray-600 leading-relaxed mb-4">
            Explore the <span className="font-semibold text-gray-700">Carnegie Museums</span>, 
            <span className="font-semibold text-gray-700"> Heinz History Center</span>, and renowned 
            <span className="font-semibold text-gray-700"> Phipps Conservatory</span>.
          </p>
          <div className="flex items-center text-sm text-gray-700 font-medium">
            <span className="mr-2">🎨</span>
            25+ Museums & Galleries
          </div>
        </div>
        
        {/* Events & Entertainment */}
        <div className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
            <span className="text-3xl">🎭</span>
          </div>
          <h3 className="text-2xl font-bold mb-4 text-gray-800">Live Entertainment</h3>
          <p className="text-gray-600 leading-relaxed mb-4">
            From <span className="font-semibold text-orange-600">Heinz Hall</span> concerts to 
            <span className="font-semibold text-orange-600"> Steelers games</span>. Discover festivals, 
            theater, and nightlife across all neighborhoods.
          </p>
          <div className="flex items-center text-sm text-orange-600 font-medium">
            <span className="mr-2">🎵</span>
            100+ Weekly Events
          </div>
        </div>
      </div>

      {/* This Week's Events */}
      <div className="bg-gradient-to-r from-gray-50 to-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h3 className="text-3xl font-bold text-gray-800 mb-2">This Week in Pittsburgh</h3>
            <p className="text-gray-600">Don't miss these exciting events happening around the Steel City</p>
          </div>
          <div className="hidden md:block">
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <span>🗓️</span>
              <span className="font-medium">Live Updates</span>
            </div>
          </div>
        </div>
        
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <div className="relative">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-yellow-400 border-t-transparent"></div>
              <div className="absolute inset-0 rounded-full border-4 border-yellow-100"></div>
            </div>
            <span className="ml-4 text-gray-600 text-lg">Discovering amazing events...</span>
          </div>
        ) : error ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">😔</span>
            </div>
            <p className="text-red-600 mb-6 text-lg">{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              🔄 Try Again
            </button>
          </div>
        ) : eventsData && eventsData.events && eventsData.events.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {eventsData.events.slice(0, 6).map((event, index) => (
                <div key={index} className="group bg-white rounded-xl p-6 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-lg flex items-center justify-center">
                      <span className="text-xl">
                        {event.environment === 'outdoor' ? '🌟' : 
                         event.environment === 'indoor' ? '🏢' : '🎭'}
                      </span>
                    </div>
                    {event.date_hint && (
                      <div className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-medium">
                        {event.date_hint.length > 15 ? 
                          event.date_hint.substring(0, 15) + '...' : 
                          event.date_hint}
                      </div>
                    )}
                  </div>
                  
                  <h4 className="font-bold text-lg mb-3 text-gray-800 line-clamp-2 group-hover:text-yellow-600 transition-colors">
                    {event.title}
                  </h4>
                  
                  {event.details && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3 leading-relaxed">
                      {event.details}
                    </p>
                  )}
                  
                  {event.url && (
                    <a 
                      href={event.url} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="inline-flex items-center text-yellow-600 hover:text-yellow-700 text-sm font-medium group-hover:underline transition-colors"
                    >
                      <span>Learn More</span>
                      <span className="ml-1 transform group-hover:translate-x-1 transition-transform">→</span>
                    </a>
                  )}
                </div>
              ))}
            </div>
            
            {/* View All Events Button */}
            <div className="text-center">
              <Link 
                to="/events" 
                className="inline-flex items-center bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                <span className="mr-2">🎉</span>
                Explore All Events
                <span className="ml-2">→</span>
              </Link>
            </div>
          </>
        ) : (
          <div className="text-center py-16">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-3xl">📅</span>
            </div>
            <h4 className="text-xl font-semibold text-gray-700 mb-2">No Events This Week</h4>
            <p className="text-gray-500 mb-6">Check back later for exciting Pittsburgh events!</p>
            <Link 
              to="/planner" 
              className="text-yellow-600 hover:text-yellow-700 font-medium"
            >
              Plan Your Own Activities →
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;