import React, { useState } from "react";
import {
  TextField,
  Button,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  CircularProgress
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import axios from "axios";

// Use environment variable or default to localhost in development
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

type AgentOutput = Record<string, string>;

const emojiMap: Record<string, string> = {
  "StakeholderAI": "📢",
  "ProductManagerAI": "📌",
  "EngineeringAI": "🛠",
  "TicketingAI": "🎯"
};

function splitByAgent(output: string): AgentOutput {
  const result: AgentOutput = {};
  const sections = output.split(/###\s+/).filter(Boolean);

  for (const section of sections) {
    const [nameLine, ...contentLines] = section.split("\n");
    // Extract just the agent name without the colon
    const agentName = nameLine.split(":")[0].trim();
    const content = contentLines.join("\n").trim();
    result[agentName] = content;
  }

  return result;
}

const FullFeatureView: React.FC = () => {
  const [idea, setIdea] = useState<string>("");
  const [output, setOutput] = useState<AgentOutput | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    if (!idea.trim()) return;
    setLoading(true);
    setOutput(null);
    try {
      const response = await axios.post(`${API_URL}/build-feature/`, {
        idea
      });
      
      // Get the combined output from all agents
      const combinedOutput = [
        `### StakeholderAI:\n${response.data.stakeholder}`,
        `### ProductManagerAI:\n${response.data.prd}`,
        `### EngineeringAI:\n${response.data.engineering}`,
        `### TicketingAI:\n${response.data.tickets}`
      ].join('\n\n');
      
      const agentSections = splitByAgent(combinedOutput);
      setOutput(agentSections);
    } catch (error: any) {
      console.error("Error:", error);
      const message = error.response?.data?.detail || error.message || "Something went wrong!";
      alert(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Typography variant="h4" gutterBottom>
        🧠 AI Product Team Demo
      </Typography>

      <TextField
        label="Enter a product idea"
        fullWidth
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        margin="normal"
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        disabled={loading}
        sx={{ mb: 4 }}
      >
        {loading ? <CircularProgress size={24} /> : "Generate"}
      </Button>

      {output &&
        Object.entries(output).map(([agent, content]) => {
          const emoji = emojiMap[agent] || "💬";
          return (
            <Accordion key={agent}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>
                  {emoji} {agent}
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                  {content}
                </pre>
              </AccordionDetails>
            </Accordion>
          );
        })}
    </>
  );
};

export default FullFeatureView;
