import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import ChatWindow from './components/ChatWindow';
import Header from './components/Header';
import { v4 as uuidv4 } from 'uuid';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 50%, #1e40af 100%);
  display: flex;
  flex-direction: column;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
`;

function App() {
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    // Generate or retrieve session ID
    let storedSessionId = localStorage.getItem('wecare_session_id');
    if (!storedSessionId) {
      storedSessionId = uuidv4();
      localStorage.setItem('wecare_session_id', storedSessionId);
    }
    setSessionId(storedSessionId);
  }, []);

  const handleNewSession = () => {
    const newSessionId = uuidv4();
    localStorage.setItem('wecare_session_id', newSessionId);
    setSessionId(newSessionId);
  };

  if (!sessionId) {
    return <div>Loading...</div>;
  }

  return (
    <AppContainer>
      <Header onNewSession={handleNewSession} />
      <MainContent>
        <ChatWindow sessionId={sessionId} />
      </MainContent>
    </AppContainer>
  );
}

export default App;