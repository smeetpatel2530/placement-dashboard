import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { getCompanies } from '../services/api'

export default function CompanyChart() {
    const [data, setData] = useState([])

    useEffect(() => {
        getCompanies().then(res => {
            const sorted = [...res.data].sort((a, b) => b.count - a.count).slice(0, 10)
            setData(sorted)
        }).catch(() => { })
    }, [])

    const colors = ['#22d3ee', '#a3e635', '#fbbf24', '#818cf8', '#34d399', '#f472b6', '#fb923c', '#60a5fa', '#e879f9', '#4ade80']

    return (
        <div style={{ backgroundColor: '#0f172a', borderRadius: '12px', padding: '20px', border: '1px solid rgba(255,255,255,0.07)' }}>
            <h3 style={{ color: 'white', fontSize: '14px', fontWeight: 600, marginBottom: '16px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Top Hiring Companies</h3>
            <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data} layout="vertical" margin={{ left: 60, right: 8 }}>
                    <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis type="category" dataKey="company" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} width={55} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: 'white', fontSize: '13px' }}
                        cursor={{ fill: 'rgba(255,255,255,0.04)' }}
                    />
                    <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                        {data.map((_, i) => <Cell key={i} fill={colors[i % colors.length]} />)}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
}