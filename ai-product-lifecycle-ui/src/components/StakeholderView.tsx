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

const StakeholderView: React.FC = () => {
  const [idea, setIdea] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!idea.trim()) return;
    setLoading(true);
    setOutput(null);
    try {
      const res = await axios.post("http://localhost:8000/generate-stakeholder-requirements", {
        idea
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
        📢 Stakeholder AI
      </Typography>

      <TextField
        label="Enter product idea"
        fullWidth
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        margin="normal"
      />

      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : "Generate Stakeholder Requirements"}
      </Button>

      {output && (
        <Accordion sx={{ mt: 3 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>📢 Stakeholder Output</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{output}</pre>
          </AccordionDetails>
        </Accordion>
      )}
    </>
  );
};

export default StakeholderView;
