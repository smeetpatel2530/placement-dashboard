
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
                            DTU M.Tech Placements 2027
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