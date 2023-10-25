import React from 'react';

interface ImageCardProps {
  title: string;
  imageUrl: string;

}

const ImageCard: React.FC<ImageCardProps> = ({ title, imageUrl }) => {
  return (
    <div className="card">
      <img src={imageUrl} alt={title} />
      <h3>{title}</h3>
 
    </div>
  );
};

export default ImageCard;
