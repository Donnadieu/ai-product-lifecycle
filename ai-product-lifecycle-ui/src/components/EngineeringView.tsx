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

const EngineeringView: React.FC = () => {
  const [prd, setPrd] = useState("");
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!prd.trim()) return;
    setLoading(true);
    setOutput(null);
    try {
      const res = await axios.post("http://localhost:8000/generate-engineering-plan", {
        prd
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
        🛠 Engineering AI
      </Typography>

      <TextField
        label="Enter Product Requirements Document (PRD)"
        fullWidth
        value={prd}
        onChange={(e) => setPrd(e.target.value)}
        margin="normal"
        multiline
        rows={8}
      />

      <Button variant="contained" color="primary" onClick={handleSubmit} disabled={loading}>
        {loading ? <CircularProgress size={24} /> : "Generate Engineering Plan"}
      </Button>

      {output && (
        <Accordion sx={{ mt: 3 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>🛠 Engineering Output</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>{output}</pre>
          </AccordionDetails>
        </Accordion>
      )}
    </>
  );
};

export default EngineeringView;
