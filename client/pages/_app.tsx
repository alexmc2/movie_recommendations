// pages/_app.tsx
import '../styles/globals.css';
import '../styles/additional-styles/utility-patterns.css';
import RootLayout from '../components/Layout';

function MyApp({ Component, pageProps }) {
  return (
    <RootLayout>
      <Component {...pageProps} />
    </RootLayout>
  );
}

export default MyApp;
