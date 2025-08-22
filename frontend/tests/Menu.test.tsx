import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom';
import App from '../src/App'; // Adjust this path to your actual Menu component

describe('Menu Component', () => {
  it('displays menu items', () => {
    render(<App />);
    
    // This is a placeholder test. You'll need to adjust this based on your actual component.
    // For example, you might look for a heading or a list of items.
    const menuHeading = screen.getByRole('heading', { name: /our menu/i });
    expect(menuHeading).toBeInTheDocument();
  });
});
