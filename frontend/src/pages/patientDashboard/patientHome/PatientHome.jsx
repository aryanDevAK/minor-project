import React from 'react'
import Chatbot from '../../../components/PatientComponents/ChatBot/ChatBot'

const PatientHome = ({ activeComponent }) => {
    const renderComponent = () => {
        switch (activeComponent) {
            case 'Dashboard':
                return <Chatbot />;
            case 'MedixifyAI':
                return <Chatbot />;
        }

    };
    return (
        <>
            <div className="admin-home-div">{renderComponent()}</div>
        </>
    )
}

export default PatientHome