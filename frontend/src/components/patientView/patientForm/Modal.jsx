import React from 'react';
import './Modal.css';

const Modal = ({ show, onClose, children }) => {
  if (!show) return null; // Don't render the modal if `show` is false

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}> {/* Prevent click events from closing modal */}
        <div className="modal-header">
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
