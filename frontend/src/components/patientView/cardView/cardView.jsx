import React from 'react';
import calculateAge from "../../helper/calculateAge";
import view_icon from "../../../assets/view.png";
import edit_icon from "../../../assets/edit.png";
import delete_icon from "../../../assets/delete.png";
import './CardView.css';

const CardView = ({ tableData, onUpdate, onDelete }) => {
    return (
        <div className="cardView">
            {tableData.length > 0 ? (
                tableData.map((patient, index) => (
                    <div className="cardView-card" key={index}>
                        <div className="cardView-info">
                            <h3>{patient.name}</h3>
                            <p>Age: {calculateAge(patient.birth_date)}</p>
                            <p>Mobile: {patient.mobile_num}</p>
                        </div>
                        <div className="operations">
                            <img src={edit_icon} alt="Edit" onClick={() => onUpdate(patient.id)} />
                            <img src={delete_icon} alt="Delete" onClick={() => onDelete(patient.id)} />
                        </div>
                    </div>
                ))
            ) : (
                <div className="no-data">No patient data available</div>
            )}
        </div>
    );
};

export default CardView;
