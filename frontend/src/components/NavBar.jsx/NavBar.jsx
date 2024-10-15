import React from 'react'
import { Link } from 'react-router-dom'
import "./navbar.css"
import menu from "../../assets/menu.png"
import logo from "../../assets/logo-color.png"
import search_icon from "../../assets/search.png"
import notfication from "../../assets/notification.png"

const NavBar = ({setsidebar,userid}) => {
  return (
      <nav className='flex-div'>
          <div className="nav-left flex-div">
              <img src={menu} alt="menu icon" onClick={()=>setsidebar(prev => prev===false?true:false)}/>
              <Link to="/admin"><img className='logo' src={logo}/></Link>
          </div>  
          <div className="nav-middle flex-div">
              <div className='search-box'>
                <input type='text' placeholder='Search' />
                <img src={search_icon} />
              </div>
          </div>
      <div className="nav-right flex-div">
        <h3>{userid}</h3>
              <img src={notfication} alt="" />
          </div>
    </nav>
  )
}

export default NavBar