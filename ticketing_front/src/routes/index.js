import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../views/Home';
import EventDetails from '../views/EventDetails';
import Login from '../views/Login';
import Register from '../views/Register';
import Profile from '../views/Profile';

const AppRoutes = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/event/:id" element={<EventDetails />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/profile" element={<Profile />} />
            </Routes>
        </Router>
    );
};

export default AppRoutes;