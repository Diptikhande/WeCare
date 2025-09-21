import axios from 'axios';

// Configure axios defaults
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      console.error(`Server error ${status}:`, data);
      
      if (status >= 500) {
        throw new Error('Server error. Please try again later.');
      } else if (status === 404) {
        throw new Error('Service not found. Please check your connection.');
      } else {
        throw new Error(data.error || 'An error occurred');
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received:', error.request);
      throw new Error('Unable to connect to the server. Please check your internet connection.');
    } else {
      // Something else happened
      console.error('Request setup error:', error.message);
      throw new Error('An unexpected error occurred');
    }
  }
);

/**
 * Send a message to the chatbot
 * @param {string} message - The user's message
 * @param {string} sessionId - The session ID
 * @returns {Promise<Object>} The chatbot's response
 */
export const sendMessage = async (message, sessionId) => {
  try {
    const response = await api.post('/api/chat', {
      message,
      session_id: sessionId,
    });
    
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

/**
 * Get chat history for a session
 * @param {string} sessionId - The session ID
 * @returns {Promise<Array>} Array of chat messages
 */
export const getChatHistory = async (sessionId) => {
  try {
    const response = await api.get(`/api/chat/history/${sessionId}`);
    return response.data.history || [];
  } catch (error) {
    console.error('Error getting chat history:', error);
    // Return empty array if history can't be loaded
    return [];
  }
};

/**
 * Reset a chat session
 * @param {string} sessionId - The session ID
 * @returns {Promise<Object>} Success response
 */
export const resetChatSession = async (sessionId) => {
  try {
    const response = await api.post(`/api/chat/reset/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error resetting chat session:', error);
    throw error;
  }
};

/**
 * Check API health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default api;