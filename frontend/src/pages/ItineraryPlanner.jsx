import { useState } from 'react';
import { apiService } from '../services/api';

const ItineraryPlanner = () => {
  const [formData, setFormData] = useState({
    city: 'Pittsburgh, PA',
    start_date: '',
    end_date: '',
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

  // Set default dates to upcoming weekend
  useState(() => {
    const now = new Date();
    const daysUntilSat = (6 - now.getDay()) % 7;
    const saturday = new Date(now);
    saturday.setDate(now.getDate() + daysUntilSat);
    saturday.setHours(9, 0, 0, 0);
    
    const sunday = new Date(saturday);
    sunday.setDate(saturday.getDate() + 1);
    sunday.setHours(21, 0, 0, 0);

    setFormData(prev => ({
      ...prev,
      start_date: saturday.toISOString().slice(0, 16),
      end_date: sunday.toISOString().slice(0, 16)
    }));
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

            {/* Date Range */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Date & Time
                </label>
                <input
                  type="datetime-local"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Date & Time
                </label>
                <input
                  type="datetime-local"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>

            {/* Budget Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Budget Level
              </label>
              <select
                name="preferences.budget_level"
                value={formData.preferences.budget_level}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="low">Low Budget</option>
                <option value="medium">Medium Budget</option>
                <option value="high">High Budget</option>
              </select>
            </div>

            {/* Interests */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Interests (select multiple)
              </label>
              <div className="grid grid-cols-3 gap-2">
                {availableInterests.map(interest => (
                  <label key={interest} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.preferences.interests.includes(interest)}
                      onChange={() => handleInterestsChange(interest)}
                      className="mr-2"
                    />
                    <span className="text-sm capitalize">{interest}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Mobility */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preferred Transportation
              </label>
              <select
                name="preferences.mobility"
                value={formData.preferences.mobility}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="walk">Walking</option>
                <option value="transit">Public Transit</option>
                <option value="drive">Driving</option>
              </select>
            </div>

            {/* Environment */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Environment Preference
              </label>
              <select
                name="preferences.environment"
                value={formData.preferences.environment}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="either">Either Indoor/Outdoor</option>
                <option value="indoor">Indoor Activities</option>
                <option value="outdoor">Outdoor Activities</option>
              </select>
            </div>

            {/* Max Distance */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Distance (miles)
              </label>
              <input
                type="number"
                name="max_distance_miles"
                value={formData.max_distance_miles}
                onChange={handleInputChange}
                min="1"
                max="50"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {loading ? 'Creating Itinerary...' : 'Create Itinerary'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-6">Your Itinerary</h3>
          
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Creating your itinerary...</span>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-600 mb-4">{error}</p>
              <button 
                onClick={() => setError(null)} 
                className="text-blue-600 hover:text-blue-800"
              >
                Try Again
              </button>
            </div>
          ) : itinerary ? (
            <div className="space-y-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-lg">{itinerary.title}</h4>
                {itinerary.summary && (
                  <p className="text-gray-700 mt-2">{itinerary.summary}</p>
                )}
              </div>

              {itinerary.days && itinerary.days.map((day, dayIndex) => (
                <div key={dayIndex} className="border-l-4 border-blue-500 pl-4">
                  <h5 className="font-semibold text-lg mb-3">
                    {new Date(day.date).toLocaleDateString('en-US', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </h5>
                  
                  {day.activities && day.activities.length > 0 ? (
                    <div className="space-y-3">
                      {day.activities.map((activity, actIndex) => (
                        <div key={actIndex} className="bg-gray-50 p-3 rounded-md">
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <h6 className="font-medium">{activity.name}</h6>
                              <p className="text-sm text-gray-600">{activity.category}</p>
                              {activity.address && (
                                <p className="text-sm text-gray-500">{activity.address}</p>
                              )}
                              {activity.notes && (
                                <p className="text-sm text-gray-700 mt-1">{activity.notes}</p>
                              )}
                            </div>
                            {activity.cost_estimate && (
                              <span className="text-sm text-green-600 font-medium">
                                ${activity.cost_estimate}
                              </span>
                            )}
                          </div>
                          {activity.start_time && (
                            <p className="text-sm text-blue-600 mt-1">
                              {activity.start_time} {activity.end_time && `- ${activity.end_time}`}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 italic">No activities planned for this day.</p>
                  )}
                </div>
              ))}

              {itinerary.warnings && itinerary.warnings.length > 0 && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                  <h6 className="font-medium text-yellow-800 mb-2">Warnings:</h6>
                  <ul className="list-disc list-inside text-sm text-yellow-700">
                    {itinerary.warnings.map((warning, index) => (
                      <li key={index}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <p>Fill out the form and click "Create Itinerary" to get started!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ItineraryPlanner;