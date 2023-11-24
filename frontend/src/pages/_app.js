import React from 'react';
import '../styles/global.css';
import MainLayout from '../layouts/MainLayout'; // Adjust the import path as necessary

function MyApp({ Component, pageProps }) {
    return (
        <MainLayout>
            <Component {...pageProps} />
        </MainLayout>
    );
}

export default MyApp;