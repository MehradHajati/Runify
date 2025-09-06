import React, { useState } from "react";
import { createAccount, login } from "../api/api";
import Header from "../heading/Header";
import HeroSection from "../heading/HeroSection";
import InfoCard from "../components/InfoCard";
import FormBox from "../components/FormBox";

const LoginPage = () => {
  // Create Account state
  const [createEmail, setCreateEmail] = useState("");
  const [createPassword, setCreatePassword] = useState("");
  const [createMessage, setCreateMessage] = useState("");

  // Sign In state
  const [signInEmail, setSignInEmail] = useState("");
  const [signInPassword, setSignInPassword] = useState("");
  const [signInError, setSignInError] = useState("");

  // Handler for creating a new account using the API helper.
  const handleCreateAccount = async (e) => {
    if (e) e.preventDefault();
    try {
      const data = await createAccount({
        email: createEmail,
        password: createPassword,
      });
      if (data.success) {
        setCreateMessage("Account Created");
      } else {
        setCreateMessage(data.message || "Account creation failed.");
      }
    } catch (error) {
      console.error("Error creating account:", error);
      setCreateMessage("Error creating account");
    }
  };

  // Handler for signing in using the API helper.
  const handleSignIn = async (e) => {
    if (e) e.preventDefault();
    try {
      const data = await login({
        email: signInEmail,
        password: signInPassword,
      });
      if (data.success) {
        // Redirect to backend's /auth endpoint for Spotify OAuth.
        window.location.href = `${process.env.REACT_APP_BACKEND_URL}/auth`;
      } else {
        setSignInError(data.message || "Invalid credentials.");
      }
    } catch (error) {
      console.error("Error during sign in:", error);
      setSignInError("Error during sign in");
    }
  };

  // Toggle between create account and sign in forms
  const toggleToSignIn = (e) => {
    e.preventDefault();
  };

  const toggleToCreateAccount = (e) => {
    e.preventDefault();
  };

  return (
    <div className="app">
      <Header />
      <HeroSection />

      <div className="login-content">
        <div className="create-account-section">
          <FormBox
            title="Create Account"
            buttonText="Submit"
            // linkText="Log In"
            // linkHref="#"
            emailValue={createEmail}
            passwordValue={createPassword}
            onEmailChange={(e) => setCreateEmail(e.target.value)}
            onPasswordChange={(e) => setCreatePassword(e.target.value)}
            onSubmit={handleCreateAccount}
            errorMessage={createMessage}
            onLinkClick={toggleToSignIn}
          />
        </div>

        <div className="sign-in-section">
          <FormBox
            title="Sign In"
            buttonText="Sign in with Spotify"
            // linkText="Create Account"
            // linkHref="#"
            emailValue={signInEmail}
            passwordValue={signInPassword}
            onEmailChange={(e) => setSignInEmail(e.target.value)}
            onPasswordChange={(e) => setSignInPassword(e.target.value)}
            onSubmit={handleSignIn}
            errorMessage={signInError}
            onLinkClick={toggleToCreateAccount}
          />
          <InfoCard className="login-info-card">
            Log in with Spotify to improve your training with personalized BPM
            playlists.
          </InfoCard>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
