// types.ts

import React from 'react';

export interface Movie {
  ID: string;
  title: string;
  imageUrl: string;
  description: string;
  year: string;
  rating: string;
}

export interface MovieBotProps {
  title: string;
  movies: Movie[];
  setDisplayedMovies: React.Dispatch<React.SetStateAction<Movie[]>>;
  // setShowVideo: React.Dispatch<React.SetStateAction<boolean>>; 
}

export interface RootLayoutProps {
  children: React.ReactNode;
  movies: Movie[];
  displayedMovies: Movie[];
  setDisplayedMovies: React.Dispatch<React.SetStateAction<Movie[]>>;
  // setShowVideo: React.Dispatch<React.SetStateAction<boolean>>;
}
