import React, { useState } from 'react';
import axios from 'axios';
import ChatAvatar from './ChatAvatar';
import ReactMarkdown from 'react-markdown';
import Send from '../assets/Send';

function Chat() {
    const [message, setMessage] = useState('');
    const [messageList, setMessageList] = useState([]);

    const sendMessage = async () => {
        let messageContent = {
            content: {
                author: 'User',
                message: message,
            },
        };

        const config = {
            headers: {
                'Content-Type': 'application/json'
            },
        };

        let systemMessage = '';
        axios.post('http://localhost:5000/chat', { "text": message }, config)
            .then((response) => {
                systemMessage = response.data;
                console.log(response.data);

                let systemMessageContent = {
                    content: {
                        author: 'System',
                        message: systemMessage,
                    },
                };

                setMessageList([...messageList, messageContent.content, systemMessageContent.content]);
                setMessage('');
            })
            .catch((err) => {
                console.log(err);
            })
        setMessage('');
    };

    return (
        <div className='space-y-4 max-w-5xl w-full flex flex-col justify-center mx-auto my-auto'>
            <div className="space-y-4 max-w-5xl w-full">
                <div className="w-full max-w-5xl p-4 bg-white rounded-xl ring-2 ring-gray-200">
                    <div className="flex flex-col gap-2 h-[70vh] overflow-auto">
                        {messageList.map((val, key) => {
                            return (
                                <div key={key} className="flex gap-2">
                                    <ChatAvatar role={val.author} />
                                    <div className="w-20">
                                        <p className='font-bold items-center'>{val.author}</p>
                                    </div>
                                    <ReactMarkdown>{val.message}</ReactMarkdown>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
            <div className="flex flex-row justify-center gap-6">
                <input
                    type="text"
                    placeholder="Type here"
                    className="input input-bordered max-w-5xl w-full"
                    onChange={(e) => {
                        setMessage(e.target.value);
                    }} />
                <button className="btn btn-neutral text-white" onClick={sendMessage}><Send />Send</button>
            </div>
        </div>
    );
}

export default Chat;