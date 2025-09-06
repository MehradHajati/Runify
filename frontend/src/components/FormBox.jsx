import React from "react";
import InputGroup from "./InputBox";
import Button from "./Button";

const FormBox = ({
  title,
  buttonText,
  linkText,
  linkHref = "#",
  emailValue,
  passwordValue,
  onEmailChange,
  onPasswordChange,
  onSubmit,
  errorMessage,
  onLinkClick,
}) => {
  return (
    <div className="form-box">
      <div className="form-title">{title}</div>
      <div className="form-container">
        <InputGroup
          label="Email"
          type="text"
          value={emailValue}
          onChange={onEmailChange}
          placeholder="Value"
        />
        <InputGroup
          label="Password"
          type="password"
          value={passwordValue}
          onChange={onPasswordChange}
          placeholder="Value"
        />
        <Button onClick={onSubmit}>{buttonText}</Button>
        {errorMessage && <div className="error-message">{errorMessage}</div>}
        <a href={linkHref} className="form-link" onClick={onLinkClick}>
          {linkText}
        </a>
      </div>
    </div>
  );
};

export default FormBox;
