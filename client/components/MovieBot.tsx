import { useState } from 'react';
import Image from 'next/image';
import Illustration from '@/public/images/bg-illustration.svg';

interface MovieBotProps {
  title: string;
}

export default function MovieBot({ title }: MovieBotProps) {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();

    // Immediately display the user's message
    setMessages([...messages, { role: 'user', content: userInput }]);

    const response = await fetch('http://localhost:8080/api/moviebot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userInput }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = '';
    let botMessage = '';

    reader.read().then(function processText({ done, value }) {
      if (done) {
        setMessages([...messages, { role: 'bot', content: botMessage }]);
        return;
      }

      buffer += decoder.decode(value, { stream: true });

      let startIdx = buffer.indexOf('{');
      while (startIdx !== -1) {
        let endIdx = buffer.indexOf('}', startIdx);
        if (endIdx === -1) {
          break;
        }

        const jsonString = buffer.substring(startIdx, endIdx + 1);
        const parsedData = JSON.parse(jsonString);

        if (parsedData && parsedData.word) {
          botMessage += ` ${parsedData.word}`;
        }

        buffer = buffer.substring(endIdx + 1);
        startIdx = buffer.indexOf('{');
      }

      return reader.read().then(processText);
    });
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
      </div>
      <form onSubmit={sendMessage} className="input-box p-4 flex items-center">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="What kind of movie are you looking for today?"
          className="flex-grow mr-2 rounded-full py-4 pl-5 pr-12 text-lg bg-slate-700 border-none" // Added border-none
        />
        <button
          type="submit"
          className="btn bg-blue-500 text-white hover:bg-blue-600 rounded-full p-3"
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
      <div className="flex justify-between p-4 pt-0">
        <button className="flex-1 btn bg-purple-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg">
          EXAMPLE
        </button>
        <button
          onClick={() => window.location.reload()}
          className="flex-1 btn bg-green-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg"
        >
          RESTART
        </button>

        <button className="flex-1 btn bg-blue-600 text-white hover:bg-gray-700 rounded-md p-4 mx-1 text-center text-lg">
          SHOW MOVIES!
        </button>
      </div>
    </div>
  );
}
