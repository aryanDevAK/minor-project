import React, { useState, useEffect } from 'react';
import add_icon from "../../assets/add_box.png";
import list_view from "../../assets/list_view.png";
import grid_view from "../../assets/grid_view.png";
import Counter from '../counter/Counter';
import TableView from '../tableView/TableView';
import ClipLoader from "react-spinners/ClipLoader";
import Notification from '../../components/notification/Notification';
import "./Patient.css";
import Modal from '../patientForm/Modal';
import CardView from '../cardView/CardView';

const Patient = () => {
  const [tableData, setTableData] = useState([]); // State to store patient data
  const [loading, setLoading] = useState(true); // State to handle loading
  const [error, setError] = useState(null); // State to handle errors
  const [notificationMessage, setNotificationMessage] = useState(""); // State to handle notifications
  const [showModal, setShowModal] = useState(false); // State to manage modal visibility
  const [newPatient, setNewPatient] = useState({ name: '', birthDate: '', mobileNum: '' });
  const [isListView, setIsListView] = useState(true);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('https://minor-project-dxsv.onrender.com/get/patients', {
          method: "GET",
          headers: {
            "Content-Type": 'application/json',
            Authorization: `Bearer ${token}`,
          }
        });
  
        if (!response.ok) {
          throw new Error('Failed to fetch patients');
        }
  
        const data = await response.json();
        setTableData(data); // Set the patient data in your table state
        setNotificationMessage("Patients loaded successfully!");
        setTimeout(() => setNotificationMessage(""), 2000); // Clear notification after 2 seconds
  
      } catch (error) {
        setError('Error loading patients. Please try again later.');
        setNotificationMessage(error.message); // Set the error message as notification
        setTimeout(() => setNotificationMessage(""), 2000); // Clear error notification after 2 seconds
  
      } finally {
        setLoading(false);
      }
    };
  
    fetchPatients();
  }, []);
   
  const handleInputChange = (e) => {
    setNewPatient({ ...newPatient, [e.target.name]: e.target.value });
  };

  const handleRegisterPatient = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('https://minor-project-dxsv.onrender.com/register/patient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          'name': newPatient.name,
          'birth-date': newPatient.birthDate,
          'mobile-num': newPatient.mobileNum,
        }),
      });
      
      if (response.ok) {
        const responseData = await response.json();
        setTableData([...tableData, responseData]);
        setNotificationMessage("Patient registered successfully!");
        setTimeout(() => setNotificationMessage(""), 2000);
        setShowModal(false); // Close the modal
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Error registering patient");
        setNotificationMessage(errorData.message || "Error registering patient");
        setTimeout(() => setNotificationMessage(""), 2000);
      }
    } catch (error) {
      setError("An error occurred while registering the patient.");
      setNotificationMessage("An error occurred while registering the patient.");
      setTimeout(() => setNotificationMessage(""), 2000);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleView = (view) => {
    setIsListView(view === 'list');
  };

  return (
    <>
      <Counter />
      <div className='flex-div middle-div'>
        <img src={add_icon} alt="" className='icon' onClick={() => setShowModal(true)}/>
        <img src={list_view} alt="" className='icon' onClick={() => handleToggleView('list')}/>
        <img src={grid_view} alt="" className='icon' onClick={() => handleToggleView('grid')}/>
      </div>
      {/* Loader while fetching data */}
      {loading && (
        <div className="loader">
          <ClipLoader color="#093594" size={50} />
        </div>
      )}

      {/* Notification */}
      {notificationMessage && (
        <Notification message={notificationMessage} type="success" />
      )}

      {/* Conditionally render TableView or CardView based on isListView */}
      <div>
        {isListView ? <TableView tableData={tableData} /> : <CardView tableData={tableData} />} {/* Switch views */}
      </div>

      {/* Modal for patient registration */}
      <Modal show={showModal} onClose={() => setShowModal(false)}>
        <h2>Register New Patient</h2>
        <form onSubmit={handleRegisterPatient}>
          <div className="form-group">
            <label>Name:</label>
            <input type="text" name="name" value={newPatient.name} onChange={handleInputChange} required />
          </div>
          <div className="form-group">
            <label>Birth Date:</label>
            <input type="date" name="birthDate" value={newPatient.birthDate} onChange={handleInputChange} required />
          </div>
          <div className="form-group">
            <label>Mobile Number:</label>
            <input type="text" name="mobileNum" value={newPatient.mobileNum} onChange={handleInputChange} required />
          </div>
          <button type="submit" className="btn">Register</button>
        </form>
      </Modal>
    </>
  );
};

export default Patient;
