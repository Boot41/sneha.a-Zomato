import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { menuAPI, restaurantsAPI, API_BASE_URL } from '../api';

interface MenuItem {
  id: number;
  name: string;
  price: number;
  category?: string;
  image?: string;
  created_at: string;
}

interface Restaurant {
  id: number;
  name: string;
  address: string;
  cuisine_type?: string;
}

const Menu: React.FC = () => {
  const { restaurantId } = useParams<{ restaurantId: string }>();
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [cart, setCart] = useState<{ [key: number]: number }>({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }
    
    if (restaurantId) {
      fetchRestaurantData(parseInt(restaurantId));
      fetchMenu(parseInt(restaurantId));
    }
  }, [restaurantId, navigate]);

  const fetchRestaurantData = async (id: number) => {
    try {
      const response = await restaurantsAPI.getById(id);
      setRestaurant(response.data);
    } catch (error) {
      console.error('Failed to fetch restaurant:', error);
    }
  };

  const fetchMenu = async (id: number) => {
    try {
      const response = await menuAPI.getByRestaurant(id);
      setMenuItems(response.data);
    } catch (error) {
      console.error('Failed to fetch menu:', error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (itemId: number) => {
    setCart(prev => ({
      ...prev,
      [itemId]: (prev[itemId] || 0) + 1
    }));
  };

  const removeFromCart = (itemId: number) => {
    setCart(prev => {
      const newCart = { ...prev };
      if (newCart[itemId] > 1) {
        newCart[itemId]--;
      } else {
        delete newCart[itemId];
      }
      return newCart;
    });
  };

  const getTotalPrice = () => {
    return Object.entries(cart).reduce((total, [itemId, quantity]) => {
      const item = menuItems.find(item => item.id === parseInt(itemId));
      return total + (item ? item.price * quantity : 0);
    }, 0);
  };

  const getTotalItems = () => {
    return Object.values(cart).reduce((total, quantity) => total + quantity, 0);
  };

  const groupedItems = menuItems.reduce((groups, item) => {
    const category = item.category || 'Other';
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(item);
    return groups;
  }, {} as { [key: string]: MenuItem[] });

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading menu...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/restaurants" className="text-2xl font-bold text-red-600">
              Zomato Clone
            </Link>
            <div className="flex items-center space-x-4">
              <Link to="/restaurants" className="text-gray-600 hover:text-gray-900">← Back to Restaurants</Link>
              <Link to="/dashboard" className="btn-secondary">Dashboard</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Restaurant Header */}
        {restaurant && (
          <div className="card mb-8">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{restaurant.name}</h1>
                <p className="text-gray-600 mb-2">{restaurant.address}</p>
                {restaurant.cuisine_type && (
                  <span className="inline-flex px-3 py-1 text-sm font-semibold bg-red-100 text-red-800 rounded-full">
                    {restaurant.cuisine_type}
                  </span>
                )}
              </div>
              <div className="text-right">
                <div className="flex items-center text-yellow-500 mb-2">
                  <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span>4.2 (120+ reviews)</span>
                </div>
                <p className="text-sm text-gray-600">30-45 min delivery</p>
              </div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Menu Items */}
          <div className="lg:col-span-3">
            {Object.entries(groupedItems).map(([category, items]) => (
              <div key={category} className="mb-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">{category}</h2>
                <div className="space-y-4">
                  {items.map((item) => (
                    <div key={item.id} className="card hover:shadow-lg transition-shadow">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.name}</h3>
                          <p className="text-xl font-bold text-red-600 mb-3">${item.price.toFixed(2)}</p>
                          <p className="text-gray-600 text-sm">Delicious {item.name.toLowerCase()} prepared with fresh ingredients</p>
                        </div>
                        
                        <div className="ml-4 flex-shrink-0">
                          <div className="w-24 h-24 bg-gray-200 rounded-lg mb-3 overflow-hidden">
                            {item.image ? (
                              <img 
                                src={`${API_BASE_URL}${item.image}`} 
                                alt={item.name}
                                className="w-full h-full object-cover"
                                onError={(e) => {
                                  e.currentTarget.style.display = 'none';
                                  const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                                  if (fallback) fallback.style.display = 'flex';
                                }}
                              />
                            ) : null}
                            <div className={`w-full h-full flex items-center justify-center ${item.image ? 'hidden' : ''}`}>
                              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                              </svg>
                            </div>
                          </div>
                          
                          {cart[item.id] ? (
                            <div className="flex items-center justify-between bg-red-600 text-white rounded-lg px-3 py-2">
                              <button
                                onClick={() => removeFromCart(item.id)}
                                className="text-white hover:text-gray-200"
                              >
                                −
                              </button>
                              <span className="mx-3 font-semibold">{cart[item.id]}</span>
                              <button
                                onClick={() => addToCart(item.id)}
                                className="text-white hover:text-gray-200"
                              >
                                +
                              </button>
                            </div>
                          ) : (
                            <button
                              onClick={() => addToCart(item.id)}
                              className="w-full btn-primary text-sm"
                            >
                              Add
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Cart Sidebar */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Order</h3>
              
              {getTotalItems() > 0 ? (
                <>
                  <div className="space-y-3 mb-4">
                    {Object.entries(cart).map(([itemId, quantity]) => {
                      const item = menuItems.find(item => item.id === parseInt(itemId));
                      if (!item) return null;
                      
                      return (
                        <div key={itemId} className="flex justify-between items-center">
                          <div>
                            <p className="font-medium text-sm">{item.name}</p>
                            <p className="text-xs text-gray-600">${item.price.toFixed(2)} × {quantity}</p>
                          </div>
                          <p className="font-semibold">${(item.price * quantity).toFixed(2)}</p>
                        </div>
                      );
                    })}
                  </div>
                  
                  <div className="border-t pt-4 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold">Total:</span>
                      <span className="font-bold text-lg">${getTotalPrice().toFixed(2)}</span>
                    </div>
                  </div>
                  
                  <Link
                    to="/orders"
                    state={{ cart, restaurant, menuItems, total: getTotalPrice() }}
                    className="w-full btn-primary text-center block"
                  >
                    Proceed to Checkout
                  </Link>
                </>
              ) : (
                <p className="text-gray-500 text-center py-8">Your cart is empty</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Menu;
