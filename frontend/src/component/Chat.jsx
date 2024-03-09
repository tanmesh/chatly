import React, { useState } from 'react';
import axios from 'axios';

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
        axios.post('http://localhost:5000/hello', config, message)
            .then((response) => {
                systemMessage = response;
            })
            .catch((err) => {
                console.log(err);
            })

        let systemMessageContent = {
            content: {
                author: 'System',
                message: systemMessage,
            },
        };
        setMessageList([...messageList, messageContent.content, systemMessageContent.content]);
        setMessage('');
    };

    return (
        <div className='space-y-4 max-w-5xl w-full flex flex-col justify-center mx-auto my-auto'>
            <div className="space-y-4 max-w-5xl w-full">
                <div className="w-full max-w-5xl p-4 bg-white rounded-xl ring-2 ring-blue-200">
                    <div className="flex flex-col gap-5 divide-y h-[70vh] overflow-auto">
                        {messageList.map((val, key) => {
                            return (
                                <div key={key} className="flex items-center space-x-2 gap-2">
                                    {val.author === 'User' ? '👤' : '🤖'}
                                    <div className="w-20">
                                        <p className='font-bold items-center'>{val.author}</p>
                                    </div>
                                    <p>:</p>
                                    <p>{val.message}</p>
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
                <button class="btn btn-neutral" onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default Chat;