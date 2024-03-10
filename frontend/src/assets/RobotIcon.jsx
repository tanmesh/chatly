import React from 'react'

function RobotIcon() {
    return (
        <svg viewBox="0 0 40 40" stroke-width="1.3" stroke-linejoin="round" stroke="#111" fill="#aab" xmlns="http://www.w3.org/2000/svg">
            <path transform="rotate(-25)" d="M7 12 7 4 3 4 3 12" />
            <path transform="rotate(25 40 0)" d="M37 12 37 4 33 4 33 12" />
            <path d="M4 6v32h32V6Z" stroke-width="2" />
            <g fill="#f87">
                <circle r="5.4" cy="16" cx="13" />
                <circle r="5.4" cy="16" cx="27" />
            </g>
            <g fill="#eee">
                <circle r="1" cy="15.5" cx="13" />
                <circle r="1" cy="15.5" cx="27" />
                <path d="M9 26V34H31V26ZM13 26V34M26.6 26V34M17.6 26V34M22 26V34M9 29.6H31" />
            </g>
        </svg>
    )
}

export default RobotIcon