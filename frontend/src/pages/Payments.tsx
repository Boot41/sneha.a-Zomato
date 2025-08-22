import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

interface PaymentMethod {
  id: string;
  type: 'card' | 'upi' | 'wallet';
  name: string;
  details: string;
  isDefault: boolean;
}

const Payments: React.FC = () => {
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([
    {
      id: '1',
      type: 'card',
      name: 'Visa ending in 1234',
      details: '**** **** **** 1234',
      isDefault: true
    },
    {
      id: '2',
      type: 'upi',
      name: 'UPI ID',
      details: 'user@paytm',
      isDefault: false
    }
  ]);
  
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPayment, setNewPayment] = useState({
    type: 'card' as 'card' | 'upi' | 'wallet',
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    holderName: '',
    upiId: ''
  });
  
  const navigate = useNavigate();

  React.useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }
  }, [navigate]);

  const handleAddPayment = (e: React.FormEvent) => {
    e.preventDefault();
    
    let newMethod: PaymentMethod;
    
    if (newPayment.type === 'card') {
      newMethod = {
        id: Date.now().toString(),
        type: 'card',
        name: `${newPayment.cardNumber.startsWith('4') ? 'Visa' : 'Mastercard'} ending in ${newPayment.cardNumber.slice(-4)}`,
        details: `**** **** **** ${newPayment.cardNumber.slice(-4)}`,
        isDefault: paymentMethods.length === 0
      };
    } else {
      newMethod = {
        id: Date.now().toString(),
        type: 'upi',
        name: 'UPI ID',
        details: newPayment.upiId,
        isDefault: paymentMethods.length === 0
      };
    }
    
    setPaymentMethods([...paymentMethods, newMethod]);
    setShowAddForm(false);
    setNewPayment({
      type: 'card',
      cardNumber: '',
      expiryDate: '',
      cvv: '',
      holderName: '',
      upiId: ''
    });
  };

  const setAsDefault = (id: string) => {
    setPaymentMethods(methods =>
      methods.map(method => ({
        ...method,
        isDefault: method.id === id
      }))
    );
  };

  const removePayment = (id: string) => {
    setPaymentMethods(methods => methods.filter(method => method.id !== id));
  };

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
              <Link to="/orders" className="text-gray-600 hover:text-gray-900">Orders</Link>
              <Link to="/dashboard" className="btn-secondary">Dashboard</Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Payment Methods</h1>
          <button
            onClick={() => setShowAddForm(true)}
            className="btn-primary"
          >
            Add Payment Method
          </button>
        </div>

        {/* Add Payment Form */}
        {showAddForm && (
          <div className="card mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Payment Method</h2>
            
            <form onSubmit={handleAddPayment} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Type
                </label>
                <select
                  className="input-field"
                  value={newPayment.type}
                  onChange={(e) => setNewPayment({...newPayment, type: e.target.value as 'card' | 'upi' | 'wallet'})}
                >
                  <option value="card">Credit/Debit Card</option>
                  <option value="upi">UPI</option>
                  <option value="wallet">Digital Wallet</option>
                </select>
              </div>

              {newPayment.type === 'card' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Card Holder Name
                    </label>
                    <input
                      type="text"
                      className="input-field"
                      value={newPayment.holderName}
                      onChange={(e) => setNewPayment({...newPayment, holderName: e.target.value})}
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Card Number
                    </label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="1234 5678 9012 3456"
                      value={newPayment.cardNumber}
                      onChange={(e) => setNewPayment({...newPayment, cardNumber: e.target.value.replace(/\s/g, '')})}
                      maxLength={16}
                      required
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Expiry Date
                      </label>
                      <input
                        type="text"
                        className="input-field"
                        placeholder="MM/YY"
                        value={newPayment.expiryDate}
                        onChange={(e) => setNewPayment({...newPayment, expiryDate: e.target.value})}
                        maxLength={5}
                        required
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        CVV
                      </label>
                      <input
                        type="text"
                        className="input-field"
                        placeholder="123"
                        value={newPayment.cvv}
                        onChange={(e) => setNewPayment({...newPayment, cvv: e.target.value})}
                        maxLength={3}
                        required
                      />
                    </div>
                  </div>
                </>
              )}

              {newPayment.type === 'upi' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    UPI ID
                  </label>
                  <input
                    type="text"
                    className="input-field"
                    placeholder="yourname@paytm"
                    value={newPayment.upiId}
                    onChange={(e) => setNewPayment({...newPayment, upiId: e.target.value})}
                    required
                  />
                </div>
              )}

              <div className="flex space-x-3">
                <button type="submit" className="btn-primary">
                  Add Payment Method
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Payment Methods List */}
        <div className="space-y-4">
          {paymentMethods.map((method) => (
            <div key={method.id} className="card">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    {method.type === 'card' && (
                      <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                      </svg>
                    )}
                    {method.type === 'upi' && (
                      <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                    )}
                  </div>
                  
                  <div>
                    <h3 className="font-semibold text-gray-900">{method.name}</h3>
                    <p className="text-sm text-gray-600">{method.details}</p>
                    {method.isDefault && (
                      <span className="inline-flex px-2 py-1 text-xs font-semibold bg-green-100 text-green-800 rounded-full mt-1">
                        Default
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {!method.isDefault && (
                    <button
                      onClick={() => setAsDefault(method.id)}
                      className="btn-secondary text-sm"
                    >
                      Set as Default
                    </button>
                  )}
                  <button
                    onClick={() => removePayment(method.id)}
                    className="text-red-600 hover:text-red-800 p-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {paymentMethods.length === 0 && (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No payment methods</h3>
            <p className="text-gray-600 mb-4">Add a payment method to start ordering</p>
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary"
            >
              Add Payment Method
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Payments;
