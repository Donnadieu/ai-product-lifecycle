import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Container } from "@mui/material";

import StakeholderView from "./components/StakeholderView";
import PMView from "./components/PMView";
import EngineeringView from "./components/EngineeringView";
import TicketingView from "./components/TicketingView";
import FullFeatureView from "./components/FullFeatureView";
import { QuickTest } from "./components/QuickTest";

const App: React.FC = () => {
  return (
    <Router>
      <AppBar position="static" sx={{ mb: 4 }}>
        <Toolbar>
          <Button color="inherit" component={Link} to="/">🌐 Full Flow</Button>
          <Button color="inherit" component={Link} to="/quick">⚡ Quick Test</Button>
          <Button color="inherit" component={Link} to="/stakeholder">📢 Stakeholder</Button>
          <Button color="inherit" component={Link} to="/pm">📌 PM</Button>
          <Button color="inherit" component={Link} to="/engineering">🛠 Eng</Button>
          <Button color="inherit" component={Link} to="/ticketing">🎯 Tickets</Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md">
        <Routes>
          <Route path="/" element={<FullFeatureView />} />
          <Route path="/quick" element={<QuickTest />} />
          <Route path="/stakeholder" element={<StakeholderView />} />
          <Route path="/pm" element={<PMView />} />
          <Route path="/engineering" element={<EngineeringView />} />
          <Route path="/ticketing" element={<TicketingView />} />
        </Routes>
      </Container>
    </Router>
  );
};

export default App;
