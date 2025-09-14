import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const ItineraryPlanner = () => {
  const [formData, setFormData] = useState({
    city: 'Pittsburgh, PA',
    user_address: 'Hamburg Hall, 4800 Forbes Ave, Pittsburgh, PA 15213',
    max_distance_miles: 5,
    preferences: {
      budget_level: 'medium',
      interests: ['food', 'museums'],
      mobility: 'walk',
      environment: 'either'
    }
  });

  const [itinerary, setItinerary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Remove start_date and end_date from form data since backend will use defaults
  useEffect(() => {
    setFormData(prev => {
      const { start_date, end_date, ...rest } = prev;
      return rest;
    });
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('preferences.')) {
      const prefKey = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        preferences: {
          ...prev.preferences,
          [prefKey]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleInterestsChange = (interest) => {
    setFormData(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        interests: prev.preferences.interests.includes(interest)
          ? prev.preferences.interests.filter(i => i !== interest)
          : [...prev.preferences.interests, interest]
      }
    }));
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await apiService.createItinerary(formData);
      setItinerary(result);
    } catch (err) {
      setError('Failed to create itinerary. Please try again.');
      console.error('Error creating itinerary:', err);
    } finally {
      setLoading(false);
    }
  };

  const availableInterests = [
    'food', 'museums', 'art', 'music', 'sports', 'outdoors', 'shopping', 'history', 'nightlife'
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Plan Your Pittsburgh Itinerary</h2>
        <p className="text-gray-600">
          Create a personalized weekend plan based on your preferences and interests.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Planning Form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-6">Your Preferences</h3>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Basic Info */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Starting Location
              </label>
              <input
                type="text"
                name="user_address"
                value={formData.user_address}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your starting address"
              />
            </div>

            {/* Weekend Planning Info */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-2">🗓️</span>
                <h4 className="text-lg font-medium text-blue-800">Weekend Planning</h4>
              </div>
              <p className="text-blue-700 text-sm">
                Your itinerary will be automatically planned for the upcoming weekend (Saturday 10am - Sunday 10pm).
                Perfect for exploring Pittsburgh's best spots!
              </p>
            </div>

            {/* Budget Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                💰 Budget Level
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'low', label: 'Budget-Friendly', icon: '🍕', color: 'green', desc: '$0-50/day' },
                  { value: 'medium', label: 'Moderate', icon: '🍔', color: 'yellow', desc: '$50-150/day' },
                  { value: 'high', label: 'Premium', icon: '🥂', color: 'purple', desc: '$150+/day' }
                ].map(budget => (
                  <button
                    key={budget.value}
                    type="button"
                    onClick={() => handleInputChange({ target: { name: 'preferences.budget_level', value: budget.value }})}
                    className={`
                      p-4 rounded-xl border-2 text-center transition-all duration-300 hover:scale-105
                      ${formData.preferences.budget_level === budget.value
                        ? budget.color === 'green' ? 'border-green-500 bg-green-50 shadow-lg' :
                          budget.color === 'yellow' ? 'border-yellow-500 bg-yellow-50 shadow-lg' :
                          'border-purple-500 bg-purple-50 shadow-lg'
                        : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                      }
                    `}
                  >
                    <div className="text-3xl mb-2">{budget.icon}</div>
                    <div className={`font-semibold text-sm mb-1 ${
                      formData.preferences.budget_level === budget.value 
                        ? budget.color === 'green' ? 'text-green-700' :
                          budget.color === 'yellow' ? 'text-yellow-700' :
                          'text-purple-700'
                        : 'text-gray-700'
                    }`}>
                      {budget.label}
                    </div>
                    <div className="text-xs text-gray-500">{budget.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Interests */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                🎯 What Interests You? (Select multiple)
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {[
                  { value: 'food', label: 'Food & Dining', icon: '🍽️', color: 'yellow' },
                  { value: 'museums', label: 'Museums', icon: '🏛️', color: 'blue' },
                  { value: 'art', label: 'Art & Culture', icon: '🎨', color: 'purple' },
                  { value: 'music', label: 'Music & Shows', icon: '🎵', color: 'pink' },
                  { value: 'sports', label: 'Sports', icon: '⚽', color: 'green' },
                  { value: 'outdoors', label: 'Outdoors', icon: '🌲', color: 'emerald' },
                  { value: 'shopping', label: 'Shopping', icon: '🛍️', color: 'indigo' },
                  { value: 'history', label: 'History', icon: '📚', color: 'amber' },
                  { value: 'nightlife', label: 'Nightlife', icon: '🌙', color: 'violet' }
                ].map(interest => (
                  <button
                    key={interest.value}
                    type="button"
                    onClick={() => handleInterestsChange(interest.value)}
                    className={`
                      p-3 rounded-xl border-2 text-center transition-all duration-300 hover:scale-105
                      ${formData.preferences.interests.includes(interest.value)
                        ? interest.color === 'yellow' ? 'border-yellow-500 bg-yellow-50 shadow-lg' :
                          interest.color === 'blue' ? 'border-blue-500 bg-blue-50 shadow-lg' :
                          interest.color === 'purple' ? 'border-purple-500 bg-purple-50 shadow-lg' :
                          interest.color === 'pink' ? 'border-pink-500 bg-pink-50 shadow-lg' :
                          interest.color === 'green' ? 'border-green-500 bg-green-50 shadow-lg' :
                          interest.color === 'emerald' ? 'border-emerald-500 bg-emerald-50 shadow-lg' :
                          interest.color === 'indigo' ? 'border-indigo-500 bg-indigo-50 shadow-lg' :
                          interest.color === 'amber' ? 'border-amber-500 bg-amber-50 shadow-lg' :
                          'border-violet-500 bg-violet-50 shadow-lg'
                        : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                      }
                    `}
                  >
                    <div className="text-2xl mb-1">{interest.icon}</div>
                    <div className={`font-medium text-xs ${
                      formData.preferences.interests.includes(interest.value) 
                        ? interest.color === 'yellow' ? 'text-yellow-700' :
                          interest.color === 'blue' ? 'text-blue-700' :
                          interest.color === 'purple' ? 'text-purple-700' :
                          interest.color === 'pink' ? 'text-pink-700' :
                          interest.color === 'green' ? 'text-green-700' :
                          interest.color === 'emerald' ? 'text-emerald-700' :
                          interest.color === 'indigo' ? 'text-indigo-700' :
                          interest.color === 'amber' ? 'text-amber-700' :
                          'text-violet-700'
                        : 'text-gray-700'
                    }`}>
                      {interest.label}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Mobility */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                🚶 How Will You Get Around?
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'walk', label: 'Walking', icon: '🚶', color: 'green', desc: 'Explore on foot' },
                  { value: 'transit', label: 'Public Transit', icon: '🚌', color: 'blue', desc: 'Buses & trains' },
                  { value: 'drive', label: 'Driving', icon: '🚗', color: 'red', desc: 'Personal vehicle' }
                ].map(mobility => (
                  <button
                    key={mobility.value}
                    type="button"
                    onClick={() => handleInputChange({ target: { name: 'preferences.mobility', value: mobility.value }})}
                    className={`
                      p-4 rounded-xl border-2 text-center transition-all duration-300 hover:scale-105
                      ${formData.preferences.mobility === mobility.value
                        ? mobility.color === 'green' ? 'border-green-500 bg-green-50 shadow-lg' :
                          mobility.color === 'blue' ? 'border-blue-500 bg-blue-50 shadow-lg' :
                          'border-red-500 bg-red-50 shadow-lg'
                        : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                      }
                    `}
                  >
                    <div className="text-3xl mb-2">{mobility.icon}</div>
                    <div className={`font-semibold text-sm mb-1 ${
                      formData.preferences.mobility === mobility.value 
                        ? mobility.color === 'green' ? 'text-green-700' :
                          mobility.color === 'blue' ? 'text-blue-700' :
                          'text-red-700'
                        : 'text-gray-700'
                    }`}>
                      {mobility.label}
                    </div>
                    <div className="text-xs text-gray-500">{mobility.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Environment */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                🌤️ Environment Preference
              </label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'either', label: 'Either', icon: '🏞️', color: 'gray', desc: 'Indoor & outdoor' },
                  { value: 'indoor', label: 'Indoor', icon: '🏢', color: 'blue', desc: 'Museums, cafés' },
                  { value: 'outdoor', label: 'Outdoor', icon: '🌳', color: 'green', desc: 'Parks, gardens' }
                ].map(env => (
                  <button
                    key={env.value}
                    type="button"
                    onClick={() => handleInputChange({ target: { name: 'preferences.environment', value: env.value }})}
                    className={`
                      p-4 rounded-xl border-2 text-center transition-all duration-300 hover:scale-105
                      ${formData.preferences.environment === env.value
                        ? env.color === 'gray' ? 'border-gray-500 bg-gray-50 shadow-lg' :
                          env.color === 'blue' ? 'border-blue-500 bg-blue-50 shadow-lg' :
                          'border-green-500 bg-green-50 shadow-lg'
                        : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                      }
                    `}
                  >
                    <div className="text-3xl mb-2">{env.icon}</div>
                    <div className={`font-semibold text-sm mb-1 ${
                      formData.preferences.environment === env.value 
                        ? env.color === 'gray' ? 'text-gray-700' :
                          env.color === 'blue' ? 'text-blue-700' :
                          'text-green-700'
                        : 'text-gray-700'
                    }`}>
                      {env.label}
                    </div>
                    <div className="text-xs text-gray-500">{env.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Max Distance Slider */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                📍 Maximum Distance: <span className="text-yellow-600 font-bold">{formData.max_distance_miles} miles</span>
              </label>
              <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
                <div className="relative">
                  <input
                    type="range"
                    name="max_distance_miles"
                    value={formData.max_distance_miles}
                    onChange={handleInputChange}
                    min="1"
                    max="50"
                    className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                    style={{
                      background: `linear-gradient(to right, #fbbf24 0%, #fbbf24 ${(formData.max_distance_miles - 1) / 49 * 100}%, #e5e7eb ${(formData.max_distance_miles - 1) / 49 * 100}%, #e5e7eb 100%)`
                    }}
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-2">
                    <span>📍 1 mile</span>
                    <span>🚗 25 miles</span>
                    <span>🛣️ 50 miles</span>
                  </div>
                </div>
                
                <div className="mt-4 text-sm text-gray-600 text-center">
                  {formData.max_distance_miles <= 5 ? (
                    <span className="flex items-center justify-center">
                      <span className="mr-2">🚶</span>
                      Perfect for walking and exploring neighborhoods
                    </span>
                  ) : formData.max_distance_miles <= 15 ? (
                    <span className="flex items-center justify-center">
                      <span className="mr-2">🚌</span>
                      Great for public transit and city exploration
                    </span>
                  ) : formData.max_distance_miles <= 25 ? (
                    <span className="flex items-center justify-center">
                      <span className="mr-2">🚗</span>
                      Ideal for suburban attractions and day trips
                    </span>
                  ) : (
                    <span className="flex items-center justify-center">
                      <span className="mr-2">🛣️</span>
                      Extended range for regional attractions
                    </span>
                  )}
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700 disabled:from-gray-400 disabled:to-gray-500 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 disabled:hover:scale-100 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent mr-3"></div>
                  Creating Your Perfect Weekend...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <span className="mr-2">⚡</span>
                  Create My Pittsburgh Weekend
                  <span className="ml-2">🏛️</span>
                </span>
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-xl p-8 border border-gray-100">
          <div className="text-center mb-8">
            <h3 className="text-3xl font-bold text-gray-800 mb-2">Your Pittsburgh Weekend</h3>
            <p className="text-gray-600">Discover the Steel City's best experiences</p>
          </div>
          
          {loading ? (
            <div className="flex flex-col items-center justify-center py-16">
              <div className="relative mb-6">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-yellow-400 border-t-transparent"></div>
                <div className="absolute inset-0 rounded-full border-4 border-yellow-100"></div>
              </div>
              <div className="text-center">
                <h4 className="text-xl font-semibold text-gray-800 mb-2">Crafting Your Perfect Weekend</h4>
                <p className="text-gray-600 mb-4">Finding the best Pittsburgh experiences just for you...</p>
                <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
                  <span className="animate-pulse">🏛️</span>
                  <span>Museums</span>
                  <span>•</span>
                  <span className="animate-pulse">🍔</span>
                  <span>Food</span>
                  <span>•</span>
                  <span className="animate-pulse">🎭</span>
                  <span>Events</span>
                </div>
              </div>
            </div>
          ) : error ? (
            <div className="text-center py-16">
              <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl">😔</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-800 mb-2">Oops! Something went wrong</h4>
              <p className="text-red-600 mb-6 max-w-md mx-auto">{error}</p>
              <button 
                onClick={() => setError(null)} 
                className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-xl font-medium transition-colors shadow-lg"
              >
                🔄 Try Again
              </button>
            </div>
          ) : itinerary ? (
            <div className="space-y-8">
              {/* Itinerary Header */}
              <div className="bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 rounded-2xl p-6 text-white shadow-lg">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-2xl font-bold">{itinerary.title}</h4>
                  <div className="flex items-center space-x-4">
                    <button 
                      onClick={() => {
                        const url = window.location.href;
                        if (navigator.share) {
                          navigator.share({
                            title: itinerary.title,
                            text: itinerary.summary,
                            url: url
                          });
                        } else {
                          navigator.clipboard.writeText(`${itinerary.title}\n\n${itinerary.summary}\n\nView at: ${url}`);
                          alert('Itinerary details copied to clipboard!');
                        }
                      }}
                      className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-md"
                    >
                      📤 Share
                    </button>
                    <button 
                      onClick={() => window.print()}
                      className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-md"
                    >
                      🖨️ Print
                    </button>
                  </div>
                </div>
                {itinerary.summary && (
                  <p className="text-yellow-100 leading-relaxed">{itinerary.summary}</p>
                )}
                
                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-yellow-300 border-opacity-30">
                  <div className="text-center">
                    <div className="text-2xl font-bold">{itinerary.days?.length || 0}</div>
                    <div className="text-yellow-200 text-sm">Days</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">
                      {itinerary.days?.reduce((total, day) => total + (day.activities?.length || 0), 0) || 0}
                    </div>
                    <div className="text-yellow-200 text-sm">Activities</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold">
                      ${itinerary.days?.reduce((total, day) => 
                        total + (day.activities?.reduce((dayTotal, activity) => 
                          dayTotal + (activity.cost_estimate || 0), 0) || 0), 0
                      ).toFixed(0) || 0}
                    </div>
                    <div className="text-yellow-200 text-sm">Est. Cost</div>
                  </div>
                </div>
              </div>

              {/* Timeline View */}
              {itinerary.days && itinerary.days.map((day, dayIndex) => (
                <div key={dayIndex} className="relative">
                  {/* Day Header */}
                  <div className="sticky top-4 z-10 bg-white rounded-xl shadow-lg p-4 mb-6 border border-gray-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <h5 className="text-2xl font-bold text-gray-800">
                          {new Date(day.date).toLocaleDateString('en-US', { 
                            weekday: 'long', 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </h5>
                        <p className="text-gray-600">
                          {day.activities?.length || 0} activities planned
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-semibold text-gray-800">
                          ${day.activities?.reduce((total, activity) => total + (activity.cost_estimate || 0), 0).toFixed(0)}
                        </div>
                        <div className="text-sm text-gray-600">estimated cost</div>
                      </div>
                    </div>
                  </div>

                  {/* Activity Timeline */}
                  {day.activities && day.activities.length > 0 ? (
                    <div className="relative">
                      {/* Timeline Line */}
                      <div className="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-yellow-400 to-yellow-600 rounded-full"></div>
                      
                      <div className="space-y-6">
                        {day.activities.map((activity, actIndex) => (
                          <div key={actIndex} className="relative flex items-start">
                            {/* Timeline Dot */}
                            <div className="flex-shrink-0 w-16 h-16 bg-white rounded-2xl border-4 border-yellow-400 shadow-lg flex items-center justify-center z-10">
                              <span className="text-2xl">
                                {activity.category === 'food' ? '🍽️' :
                                 activity.category === 'museum' ? '🏛️' :
                                 activity.category === 'outdoor' ? '🌳' :
                                 activity.category === 'entertainment' ? '🎭' :
                                 activity.category === 'shopping' ? '🛍️' :
                                 activity.category === 'history' ? '📚' : '📍'}
                              </span>
                            </div>
                            
                            {/* Activity Card */}
                            <div className="flex-1 ml-6 bg-white rounded-2xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-shadow">
                              <div className="flex justify-between items-start mb-4">
                                <div className="flex-1">
                                  <h6 className="text-xl font-bold text-gray-800 mb-1">{activity.name}</h6>
                                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                                    <span className="bg-gray-100 px-3 py-1 rounded-full capitalize font-medium">
                                      {activity.category}
                                    </span>
                                    {activity.environment && (
                                      <span className="flex items-center">
                                        {activity.environment === 'outdoor' ? '🌞' : '🏢'} {activity.environment}
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <div className="text-right flex flex-col space-y-2">
                                  {/* Weather Info */}
                                  {activity.weather_icon && (
                                    <div className="flex items-center justify-end space-x-1">
                                      <span className="text-2xl">{activity.weather_icon}</span>
                                      {activity.weather_info?.temp_avg_f && (
                                        <span className="text-sm font-medium text-gray-700">
                                          {Math.round(activity.weather_info.temp_avg_f)}°F
                                        </span>
                                      )}
                                    </div>
                                  )}
                                  {/* Cost Estimate */}
                                  {activity.cost_estimate && (
                                    <div>
                                      <div className="text-2xl font-bold text-green-600">
                                        ${Math.round(activity.cost_estimate)}
                                      </div>
                                      <div className="text-xs text-gray-500">estimated</div>
                                    </div>
                                  )}
                                </div>
                              </div>
                              
                              {activity.address && (
                                <div className="flex items-center text-sm text-gray-600 mb-3">
                                  <span className="mr-2">📍</span>
                                  <span>{activity.address}</span>
                                  {activity.distance_miles && (
                                    <span className="ml-4 bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs">
                                      {activity.distance_miles.toFixed(1)} miles
                                    </span>
                                  )}
                                </div>
                              )}
                              
                              {activity.start_time && (
                                <div className="flex items-center text-sm text-blue-600 font-medium mb-3">
                                  <span className="mr-2">🕒</span>
                                  <span>
                                    {activity.start_time}
                                    {activity.end_time && ` - ${activity.end_time}`}
                                    {activity.travel_time_minutes && (
                                      <span className="ml-4 text-gray-500">
                                        ({activity.travel_time_minutes}min travel)
                                      </span>
                                    )}
                                  </span>
                                </div>
                              )}
                              
                              {/* Weather Details */}
                              {activity.weather_info && (
                                <div className="flex items-center text-sm text-gray-600 mb-3">
                                  <span className="mr-2">{activity.weather_icon || '🌤️'}</span>
                                  <span>
                                    {activity.weather_info.temp_avg_f && `${Math.round(activity.weather_info.temp_avg_f)}°F`}
                                    {activity.weather_info.precip_prob_avg && activity.weather_info.precip_prob_avg > 0.1 && (
                                      <span className="ml-2 text-blue-600">
                                        {Math.round(activity.weather_info.precip_prob_avg * 100)}% chance of rain
                                      </span>
                                    )}
                                    {activity.weather_info.suitability && (
                                      <span className={`ml-4 px-2 py-1 rounded-full text-xs ${
                                        activity.weather_info.suitability > 0.7 ? 'bg-green-100 text-green-700' :
                                        activity.weather_info.suitability > 0.4 ? 'bg-yellow-100 text-yellow-700' :
                                        'bg-red-100 text-red-700'
                                      }`}>
                                        {activity.weather_info.suitability > 0.7 ? 'Great weather' :
                                         activity.weather_info.suitability > 0.4 ? 'Fair weather' :
                                         'Poor weather'}
                                      </span>
                                    )}
                                  </span>
                                </div>
                              )}
                              
                              {activity.notes && (
                                <p className="text-gray-700 leading-relaxed bg-gray-50 p-3 rounded-lg">
                                  {activity.notes}
                                </p>
                              )}
                              
                              {activity.external_url && (
                                <div className="mt-4">
                                  <a 
                                    href={activity.external_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="inline-flex items-center text-yellow-600 hover:text-yellow-700 font-medium group"
                                  >
                                    Learn More
                                    <span className="ml-1 transform group-hover:translate-x-1 transition-transform">→</span>
                                  </a>
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-16 bg-gray-50 rounded-2xl">
                      <span className="text-6xl mb-4 block">📅</span>
                      <p className="text-gray-500 text-lg">No activities planned for this day</p>
                    </div>
                  )}
                </div>
              ))}

              {/* Warnings */}
              {itinerary.warnings && itinerary.warnings.length > 0 && (
                <div className="bg-amber-50 border-2 border-amber-200 rounded-2xl p-6">
                  <div className="flex items-center mb-4">
                    <span className="text-2xl mr-3">⚠️</span>
                    <h6 className="font-bold text-amber-800 text-lg">Important Notes</h6>
                  </div>
                  <ul className="space-y-2">
                    {itinerary.warnings.map((warning, index) => (
                      <li key={index} className="flex items-start">
                        <span className="text-amber-600 mr-2 mt-1">•</span>
                        <span className="text-amber-700">{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              
              {/* Source Attribution */}
              {itinerary.sources && Object.keys(itinerary.sources).length > 0 && (
                <div className="bg-gray-100 rounded-2xl p-6">
                  <h6 className="font-semibold text-gray-800 mb-4 flex items-center">
                    <span className="mr-2">📊</span>
                    Data Sources
                  </h6>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(itinerary.sources).map(([source, count]) => (
                      <div key={source} className="text-center">
                        <div className="text-xl font-bold text-gray-700">{count}</div>
                        <div className="text-sm text-gray-600 capitalize">{source}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl">🏛️</span>
              </div>
              <h4 className="text-2xl font-bold text-gray-800 mb-4">Ready to Explore Pittsburgh?</h4>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Fill out your preferences and let's create the perfect Steel City weekend adventure for you!
              </p>
              <div className="flex items-center justify-center space-x-6 text-sm text-gray-500">
                <span className="flex items-center"><span className="mr-2">🍔</span>Food</span>
                <span className="flex items-center"><span className="mr-2">🏛️</span>Museums</span>
                <span className="flex items-center"><span className="mr-2">🎭</span>Events</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ItineraryPlanner;