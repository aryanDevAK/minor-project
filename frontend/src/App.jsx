import './App.css';
import LoginCard from './components/LoginCard';
import LoginPageStaff from "./pages/LoginStaff";
import LoginPagePatient from "./pages/LoginPatient";
import { useState } from 'react';

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
    <div className="App">
      {loginPage ? (
        loginPage === 'staff' ? <LoginPageStaff /> : <LoginPagePatient />
      ) : (
        <div className="cont">
          <LoginCard name="Doctor" data="Login as a doctor to manage your patients and schedule." onClick={handleLoginClick} />
          <LoginCard name="Nurse" data="Login as a nurse to manage patient care and tasks." onClick={handleLoginClick} />
          <LoginCard name="Staff" data="Login as a staff member to access administrative services." onClick={handleLoginClick} />
          <LoginCard name="Patient" data="Login as a patient to view your medical records and appointments." onClick={handleLoginClick} />
        </div>
      )}
    </div>
  );
}

export default App;