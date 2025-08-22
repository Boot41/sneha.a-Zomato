import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom'; // For additional matchers
import App from '../src/App'; // Adjust the import path as needed

describe('Auth Component', () => {
  it('renders the login button', () => {
    render(<App />);
    
    // Check if a button with the text "Login" is present
    const loginButton = screen.getByRole('button', { name: /login/i });
    expect(loginButton).toBeInTheDocument();
  });
});
