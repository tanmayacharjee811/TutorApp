import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [classNum, setClassNum] = useState('');
  const [subject, setSubject] = useState('');
  const [points, setPoints] = useState(0);
  const [badge, setBadge] = useState('');

  const sendMessage = () => {
    fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: `Class ${classNum}, ${subject}: ${message}` })
    })
    .then(res => res.json())
    .then(data => {
      setResponse(data.response);
      setPoints(data.points);
      setBadge(data.badge);
    });
  };

  const uploadImage = (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      setResponse(data.response);
      setPoints(data.points);
      setBadge(data.badge);
    });
  };

  return (
    <div>
      <h1>Tutor App</h1>
      <select onChange={(e) => setClassNum(e.target.value)}>
        <option value="">Select Class</option>
        {[...Array(12)].map((_, i) => (
          <option value={i + 1}>{i + 1}</option>
        ))}
      </select>
      <select onChange={(e) => setSubject(e.target.value)}>
        <option value="">Select Subject</option>
        <option value="Math">Math</option>
        <option value="Science">Science</option>
        <option value="Social Studies">Social Studies</option>
        <option value="Languages">Languages</option>
      </select>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your question"
      />
      <button onClick={sendMessage}>Send</button>
      <input type="file" onChange={uploadImage} />
      <p><strong>Answer:</strong> {response}</p>
      <p><strong>Points:</strong> {points} | <strong>Badge:</strong> {badge}</p>
    </div>
  );
}

export default App;