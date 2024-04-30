import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import './NavBar.css';
import axios from "axios";
import { toast } from "react-toastify";


const NavBar = () => {

  const [userName, setUserName] = useState();

  useEffect(() => {
    const token = localStorage.getItem('token');    
    axios.get('http://localhost:8000/users/me/', { headers: { "Authorization": `Bearer ${token}` } })    
      .then(r => {
        setUserName(r.data.username);
      })
      .catch(e => {
        console.log(e);
    })
  })

  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem('token')
    navigate('/login')
    toast('Logged out')
  }

  return <div className="NavBar">
    <div className="leftNav">
      <Link to='/'>Home</Link>
      <Link to='/history'>History</Link>
      <Link to='/recommend'>Recommend</Link>
    </div>
    <div className="rightNav">
      <div>Logged in as {userName}</div>
      <button onClick={logout}>Logout</button>
    </div>
  </div>;
};

export default NavBar;
