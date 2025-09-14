import { useState, useEffect } from 'react';

const DatePicker = ({ startDate, endDate, onDateChange, className = "" }) => {
  const [selectedStartDate, setSelectedStartDate] = useState(startDate);
  const [selectedEndDate, setSelectedEndDate] = useState(endDate);
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectMode, setSelectMode] = useState('start'); // 'start' or 'end'

  useEffect(() => {
    setSelectedStartDate(startDate);
    setSelectedEndDate(endDate);
  }, [startDate, endDate]);

  // Calculate upcoming weekend as default
  const getUpcomingWeekend = () => {
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 = Sunday, 6 = Saturday
    const daysUntilSaturday = dayOfWeek === 6 ? 0 : (6 - dayOfWeek) % 7;
    
    const saturday = new Date(today);
    saturday.setDate(today.getDate() + daysUntilSaturday);
    saturday.setHours(10, 0, 0, 0);
    
    const sunday = new Date(saturday);
    sunday.setDate(saturday.getDate() + 1);
    sunday.setHours(22, 0, 0, 0);
    
    return { saturday, sunday };
  };

  const formatDateForInput = (date) => {
    if (!date) return '';
    return date.toISOString().slice(0, 16);
  };

  const handleDateClick = (date) => {
    const clickedDate = new Date(date);
    
    if (selectMode === 'start') {
      // Set start date with 10 AM default
      clickedDate.setHours(10, 0, 0, 0);
      setSelectedStartDate(clickedDate);
      setSelectMode('end');
      onDateChange(formatDateForInput(clickedDate), selectedEndDate ? formatDateForInput(selectedEndDate) : '');
    } else {
      // Set end date with 10 PM default  
      clickedDate.setHours(22, 0, 0, 0);
      setSelectedEndDate(clickedDate);
      setSelectMode('start');
      onDateChange(selectedStartDate ? formatDateForInput(selectedStartDate) : '', formatDateForInput(clickedDate));
    }
  };

  const handleManualDateChange = (field, value) => {
    if (field === 'start') {
      const newDate = value ? new Date(value) : null;
      setSelectedStartDate(newDate);
      onDateChange(value, selectedEndDate ? formatDateForInput(selectedEndDate) : '');
    } else {
      const newDate = value ? new Date(value) : null;
      setSelectedEndDate(newDate);
      onDateChange(selectedStartDate ? formatDateForInput(selectedStartDate) : '', value);
    }
  };

  const handleQuickSelect = (type) => {
    const weekend = getUpcomingWeekend();
    let start, end;
    
    switch (type) {
      case 'this-weekend':
        start = weekend.saturday;
        end = weekend.sunday;
        break;
      case 'next-weekend':
        start = new Date(weekend.saturday);
        start.setDate(start.getDate() + 7);
        end = new Date(weekend.sunday);
        end.setDate(end.getDate() + 7);
        break;
      case 'friday-night':
        start = new Date(weekend.saturday);
        start.setDate(start.getDate() - 1);
        start.setHours(18, 0, 0, 0);
        end = weekend.sunday;
        break;
      default:
        return;
    }
    
    setSelectedStartDate(start);
    setSelectedEndDate(end);
    setIsSelectingEnd(false);
    onDateChange(formatDateForInput(start), formatDateForInput(end));
  };

  const generateCalendarDays = () => {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    const days = [];
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    for (let i = 0; i < 42; i++) { // 6 weeks * 7 days
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      
      const isCurrentMonth = date.getMonth() === month;
      const isToday = date.getTime() === today.getTime();
      const isWeekend = date.getDay() === 0 || date.getDay() === 6;
      const isPast = date < today;
      const isSelected = (selectedStartDate && date.getTime() === new Date(selectedStartDate).setHours(0, 0, 0, 0)) ||
                        (selectedEndDate && date.getTime() === new Date(selectedEndDate).setHours(0, 0, 0, 0));
      const isInRange = selectedStartDate && selectedEndDate &&
                       date >= new Date(selectedStartDate).setHours(0, 0, 0, 0) &&
                       date <= new Date(selectedEndDate).setHours(0, 0, 0, 0);
      
      days.push({
        date,
        day: date.getDate(),
        isCurrentMonth,
        isToday,
        isWeekend,
        isPast,
        isSelected,
        isInRange
      });
    }
    
    return days;
  };

  const navigateMonth = (direction) => {
    const newMonth = new Date(currentMonth);
    newMonth.setMonth(currentMonth.getMonth() + direction);
    setCurrentMonth(newMonth);
  };

  const calendarDays = generateCalendarDays();
  const monthYear = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  return (
    <div className={`bg-white rounded-xl shadow-lg border border-gray-200 p-6 ${className}`}>
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-800 mb-2">Select Your Dates</h3>
        <p className="text-sm text-gray-600">
          {selectMode === 'start' ? 'Choose your start date' : 'Now choose your end date'}
        </p>
      </div>

      {/* Manual Date Input Fields */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📅 Start Date & Time
          </label>
          <input
            type="datetime-local"
            value={selectedStartDate ? formatDateForInput(selectedStartDate) : ''}
            onChange={(e) => handleManualDateChange('start', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📅 End Date & Time
          </label>
          <input
            type="datetime-local"
            value={selectedEndDate ? formatDateForInput(selectedEndDate) : ''}
            onChange={(e) => handleManualDateChange('end', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Quick Select Buttons */}
      <div className="grid grid-cols-3 gap-2 mb-6">
        <button
          onClick={() => handleQuickSelect('this-weekend')}
          className="bg-yellow-100 hover:bg-yellow-200 text-yellow-800 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          🗓️ This Weekend
        </button>
        <button
          onClick={() => handleQuickSelect('next-weekend')}
          className="bg-blue-100 hover:bg-blue-200 text-blue-800 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          📅 Next Weekend
        </button>
        <button
          onClick={() => handleQuickSelect('friday-night')}
          className="bg-purple-100 hover:bg-purple-200 text-purple-800 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          🌙 Friday Night
        </button>
      </div>

      {/* Calendar Header */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={() => navigateMonth(-1)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <span className="text-gray-600">←</span>
        </button>
        <h4 className="text-lg font-semibold text-gray-800">{monthYear}</h4>
        <button
          onClick={() => navigateMonth(1)}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <span className="text-gray-600">→</span>
        </button>
      </div>

      {/* Day Labels */}
      <div className="grid grid-cols-7 gap-1 mb-2">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="text-center text-xs font-medium text-gray-500 py-2">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-1">
        {calendarDays.map((dayInfo, index) => (
          <button
            key={index}
            onClick={() => !dayInfo.isPast && dayInfo.isCurrentMonth && handleDateClick(dayInfo.date)}
            disabled={dayInfo.isPast}
            className={`
              relative h-10 text-sm rounded-lg transition-all duration-200 
              ${dayInfo.isCurrentMonth ? 'text-gray-800' : 'text-gray-300'}
              ${dayInfo.isPast ? 'cursor-not-allowed opacity-40' : 'hover:bg-gray-100'}
              ${dayInfo.isToday ? 'ring-2 ring-yellow-400 font-bold' : ''}
              ${dayInfo.isWeekend && dayInfo.isCurrentMonth && !dayInfo.isPast ? 'bg-yellow-50 text-yellow-700' : ''}
              ${dayInfo.isSelected ? 'bg-yellow-400 text-white font-bold' : ''}
              ${dayInfo.isInRange && !dayInfo.isSelected ? 'bg-yellow-100 text-yellow-800' : ''}
            `}
          >
            {dayInfo.day}
            {dayInfo.isWeekend && dayInfo.isCurrentMonth && !dayInfo.isPast && (
              <div className="absolute top-0 right-0 w-2 h-2 bg-yellow-400 rounded-full"></div>
            )}
          </button>
        ))}
      </div>

      {/* Selected Dates Display */}
      {(selectedStartDate || selectedEndDate) && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <div className="text-sm text-gray-600 mb-2">Selected Dates:</div>
          <div className="space-y-2">
            {selectedStartDate && (
              <div className="flex items-center text-sm">
                <span className="text-green-600 mr-2">📅</span>
                <span className="font-medium">Start:</span>
                <span className="ml-2 text-gray-800">
                  {selectedStartDate.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    month: 'long', 
                    day: 'numeric',
                    hour: 'numeric',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            )}
            {selectedEndDate && (
              <div className="flex items-center text-sm">
                <span className="text-red-600 mr-2">📅</span>
                <span className="font-medium">End:</span>
                <span className="ml-2 text-gray-800">
                  {selectedEndDate.toLocaleDateString('en-US', { 
                    weekday: 'long', 
                    month: 'long', 
                    day: 'numeric',
                    hour: 'numeric',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DatePicker;