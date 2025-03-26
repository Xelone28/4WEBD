import React from "react";
import "../css/EventCard.css";

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("fr-FR", {
        weekday: "short",
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const EventCard = ({ event }) => {
    const { name, description, location, date, available_tickets, total_tickets } = event;

    const soldPercentage = 100 - Math.round((available_tickets / total_tickets) * 100);

    return (
        <div className="event-card">
            <div className="event-card-content">
                <h3 className="event-title">{name}</h3>
                <p className="event-date">{formatDate(date)}</p>
                <p className="event-location">{location}</p>
                <p className="event-description">{description}</p>
                <div className="event-progress">
                    <div className="progress-bar">
                        <div
                            className="progress-filled"
                            style={{ width: `${soldPercentage}%` }}
                        />
                    </div>
                    <span className="progress-text">
                        {available_tickets} billets restants / {total_tickets}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default EventCard;