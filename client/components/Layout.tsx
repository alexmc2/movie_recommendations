import Theme from '../pages/theme-provider';
import Header from '@/components/ui/header';
import MovieBot from '../components/MovieBot';

export const metadata = {
  title: 'Movie App',
  description: 'Movie recommendation app built with Next.js and Python',
};

// layout.tsx

import { RootLayoutProps } from '@/pages/types'; // Ensure you import the type

export default function RootLayout({
  children,
  movies,
  displayedMovies,
  setDisplayedMovies,
}: RootLayoutProps) {
  return (
    <Theme>
      <div className="flex flex-col min-h-screen overflow-hidden">
        <Header />
        <div className="grow flex flex-col lg:flex-row">
          <MovieBot
            title="MovieBot"
            movies={movies}
            setDisplayedMovies={setDisplayedMovies}
          />
          <main className="max-lg:grow flex flex-col w-full lg:w-1/2 lg:ml-auto">
            {children}
          </main>
        </div>
      </div>
    </Theme>
  );
}
