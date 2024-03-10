import React from 'react'
import ChatAvatar from './ChatAvatar';
import ReactMarkdown from 'react-markdown';

function Message({ author, message }) {
    return (
        <>
            <ChatAvatar role={author} />
            <div className="w-20">
                <p className='font-bold items-center'>{author}</p>
            </div>
            <ReactMarkdown
                components={{
                    a: ({ node, ...props }) => <a style={{ color: 'blue' }} {...props} />
                }}
            >
                {message}
            </ReactMarkdown>
        </>
    )
}

export default Message