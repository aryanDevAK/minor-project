import React, { useState } from 'react';
import axios from 'axios';
import './Chatbot.css'; // Import the CSS file

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message) return;

    const userMessage = { sender: 'user', text: message };
    setChatHistory([...chatHistory, userMessage]);

    setLoading(true);

    try {
      const res = await axios.post('http://127.0.0.1:5000/medixify/chatbot', {
        message: message,
      });

      const botMessage = { sender: 'Medixify AI', text: res.data.reply };
      setChatHistory((prev) => [...prev, botMessage]);

    } catch (error) {
      const errorMessage = { sender: 'Medixify AI', text: 'Error communicating with the chatbot.' };
      setChatHistory((prev) => [...prev, errorMessage]);
    }

    setMessage('');
    setLoading(false);
  };

  return (
    <div className="chat-container">
      <h2>Medixify HealthCare AI</h2>
      <div className="chat-box">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender === 'user' ? '' : 'bot'}`}>
            <strong>{msg.sender}:</strong> {msg.text}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask me something..."
          className="input"
        />
        <button type="submit" className="btn">
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default Chatbot;
