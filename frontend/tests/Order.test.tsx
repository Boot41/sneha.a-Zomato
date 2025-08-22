import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';
import App from '../src/App'; // Adjust this path to your actual Order component

describe('Order Component', () => {
  it('renders the place order button', () => {
    render(<App />);
    
    // This is a placeholder test. You'll need to adjust this based on your actual component.
    const placeOrderButton = screen.getByRole('button', { name: /place order/i });
    expect(placeOrderButton).toBeInTheDocument();
  });
});
