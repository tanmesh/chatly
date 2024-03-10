import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Send from '../assets/Send';
import Loading from './Loading';
import Message from './Message';

function Chat() {
    const [message, setMessage] = useState('');
    const [messageList, setMessageList] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [accessToken, setAccessToken] = useState('');

    useEffect(() => {
        setAccessToken(localStorage.getItem('accessToken'));
    }, []) 

    useEffect(() => {
        const timeout = setTimeout(() => {
            setError(null);
        }, 5000);

        return () => clearTimeout(timeout);
    }, [error]);

    const sendMessage = async () => {
        setLoading(true);
        let messageContent = {
            content: {
                author: 'User',
                message: message,
            },
        };

        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': accessToken,
            },
        };

        let systemMessage = '';
        axios.post('http://localhost:5000/chat', { "text": message }, config)
            .then((response) => {
                systemMessage = response.data;

                let systemMessageContent = {
                    content: {
                        author: 'Chatly',
                        message: systemMessage,
                    },
                };

                setMessageList([...messageList, messageContent.content, systemMessageContent.content]);
                setMessage('');
                setLoading(false);
            })
            .catch((err) => {
                setLoading(false);
                setError(`Error sending message: ${err.response.data.error}`);
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
                                    <Message author={val.author} message={val.message} />
                                </div>
                            );
                        })}
                        {loading && <Loading />}
                    </div>
                </div>
            </div>
            {error && <div className="text-red-500 text-sm">{error}</div>}
            <form
                className="flex flex-row justify-center gap-6"
                onSubmit={(e) => {
                    e.preventDefault();
                    sendMessage();
                    setMessage('');
                }}
            >
                <input
                    type="text"
                    placeholder="Type here"
                    className="input input-bordered max-w-5xl w-full"
                    value={message}
                    onChange={(e) => {
                        setMessage(e.target.value);
                    }}
                />
                <button className="btn btn-neutral text-white" type="submit">
                    <Send />Send
                </button>
            </form>
        </div>
    );
}

export default Chat;