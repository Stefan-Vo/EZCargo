import React, { useState } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, getDay } from 'date-fns';
import Layout from './dashboard'; 

const Calendar = () => {
    const [currentDate, setCurrentDate] = useState(new Date());
    const [events, setEvents] = useState([]);
    const [newEvent, setNewEvent] = useState({ title: '', date: '', time: '' });
  
    // Get days in current month
    const monthStart = startOfMonth(currentDate);
    const monthEnd = endOfMonth(currentDate);
    const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });
  
    // Get the day of week for the first day (0 = Sunday, 6 = Saturday)
    const startDay = getDay(monthStart);
  
    // Create blank days for proper calendar alignment
    const blanks = Array(startDay).fill(null);
    const totalSlots = [...blanks, ...daysInMonth];
  
    // Month navigation handlers
    const handlePrevMonth = () => {
      setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
    };
  
    const handleNextMonth = () => {
      setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
    };
  
    // Event handling
    const handleAddEvent = (e) => {
      e.preventDefault();
      if (newEvent.title && newEvent.date && newEvent.time) {
        setEvents([...events, newEvent]);
        setNewEvent({ title: '', date: '', time: '' });
      } else {
        alert('Please fill in all fields');
      }
    };

  return (
    <Layout>
      <div className="bg-gray-900 flex flex-col items-center py-8 h-screen w-screen">
        <div className="w-full max-w-[95%] mx-auto bg-slate-800 rounded-lg shadow-lg p-6">
          {/* Calendar Header */}
          <div className="flex justify-between items-center mb-6">
            <button
              onClick={handlePrevMonth}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Previous
            </button>
            <h2 className="text-2xl font-bold text-gray-800">
              {format(currentDate, 'MMMM yyyy')}
            </h2>
            <button
              onClick={handleNextMonth}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Next
            </button>
          </div>

          {/* Calendar Grid */}
          <div className="grid grid-cols-7 gap-2 mb-6">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center font-bold py-2 bg-gray-300">
                {day}
              </div>
            ))}
            {totalSlots.map((date, index) => (
              <div
                key={index}
                className={`min-h-[120px] p-2 border ${
                  date ? 'bg-gray-500' : 'bg-gray-50'
                } hover:bg-gray-50`}
              >
                {date && (
                  <>
                    <div className="font-semibold">{format(date, 'd')}</div>
                    <div className="overflow-y-auto max-h-[80px]">
                      {events
                        .filter(event => event.date === format(date, 'yyyy-MM-dd'))
                        .map((event, eventIndex) => (
                          <div
                            key={eventIndex}
                            className="text-sm p-1 mt-1 bg-blue-100 rounded"
                          >
                            {event.title} - {event.time}
                          </div>
                        ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>

          {/* Add Event Form */}
          <div className="mt-6 p-4 bg-slate-800 rounded-lg">
            <h3 className="text-lg font-semibold mb-4 text-white">Add New Event</h3>
            <form onSubmit={handleAddEvent} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input
                  type="text"
                  placeholder="Event Title"
                  value={newEvent.title}
                  onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                  className="w-full p-2 border rounded "
                />
                <input
                  type="date"
                  value={newEvent.date}
                  onChange={(e) => setNewEvent({ ...newEvent, date: e.target.value })}
                  className="w-full p-2 border rounded"
                />
                <input
                  type="time"
                  value={newEvent.time}
                  onChange={(e) => setNewEvent({ ...newEvent, time: e.target.value })}
                  className="w-full p-2 border rounded"
                />
              </div>
              <button
                type="submit"
                className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Add Event
              </button>
            </form>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Calendar;