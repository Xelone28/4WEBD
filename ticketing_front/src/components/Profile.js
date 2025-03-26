import React from "react";
import "../css/Profile.css";
import Footer from "../components/Footer";
import Header from "../components/Header";


const Profile = () => {

    return (
        <>
            <Header />

            <div className="profile-content">
                <h2>My Profile</h2>
            </div>


            <Footer />
        </>
    );
};

export default Profile;