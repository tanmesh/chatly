import React from 'react'
import { useNavigate } from 'react-router-dom'

function Navbar({ title }) {
    const navigate = useNavigate()

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        navigate('/login')
    }

    return (
        <div className="navbar">
            <div className="flex-1">
                <p className="btn btn-ghost hover:bg-blue-200 text-blue-700 text-4xl">{title}</p>
            </div>
            <div className="flex-none gap-2">
                <div className="dropdown dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar">
                        <div className="w-10 rounded-full">
                            <img alt="Tailwind CSS Navbar component" src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
                        </div>
                    </div>
                    <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                        <li><a onClick={() => handleLogout()}>Logout</a></li>
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default Navbar