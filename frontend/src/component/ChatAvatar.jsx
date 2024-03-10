import React from 'react'
import PropTypes from 'prop-types'
import UserIcon from '../assets/UserIcon'
import RobotIcon from '../assets/RobotIcon'

const ChatAvatar = ({ role }) => {
  return (
    <div className={`flex h-6 w-6 shrink-0 select-none items-center justify-center ${role === 'User' ? 'rounded-md border' : ''}`}>
      {role === 'User' ? <UserIcon /> : <RobotIcon />}
    </div>
  )
}

ChatAvatar.propTypes = {
  role: PropTypes.string.isRequired,
}

export default ChatAvatar