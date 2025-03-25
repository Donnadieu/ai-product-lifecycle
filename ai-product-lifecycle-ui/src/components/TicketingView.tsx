import React, { useState } from "react";
import {
  Typography,
  TextField,
  Button,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import axios from "axios";

const TicketingView: React.FC = () => {
  const [plan, setPlan] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!plan.trim()) return;
    setLoading(true);
    setOutput(null);
    try {
      const res = await axios.post("http://localhost:8000/generate-tickets", {
        plan
      });
      setOutput(res.data.output);
    } catch (err) {
      console.error(err);
      alert("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Typography variant="h5" gutterBottom>
        🎯 Ticketing AI
      </Typography>

      <TextField
        label="Enter Engineering Plan"
        fullWidth
        value={plan}
        onChange={(e) => setPlan(e.target.value)}
        margin="normal"
        multiline
        rows={8}
      />

      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : "Generate Tasks"}
      </Button>

      {output && (
        <Accordion sx={{ mt: 3 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>🎯 Ticketing Output</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{output}</pre>
          </AccordionDetails>
        </Accordion>
      )}
    </>
  );
};

export default TicketingView;
