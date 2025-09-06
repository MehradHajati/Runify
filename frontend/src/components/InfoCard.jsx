import React from "react";

const InfoCard = ({ children, className = "" }) => {
  return <div className={`info-card ${className}`}>{children}</div>;
};

export default InfoCard;
