import PropTypes from 'prop-types'
import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage.jsx'
import StatsPage from './pages/StatsPage.jsx'
import './App.css'

function App({ appName = 'Rak Buku Saya' }) {
  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="header-inner">
          <NavLink to="/" className="site-name">{appName}</NavLink>
          <nav aria-label="Navigasi utama">
            <NavLink to="/" end>Daftar Buku</NavLink>
            <NavLink to="/statistik">Statistik</NavLink>
          </nav>
        </div>
      </header>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/statistik" element={<StatsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <footer className="site-footer">Praktikum Pengembangan Aplikasi Web · Pertemuan 3 · RA</footer>
    </div>
  )
}

App.propTypes = {
  appName: PropTypes.string,
}

export default App
