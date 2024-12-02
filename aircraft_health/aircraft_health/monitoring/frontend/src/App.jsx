// frontend/src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import ADAPTDashboard from './components/ADAPTDashboard';
import LandingPage from './components/Landingpage';
import Navigation from './components/Navigation';

function App() {
    return (
        <Router>
            <Navigation />
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/dashboard" element={<ADAPTDashboard />} />
                {/* Fallback route for any other paths */}
                <Route path="*" element={<LandingPage />} />
            </Routes>
        </Router>
    );
}

export default App;