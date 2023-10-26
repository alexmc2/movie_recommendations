import Link from 'next/link';
import Image from 'next/image';
import ThemeToggle from './theme-toggle';

export default function Header() {
  return (
    <header className="absolute w-full z-30">
      <div className="max-w-xl lg:max-w-[calc(50%+theme(maxWidth.xl))] mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16 md:h-20">
          {/* Site branding */}
          <div className="shrink-0 mr-4 lg:fixed">
            {/* Logo */}
            <Link
              className="flex items-center space-x-4"
              href="/"
              aria-label="Movie App"
            ></Link>
          </div>

          {/* Right side */}
          <div className="flex grow justify-end">
            {/* Light switch */}
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>
  );
}
