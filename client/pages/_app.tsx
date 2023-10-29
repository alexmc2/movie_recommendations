import '../styles/globals.css';
import '../styles/additional-styles/utility-patterns.css';
import RootLayout from '../components/Layout';
import { useState, useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8080/api/movies')
      .then((response) => response.json())
      .then((data) => {
        setMovies(data);
      });
  }, []);

  return (
    <RootLayout movies={movies}>
      <Component {...pageProps} />
    </RootLayout>
  );
}

export default MyApp;