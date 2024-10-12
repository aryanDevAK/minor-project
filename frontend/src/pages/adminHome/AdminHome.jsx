import React from 'react'
import "./adminhome.css"
import Counter from '../../components/counter/Counter'
import Dashboard from '../../components/home-component/Dashboard'
import Patient from '../../components/Patient/Patient'

const AdminHome = ({ activeComponent }) => {
    const renderComponent = () => {
        switch (activeComponent) {
          case 'Dashboard':
            return <Dashboard />;
          case 'Patient':
            return <Patient />;
          case 'Nurse':
            return <Patient />;
          case 'Doctor':
            return <Patient />;
          case 'Staff':
            return <Patient />;
          case 'Labs':
            return <Patient />;
          case 'Appointments':
            return <Patient />;
          case 'Pharmacies':
            return <Patient />;
          case 'Reports':
            return <Counter />;
          case 'Inventory':
            return <Dashboard />;
            case "Settings":
            return <Dashboard/>    
          default:
            return <Dashboard />;
        }
      };
    return (
        <>
            <Counter />
            <div className="admin-home-div">{renderComponent()}</div>
        </>
  )
}

export default AdminHome