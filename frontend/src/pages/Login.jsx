import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Alert from '../component/Alert'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [accessToken, setAccessToken] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    useEffect(() => {
        localStorage.setItem('accessToken', accessToken);
    }, [accessToken])

    useEffect(() => {
        const timeout = setTimeout(() => {
            setError('');
        }, 3000);

        return () => clearTimeout(timeout);
    }, [error])

    const handleSubmit = (e) => {
        e.preventDefault()

        if (!email || !password) {
            setError('Please fill in all fields');
            return;
        }

        const config = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const body = JSON.stringify({ email, password: btoa(password) });

        axios.post('http://localhost:5000/login', body, config)
            .then((response) => {
                setAccessToken(response.data.token);
                navigate('/')
            })
            .catch((err) => {
                console.log(err);
                setError(err.response.data.error);
            })
    }

    return (
        <div className="hero">
            <div className="hero-content text-center">
                <div className="max-w-md space-y-4" onSubmit={handleSubmit}>
                    <p className="py-6">Effortlessly manage your schedule with our intuitive chatbot. Simplify event listing and cancellations with ease. Experience the convenience today!</p>
                    <Alert message={error} />   
                    <form className="flex flex-col gap-4">
                        <label className="input input-bordered flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70">
                                <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
                                <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
                            </svg>
                            <input type="text" className="grow" placeholder="Email" value={email} onChange={(e) => { setEmail(e.target.value) }} />
                        </label>
                        <label className="input input-bordered flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70">
                                <path fillRule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clipRule="evenodd" />
                            </svg>
                            <input type="password" className="grow" placeholder="Password" value={password} onChange={(e) => { setPassword(e.target.value) }} />
                        </label>
                        <button type="submit" className="btn btn-neutral text-white w-40 mx-auto">Login</button>
                    </form>
                    <p className="text-xs text-gray-500">
                        Don't have an account? Click <Link to="/signup" className='text-blue-800 underline'>here</Link> to Sign up!
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Login