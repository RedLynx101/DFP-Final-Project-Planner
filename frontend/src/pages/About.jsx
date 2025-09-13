const About = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">About Pittsburgh Weekend Planner</h2>
        
        <div className="prose prose-lg">
          <p className="text-gray-700 mb-6">
            The Pittsburgh Weekend Planner is an intelligent itinerary planning application designed to help 
            visitors and locals discover the best that the Steel City has to offer. Whether you're interested 
            in world-class museums, delicious food, outdoor activities, or cultural events, our planner creates 
            personalized recommendations based on your preferences.
          </p>

          <h3 className="text-2xl font-semibold text-gray-800 mb-4">Features</h3>
          <ul className="list-disc list-inside text-gray-700 mb-6 space-y-2">
            <li>Personalized itinerary generation based on your interests and budget</li>
            <li>Real-time events and activities from multiple sources</li>
            <li>Restaurant and food recommendations via Yelp integration</li>
            <li>Transportation options including walking, transit, and driving directions</li>
            <li>Distance and travel time calculations from your starting location</li>
            <li>Indoor and outdoor activity filtering based on weather preferences</li>
          </ul>

          <h3 className="text-2xl font-semibold text-gray-800 mb-4">How It Works</h3>
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">1️⃣</span>
              </div>
              <h4 className="font-semibold mb-2">Set Your Preferences</h4>
              <p className="text-sm text-gray-600">
                Tell us about your interests, budget, mobility preferences, and desired dates.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">2️⃣</span>
              </div>
              <h4 className="font-semibold mb-2">AI-Powered Planning</h4>
              <p className="text-sm text-gray-600">
                Our intelligent system analyzes available activities and creates optimized itineraries.
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">3️⃣</span>
              </div>
              <h4 className="font-semibold mb-2">Enjoy Your Weekend</h4>
              <p className="text-sm text-gray-600">
                Follow your personalized itinerary with detailed information and directions.
              </p>
            </div>
          </div>

          <h3 className="text-2xl font-semibold text-gray-800 mb-4">Data Sources</h3>
          <p className="text-gray-700 mb-4">
            Our recommendations are powered by multiple trusted sources:
          </p>
          <ul className="list-disc list-inside text-gray-700 mb-6 space-y-1">
            <li><strong>Visit Pittsburgh:</strong> Official events and attractions</li>
            <li><strong>Yelp:</strong> Restaurant recommendations and reviews</li>
            <li><strong>Ticketmaster:</strong> Concerts and entertainment events</li>
            <li><strong>Google Maps:</strong> Locations, distances, and travel times</li>
            <li><strong>Weather Services:</strong> Current conditions for activity planning</li>
          </ul>

          <h3 className="text-2xl font-semibold text-gray-800 mb-4">Team</h3>
          <p className="text-gray-700 mb-6">
            The Pittsburgh Weekend Planner was developed by the Purple Turtles team: Gwen Li, Aadya Agarwal, 
            Emma Peng, and Noah Hicks. This project combines AI-powered planning with real-time data to 
            create the ultimate Pittsburgh experience.
          </p>

          <div className="bg-blue-50 p-6 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Ready to Explore Pittsburgh?</h4>
            <p className="text-blue-700 mb-4">
              Start planning your perfect Pittsburgh weekend with our intelligent itinerary planner.
            </p>
            <a 
              href="/planner" 
              className="inline-block bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Plan Your Itinerary
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;