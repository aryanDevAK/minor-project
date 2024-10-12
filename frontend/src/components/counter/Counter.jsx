import React from 'react'
import "./counter.css"
import patient from "../../assets/person1.png"

const Counter = () => {
  return (
      <div className="flex-div main-card">
          <div className="flex-div card">
              <img src={patient} alt="" />
              <div className="info">
                  <h2>Count</h2>
                  <h3>Total Patients</h3>
              </div>
          </div>
          <div className="flex-div card">
              <img src={patient} alt="" />
              <div className="info">
                  <h2>Count</h2>
                  <h3>Total Patients</h3>
              </div>
          </div>
          <div className="flex-div card">
              <img src={patient} alt="" />
              <div className="info">
                  <h2>Count</h2>
                  <h3>Total Patients</h3>
              </div>
          </div>
          <div className="flex-div card">
              <img src={patient} alt="" />
              <div className="info">
                  <h2>Count</h2>
                  <h3>Total Patients</h3>
              </div>
          </div>
          <div className="flex-div card">
              <img src={patient} alt="" />
              <div className="info">
                  <h2>Count</h2>
                  <h3>Total Patients</h3>
              </div>
          </div>
    </div>
  )
}

export default Counter