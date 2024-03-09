import React from 'react'

function Navbar({ title }) {
    return (
        <div className="navbar mb-12 bg-base-100 flex flex-row justify-between">
            <div>
                <a className="btn btn-ghost text-blue-700 text-4xl">{title}</a>
            </div>

            <div className='gap-3'>
                <a className="bg-blue-700 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">Schedule event 🔗</a>
                <a className="bg-blue-700 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">About</a>
            </div>
        </div>
    )
}

export default Navbar