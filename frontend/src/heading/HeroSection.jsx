import React from "react";

const HeroSection = () => {
  return (
    <div className="hero-section">
      <img
        src="https://cdn.builder.io/api/v1/image/assets/TEMP/366d14130b5bd37b7908e830383c30683be468ae"
        alt="Mountain landscape with runner"
        className="hero-image"
      />
      <div className="hero-text">
        <span>Music helps runners maintain consistent pacing.</span>
        <br />
        <span>Runify helps runners find their beat.</span>
      </div>
    </div>
  );
};

export default HeroSection;
