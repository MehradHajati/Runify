import React from "react";

const Header = () => {
  return (
    <header className="header">
      <div className="logo">Runify</div>
      <div className="menu-button">
        <svg
          width="48"
          height="48"
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="menu-icon"
        >
          <path
            d="M6 24H42M6 12H42M6 36H42"
            stroke="white"
            strokeWidth="4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </header>
  );
};

export default Header;
