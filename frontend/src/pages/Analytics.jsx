import { useEffect, useState, useMemo } from 'react'
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, Legend, CartesianGrid
} from 'recharts'
import { getCTCDistribution, getDepartments, getRoles } from '../services/api'

const COLORS = ['#22d3ee', '#a3e635', '#fbbf24', '#818cf8', '#34d399', '#f472b6', '#fb923c', '#60a5fa', '#e879f9', '#4ade80']

const card = {
    backgroundColor: '#0f172a',
    borderRadius: '12px',
    padding: '20px',
    border: '1px solid rgba(255,255,255,0.07)'
}

const sectionTitle = {
    color: 'white',
    fontSize: '14px',
    fontWeight: 600,
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
    marginBottom: '16px'
}

const tooltipStyle = {
    contentStyle: {
        backgroundColor: '#1e293b',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '8px',
        color: 'white',
        fontSize: '13px'
    }
}

function EmptyChart({ message = 'No data available' }) {
    return (
        <div style={{
            height: 220, display: 'flex', alignItems: 'center',
            justifyContent: 'center', color: '#475569', fontSize: '13px'
        }}>
            {message}
        </div>
    )
}

export default function Analytics() {
    const [ctcDist, setCtcDist] = useState([])
    const [depts, setDepts] = useState([])
    const [roles, setRoles] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768)

    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 768)
        window.addEventListener('resize', handleResize)
        return () => window.removeEventListener('resize', handleResize)
    }, [])

    useEffect(() => {
        Promise.all([getCTCDistribution(), getDepartments(), getRoles()])
            .then(([cRes, dRes, rRes]) => {
                setCtcDist(Array.isArray(cRes.data) ? cRes.data : [])
                setDepts(Array.isArray(dRes.data) ? dRes.data : [])
                setRoles(Array.isArray(rRes.data) ? rRes.data : [])
            })
            .catch(err => {
                console.error('Analytics load error:', err)
                setError('Failed to load analytics data. Check backend.')
            })
            .finally(() => setLoading(false))
    }, [])

    const deptCTCData = useMemo(() =>
        depts
            .filter(d => d.median_ctc > 0)
            .sort((a, b) => b.median_ctc - a.median_ctc)
            .map(d => ({ dept: d.department, median: d.median_ctc, placed: d.placed })),
        [depts]
    )

    // ── Fixed: uses fte_count / ppo_count / intern_count (no more fte_intern_count) ──
    const typePieData = useMemo(() => {
        const fte = depts.reduce((s, d) => s + (d.fte_count || 0), 0)
        const ppo = depts.reduce((s, d) => s + (d.ppo_count || 0), 0)
        const intern = depts.reduce((s, d) => s + (d.intern_count || 0), 0)

        const data = []
        if (fte > 0) data.push({ name: 'FTE (Direct)', value: fte })
        if (ppo > 0) data.push({ name: 'PPO / Converted', value: ppo })
        if (intern > 0) data.push({ name: 'Intern Only', value: intern })
        return data
    }, [depts])

    const topRoles = useMemo(() =>
        [...roles].sort((a, b) => b.count - a.count).slice(0, 10),
        [roles]
    )

    // Dept placement % bar data
    const deptPlacementData = useMemo(() =>
        depts
            .filter(d => d.batch_strength > 0)
            .sort((a, b) => b.percentage - a.percentage)
            .map(d => ({
                dept: d.department,
                placed: d.placed,
                total: d.batch_strength,
                pct: d.percentage
            })),
        [depts]
    )

    if (loading) return <p style={{ color: '#64748b', padding: '20px 0' }}>Loading analytics...</p>
    if (error) return <p style={{ color: '#f87171', padding: '20px 0' }}>{error}</p>

    const twoColGrid = {
        display: 'grid',
        gridTemplateColumns: isMobile ? '1fr' : '1fr 1fr',
        gap: '16px',
        marginBottom: '16px'
    }

    const roleLeftMargin = isMobile ? 10 : 120
    const roleYWidth = isMobile ? 80 : 115

    return (
        <div>
            <h1 style={{ color: 'white', fontSize: isMobile ? '20px' : '22px', fontWeight: 700, marginBottom: '8px' }}>
                Analytics
            </h1>
            <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '24px' }}>
                Deep dive into placement data
            </p>

            {/* Row 1 — CTC Distribution + Offer Type Pie */}
            <div style={twoColGrid}>

                {/* CTC Distribution */}
                <div style={card}>
                    <p style={sectionTitle}>CTC Distribution</p>
                    {ctcDist.length > 0 ? (
                        <ResponsiveContainer width="100%" height={240}>
                            <BarChart data={ctcDist} margin={{ bottom: 8, left: 0, right: 8 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="range" tick={{ fill: '#64748b', fontSize: isMobile ? 9 : 10 }} axisLine={false} tickLine={false} />
                                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} width={28} allowDecimals={false} />
                                <Tooltip {...tooltipStyle} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
                                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                                    {ctcDist.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    ) : <EmptyChart />}
                </div>

                {/* Offer Type Pie */}
                <div style={card}>
                    <p style={sectionTitle}>Offer Type Breakdown</p>
                    {typePieData.length > 0 ? (
                        <ResponsiveContainer width="100%" height={280}>
                            <PieChart>
                                <Pie
                                    data={typePieData}
                                    cx="50%"
                                    cy="42%"
                                    innerRadius={isMobile ? 50 : 65}
                                    outerRadius={isMobile ? 80 : 100}
                                    paddingAngle={3}
                                    dataKey="value"
                                >
                                    {typePieData.map((_, i) => (
                                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    {...tooltipStyle}
                                    formatter={(value, name) => [`${value} students`, name]}
                                />
                                <Legend
                                    iconType="circle"
                                    iconSize={8}
                                    formatter={(value, entry) => {
                                        const total = typePieData.reduce((s, d) => s + d.value, 0)
                                        const pct = total > 0 ? ((entry.payload.value / total) * 100).toFixed(0) : 0
                                        return `${value} — ${entry.payload.value} (${pct}%)`
                                    }}
                                    wrapperStyle={{ fontSize: isMobile ? '11px' : '12px', color: '#94a3b8', paddingTop: '12px' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    ) : <EmptyChart message="No offer type data." />}
                </div>
            </div>

            {/* Row 2 — Dept Placement % */}
            <div style={{ ...card, marginBottom: '16px' }}>
                <p style={sectionTitle}>Placement % by Department</p>
                {deptPlacementData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={deptPlacementData} margin={{ bottom: 8, left: 0, right: 8 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="dept" tick={{ fill: '#94a3b8', fontSize: isMobile ? 10 : 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} unit="%" width={36} domain={[0, 100]} />
                            <Tooltip
                                {...tooltipStyle}
                                formatter={(v, _, props) => [
                                    `${v}% (${props.payload.placed}/${props.payload.total})`,
                                    'Placed'
                                ]}
                                cursor={{ fill: 'rgba(255,255,255,0.04)' }}
                            />
                            <Bar dataKey="pct" radius={[4, 4, 0, 0]}>
                                {deptPlacementData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                ) : <EmptyChart message="No department data." />}
            </div>

            {/* Row 3 — Dept Median CTC */}
            <div style={{ ...card, marginBottom: '16px' }}>
                <p style={sectionTitle}>Median CTC by Department (LPA)</p>
                {deptCTCData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={deptCTCData} margin={{ bottom: 8, left: 0, right: 8 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="dept" tick={{ fill: '#94a3b8', fontSize: isMobile ? 10 : 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} unit="L" width={32} />
                            <Tooltip
                                {...tooltipStyle}
                                formatter={(v) => [`${v} LPA`, 'Median CTC']}
                                cursor={{ fill: 'rgba(255,255,255,0.04)' }}
                            />
                            <Bar dataKey="median" radius={[4, 4, 0, 0]}>
                                {deptCTCData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                ) : <EmptyChart message="No CTC data per department." />}
            </div>

            {/* Row 4 — Top Roles */}
            <div style={card}>
                <p style={sectionTitle}>Top Job Roles</p>
                {topRoles.length > 0 ? (
                    <ResponsiveContainer width="100%" height={isMobile ? 300 : 260}>
                        <BarChart data={topRoles} layout="vertical" margin={{ left: roleLeftMargin, right: 16, top: 4, bottom: 4 }}>
                            <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} allowDecimals={false} />
                            <YAxis
                                type="category"
                                dataKey="role"
                                tick={{ fill: '#94a3b8', fontSize: isMobile ? 9 : 11 }}
                                axisLine={false}
                                tickLine={false}
                                width={roleYWidth}
                            />
                            <Tooltip {...tooltipStyle} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
                            <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                                {topRoles.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                ) : <EmptyChart message="No role data available." />}
            </div>
        </div>
    )
}