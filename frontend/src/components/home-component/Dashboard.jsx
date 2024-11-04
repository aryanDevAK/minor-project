import React, { useEffect, useState } from 'react'
import "./dashboard.css"
import Counter from '../counter/Counter'

const HomeComponent = () => {
  const [counts, setCounts] = useState({});
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const access_token = localStorage.getItem("access_token");
    
        const response = await fetch("https://minor-project-dxsv.onrender.com/get/count", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
    
        if (response.status === 401 || response.status === 422) {
          throw new Error("Unauthorized or Unprocessable Entity");
        }
        if (!response.ok) throw new Error("Failed to fetch counts");
    
        const data = await response.json();
        setCounts(data);
      } catch (err) {
        setError(err.message);
        console.error("Fetch error:", err);
      }
    };
    

    fetchCounts();
  }, []);

  return (
    <div>
      <Counter counts={counts} />
    </div>
  )
}

export default HomeComponent