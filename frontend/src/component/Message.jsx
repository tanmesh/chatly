import React from 'react'
import ChatAvatar from './ChatAvatar';
import ReactMarkdown from 'react-markdown';

function Message({ author, message }) {
    return (
        <div className='flex items-start gap-4 pr-5 pt-2'>
            <ChatAvatar role={author} />
            <div className='group flex flex-1 justify-between gap-2'>
                <ReactMarkdown
                    components={{
                        a: ({ node, ...props }) => <a style={{ color: 'blue' }} {...props} />
                    }}
                >
                    {message}
                </ReactMarkdown>
            </div>
        </div>
    )
}

export default Message