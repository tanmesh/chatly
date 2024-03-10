import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Navbar({ title }) {
    const navigate = useNavigate()
    const [accessToken, setAccessToken] = useState('')

    useEffect(() => {
        setAccessToken(localStorage.getItem('accessToken'))
    })

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login')
    }

    return (
        <div className="navbar">
            <div className="navbar-start"></div>
            <div className="navbar-center">
                <h1 className="text-4xl text-blue-700 font-bold ml-2">{title}</h1>
            </div>
            <div className="navbar-end">
                <div className="dropdown dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
                        <div className="w-10 rounded-full">
                            <img alt="Tailwind CSS Navbar component" src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
                        </div>
                    </div>
                    {accessToken &&
                        <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                            <li><p onClick={() => handleLogout()}>Logout</p></li>
                        </ul>
                    }
                </div>
            </div>
        </div>
    )
}

export default Navbar