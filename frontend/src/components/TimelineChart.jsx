import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { getTimeline } from '../services/api'

export default function TimelineChart() {
    const [data, setData] = useState([])

    useEffect(() => {
        getTimeline().then(res => setData(res.data)).catch(() => { })
    }, [])

    return (
        <div style={{ backgroundColor: '#0f172a', borderRadius: '12px', padding: '20px', border: '1px solid rgba(255,255,255,0.07)' }}>
            <h3 style={{ color: 'white', fontSize: '14px', fontWeight: 600, marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Placements Over Time</h3>
            <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="teal" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <XAxis dataKey="month" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: 'white', fontSize: '13px' }}
                    />
                    <Area type="monotone" dataKey="count" stroke="#22d3ee" strokeWidth={2} fill="url(#teal)" dot={{ fill: '#22d3ee', r: 3 }} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    )
}