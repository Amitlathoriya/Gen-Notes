import React, { useState } from 'react';
import './App.css';

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setNotes('');
    try {
      const formData = new FormData();
      formData.append('youtube_url', youtubeUrl);
      const response = await fetch('http://192.168.43.140:8000/generate-notes', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Failed to fetch notes');
      }
      const data = await response.json();
      setNotes(data.notes || 'No notes found.');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App animated-bg">
      <h1>YouTube Notes Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter YouTube URL"
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Notes'}
        </button>
      </form>
      {loading && (
        <div className="spinner-container">
          <div className="spinner"></div>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {notes && !loading && (
        <div className="notes-box">
          <h2>Generated Notes</h2>
          <pre style={{ textAlign: 'left', whiteSpace: 'pre-wrap' }}>{notes}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
