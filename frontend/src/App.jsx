import { Routes, Route, Navigate } from 'react-router'
import Search from './views/search'
import Login from './views/matriculas'

export default function App() {
  return (
    <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/search" element={<Search />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}