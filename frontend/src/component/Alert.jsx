import React from 'react'

function Alert({ message }) {
    return (
        <>
            {message ? (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-1 rounded relative" role="alert">
                    <span className="block sm:inline">{message}</span>
                </div>
            ) : (
                <div style={{ height: '2rem' }} />
            )}
        </>
    )
}

export default Alert