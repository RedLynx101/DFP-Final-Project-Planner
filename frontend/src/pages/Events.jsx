import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEnvironment, setSelectedEnvironment] = useState('all');
  const [sortBy, setSortBy] = useState('date');
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const data = await apiService.getEventsThisWeek();
        setEvents(data.events || []);
      } catch (err) {
        setError('Failed to load events');
        console.error('Error fetching events:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  // Filter and sort events
  const filteredEvents = events
    .filter(event => {
      const matchesSearch = event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           (event.details && event.details.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesEnvironment = selectedEnvironment === 'all' || 
                                event.environment === selectedEnvironment ||
                                (selectedEnvironment === 'unknown' && !event.environment);
      
      return matchesSearch && matchesEnvironment;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'date':
          return (a.date_hint || '').localeCompare(b.date_hint || '');
        default:
          return 0;
      }
    });

  const handleEventClick = (event) => {
    setSelectedEvent(event);
  };

  const closeModal = () => {
    setSelectedEvent(null);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="bg-gradient-to-r from-yellow-400 via-yellow-500 to-black rounded-2xl p-8 mb-8 text-white shadow-2xl">
        <div className="max-w-4xl">
          <div className="inline-flex items-center bg-black bg-opacity-20 backdrop-blur-sm rounded-full px-4 py-2 mb-6 border border-yellow-300 border-opacity-30">
            <span className="text-yellow-300 mr-2">🎭</span>
            <span className="text-sm font-semibold text-yellow-100 tracking-wide">HAPPENING NOW</span>
          </div>
          
          <h1 className="text-4xl lg:text-5xl font-bold mb-4 leading-tight">
            <span className="text-yellow-300">Pittsburgh</span>
            <br />
            <span className="text-white">Events & Entertainment</span>
          </h1>
          
          <p className="text-xl text-yellow-100 leading-relaxed max-w-2xl">
            Discover concerts, festivals, theater, sports, and cultural events happening across the Steel City.
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-gray-100">
        <div className="flex flex-col lg:flex-row gap-6 items-start lg:items-center">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                placeholder="Search events, venues, or activities..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-lg"
              />
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <span className="text-2xl">🔍</span>
              </div>
            </div>
          </div>

          {/* Environment Filter */}
          <div className="flex flex-wrap gap-2">
            {[
              { value: 'all', label: 'All Events', icon: '🎯' },
              { value: 'indoor', label: 'Indoor', icon: '🏢' },
              { value: 'outdoor', label: 'Outdoor', icon: '🌞' },
              { value: 'unknown', label: 'Mixed', icon: '🎭' }
            ].map(env => (
              <button
                key={env.value}
                onClick={() => setSelectedEnvironment(env.value)}
                className={`
                  flex items-center px-4 py-2 rounded-lg font-medium transition-all duration-300
                  ${selectedEnvironment === env.value
                    ? 'bg-yellow-500 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                <span className="mr-2">{env.icon}</span>
                {env.label}
              </button>
            ))}
          </div>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-500 bg-white"
          >
            <option value="date">Sort by Date</option>
            <option value="title">Sort by Name</option>
          </select>
        </div>

        {/* Results Count */}
        <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
          <span>
            {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
            {searchTerm && ` for "${searchTerm}"`}
          </span>
          
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="text-yellow-600 hover:text-yellow-700 font-medium"
            >
              Clear search ✕
            </button>
          )}
        </div>
      </div>

      {/* Events Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-16">
          <div className="relative mb-6">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-yellow-400 border-t-transparent"></div>
            <div className="absolute inset-0 rounded-full border-4 border-yellow-100"></div>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Finding Amazing Events</h3>
          <p className="text-gray-600">Discovering the best Pittsburgh has to offer...</p>
        </div>
      ) : error ? (
        <div className="text-center py-16">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <span className="text-4xl">😔</span>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Unable to Load Events</h3>
          <p className="text-red-600 mb-6">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-xl font-medium transition-colors shadow-lg"
          >
            🔄 Try Again
          </button>
        </div>
      ) : filteredEvents.length === 0 ? (
        <div className="text-center py-16">
          <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <span className="text-4xl">🔍</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">No Events Found</h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            {searchTerm 
              ? `No events match "${searchTerm}". Try adjusting your search or filters.`
              : 'No events available for the selected criteria.'
            }
          </p>
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="text-yellow-600 hover:text-yellow-700 font-medium"
            >
              Clear search to see all events
            </button>
          )}
        </div>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
          {filteredEvents.map((event, index) => (
            <div 
              key={index} 
              onClick={() => handleEventClick(event)}
              className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100 cursor-pointer overflow-hidden"
            >
              {/* Event Header */}
              <div className="p-6 pb-4">
                <div className="flex items-start justify-between mb-4">
                  <div className="w-14 h-14 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <span className="text-2xl">
                      {event.environment === 'outdoor' ? '🌟' : 
                       event.environment === 'indoor' ? '🏢' : '🎭'}
                    </span>
                  </div>
                  
                  {event.date_hint && (
                    <div className="bg-yellow-100 text-yellow-800 text-xs px-3 py-2 rounded-full font-semibold">
                      {event.date_hint.length > 20 ? 
                        event.date_hint.substring(0, 20) + '...' : 
                        event.date_hint}
                    </div>
                  )}
                </div>

                <h3 className="text-xl font-bold text-gray-800 mb-3 line-clamp-2 group-hover:text-yellow-600 transition-colors">
                  {event.title}
                </h3>

                {event.details && (
                  <p className="text-gray-600 text-sm leading-relaxed mb-4 line-clamp-3">
                    {event.details}
                  </p>
                )}

                {/* Event Type Badge */}
                <div className="flex items-center mb-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    event.environment === 'outdoor' 
                      ? 'bg-green-100 text-green-700'
                      : event.environment === 'indoor'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-purple-100 text-purple-700'
                  }`}>
                    {event.environment === 'outdoor' ? '🌞 Outdoor Event' :
                     event.environment === 'indoor' ? '🏢 Indoor Event' :
                     '🎭 Event'}
                  </span>
                </div>
              </div>

              {/* Event Footer */}
              <div className="px-6 pb-6">
                <div className="flex items-center justify-between">
                  <span className="text-yellow-600 font-medium text-sm group-hover:underline">
                    View Details →
                  </span>
                  
                  {event.url && (
                    <div className="flex items-center text-xs text-gray-500">
                      <span className="mr-1">🌐</span>
                      <span>External Link</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Event Detail Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-yellow-400 to-yellow-600 p-6 text-white rounded-t-2xl">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-2">{selectedEvent.title}</h2>
                  {selectedEvent.date_hint && (
                    <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-lg px-3 py-2 inline-block">
                      <span className="font-medium">🗓️ {selectedEvent.date_hint}</span>
                    </div>
                  )}
                </div>
                <button
                  onClick={closeModal}
                  className="bg-white bg-opacity-20 hover:bg-opacity-30 p-2 rounded-full transition-colors"
                >
                  <span className="text-white text-xl">✕</span>
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              {selectedEvent.details && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3">Event Details</h3>
                  <p className="text-gray-700 leading-relaxed">{selectedEvent.details}</p>
                </div>
              )}

              {/* Event Info */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-gray-50 rounded-xl p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-2xl mr-3">
                      {selectedEvent.environment === 'outdoor' ? '🌞' : 
                       selectedEvent.environment === 'indoor' ? '🏢' : '🎭'}
                    </span>
                    <span className="font-semibold text-gray-800">Environment</span>
                  </div>
                  <span className="text-gray-600 capitalize">
                    {selectedEvent.environment || 'Mixed/Unknown'}
                  </span>
                </div>

                <div className="bg-gray-50 rounded-xl p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-2xl mr-3">📅</span>
                    <span className="font-semibold text-gray-800">When</span>
                  </div>
                  <span className="text-gray-600">
                    {selectedEvent.date_hint || 'Check event website'}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                {selectedEvent.url && (
                  <a
                    href={selectedEvent.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white text-center py-3 px-4 rounded-xl font-medium transition-colors shadow-lg"
                  >
                    🌐 Visit Event Website
                  </a>
                )}
                
                <button
                  onClick={closeModal}
                  className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 py-3 px-4 rounded-xl font-medium transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Events;