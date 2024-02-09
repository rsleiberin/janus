import React from 'react';
import styles from './mainLayout.module.css'; // Adjust the import path as necessary
import Header from './header/Header';
import Footer from './footer/Footer';

const MainLayout = ({ children }) => {
  return (
    <div className={styles.mainLayout}>
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
};

export default MainLayout;
