import { useState } from 'react'
import './App.css'
import Dashboard from './pages/dashboard'
import DashboardLayout from './layout/dashboard_layout'
import { BrowserRouter, Routes, Route } from 'react-router-dom'


function App() {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    )
}

 

export default App
