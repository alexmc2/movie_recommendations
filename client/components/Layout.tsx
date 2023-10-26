import Theme from '../pages/theme-provider';
import Header from '@/components/ui/header';
import MovieBot from '@/components/movie-bot-page';

export const metadata = {
  title: 'Movie App',
  description: 'Movie recommendation app built with Next.js and Python',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <Theme>
      <div className="flex flex-col min-h-screen overflow-hidden">
        <Header />

        <div className="grow flex flex-col lg:flex-row">
          {/* Left side */}
          <MovieBot title="AI Movie Recommendation App" />

          {/* Right side */}
          <main className="max-lg:grow flex flex-col w-full lg:w-1/2 lg:ml-auto">
            {children}
          </main>
        </div>
      </div>
    </Theme>
  );
}
