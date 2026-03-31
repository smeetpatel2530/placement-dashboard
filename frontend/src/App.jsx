import { Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import Students from './pages/Students.jsx'
import Analytics from './pages/Analytics.jsx'
import Navbar from './components/Navbar.jsx'

function App() {
    return (
        <div className="min-h-screen bg-gray-950 text-white">
            <Navbar />
            <main className="max-w-7xl mx-auto px-4 py-8">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/students" element={<Students />} />
                    <Route path="/analytics" element={<Analytics />} />
                </Routes>
            </main>
        </div>
    )
}

export default App