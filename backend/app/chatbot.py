import os
import json
import logging
import re
from typing import List, Dict, Any
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class TherapistChatbot:
    def __init__(self):
        """Initialize the therapist chatbot with simple pattern matching"""
        self.data_path = os.getenv('CHROMA_DB_PATH', './data')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_path, exist_ok=True)
        
        # Chat sessions storage
        self.chat_sessions = {}
        
        # Initialize therapist knowledge base with pattern-response mapping
        self.knowledge_base = self._initialize_therapist_knowledge()
        
        logger.info("Therapist chatbot initialized successfully")
    
    def _initialize_therapist_knowledge(self):
        """Initialize the knowledge base with pattern-response mapping"""
        logger.info("Initializing therapist knowledge base...")
        
        return {
            # Greeting patterns
            r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b': [
                "Hello, I'm here to listen and support you. How are you feeling today? Please feel free to share what's on your mind.",
                "Hi there! It's good to see you. How are you doing today? I'm here to listen to whatever you'd like to share.",
                "Hello! Welcome. I'm glad you're here. What's been on your mind lately?"
            ],
            
            # Anxiety patterns
            r'\b(anxious|anxiety|worried|stress|panic|nervous|overwhelmed)\b': [
                "I understand you're feeling anxious. That's completely normal and valid. Let's take a moment to breathe together. Can you tell me more about what's causing these feelings?",
                "Anxiety can feel overwhelming, but you're not alone in this. It takes courage to acknowledge these feelings. What specific situations or thoughts are triggering your anxiety?",
                "I hear that you're experiencing stress and worry. These feelings are very common. Would you like to talk about what's been weighing on your mind?"
            ],
            
            # Depression patterns
            r'\b(depressed|depression|sad|low|down|hopeless|empty|lonely)\b': [
                "I hear that you're going through a difficult time. It takes courage to reach out and talk about these feelings. You're not alone in this. What has been particularly challenging for you lately?",
                "Depression can make everything feel heavy and difficult. Thank you for sharing this with me. You've taken an important step by reaching out. How long have you been feeling this way?",
                "I'm sorry you're experiencing these low feelings. Your emotions are valid, and it's important that you're talking about them. What does a typical day look like for you right now?"
            ],
            
            # Relationship patterns
            r'\b(relationship|partner|boyfriend|girlfriend|marriage|divorce|breakup|conflict)\b': [
                "Relationships can be complex and challenging. It sounds like you're dealing with some difficulties. Would you like to share more about what's happening in your relationship?",
                "Relationship issues can be emotionally draining. I'm here to listen without judgment. What aspects of your relationship are causing you the most concern?",
                "It sounds like you're navigating some relationship challenges. These situations can be really tough. How are you feeling about everything that's going on?"
            ],
            
            # Work stress patterns
            r'\b(work|job|boss|career|deadline|pressure|workplace|colleague)\b': [
                "Work-related stress is very common, and it's important to address it. It sounds like you're feeling overwhelmed. What aspects of your work are causing you the most stress?",
                "Job stress can really impact our well-being. Thank you for bringing this up. Can you tell me more about what's happening at work that's affecting you?",
                "Workplace challenges can be particularly draining. You're right to seek support. What would you say is the biggest source of stress in your work environment?"
            ],
            
            # Self-esteem patterns
            r'\b(self esteem|confidence|worth|worthless|failure|not good enough|insecure)\b': [
                "Your feelings about yourself matter, and I want you to know that you have inherent worth. Self-esteem can fluctuate, and that's part of being human. What's been affecting how you see yourself?",
                "I hear you're struggling with self-worth, and that must be really painful. You are valuable just as you are. Can you tell me about when these feelings started or what triggers them?",
                "Self-doubt can be so difficult to deal with. Thank you for sharing something so personal. What are some of the thoughts that go through your mind about yourself?"
            ],
            
            # Sleep patterns
            r'\b(sleep|insomnia|tired|exhausted|can\'t sleep|nightmares)\b': [
                "Sleep issues can really impact how we feel and function. It's important to address this. Can you tell me about your sleep patterns and what might be keeping you awake?",
                "Sleep problems are more common than you might think. They can affect everything else in our lives. How long have you been having trouble sleeping?",
                "I understand that sleep difficulties can be frustrating and exhausting. What does your typical bedtime routine look like?"
            ],
            
            # Family patterns
            r'\b(family|parents|mother|father|children|siblings|home)\b': [
                "Family relationships can be both rewarding and challenging. It sounds like you're experiencing some difficulties. Would you like to talk about what's happening with your family?",
                "Family dynamics can be complex and emotionally charged. I'm here to listen to whatever you'd like to share about your family situation.",
                "Family issues can be particularly difficult because these relationships are so important to us. What's been going on with your family that's concerning you?"
            ],
            
            # Trauma patterns
            r'\b(trauma|abuse|assault|accident|loss|grief|death|hurt)\b': [
                "Thank you for trusting me with something so personal. Trauma can have lasting effects, and it's brave of you to address it. We can work through this together at your pace. How are you feeling right now?",
                "I'm so sorry you've experienced trauma. It takes tremendous courage to talk about these experiences. Please know that you're in a safe space here. What kind of support do you feel you need right now?",
                "Trauma affects everyone differently, and there's no right or wrong way to feel about it. Thank you for sharing this with me. How has this been impacting your daily life?"
            ],
            
            # Anger patterns
            r'\b(angry|mad|furious|rage|frustrated|irritated|upset)\b': [
                "It's okay to feel angry - anger is a valid emotion that tells us something needs attention. Let's explore what's behind these feelings. What's been triggering your anger?",
                "I can hear that you're feeling really frustrated and upset. Anger often masks other emotions like hurt or fear. What do you think might be underneath these angry feelings?",
                "Thank you for sharing your anger with me. These feelings are completely valid. Can you tell me about what situations or thoughts seem to trigger these feelings most?"
            ],
            
            # Coping patterns
            r'\b(coping|help|strategies|techniques|better|improve|manage)\b': [
                "It's great that you're looking for healthy coping strategies. There are many techniques we can explore together, such as mindfulness, breathing exercises, and cognitive reframing. What has helped you in the past?",
                "I'm glad you're seeking ways to cope better. That shows real strength and self-awareness. What kinds of situations do you most need coping strategies for?",
                "Looking for coping techniques is a positive step. Different strategies work for different people. Are you looking for ways to manage specific emotions or situations?"
            ],
            
            # Crisis patterns
            r'\b(suicide|kill myself|hurt myself|end it all|can\'t go on)\b': [
                "I'm very concerned about your safety right now. If you're having thoughts of hurting yourself, please reach out to emergency services immediately or call 988 (Suicide & Crisis Lifeline). Your life has value, and help is available. Can you tell me if you're safe right now?"
            ],
            
            # Positive patterns
            r'\b(better|good|progress|improving|happy|grateful|thankful)\b': [
                "It's wonderful to hear about your progress! Growth and healing take time, and celebrating these moments is important. What changes have you noticed in yourself?",
                "I'm so glad to hear that you're feeling better. What do you think has contributed to this positive change?",
                "That's really encouraging to hear! Progress isn't always linear, but it sounds like you're moving in a positive direction. What's been helping you the most?"
            ]
        }
    
    def get_response(self, user_message: str, session_id: str = "default") -> str:
        """Get a response from the therapist chatbot using pattern matching"""
        try:
            # Store user message in session
            if session_id not in self.chat_sessions:
                self.chat_sessions[session_id] = []
            
            self.chat_sessions[session_id].append({
                "role": "user",
                "message": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Convert message to lowercase for pattern matching
            message_lower = user_message.lower()
            
            # Find matching patterns
            matched_responses = []
            for pattern, responses in self.knowledge_base.items():
                if re.search(pattern, message_lower):
                    matched_responses.extend(responses)
            
            # Select response
            if matched_responses:
                # Simple selection - could be improved with more sophisticated logic
                import random
                response = random.choice(matched_responses)
                category = "matched"
            else:
                # Default response if no pattern matches
                default_responses = [
                    "I'm here to listen and support you. Could you tell me a bit more about what you're experiencing? Sometimes it helps to talk through your feelings.",
                    "Thank you for sharing that with me. I can see this is important to you. Can you help me understand more about what you're going through?",
                    "I hear you, and I want to make sure I understand. Could you elaborate on what you're feeling or what's been on your mind?",
                    "It sounds like there's a lot going on for you. I'm here to listen. What feels most important for you to talk about right now?"
                ]
                import random
                response = random.choice(default_responses)
                category = "default"
            
            # Store bot response in session
            self.chat_sessions[session_id].append({
                "role": "therapist",
                "message": response,
                "category": category,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I'm having trouble processing your message right now. Could you please try again?"
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        return self.chat_sessions.get(session_id, [])
    
    def reset_session(self, session_id: str):
        """Reset a chat session"""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
    
    def add_knowledge(self, pattern: str, response: str, category: str):
        """Add new knowledge to the pattern database"""
        try:
            if pattern not in self.knowledge_base:
                self.knowledge_base[pattern] = []
            self.knowledge_base[pattern].append(response)
            logger.info(f"Added new knowledge item: {category}")
        except Exception as e:
            logger.error(f"Error adding knowledge: {str(e)}")