import React from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Home from './pages/Home';
import Navbar from './component/Navbar';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <Router>
      <div className="flex flex-col h-screen bg-blue-100">
        <Navbar title="Chatly"/>
        <main className="container mx-auto px-3 pb-12">
          <Routes>
            <Route path="/" element={<Home />} exact />
            <Route path="/login" element={<Login />} exact />
            <Route path="/signup" element={<Signup />} exact />
          </Routes>
        </main>
      </div>
    </Router >
  );
}

export default App;
