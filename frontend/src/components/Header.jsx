import { Link, useLocation } from 'react-router-dom';
import logo from '../assets/logo.png';

const Header = ({ isBackendHealthy }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <img 
              src={logo} 
              alt="Pittsburgh Weekend Planner Logo" 
              className="w-10 h-10 rounded-lg object-cover"
            />
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Pittsburgh Weekend Planner</h1>
              <p className="text-sm text-gray-600">Discover the Steel City</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              Home
            </Link>
            <Link
              to="/planner"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/planner') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              Plan Itinerary
            </Link>
            <Link
              to="/about"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive('/about') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
              }`}
            >
              About
            </Link>
          </nav>

          {/* Backend Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isBackendHealthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isBackendHealthy ? 'API Connected' : 'API Offline'}
            </span>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden pb-4">
          <nav className="flex space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/') ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
              }`}
            >
              Home
            </Link>
            <Link
              to="/planner"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/planner') ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
              }`}
            >
              Plan
            </Link>
            <Link
              to="/about"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/about') ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
              }`}
            >
              About
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;