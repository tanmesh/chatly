import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Room() {
    const [data, setData] = useState('')

    useEffect(() => {
        axios.get('http://localhost:8000/room')
            .then(res => {
                setData(res.data)
            })
            .catch(err => {
                setData(err.message)
            })
    })

    return (
        <div>
            <h1>{data}</h1>
        </div>
    )
}

export default Room