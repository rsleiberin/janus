import '../styles/globals.css'; // This line imports the global styles
import MainLayout from '../layouts/MainLayout'; // Adjust the import path as necessary

function MyApp({ Component, pageProps }) {
  return (
    <MainLayout>
      <Component {...pageProps} />
    </MainLayout>
  );
}

export default MyApp;
