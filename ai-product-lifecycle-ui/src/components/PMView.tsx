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

const PMView: React.FC = () => {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setOutput(null);
    try {
      const res = await axios.post("http://localhost:8000/generate-pm-specs", {
        idea: input
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
        📌 Product Manager AI
      </Typography>

      <TextField
        label="Enter stakeholder input or product idea"
        fullWidth
        value={input}
        onChange={(e) => setInput(e.target.value)}
        margin="normal"
      />

      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : "Generate PRD"}
      </Button>

      {output && (
        <Accordion sx={{ mt: 3 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>📌 Product Manager Output</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{output}</pre>
          </AccordionDetails>
        </Accordion>
      )}
    </>
  );
};

export default PMView;
