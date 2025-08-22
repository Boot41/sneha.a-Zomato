import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { ordersAPI } from '../api';

const Orders: React.FC = () => {
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [cart, setCart] = useState<{[key: string]: number}>({});
  const [total, setTotal] = useState<number>(0);
  const navigate = useNavigate();
  const location = useLocation();
  const { cart: initialCart, restaurant, menuItems, total: initialTotal } = location.state || {};

  // Initialize cart and total from location state if available
  useEffect(() => {
    if (initialCart) setCart(initialCart);
    if (initialTotal) setTotal(initialTotal);
  }, [initialCart, initialTotal]);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      if (parsedUser && parsedUser.id) {
        fetchOrders(parsedUser.id);
      } else {
        setLoading(false);
      }
    } else {
      navigate('/login');
    }
  }, [navigate]);

  const fetchOrders = async (userId: number) => {
    if (!userId) {
      setLoading(false);
      return;
    }
    
    try {
      const response = await ordersAPI.getByCustomer(userId);
      setOrders(response.data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePlaceOrder = async () => {
    if (!user || !restaurant || !cart || !total) {
      alert('Missing order information. Please try again.');
      return;
    }

    const orderItems = Object.entries(cart).map(([itemId, quantity]: [string, any]) => {
      const item = menuItems?.find((menuItem: any) => menuItem.id === parseInt(itemId));
      return {
        menu_item_id: parseInt(itemId),
        quantity: quantity,
        price: item ? parseFloat(item.price) : 0,
      };
    });

    try {
      // Show loading state
      setLoading(true);
      
      const orderData = {
        customer_id: user.id,
        restaurant_id: restaurant.id,
        total_price: parseFloat(total.toString()),
        items: orderItems,
      };

      console.log('Sending order data:', orderData);
      
      // Create the order
      const response = await ordersAPI.create(orderData);
      console.log('Order created:', response.data);
      
      // Fetch the latest orders to ensure we have all data
      const ordersResponse = await ordersAPI.getByCustomer(user.id);
      const updatedOrders = ordersResponse.data;
      
      // Update the orders list with the server response
      setOrders(updatedOrders);
      
      // Clear the cart
      if (location.state) {
        location.state.cart = {};
        location.state.total = 0;
        setCart({});
        setTotal(0);
      }
      
      // Show success message
      alert('Order placed successfully! It will appear in your order history.');
      
    } catch (error: any) {
      console.error('Failed to place order:', error);
      console.error('Error response:', error.response?.data);
      alert(`Failed to place order: ${error.response?.data?.detail || 'Please try again.'}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading orders...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/dashboard" className="text-2xl font-bold text-red-600">
              Zomato Clone
            </Link>
            <div className="flex items-center space-x-4">
              <Link to="/restaurants" className="text-gray-600 hover:text-gray-900">Restaurants</Link>
              <Link to="/dashboard" className="btn-secondary">Dashboard</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Order Checkout Section */}
        {cart && restaurant && (
          <div className="card mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Complete Your Order</h2>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <p className="font-semibold text-gray-900">{restaurant.name}</p>
                  <p className="text-sm text-gray-600">{restaurant.address}</p>
                </div>
                
                <div className="space-y-3">
                  {Object.entries(cart).map(([itemId, quantity]: [string, any]) => {
                    const item = menuItems?.find((item: any) => item.id === parseInt(itemId));
                    if (!item) return null;
                    
                    return (
                      <div key={itemId} className="flex justify-between items-center py-2 border-b">
                        <div>
                          <p className="font-medium">{item.name}</p>
                          <p className="text-sm text-gray-600">Qty: {quantity}</p>
                        </div>
                        <p className="font-semibold">${(item.price * quantity).toFixed(2)}</p>
                      </div>
                    );
                  })}
                </div>
                
                <div className="border-t pt-4 mt-4">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>Total:</span>
                    <span>${total?.toFixed(2)}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Delivery Details</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Delivery Address
                    </label>
                    <textarea
                      className="input-field"
                      rows={3}
                      placeholder="Enter your delivery address"
                      defaultValue="123 Main St, City, State 12345"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      className="input-field"
                      placeholder="Your phone number"
                      defaultValue={user?.phone || ''}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Special Instructions
                    </label>
                    <textarea
                      className="input-field"
                      rows={2}
                      placeholder="Any special requests..."
                    />
                  </div>
                </div>

                <button
                  onClick={handlePlaceOrder}
                  disabled={!user || !restaurant || !cart || Object.keys(cart).length === 0}
                  className="w-full bg-red-600 text-white py-3 px-4 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  Place Order
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Order History */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Order History</h2>
          
          {orders.length > 0 ? (
            <div className="space-y-4">
              {orders.map((order: any) => (
                <div key={order.id} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{order.restaurant_name}</h3>
                      <p className="text-sm text-gray-600">Order #{order.id}</p>
                      <p className="text-sm text-gray-500">
                        Ordered on {new Date(order.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex flex-col items-end space-y-1">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        order.status === 'delivered' ? 'bg-green-100 text-green-800' : 
                        order.status === 'preparing' ? 'bg-blue-100 text-blue-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {order.status?.charAt(0).toUpperCase() + order.status?.slice(1) || 'Pending'}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-xs ${
                        order.payment_status === 'Paid' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                      }`}>
                        {order.payment_status || 'Unpaid'}
                      </span>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Items:</h4>
                    <ul className="list-disc list-inside text-sm text-gray-600">
                      {order.items && order.items.map((item: any) => (
                        <li key={item.id} className="mb-1">
                          {item.quantity} x {item.name} - ${(item.price * item.quantity).toFixed(2)}
                          {item.quantity > 1 && ` ($${item.price.toFixed(2)} each)`}
                        </li>
                      ))}
                    </ul>
                    <div className="mt-2 pt-2 border-t border-gray-100">
                      <p className="text-right font-medium">
                        Total: ${order.total_price?.toFixed(2) || '0.00'}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3 mt-4">
                    <button className="btn-secondary text-sm">
                      View Details
                    </button>
                    <button className="btn-secondary text-sm">
                      Reorder
                    </button>
                    {order.status === 'delivered' && (
                      <button className="btn-secondary text-sm">
                        Rate & Review
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No orders yet</h3>
              <p className="text-gray-600 mb-4">Start by browsing restaurants and adding items to your cart</p>
              <Link to="/restaurants" className="btn-primary">
                Browse Restaurants
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Orders;
