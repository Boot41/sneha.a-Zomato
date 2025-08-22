import React, { useState } from 'react';
import { Link } from 'react-router-dom';

// Sample food items data
const foodItems = [
  {
    id: 1,
    name: 'Butter Chicken',
    image: 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400&h=300&fit=crop&crop=center',
    rating: 4.5,
    time: '30 min',
    price: '₹250',
    restaurant: 'Punjabi Dhaba'
  },
  {
    id: 2,
    name: 'Paneer Tikka',
    image: 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop&crop=center',
    rating: 4.3,
    time: '25 min',
    price: '₹180',
    restaurant: 'Tandoori Nights'
  },
  {
    id: 3,
    name: 'Masala Dosa',
    image: 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400&h=300&fit=crop&crop=center',
    rating: 4.7,
    time: '20 min',
    price: '₹120',
    restaurant: 'Udupi Grand'
  },
  {
    id: 4,
    name: 'Biryani',
    image: 'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop&crop=center',
    rating: 4.6,
    time: '35 min',
    price: '₹280',
    restaurant: 'Paradise'
  },
  {
    id: 5,
    name: 'Chole Bhature',
    image: 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400&h=300&fit=crop&crop=center',
    rating: 4.4,
    time: '25 min',
    price: '₹150',
    restaurant: 'Haldiram'
  },
  {
    id: 6,
    name: 'Pizza Margherita',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop&crop=center',
    rating: 4.2,
    time: '30 min',
    price: '₹320',
    restaurant: 'Oven Story'
  }
];

const Landing: React.FC = () => {
  const [hoveredItem, setHoveredItem] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <svg className="h-8 w-auto" viewBox="0 0 200 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <text x="10" y="28" fontFamily="Arial, sans-serif" fontSize="24" fontWeight="bold" fill="#e23744">
                  Zomato
                </text>
              </svg>
            </div>
            <div className="flex space-x-4">
              <Link to="/login" className="btn-secondary">
                Login
              </Link>
              <Link to="/register" className="btn-primary">
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative bg-red-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Discover the best food & drinks
          </h1>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Order from your favorite restaurants and get food delivered to your doorstep
          </p>
        </div>
      </div>

      {/* Food Items Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Popular dishes around you
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {foodItems.map((item) => (
            <div 
              key={item.id}
              className="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 transform hover:-translate-y-2 hover:shadow-xl cursor-pointer"
              onMouseEnter={() => setHoveredItem(item.id)}
              onMouseLeave={() => setHoveredItem(null)}
            >
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={item.image} 
                  alt={item.name}
                  className={`w-full h-full object-cover transition-transform duration-500 ${hoveredItem === item.id ? 'scale-110' : ''}`}
                />
                <div className="absolute top-3 right-3 bg-white bg-opacity-90 px-2 py-1 rounded-full text-sm font-semibold text-gray-800 flex items-center">
                  <span>⭐ {item.rating}</span>
                </div>
              </div>
              <div className="p-4">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-semibold text-gray-900">{item.name}</h3>
                  <span className="text-red-600 font-bold">{item.price}</span>
                </div>
                <p className="text-gray-600 text-sm mt-1">{item.restaurant}</p>
                <div className="flex items-center mt-2 text-sm text-gray-500">
                  <span>{item.time}</span>
                  <span className="mx-2">•</span>
                  <span>⭐ {item.rating}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Why Choose Us
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">Fast Delivery</h3>
            <p className="text-gray-600">Get your food delivered in 30 minutes or less</p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">Quality Food</h3>
            <p className="text-gray-600">Fresh ingredients from the best restaurants</p>
          </div>
          
          <div className="text-center p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow">
            <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">Easy Payment</h3>
            <p className="text-gray-600">Pay online or cash on delivery</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
