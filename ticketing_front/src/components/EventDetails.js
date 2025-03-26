import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../css/EventDetails.css';
import Header from './Header';
import Footer from './Footer';
import { FaMapMarkerAlt, FaCalendarAlt, FaTicketAlt, FaChevronLeft } from 'react-icons/fa';

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("fr-FR", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const EventDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [event, setEvent] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchEvent = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_API_URL}/events/${id}`);
                if (!response.ok) {
                    throw new Error('Erreur lors du chargement de l’événement');
                }
                const data = await response.json();
                setEvent(data);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchEvent();
    }, [id]);

    if (error) return <div className="error-message">{error}</div>;
    if (!event) return <div className="loading">Chargement...</div>;

    const { name, location, description, date, available_tickets, total_tickets } = event;

    const soldPercentage = 100 - Math.round((available_tickets / total_tickets) * 100);

    return (
        <>
            <Header />

            <div className="event-details-component">
                <button className="event-details-back-btn" onClick={() => navigate('/')}><FaChevronLeft /><span>Retour à la liste</span></button>

                <div className="event-details-container">
                
                    <div className="event-details-header">
                        <h1>{name}</h1>
                        <div className="event-details-meta">
                            <p><FaCalendarAlt /> {formatDate(date)}</p>
                            <p><FaMapMarkerAlt /> {location}</p>
                        </div>
                    </div>

                    <div className="event-details-description">
                        <p>{description}</p>
                    </div>

                    <div className="event-details-ticket-info">
                        <p className='event-details-remaining-tickets'><FaTicketAlt /> <span>{available_tickets} billets restants</span></p>
                        <div className="event-details-ticket-progress-bar">
                            <div className="filled" style={{ width: `${soldPercentage}%` }}></div>
                        </div>
                        <p className="event-details-progress-text">{soldPercentage}% des billets vendus</p>
                    </div>
                </div>
            </div>

            <Footer />
        </>
    );
};

export default EventDetails;