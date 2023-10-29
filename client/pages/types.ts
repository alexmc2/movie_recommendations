// types.ts

export interface Movie {
  title: string;
  imageUrl: string;
  description: string;
  year: string;
  rating: string;
}

export interface MovieBotProps {
  title: string;
  movies: Movie[];
}

export interface RootLayoutProps {
  children: React.ReactNode;
  movies: Movie[];
}
