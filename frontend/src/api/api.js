const backendUrl = process.env.REACT_APP_BACKEND_URL;

export async function createAccount({ email, password }) {
  try {
    const response = await fetch(`${backendUrl}/create-account`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return await response.json();
  } catch (error) {
    console.error("Error in createAccount:", error);
    throw error;
  }
}

export async function login({ email, password }) {
  try {
    const response = await fetch(`${backendUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return await response.json();
  } catch (error) {
    console.error("Error in login:", error);
    throw error;
  }
}