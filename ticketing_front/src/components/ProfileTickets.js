import React, { useState, useEffect } from "react";
import "../css/ProfileTickets.css";
import Footer from "../components/Footer";
import Header from "../components/Header";
import { FaCalendarAlt, FaMapMarkerAlt, FaTicketAlt, FaTrash } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const options = {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    };
    const timeOptions = {
        hour: "2-digit",
        minute: "2-digit"
    };
    return `${date.toLocaleDateString("en-US", options)} at ${date.toLocaleTimeString("en-US", timeOptions)}`;
};

const mockTickets = [
    {
        id: 1,
        ticket_number: "ABC123456",
        purchase_date: "2025-06-21T19:00:00",
        event_id: 1,
        user_id: 1,
        event_name: "Coldplay - World Tour",
        location: "Paris, Accor Arena"
    },
    {
        id: 2,
        ticket_number: "XYZ987654",
        purchase_date: "2025-07-10T20:30:00",
        event_id: 2,
        user_id: 1,
        event_name: "Imagine Dragons Live",
        location: "Lyon, Halle Tony Garnier"
    }
];

const ProfileTickets = () => {
    const navigate = useNavigate();
    const [tickets, setTickets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [ticketToDelete, setTicketToDelete] = useState(null);

    // useEffect(() => {
    //     const fetchTickets = async () => {
    //         const token = localStorage.getItem("token");
    //         if (!token) {
    //             navigate("/login");
    //             return;
    //         }

    //         try {
    //             const userResponse = await fetch(`${process.env.REACT_APP_API_URL}/users/me`, {
    //                 headers: { Authorization: `Bearer ${token}` },
    //             });
    //             if (!userResponse.ok) throw new Error("Failed to fetch user.");

    //             const userData = await userResponse.json();

    //             const ticketsResponse = await fetch(`${process.env.REACT_APP_API_URL}/tickets/user/${userData.id}`, {
    //                 headers: { Authorization: `Bearer ${token}` },
    //             });
    //             if (!ticketsResponse.ok) throw new Error("Failed to fetch tickets.");

    //             const data = await ticketsResponse.json();
    //             setTickets(data);
    //         } catch (err) {
    //             setError(err.message);
    //         } finally {
    //             setLoading(false);
    //         }
    //     };

    //     fetchTickets();
    // }, [navigate]);

    useEffect(() => {
        const enrichTicketsWithEventData = async () => {
            try {
                const baseTickets = mockTickets;

                const enrichedTickets = await Promise.all(
                    baseTickets.map(async (ticket) => {
                        try {
                            const res = await fetch(`${process.env.REACT_APP_API_URL}/events/${ticket.event_id}`);
                            if (!res.ok) throw new Error("Event not found");
                            const eventData = await res.json();
                            console.log(eventData);
                            return {
                                ...ticket,
                                event_name: eventData.name,
                                location: eventData.location,
                                event_date: eventData.date
                            };
                        } catch {
                            return {
                                ...ticket,
                                event_name: "Unknown Event",
                                location: "Unknown",
                                event_date: null
                            };
                        }
                    })
                );

                setTickets(enrichedTickets);
            } catch (err) {
                setError("Failed to enrich tickets with event data.");
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        enrichTicketsWithEventData();
    }, []);

    const handleDeleteTicket = async () => {
        const token = localStorage.getItem("token");
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/tickets/${ticketToDelete.id}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
    
            if (!response.ok) throw new Error("Failed to delete ticket");
    
            setTickets(prev => prev.filter(t => t.id !== ticketToDelete.id));
            setIsDeleteModalOpen(false);
            setTicketToDelete(null);
        } catch (err) {
            console.error("Error deleting ticket:", err);
            setError("Could not delete ticket.");
        }
    };


    return (
        <>
            <Header />

            <div className="profile-tickets-content">
                <h2>My Tickets</h2>

                {loading ? (
                    <p>Loading tickets...</p>
                ) : error ? (
                    <p className="profile-tickets-error-message">{error}</p>
                ) : tickets.length === 0 ? (
                    <p>You haven't booked any tickets yet.</p>
                ) : (
                    <div className="profile-tickets-list">
                        {tickets.map((ticket) => (
                            <div className="profile-tickets-ticket-card" key={ticket.id}>
                                <div className="profile-tickets-ticket-header">
                                    <h3>🎟 {ticket.event_name}</h3>
                                    <FaTrash
                                        className="profile-tickets-delete-ticket-icon"
                                        onClick={() => {
                                            setTicketToDelete(ticket);
                                            setIsDeleteModalOpen(true);
                                        }}
                                        title="Delete Ticket"
                                    />
                                </div>
                                <p><FaCalendarAlt /> {ticket.event_date ? formatDate(ticket.event_date) : 'No event date'}</p>
                                <p><FaMapMarkerAlt /> {ticket.location}</p>
                                <p><FaTicketAlt /> Ticket #{ticket.ticket_number}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <Footer />

            {isDeleteModalOpen && (
                <div className="profile-tickets-modal-overlay">
                    <div className="profile-tickets-modal-content">
                        <h3>Delete Ticket</h3>
                        <p>Are you sure you want to delete ticket #{ticketToDelete?.ticket_number}?</p>
                        <div className="profile-tickets-modal-buttons">
                            <button className="profile-tickets-cancel-button" onClick={() => setIsDeleteModalOpen(false)}>Cancel</button>
                            <button className="profile-tickets-save-button" onClick={handleDeleteTicket}>Yes, Delete</button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default ProfileTickets;