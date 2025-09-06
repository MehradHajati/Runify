import React from "react";

const InputGroup = ({
  label,
  type,
  value,
  onChange,
  placeholder = "Value",
  className = "",
  ...props
}) => {
  return (
    <div className={`input-group ${className}`}>
      <div className="input-label">{label}</div>
      <input
        type={type}
        value={value}
        onChange={onChange}
        className="input-field"
        placeholder={placeholder}
        {...props}
      />
    </div>
  );
};

export default InputGroup;
