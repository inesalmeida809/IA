import { Routes, Route } from 'react-router'
import Search from './views/search'
import Login from './views/matriculas'

export default function App() {
  return (
    <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/search" element={<Search />} />
    </Routes>
  )
}