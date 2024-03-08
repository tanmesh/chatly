import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Home() {
    const [data, setData] = useState('')

    useEffect(() => {
        axios.get('http://localhost:8000/')
            .then(res => {
                setData(res.data)
            })
    })

    return (
        <div>
            <h1>{data}</h1>
        </div>
    )
}

export default Home