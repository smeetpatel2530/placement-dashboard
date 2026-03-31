import { useEffect, useState } from 'react'
import { getDepartments } from '../services/api'

export default function DepartmentCards() {
    const [depts, setDepts] = useState([])

    useEffect(() => {
        getDepartments().then(res => setDepts(res.data)).catch(() => { })
    }, [])

    return (
        <div style={{ marginBottom: '40px' }}>
            <h2 style={{ color: 'white', fontSize: '14px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '16px' }}>
                Department Breakdown
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '12px' }}>
                {depts.map(dept => {
                    const pct = Math.min((dept.placed / dept.batch_strength) * 100, 100)
                    return (
                        <div key={dept.department} style={{ backgroundColor: '#0f172a', borderRadius: '10px', padding: '16px', border: '1px solid rgba(255,255,255,0.07)' }}>
                            <div style={{ fontSize: '13px', fontWeight: 700, color: 'white', marginBottom: '4px' }}>{dept.department}</div>
                            <div style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>
                                {dept.placed} / {dept.batch_strength} placed
                            </div>
                            <div style={{ height: '4px', backgroundColor: '#1e293b', borderRadius: '4px', overflow: 'hidden' }}>
                                <div style={{ height: '100%', width: `${pct}%`, backgroundColor: pct >= 80 ? '#22d3ee' : pct >= 50 ? '#a3e635' : '#fbbf24', borderRadius: '4px', transition: 'width 0.8s ease' }} />
                            </div>
                            <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '6px', textAlign: 'right' }}>{pct.toFixed(0)}%</div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}