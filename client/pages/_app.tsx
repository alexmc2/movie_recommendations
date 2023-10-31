import '../styles/globals.css';
import '../styles/additional-styles/utility-patterns.css';
import RootLayout from '../components/Layout';
import { useState, useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  const [movies, setMovies] = useState([]);
  const [displayedMovies, setDisplayedMovies] = useState([]);


  return (
    <RootLayout
      movies={movies}
      displayedMovies={displayedMovies}
      setDisplayedMovies={setDisplayedMovies}
    >
      <Component {...pageProps} displayedMovies={displayedMovies} />
    </RootLayout>
  );
}

export default MyApp;
