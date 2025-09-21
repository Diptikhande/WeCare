import React from 'react';
import styled from 'styled-components';

const MessageListContainer = styled.div`
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MessageBubble = styled.div`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.4;
  position: relative;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  
  ${props => props.isUser ? `
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border-bottom-right-radius: 6px;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  ` : `
    background: white;
    color: #1f2937;
    border-bottom-left-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
  `}
`;

const MessageMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
`;

const SenderAvatar = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: white;
  
  ${props => props.isUser ? `
    background: linear-gradient(135deg, #f59e0b, #d97706);
    order: 1;
  ` : `
    background: linear-gradient(135deg, #10b981, #059669);
  `}
`;

const SenderName = styled.span`
  font-size: 0.8rem;
  color: #6b7280;
  font-weight: 500;
`;

const Timestamp = styled.span`
  font-size: 0.75rem;
  color: #9ca3af;
`;

const MessageContent = styled.div`
  white-space: pre-wrap;
`;

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

const MessageList = ({ messages }) => {
  return (
    <MessageListContainer>
      {messages.map((message) => (
        <div key={message.id}>
          <MessageMeta isUser={message.sender === 'user'}>
            <SenderAvatar isUser={message.sender === 'user'}>
              {message.sender === 'user' ? '👤' : '🧠'}
            </SenderAvatar>
            <SenderName>
              {message.sender === 'user' ? 'You' : 'Therapist'}
            </SenderName>
            <Timestamp>
              {formatTime(message.timestamp)}
            </Timestamp>
          </MessageMeta>
          <MessageBubble isUser={message.sender === 'user'}>
            <MessageContent>{message.content}</MessageContent>
          </MessageBubble>
        </div>
      ))}
    </MessageListContainer>
  );
};

export default MessageList;