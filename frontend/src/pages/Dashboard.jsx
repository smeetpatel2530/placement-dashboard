import { useEffect, useState } from 'react'
import { getStats } from '../services/api'
import CompanyChart from '../components/CompanyChart.jsx'
import TimelineChart from '../components/TimelineChart.jsx'
import DepartmentCards from '../components/DepartmentCards.jsx'
import MotivationalQuote from '../components/MotivationalQuote.jsx'

const statCards = [
    { key: 'total_placed', label: 'Students Placed', suffix: '', color: '#22d3ee' },
    { key: 'placement_percentage', label: 'Placement %', suffix: '%', color: '#a3e635' },
    { key: 'max_ctc', label: 'Highest CTC', suffix: ' LPA', color: '#fbbf24' },
    { key: 'median_ctc', label: 'Median CTC', suffix: ' LPA', color: '#818cf8' },
    { key: 'avg_ctc', label: 'Average CTC', suffix: ' LPA', color: '#34d399' },
    { key: 'fte_count', label: 'FTE Offers', suffix: '', color: '#f472b6' },
    { key: 'ppo_count', label: 'PPO Offers', suffix: '', color: '#fb923c' },
    { key: 'total_batch', label: 'Total Batch', suffix: '', color: '#94a3b8' },
]

function AnimatedNumber({ value, suffix }) {
    const [display, setDisplay] = useState(0)

    useEffect(() => {
        if (!value) return
        const target = parseFloat(value)
        const duration = 1200
        const steps = 40
        const increment = target / steps
        let current = 0
        const timer = setInterval(() => {
            current += increment
            if (current >= target) {
                setDisplay(target)
                clearInterval(timer)
            } else {
                setDisplay(current)
            }
        }, duration / steps)
        return () => clearInterval(timer)
    }, [value])

    const formatted = Number.isInteger(parseFloat(value))
        ? Math.round(display)
        : display.toFixed(2)

    return <span>{formatted}{suffix}</span>
}

export default function Dashboard() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        getStats()
            .then(res => setStats(res.data))
            .catch(() => setError('Failed to load stats'))
            .finally(() => setLoading(false))
    }, [])

    if (loading) return (
        <div style={{ color: '#94a3b8', padding: '32px 0' }}>Loading stats...</div>
    )

    if (error) return (
        <div style={{ color: '#f87171', padding: '32px 0' }}>{error}</div>
    )

    return (
        <div>
            <h1 style={{ color: 'white', fontSize: '22px', fontWeight: 700, marginBottom: '8px' }}>
                Placement Overview — M.Tech 2026
            </h1>
            <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '28px' }}>
                Real-time data from placements.xlsx
            </p>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
                gap: '16px',
                marginBottom: '40px',
            }}>

                {statCards.map(card => (
                    <div key={card.key} style={{
                        backgroundColor: '#0f172a',
                        border: '1px solid rgba(255,255,255,0.07)',
                        borderRadius: '12px',
                        padding: '20px',
                    }}>
                        <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
                            {card.label}
                        </div>
                        <div style={{ fontSize: '28px', fontWeight: 700, color: card.color, fontVariantNumeric: 'tabular-nums' }}>
                            {stats ? <AnimatedNumber value={stats[card.key]} suffix={card.suffix} /> : '—'}
                        </div>
                    </div>
                ))}
            </div>
            {/* Charts grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '40px' }}>
                <CompanyChart />
                <TimelineChart />
            </div>
            {/* Department breakdown */}
            <DepartmentCards />
            <MotivationalQuote />
        </div>
    )
}