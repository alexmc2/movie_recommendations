import { useState, useEffect } from 'react'; // Added useEffect
import Image from 'next/image';
import Illustration from '@/public/images/bg-illustration.svg';
import { MovieBotProps } from '@/pages/types';

export default function MovieBot({ title, movies }: MovieBotProps) {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [thinkingDots, setThinkingDots] = useState(''); // State for dynamic dots
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [displayedMovies, setDisplayedMovies] = useState([]);

  useEffect(() => {
    let interval;
    if (thinkingDots !== '') {
      interval = setInterval(() => {
        setThinkingDots((prevDots) => {
          switch (prevDots) {
            case '.':
              return '..';
            case '..':
              return '...';
            default:
              return '.';
          }
        });
      }, 500); // Change dots every 500ms
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval); // Cleanup on unmount
  }, [thinkingDots]);

  const sendMessage = async (e) => {
    e.preventDefault();

    // Immediately display the user's message
    setMessages((prevMessages) => [
      ...prevMessages,
      { role: 'user', content: userInput },
    ]);

    setThinkingDots('.'); // Start the "thinking" dots

    try {
      const response = await fetch('http://localhost:8080/api/moviebot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setRecommendedMovies(data.recommended_movies);

      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'bot', content: data.bot_msg },
      ]);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setThinkingDots(''); // End the "thinking" dots
    }
  };

  const fetchRecommendedMovies = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/movies');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const movies = await response.json();

      // Check if movies is an empty object
      if (!movies || Object.keys(movies).length === 0) {
        console.error('No movies found in the API response.');
        return;
      }

      setDisplayedMovies(movies);
    } catch (error) {
      console.error(
        'There was a problem fetching the recommended movies:',
        error
      );
    }
  };

  return (
    <div className="relative w-full lg:w-1/2 lg:fixed lg:inset-0 lg:overflow-y-auto no-scrollbar bg-slate-900 flex flex-col justify-between">
      {/* Background Illustration */}
      <div
        className="absolute top-0 -translate-y-64 left-1/2 -translate-x-1/2 blur-3xl pointer-events-none"
        aria-hidden="true"
      >
        <Image
          className="max-w-none"
          src={Illustration}
          width={785}
          height={685}
          alt="Bg illustration"
        />
      </div>

      <div className="chat-box p-4 rounded-lg overflow-y-auto h-80 mt-auto no-scrollbar">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`my-2 p-2 rounded-lg ${
              message.role === 'user'
                ? 'bg-blue-700 text-yellow-200'
                : 'bg-blue-950 text-white'
            }`}
          >
            {message.content}
          </div>
        ))}
        {thinkingDots && (
          <div className="my-2 p-2 rounded-lg bg-blue-950 text-white">
            {thinkingDots}
          </div>
        )}{' '}
        {/* Dynamic "thinking" dots */}
      </div>
      <form onSubmit={sendMessage} className="input-box p-4 flex items-center">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="What kind of movie are you looking for today?"
          className="flex-grow mr-2 rounded-full py-4 pl-5 pr-12 text-lg bg-slate-700 border-none"
        />
        <button
          type="submit"
          className=" bg-blue-500 text-white hover:bg-blue-600 rounded-full p-3"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </form>
      <div className="flex justify-between p-4 pt-0 btn">
        <button className="flex-1 btn bg-purple-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg">
          EXAMPLE
        </button>
        <button
          onClick={() => window.location.reload()}
          className="flex-1 btn bg-green-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg "
        >
          RESTART
        </button>

        <button
          onClick={fetchRecommendedMovies}
          className="flex-1 btn bg-blue-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg"
        >
          SHOW MOVIES!
        </button>
      </div>
    </div>
  );
}
