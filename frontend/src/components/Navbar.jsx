import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
    const { pathname } = useLocation()

    const links = [
        { to: '/', label: 'Dashboard' },
        { to: '/students', label: 'Students' },
        { to: '/analytics', label: 'Analytics' },
    ]

    return (
        <header style={{
            position: 'sticky',
            top: 0,
            zIndex: 50,
            backgroundColor: 'rgba(3, 7, 18, 0.92)',
            borderBottom: '1px solid rgba(255,255,255,0.08)',
            backdropFilter: 'blur(12px)',
        }}>
            <div style={{
                maxWidth: '1280px',
                margin: '0 auto',
                padding: '0 16px',
                height: '56px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <img src="/dtu-logo.png" alt="DTU Logo" style={{ height: '32px', width: '32px', objectFit: 'contain' }} />
                    <span style={{
                        fontWeight: 700, color: 'white',
                        fontSize: '13px', letterSpacing: '0.02em',
                        whiteSpace: 'nowrap'
                    }}>
                        DTU M.Tech Placements 2026
                    </span>
                </div>
                <nav style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    {links.map(link => (
                        <Link
                            key={link.to}
                            to={link.to}
                            style={{
                                padding: '6px 12px',
                                borderRadius: '6px',
                                fontSize: '14px',
                                fontWeight: 500,
                                textDecoration: 'none',
                                color: pathname === link.to ? 'white' : '#9ca3af',
                                backgroundColor: pathname === link.to ? 'rgba(255,255,255,0.1)' : 'transparent',
                                transition: 'all 0.15s',
                            }}
                        >
                            {link.label}
                        </Link>
                    ))}
                </nav>
            </div>
        </header>
    )
}