import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Room from './pages/Room';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/room" element={<Room />} exact />
        <Route path="/" element={<Home />} exact />
      </Routes>
    </Router>
  );
}

export default App;
