import React from 'react';
import "./counter.css";
import patient from "../../assets/person1.png";

const Counter = ({ counts }) => {
  // Convert counts object to an array of values
  const countArray = Object.values(counts);

  return (
    <div className="flex-div main-card">
      {countArray.map((count, index) => (
        <div key={index} className="card">
            <h2>{count.count}</h2> {/* Display the count */}
            <h3>{count.name}</h3> {/* Display the name */}
        </div>
      ))}
    </div>
  );
};

export default Counter;
