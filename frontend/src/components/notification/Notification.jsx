import React from 'react'
import "./notification.css"

const Notification = ({message,type}) => {
  return (
      <div>
          <div className={`notification ${type}`}>
              <h3>{message}</h3>
          </div>
    </div>
  )
}

export default Notification