import React from 'react';
import Navigation from '../components/Navigation';

export default function MainLayout({ children }) {
  return (
    <div className='container mx-auto p-4'>
      <Navigation />
      {children}
    </div>
  );
}
