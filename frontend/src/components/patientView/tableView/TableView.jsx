import React from 'react';
import "./tableView.css"
import calculateAge from "../../helper/calculateAge"
import view_icon from "../../../assets/view.png"
import edit_icon from "../../../assets/edit.png";
import delete_icon from "../../../assets/delete.png"

const TableView = ({ tableData, onView, onUpdate, onDelete }) => {
    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Mobile Number</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {tableData.length > 0 ? (
                        tableData.map((patient, index) => (
                            <tr key={index}>
                                <td>{patient.id}</td>
                                <td>{patient.name}</td>
                                <td>{calculateAge(patient.birth_date)}</td> 
                                <td>{patient.mobile_num}</td>
                                <td>
                                    <div className="operations">
                                        <img src={view_icon} alt="View" onClick={() => onView(patient.id)} />
                                        <img src={edit_icon} alt="Edit" onClick={() => onUpdate(patient.id)} />
                                        <img src={delete_icon} alt="Delete" onClick={() => onDelete(patient.id)} />
                                    </div>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="5" className="no-data">No patient data available</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default TableView;