import { Link, useLocation } from 'react-router-dom';
import logo from '../assets/logo.png';

const Header = ({ isBackendHealthy }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        {/* Main Header Row */}
        <div className="flex justify-between items-center py-3 sm:py-4">
          {/* Logo and Title - Mobile Optimized */}
          <Link to="/" className="flex items-center space-x-2 sm:space-x-3 hover:opacity-80 transition-opacity group">
            <img 
              src={logo} 
              alt="Pittsburgh Weekend Planner Logo" 
              className="w-8 h-8 sm:w-10 sm:h-10 rounded-lg object-cover shadow-sm group-hover:shadow-md transition-shadow"
            />
            <div className="min-w-0">
              <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-800 truncate leading-tight">
                Pittsburgh Weekend Planner
              </h1>
              <p className="text-xs sm:text-sm text-gray-600 leading-tight hidden sm:block">
                Discover the Steel City
              </p>
              {/* Mobile tagline */}
              <p className="text-xs text-gray-500 leading-tight sm:hidden">
                Steel City Adventures
              </p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-6">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive('/') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-700 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              🏠 Home
            </Link>
            <Link
              to="/planner"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive('/planner') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-700 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              📅 Plan Itinerary
            </Link>
            <Link
              to="/events"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive('/events') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-700 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              🎭 Events
            </Link>
            <Link
              to="/about"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                isActive('/about') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-700 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              ℹ️ About
            </Link>
          </nav>

          {/* Status & Mobile Menu Button */}
          <div className="flex items-center space-x-3">
            {/* Backend Status - Improved Mobile */}
            <div className="flex items-center space-x-1 sm:space-x-2">
              <div className={`w-2 h-2 sm:w-3 sm:h-3 rounded-full ${isBackendHealthy ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
              <span className="text-xs sm:text-sm text-gray-600 font-medium">
                <span className="hidden sm:inline">
                  {isBackendHealthy ? 'API Connected' : 'API Offline'}
                </span>
                <span className="sm:hidden">
                  {isBackendHealthy ? '✓' : '✗'}
                </span>
              </span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation - Enhanced */}
        <div className="lg:hidden border-t border-gray-100">
          <nav className="flex items-center justify-center py-3 space-x-1">
            <Link
              to="/"
              className={`flex-1 flex flex-col items-center px-2 py-3 rounded-lg text-xs font-medium transition-all duration-200 ${
                isActive('/') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              <span className="text-lg mb-1">🏠</span>
              <span>Home</span>
            </Link>
            <Link
              to="/planner"
              className={`flex-1 flex flex-col items-center px-2 py-3 rounded-lg text-xs font-medium transition-all duration-200 ${
                isActive('/planner') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              <span className="text-lg mb-1">📅</span>
              <span>Plan</span>
            </Link>
            <Link
              to="/events"
              className={`flex-1 flex flex-col items-center px-2 py-3 rounded-lg text-xs font-medium transition-all duration-200 ${
                isActive('/events') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              <span className="text-lg mb-1">🎭</span>
              <span>Events</span>
            </Link>
            <Link
              to="/about"
              className={`flex-1 flex flex-col items-center px-2 py-3 rounded-lg text-xs font-medium transition-all duration-200 ${
                isActive('/about') 
                  ? 'bg-yellow-100 text-yellow-800 shadow-sm' 
                  : 'text-gray-600 hover:text-yellow-600 hover:bg-yellow-50'
              }`}
            >
              <span className="text-lg mb-1">ℹ️</span>
              <span>About</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;