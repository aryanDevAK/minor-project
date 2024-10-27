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
import doctor from "./assets/sthetescope.png"
import person1 from "./assets/person1.png"
import nurse from "./assets/nurse.png"
import logo from "./assets/logo-black.png"
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
                <LoginCard name="Doctor" data="Login as a doctor with your id and password. Treat well!" onClick={handleLoginClick} image={doctor} />
                <LoginCard name="Medical Staff" data="Login as a staff and ensure the operations of hospital run smoothly." onClick={handleLoginClick} image={nurse} />
                <LoginCard name="Staff" data="Login as a staff member to access administrative services." onClick={handleLoginClick} image={person1} />
                <LoginCard name="Patient" data="Login as a patient with your registered mobile number to monitor your health" onClick={handleLoginClick} image={person1} />
              </div></div>
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
