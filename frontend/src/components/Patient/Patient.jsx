import React, { useState, useEffect } from 'react';
import add_icon from "../../assets/add_box.png";
import list_view from "../../assets/list_view.png";
import grid_view from "../../assets/grid_view.png";
import Counter from '../counter/Counter';
import TableView from '../patientView/tableView/TableView';
import ClipLoader from "react-spinners/ClipLoader";
import Notification from '../../components/notification/Notification';
import "./Patient.css";
import Modal from '../patientView/patientForm/Modal';
import CardView from '../patientView/cardView/CardView';

const Patient = () => {
    const [tableData, setTableData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [notificationMessage, setNotificationMessage] = useState("");
    const [showModal, setShowModal] = useState(false);
    const [newPatient, setNewPatient] = useState({ name: '', birthDate: '', mobileNum: '' });
    const [selectedPatient, setSelectedPatient] = useState(null);
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
                setTableData(data);
                setNotificationMessage("Patients loaded successfully!");
                setTimeout(() => setNotificationMessage(""), 2000);

            } catch (error) {
                setError('Error loading patients. Please try again later.');
                setNotificationMessage(error.message);
                setTimeout(() => setNotificationMessage(""), 2000);
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
                setShowModal(false);
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

    const handleViewPatient = (id) => {
        console.log(`Viewing patient with ID: ${id}`);
        // Additional view logic can be implemented here
    };

    const handleUpdatePatient = (id) => {
        const patientToEdit = tableData.find(patient => patient.id === id);
        setSelectedPatient(patientToEdit);
        setNewPatient({
            name: patientToEdit.name,
            birthDate: patientToEdit.birth_date,
            mobileNum: patientToEdit.mobile_num
        });
        setShowModal(true);
    };

    const handleDeletePatient = async (id) => {
        const confirmDelete = window.confirm("Are you sure you want to delete this patient?");
        if (confirmDelete) {
            setLoading(true);
            try {
                const token = localStorage.getItem('access_token');
                const response = await fetch(`https://minor-project-dxsv.onrender.com/delete/patient/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    setTableData(tableData.filter(patient => patient.id !== id));
                    setNotificationMessage("Patient deleted successfully!");
                    setTimeout(() => setNotificationMessage(""), 2000);
                } else {
                    const errorData = await response.json();
                    setError(errorData.message || "Error deleting patient");
                    setNotificationMessage(errorData.message || "Error deleting patient");
                    setTimeout(() => setNotificationMessage(""), 2000);
                }
            } catch (error) {
                setError("An error occurred while deleting the patient.");
                setNotificationMessage("An error occurred while deleting the patient.");
                setTimeout(() => setNotificationMessage(""), 2000);
            } finally {
                setLoading(false);
            }
        }
    };

    const handleEditPatient = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`https://minor-project-dxsv.onrender.com/update/patient/${selectedPatient.id}`, {
                method: 'PUT',
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
                const updatedPatient = await response.json();
                setTableData(tableData.map(patient => (patient.id === updatedPatient.id ? updatedPatient : patient)));
                setNotificationMessage("Patient updated successfully!");
                setTimeout(() => setNotificationMessage(""), 2000);
                setShowModal(false);
                setSelectedPatient(null);
            } else {
                const errorData = await response.json();
                setError(errorData.message || "Error updating patient");
                setNotificationMessage(errorData.message || "Error updating patient");
                setTimeout(() => setNotificationMessage(""), 2000);
            }
        } catch (error) {
            setError("An error occurred while updating the patient.");
            setNotificationMessage("An error occurred while updating the patient.");
            setTimeout(() => setNotificationMessage(""), 2000);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Counter tableData={tableData} />
            <div className='flex-div middle-div operations'>
                <img src={add_icon} alt="" className='icon' onClick={() => {
                    setNewPatient({ name: '', birthDate: '', mobileNum: '' });
                    setShowModal(true);
                }} />
                <img src={list_view} alt="" className='icon' onClick={() => handleToggleView('list')} />
                <img src={grid_view} alt="" className='icon' onClick={() => handleToggleView('grid')} />
            </div>

            {loading && (
                <div className="loader">
                    <ClipLoader color="#093594" size={50} />
                </div>
            )}

            {notificationMessage && (
                <Notification message={notificationMessage} type="success" />
            )}

            <div>
                {isListView ? 
                    <TableView 
                        tableData={tableData} 
                        onView={handleViewPatient} 
                        onUpdate={handleUpdatePatient} 
                        onDelete={handleDeletePatient} 
                    /> 
                    : <CardView tableData={tableData} 
                    onView={handleViewPatient} 
                    onUpdate={handleUpdatePatient} 
                    onDelete={handleDeletePatient} />
                }
            </div>

            <Modal show={showModal} onClose={() => setShowModal(false)}>
                <h2>{selectedPatient ? "Edit Patient" : "Register New Patient"}</h2>
                <form onSubmit={selectedPatient ? handleEditPatient : handleRegisterPatient}>
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
                    <button className='btn' type="submit">{selectedPatient ? "Update Patient" : "Register Patient"}</button>
                </form>
            </Modal>
        </>
    );
};

export default Patient;
