import { Routes, Route, Navigate } from 'react-router-dom'
import Search from './views/search'
import Login from './views/matriculas'
import Base from './views/base'

export default function App() {
  return (
    <Routes>
        <Route path="/" element={<Base />}>
            <Route index element={<Navigate to="/login" replace />} />
            <Route path="login" element={<Login />} />
            <Route path="search" element={<Search />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}