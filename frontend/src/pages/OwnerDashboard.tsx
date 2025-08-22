import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { menuAPI, restaurantsAPI, uploadAPI, ordersAPI, API_BASE_URL } from '../api';

const OwnerDashboard: React.FC = () => {
  const [restaurant, setRestaurant] = useState<any>(null);
  const [menuItems, setMenuItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddItem, setShowAddItem] = useState(false);
  const [newItem, setNewItem] = useState({
    name: '',
    price: '',
    category: '',
    image: ''
  });
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [orders, setOrders] = useState<any[]>([]);

  useEffect(() => {
    fetchRestaurantData();
    
    // Set up interval to refresh data every 30 seconds
    const intervalId = setInterval(fetchRestaurantData, 30000);
    
    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const fetchRestaurantData = async () => {
    try {
      // Get user data from localStorage
      const userStr = localStorage.getItem('user');
      if (!userStr) {
        console.error('No user data found');
        return;
      }
      
      const user = JSON.parse(userStr);
      
      // Check if user has a restaurant ID
      if (!user.restaurantId) {
        console.log('No restaurant ID found in user data:', user);
        // Redirect to restaurant setup if no restaurant is configured
        window.location.href = '/restaurant-setup';
        return;
      }
      
      console.log('Fetching data for restaurant ID:', user.restaurantId);
      
      const [restaurantRes, menuRes, ordersRes] = await Promise.all([
        restaurantsAPI.getById(user.restaurantId),
        menuAPI.getByRestaurant(user.restaurantId),
        ordersAPI.getByRestaurant(user.restaurantId)
      ]);
      
      // Set restaurant data - handle both direct object and response wrapper
      const restaurantData = restaurantRes.data || restaurantRes;
      console.log('Restaurant data received:', restaurantData);
      setRestaurant(restaurantData);
      setMenuItems(menuRes.data || []);
      setOrders(ordersRes.data || []);
    } catch (error: any) {
      console.error('Error fetching restaurant data:', error);
      // If restaurant not found, redirect to setup
      if (error.response?.status === 404) {
        window.location.href = '/restaurant-setup';
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);

    let imageUrl = newItem.image;

    try {
      if (imageFile) {
        const uploadRes = await uploadAPI.uploadImage(imageFile);
        imageUrl = uploadRes.data.image_url;
      }

      const currentRestaurantId = restaurant?.id;
      if (!currentRestaurantId) {
        console.error("Restaurant ID not found");
        return;
      }

      await menuAPI.addItem(currentRestaurantId, {
        name: newItem.name,
        price: parseFloat(newItem.price),
        category: newItem.category,
        image: imageUrl,
      });

      setNewItem({ name: '', price: '', category: '', image: '' });
      setImageFile(null);
      setShowAddItem(false);
      fetchRestaurantData();
    } catch (error) {
      console.error('Failed to add menu item:', error);
    } finally {
      setUploading(false);
    }
  };

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handleDeleteItem = async (itemId: number) => {
    try {
      await menuAPI.deleteItem(itemId);
      fetchRestaurantData(); // Refresh menu items
    } catch (error) {
      console.error('Error deleting menu item:', error);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link to="/" className="text-2xl font-bold text-red-600">Zomato Clone</Link>
              <span className="ml-4 text-gray-600">Restaurant Owner Dashboard</span>
            </div>
            <div className="flex space-x-4">
              <Link to="/orders" className="btn-secondary">Orders</Link>
              <button 
                onClick={() => {
                  localStorage.removeItem('user');
                  window.location.href = '/';
                }}
                className="btn-secondary"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Restaurant Info */}
        <div className="bg-white overflow-hidden shadow rounded-lg mb-6">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {restaurant?.name || 'Your Restaurant'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {restaurant?.address || 'Restaurant Address'}
            </p>
            <p className="mt-1 text-xs text-gray-400">
              Restaurant ID: {restaurant?.id || 'Not set'}
            </p>
            <div className="mt-3">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Active
              </span>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">M</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Menu Items</dt>
                    <dd className="text-lg font-medium text-gray-900">{menuItems.length}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">O</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Today's Orders</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {orders.filter(order => {
                        const orderDate = new Date(order.created_at);
                        const today = new Date();
                        return orderDate.toDateString() === today.toDateString();
                      }).length}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-bold">$</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Today's Revenue</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      ${orders
                        .filter(order => {
                          const orderDate = new Date(order.created_at);
                          const today = new Date();
                          return orderDate.toDateString() === today.toDateString();
                        })
                        .reduce((acc, order) => acc + parseFloat(order.total_price), 0)
                        .toFixed(2)}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Menu Management */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Menu Management</h3>
              <button
                onClick={() => setShowAddItem(true)}
                className="btn-primary"
              >
                Add New Item
              </button>
            </div>

            {/* Add Item Form */}
            {showAddItem && (
              <div className="mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
                <h4 className="text-md font-medium text-gray-900 mb-3">Add New Menu Item</h4>
                <form onSubmit={handleAddItem} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Item Name</label>
                    <input
                      type="text"
                      required
                      className="input-field"
                      value={newItem.name}
                      onChange={(e) => setNewItem({...newItem, name: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Price ($)</label>
                    <input
                      type="number"
                      step="0.01"
                      required
                      className="input-field"
                      value={newItem.price}
                      onChange={(e) => setNewItem({...newItem, price: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Category</label>
                    <input
                      type="text"
                      className="input-field"
                      value={newItem.category}
                      onChange={(e) => setNewItem({...newItem, category: e.target.value})}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Image</label>
                    <input
                      type="file"
                      className="input-field"
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                  </div>
                  <div className="md:col-span-2 flex space-x-3">
                    <button 
                      type="submit" 
                      disabled={uploading}
                      className="btn-primary disabled:opacity-50"
                    >
                      {uploading ? 'Uploading...' : 'Add Item'}
                    </button>
                    <button 
                      type="button" 
                      onClick={() => {
                        setShowAddItem(false);
                        setNewItem({ name: '', price: '', category: '', image: '' });
                      }}
                      className="btn-secondary"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}

            {/* Menu Items List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {menuItems.map((item) => (
                <div key={item.id} className="border border-gray-200 rounded-lg p-4">
                  {item.image && (
                    <img 
                      src={`${API_BASE_URL}${item.image}`} 
                      alt={item.name}
                      className="w-full h-32 object-cover rounded-md mb-3"
                    />
                  )}
                  <h4 className="font-medium text-gray-900">{item.name}</h4>
                  <p className="text-sm text-gray-500">{item.category}</p>
                  <p className="text-lg font-bold text-green-600">${item.price}</p>
                  <div className="mt-3 flex space-x-2">
                    <button 
                      onClick={() => handleDeleteItem(item.id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {menuItems.length === 0 && (
              <div className="text-center py-8">
                <p className="text-gray-500">No menu items yet. Add your first item to get started!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OwnerDashboard;
