import React, { useState } from 'react';
import { Box, Button, TextField, Typography, CircularProgress, Paper } from '@mui/material';

interface QuickTestResponse {
  summary: string;
  key_features: string[];
  technical_stack: string[];
  challenges: string[];
}

export const QuickTest: React.FC = () => {
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QuickTestResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:8000/quick-test/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to analyze idea');
      }

      const rawData = await res.json();
      try {
        // Try to parse the response string as JSON
        const data = typeof rawData === 'string' ? JSON.parse(rawData) : rawData;
        setResponse(data);
      } catch (parseError) {
        // If parsing fails, show the raw response
        setError('Failed to parse LLM response as JSON. Raw response: ' + rawData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Quick Product Analysis
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          multiline
          rows={4}
          variant="outlined"
          label="Enter your product idea"
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          sx={{ mb: 2 }}
        />
        
        <Button 
          variant="contained" 
          type="submit" 
          disabled={loading || !idea.trim()}
          sx={{ mb: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Analyze'}
        </Button>
      </form>

      {error && (
        <Paper sx={{ p: 2, mb: 2, bgcolor: '#ffebee' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}

      {response && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>Summary</Typography>
          <Typography paragraph>{response.summary}</Typography>

          <Typography variant="h6" gutterBottom>Key Features</Typography>
          <ul>
            {response.key_features.map((feature, i) => (
              <Typography component="li" key={i}>{feature}</Typography>
            ))}
          </ul>

          <Typography variant="h6" gutterBottom>Technical Stack</Typography>
          <ul>
            {response.technical_stack.map((tech, i) => (
              <Typography component="li" key={i}>{tech}</Typography>
            ))}
          </ul>

          <Typography variant="h6" gutterBottom>Challenges</Typography>
          <ul>
            {response.challenges.map((challenge, i) => (
              <Typography component="li" key={i}>{challenge}</Typography>
            ))}
          </ul>
        </Paper>
      )}
    </Box>
  );
};
