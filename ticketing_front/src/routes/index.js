import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../views/Home';
import EventDetails from '../views/EventDetails';

const AppRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/event/:id" element={<EventDetails />} />
            </Routes>
        </Router>
    );
};

export default AppRoutes;