import React from 'react';

interface ImageCardProps {
  title: string;
  imageUrl: string;
  description: string;
  // year: number;
  rating: number;
}

const ImageCard: React.FC<ImageCardProps> = ({
  title,
  imageUrl,
  description,
  // year,
  rating,
}) => {
  console.log('Rendering ImageCard for movie:', title);

  return (
    <div className="card bg-gray-800 shadow-md rounded overflow-hidden max-w-sm m-4">
      <img src={imageUrl} alt={title} className="w-full h-60 object-cover" />
      <div className="p-4">
        <h3 className="text-xl font-bold mb-2 text-white">{title}</h3>
        <p className="text-white text-sm">{description}</p>
        <p className="mt-2 text-white">
          <small> Rating: {rating}</small>
        </p>
      </div>
    </div>
  );
};

export default ImageCard;
