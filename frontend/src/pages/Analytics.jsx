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
        <div style={{ height: 220, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#475569', fontSize: '13px' }}>
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

    useEffect(() => {
        Promise.all([getCTCDistribution(), getDepartments(), getRoles()])
            .then(([cRes, dRes, rRes]) => {
                setCtcDist(cRes.data || [])
                setDepts(dRes.data || [])
                setRoles(rRes.data || [])
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

    const typePieData = useMemo(() => {
        const fte = depts.reduce((sum, d) => sum + (d.fte_count || 0), 0)
        const ppo = depts.reduce((sum, d) => sum + (d.ppo_count || 0), 0)
        const intern = depts.reduce((sum, d) => sum + (d.intern_count || 0), 0)
        const data = []
        if (fte > 0) data.push({ name: 'FTE', value: fte })
        if (ppo > 0) data.push({ name: 'PPO→FTE', value: ppo })
        if (intern > 0) data.push({ name: 'Intern Only', value: intern })
        return data
    }, [depts])

    const topRoles = useMemo(() =>
        [...roles].sort((a, b) => b.count - a.count).slice(0, 10),
        [roles]
    )

    if (loading) return <p style={{ color: '#64748b', padding: '20px 0' }}>Loading analytics...</p>
    if (error) return <p style={{ color: '#f87171', padding: '20px 0' }}>{error}</p>

    return (
        <div>
            <h1 style={{ color: 'white', fontSize: '22px', fontWeight: 700, marginBottom: '8px' }}>Analytics</h1>
            <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '28px' }}>Deep dive into placement data</p>

            {/* Row 1 — CTC Distribution + Offer Type Pie */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '24px' }}>

                {/* CTC Distribution */}
                <div style={card}>
                    <p style={sectionTitle}>CTC Distribution</p>
                    {ctcDist.length > 0 ? (
                        <ResponsiveContainer width="100%" height={260}>
                            <BarChart data={ctcDist} margin={{ bottom: 8 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                <XAxis dataKey="range" tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} />
                                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
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
                                    cy="45%"
                                    innerRadius={65}
                                    outerRadius={100}
                                    paddingAngle={3}
                                    dataKey="value"
                                >
                                    {typePieData.map((entry, i) => (
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
                                    wrapperStyle={{ fontSize: '12px', color: '#94a3b8', paddingTop: '12px' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    ) : <EmptyChart message="No offer type data. Check ppo_type column in Excel." />}
                </div>
            </div>

            {/* Row 2 — Dept Median CTC */}
            <div style={{ ...card, marginBottom: '24px' }}>
                <p style={sectionTitle}>Median CTC by Department (LPA)</p>
                {deptCTCData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={deptCTCData} margin={{ bottom: 8 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="dept" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                            <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} unit=" L" />
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

            {/* Row 3 — Top Roles */}
            <div style={card}>
                <p style={sectionTitle}>Top Job Roles</p>
                {topRoles.length > 0 ? (
                    <ResponsiveContainer width="100%" height={260}>
                        <BarChart data={topRoles} layout="vertical" margin={{ left: 120, right: 16 }}>
                            <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                            <YAxis type="category" dataKey="role" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} width={115} />
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