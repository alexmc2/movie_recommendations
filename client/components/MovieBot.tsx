import { useState, useEffect } from 'react';
import Image from 'next/image';
import Illustration from '@/public/images/bg-illustration.svg';
import { MovieBotProps } from '@/pages/types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilm } from '@fortawesome/free-solid-svg-icons';

export default function MovieBot({
  title,
  movies,
  setDisplayedMovies,
}: MovieBotProps) {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [thinkingDots, setThinkingDots] = useState('');
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [extractedMovieTitles, setExtractedMovieTitles] = useState([]);

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
      console.log('Raw Response:', response);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setRecommendedMovies(data.recommendedMovies);

      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'bot', content: data.bot_msg },
      ]);

      setExtractedMovieTitles(data.recommendedMovies);
      console.log(
        'Recommended IMDb IDs from backend:',
        data.recommendedMovies
      );
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setThinkingDots(''); // End the "thinking" dots
    }
  };

  const fetchRecommendedMovies = async () => {
    try {
      // Use IMDb IDs when making the API call
      console.log('Extracted IMDb IDs:', extractedMovieTitles);

      const response = await fetch(
        `http://localhost:8080/api/movies?imdb_ids=${extractedMovieTitles.join(
          '&imdb_ids='
        )}`
      );
      const moviesData = await response.json();
      setDisplayedMovies(moviesData);
    } catch (error) {
      console.error('There was a problem fetching recommended movies:', error);
    }
  };

  return (
    <div className="relative w-full lg:w-1/2 lg:fixed lg:inset-0 lg:overflow-y-auto no-scrollbar bg-slate-900 flex flex-col justify-between">
      {/* Background Illustration */}

      <div className="text-orange-600 sm:text-6xl text-5xl font-bold pt-20  flex justify-center items-center  px-2 ">
        <FontAwesomeIcon
          icon={faFilm}
          style={{ color: '	#00BFFF', fontSize: '3rem' }}
          className="mr-4 "
        />
        Movie Mine
      </div>
      <div className="text-white md:text-lg text-md flex justify-center items-center pt-2 pb-3 px-3 ">
        Find the perfect film with the help of AI
      </div>

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
      <form
        onSubmit={sendMessage}
        className="input-box p-4 flex items-center relative "
      >
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="What kind of movie are you looking for?"
          className="flex-grow rounded-full sm:py-4 py-2 pl-4 pr-14 sm:pr-10 text-lg bg-slate-700 border-none min-h-[2rem] max-h-[6rem] overflow-y-auto resize-y"
        />
        <button
          type="submit"
          className="absolute sm:right-6 right-5 top-1/2 transform -translate-y-1/2 bg-blue-500 text-white hover:bg-blue-600 rounded-full p-2 sm:p-3"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 sm:h-6 sm:w-6"
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
        <button className="flex-1 bg-green-600 text-white hover:bg-gray-700 rounded-md sm:p-3 p-3 mx-1 text-center sm:text-lg text-xs">
          INSPIRE ME!
        </button>
        <button
          onClick={() => window.location.reload()}
          className="flex-1  bg-orange-600 text-white hover:bg-gray-700 rounded-md sm:p-3 p-3 mx-1 text-center sm:text-lg text-xs"
        >
          RESTART
        </button>

        <button
          onClick={fetchRecommendedMovies}
          className="flex-1 bg-blue-600 text-white hover:bg-gray-700 rounded-md sm:p-3 p-3 mx-1 text-center sm:text-lg text-xs"
        >
          <span className="hidden md:inline">SHOW MOVIES!</span>
          <span className="md:hidden">SHOW ME!</span>
        </button>
      </div>
    </div>
  );
}
