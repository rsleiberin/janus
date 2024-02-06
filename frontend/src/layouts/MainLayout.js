import React from 'react';
import styles from './mainLayout.module.css'; // Adjust the import path as necessary
import Header from '../components/organisms/Header';
import Footer from '../components/organisms/Footer';

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
