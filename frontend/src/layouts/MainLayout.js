import React from 'react';
import Navigation from '../components/Navigation';
import Breadcrumbs from '../components/Breadcrumbs';

const MainLayout = ({ children }) => {
  return (
    <>
      <Navigation />
      <Breadcrumbs />
      <main>{children}</main>
    </>
  );
};

export default MainLayout;
