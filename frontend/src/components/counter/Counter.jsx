import React from 'react';
import "./counter.css";
import patient from "../../assets/person1.png";

const Counter = ({ tableData = [] }) => { // Default value to an empty array
  const totalPatients = tableData.length; // Calculating total number of patients from tableData

  return (
    <div className="flex-div main-card">
      <div className="flex-div card">
        <img src={patient} alt="Patient Icon" />
        <div className="info">
          <h2>{totalPatients}</h2> {/* Display patient count */}
          <h3>Total Patients</h3>
        </div>
      </div>
      <div className="flex-div card">
        <img src={patient} alt="Patient Icon" />
        <div className="info">
          <h2>{totalPatients}</h2> {/* Reuse totalPatients for other sections */}
          <h3>Total Patients</h3>
        </div>
      </div>
      <div className="flex-div card">
        <img src={patient} alt="Patient Icon" />
        <div className="info">
          <h2>{totalPatients}</h2>
          <h3>Total Patients</h3>
        </div>
      </div>
    </div>
  );
};

export default Counter;
