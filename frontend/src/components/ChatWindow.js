import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendMessage, getChatHistory } from '../utils/api';

const ChatContainer = styled.div`
  width: 100%;
  max-width: 800px;
  height: 700px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.2);

  @media (max-width: 768px) {
    height: 80vh;
    margin: 10px;
    border-radius: 16px;
  }
`;

const ChatHeader = styled.div`
  background: linear-gradient(135deg, #1e40af, #3730a3);
  color: white;
  padding: 1rem 1.5rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

const ChatTitle = styled.h2`
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
`;

const ChatSubtitle = styled.p`
  margin: 4px 0 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
`;

const InputContainer = styled.div`
  background: white;
  border-top: 1px solid rgba(226, 232, 240, 0.5);
  padding: 1rem;
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  color: #64748b;
  font-style: italic;
`;

const ErrorMessage = styled.div`
  background: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  margin: 1rem;
  border-radius: 8px;
  border: 1px solid #fecaca;
`;

const ChatWindow = ({ sessionId }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Load chat history when session changes
    loadChatHistory();
  }, [sessionId]);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = async () => {
    try {
      const history = await getChatHistory(sessionId);
      const formattedMessages = history.map(item => ({
        id: Date.now() + Math.random(),
        content: item.message,
        sender: item.role === 'user' ? 'user' : 'therapist',
        timestamp: new Date(item.timestamp)
      }));
      setMessages(formattedMessages);
    } catch (err) {
      console.error('Error loading chat history:', err);
      // Start with a welcome message if no history
      setMessages([{
        id: 1,
        content: "Hello! I'm here to listen and support you. How are you feeling today? Please feel free to share what's on your mind.",
        sender: 'therapist',
        timestamp: new Date()
      }]);
    }
  };

  const handleSendMessage = async (messageContent) => {
    if (!messageContent.trim()) return;

    const userMessage = {
      id: Date.now(),
      content: messageContent,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(messageContent, sessionId);
      
      const therapistMessage = {
        id: Date.now() + 1,
        content: response.response,
        sender: 'therapist',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, therapistMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Sorry, I\'m having trouble responding right now. Please try again.');
      
      const errorMessage = {
        id: Date.now() + 1,
        content: 'I apologize, but I\'m experiencing some technical difficulties. Please try sending your message again.',
        sender: 'therapist',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContainer>
      <ChatHeader>
        <ChatTitle>💙 Your Personal Therapist</ChatTitle>
        <ChatSubtitle>I'm here to listen and support you</ChatSubtitle>
      </ChatHeader>
      
      <MessagesContainer>
        <MessageList messages={messages} />
        {isLoading && (
          <LoadingIndicator>
            Therapist is thinking...
          </LoadingIndicator>
        )}
        {error && (
          <ErrorMessage>
            {error}
          </ErrorMessage>
        )}
        <div ref={messagesEndRef} />
      </MessagesContainer>
      
      <InputContainer>
        <MessageInput 
          onSendMessage={handleSendMessage} 
          disabled={isLoading}
        />
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatWindow;