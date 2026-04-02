// import { Link, useLocation } from 'react-router-dom'

// export default function Navbar() {
//     const { pathname } = useLocation()

//     const links = [
//         { to: '/', label: 'Dashboard' },
//         { to: '/students', label: 'Students' },
//         { to: '/analytics', label: 'Analytics' },
//     ]

//     return (
//         <header style={{
//             position: 'sticky',
//             top: 0,
//             zIndex: 50,
//             backgroundColor: 'rgba(3, 7, 18, 0.92)',
//             borderBottom: '1px solid rgba(255,255,255,0.08)',
//             backdropFilter: 'blur(12px)',
//         }}>
//             <div style={{
//                 maxWidth: '1280px',
//                 margin: '0 auto',
//                 padding: '0 16px',
//                 height: '56px',
//                 display: 'flex',
//                 alignItems: 'center',
//                 justifyContent: 'space-between',
//             }}>
//                 <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
//                     <img src="/dtu-logo.png" alt="DTU Logo" style={{ height: '32px', width: '32px', objectFit: 'contain' }} />
//                     <span style={{
//                         fontWeight: 700, color: 'white',
//                         fontSize: '13px', letterSpacing: '0.02em',
//                         whiteSpace: 'nowrap'
//                     }}>
//                         DTU M.Tech Placements 2026
//                     </span>
//                 </div>
//                 <nav style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
//                     {links.map(link => (
//                         <Link
//                             key={link.to}
//                             to={link.to}
//                             style={{
//                                 padding: '6px 12px',
//                                 borderRadius: '6px',
//                                 fontSize: '14px',
//                                 fontWeight: 500,
//                                 textDecoration: 'none',
//                                 color: pathname === link.to ? 'white' : '#9ca3af',
//                                 backgroundColor: pathname === link.to ? 'rgba(255,255,255,0.1)' : 'transparent',
//                                 transition: 'all 0.15s',
//                             }}
//                         >
//                             {link.label}
//                         </Link>
//                     ))}
//                 </nav>
//             </div>
//         </header>
//     )
// }

import { NavLink } from 'react-router-dom'

function Navbar() {
    return (
        <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-3 sm:px-4">
                <div className="flex items-center justify-between h-14 sm:h-16">
                    {/* Logo */}
                    <div className="flex items-center gap-2 min-w-0">
                        <img src="/dtu-logo.png" alt="DTU" className="w-8 h-8 sm:w-10 sm:h-10 rounded-full flex-shrink-0" />
                        <span className="font-bold text-white text-sm sm:text-base truncate">
                            DTU M.Tech Placements 2026
                        </span>
                    </div>
                    {/* Nav links */}
                    <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
                        {['/', '/students', '/analytics'].map((path, i) => {
                            const labels = ['Dashboard', 'Students', 'Analytics']
                            return (
                                <NavLink
                                    key={path}
                                    to={path}
                                    end={path === '/'}
                                    className={({ isActive }) =>
                                        `px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors whitespace-nowrap ${isActive
                                            ? 'bg-cyan-500 text-gray-950'
                                            : 'text-gray-400 hover:text-white hover:bg-gray-800'
                                        }`
                                    }
                                >
                                    {labels[i]}
                                </NavLink>
                            )
                        })}
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Navbar