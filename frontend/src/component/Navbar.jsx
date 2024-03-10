import React from 'react'

function Navbar({ title }) {
    return (
        <div className="navbar mb-12 flex flex-row justify-between">
            <p className="btn btn-ghost hover:bg-blue-200 text-blue-700 text-4xl">{title}</p>
            <p className="btn btn-ghost hover:bg-blue-200 text-blue-700 text-xl font-bold py-2 px-4 rounded">About</p>
        </div>
    )
}

export default Navbar