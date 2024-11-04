import './App.css';
import LoginCard from '../src/components/loginCard/LoginCard';
import LoginPageStaff from './pages/loginStaff/LoginStaff';
import LoginPagePatient from './pages/loginPatient/LoginPatient';
import AdminDashboard from './pages/admin/Admin';
// import DoctorDashboard from './pages/DoctorDashboard';
// import NurseDashboard from './pages/NurseDashboard';
// import StaffDashboard from './pages/StaffDashboard';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import doctor from "./assets/stethoscope_white.png"
import person1 from "./assets/person1.png"
import nurse from "./assets/nurse.png"
import logo from "./assets/logo-color.png"
import PatientDashboard from './pages/patientDashboard/PatientDashboard';

function App() {
  const [loginPage, setLoginPage] = useState(null);

  const handleLoginClick = (name) => {
    if (name.toLowerCase() === 'patient') {
      setLoginPage('patient');
    } else {
      setLoginPage('staff');
    }
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Default route for "/" */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          
          {/* Login routes */}
          <Route path="/login" element={
            loginPage ? (loginPage === 'staff' ? (<LoginPageStaff />) : (<LoginPagePatient />)) : (
              <div>
                <img className='logo-main' src={logo} alt="logo" />
                <div className="cont">
                  <div className='cont-left'>
                    <LoginCard myClass="right" name="Hospital Administration" data="Click the button below to log in using your hospital ID and password, granting you access to manage patient records and essential healthcare tasks efficiently." onClick={handleLoginClick} image={doctor} buttonname={"For Hospital Staff"} btnClass={"btn"} />
                  </div>
                  <div className="cont-right">
                    <LoginCard myClass="left" name="Patient" data="Log in with your registered mobile number to access your health dashboard, monitor medical records, manage appointments, and use Medixify’s AI Assistant for health guidance and support." onClick={handleLoginClick} image={person1} buttonname={"For Patient"} btnClass={"btn-border"} />
                  </div>
                </div>
              </div>
            )
          } />

          {/* Dashboard routes */}
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/patient-dashboard" element={<PatientDashboard/>} />
          {/* Uncomment and add other dashboard routes as needed */}
          {/* <Route path="/doctor-dashboard" element={<DoctorDashboard />} />
          <Route path="/nurse-dashboard" element={<NurseDashboard />} />
          <Route path="/staff-dashboard" element={<StaffDashboard />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
