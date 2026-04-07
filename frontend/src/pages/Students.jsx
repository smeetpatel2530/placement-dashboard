import { useEffect, useState, useMemo } from 'react'
import { getStudents, getDepartments } from '../services/api'

function badge(text, color) {
    return (
        <span style={{
            display: 'inline-block',
            padding: '2px 8px',
            borderRadius: '999px',
            fontSize: '11px',
            fontWeight: 600,
            backgroundColor: color + '22',
            color: color,
            whiteSpace: 'nowrap'
        }}>
            {text}
        </span>
    )
}

function formatDate(dateStr) {
    if (!dateStr) return '—'
    const d = String(dateStr).split(' ')[0].split('T')[0]
    if (!d || d === 'None' || d === 'nan') return '—'
    const parts = d.split('-')
    if (parts.length === 3) return `${parts[2]}/${parts[1]}/${parts[0]}`
    return d
}

function ppoColor(t) {
    if (!t) return '#818cf8'
    const val = t.toUpperCase()
    if (val.includes('PPO') && val.includes('INTERN')) return '#a3e635'
    if (val.includes('PPO')) return '#a3e635'
    if (val.includes('INTERN')) return '#fb923c'
    if (val.includes('FTE')) return '#22d3ee'
    return '#818cf8'
}

function ppoLabel(t) {
    if (!t || t === '-' || t.toLowerCase() === 'nan') return null
    return t
}

export default function Students() {
    const [students, setStudents] = useState([])
    const [depts, setDepts] = useState([])
    const [search, setSearch] = useState('')
    const [deptFilter, setDeptFilter] = useState('')
    const [typeFilter, setTypeFilter] = useState('')
    const [loading, setLoading] = useState(true)
    const [isMobile, setIsMobile] = useState(window.innerWidth < 640)

    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 640)
        window.addEventListener('resize', handleResize)
        return () => window.removeEventListener('resize', handleResize)
    }, [])

    useEffect(() => {
        Promise.all([getStudents(), getDepartments()])
            .then(([sRes, dRes]) => {
                setStudents(Array.isArray(sRes.data) ? sRes.data : [])
                setDepts(Array.isArray(dRes.data) ? dRes.data : [])
            })
            .catch(() => {
                setStudents([])
                setDepts([])
            })
            .finally(() => setLoading(false))
    }, [])

    const filtered = useMemo(() => {
        let result = [...students]
        if (deptFilter) result = result.filter(s => s.department === deptFilter)
        if (typeFilter) {
            result = result.filter(s => {
                const val = (s.ppo_type || '').toUpperCase()
                if (typeFilter === 'FTE') return val === 'FTE' || val === ''
                if (typeFilter === 'PPO') return val.includes('PPO')
                if (typeFilter === 'Intern') return val.includes('INTERN') && !val.includes('PPO')
                return true
            })
        }
        if (search) {
            const q = search.toLowerCase()
            result = result.filter(s =>
                s.name?.toLowerCase().includes(q) ||
                s.company?.toLowerCase().includes(q) ||
                s.role?.toLowerCase().includes(q) ||
                s.roll_no?.toLowerCase().includes(q)
            )
        }
        return result
    }, [search, deptFilter, typeFilter, students])

    const inputStyle = {
        padding: '8px 14px',
        backgroundColor: '#0f172a',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '8px',
        color: 'white',
        fontSize: '14px',
        outline: 'none'
    }

    return (
        <div>
            <h1 style={{ color: 'white', fontSize: isMobile ? '18px' : '22px', fontWeight: 700, marginBottom: '8px' }}>
                All Students
            </h1>
            <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '20px' }}>
                {filtered.length} of {students.length} students
            </p>

            {/* ── Filters ── */}
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
                <input
                    type="text"
                    placeholder="Search name, company, role..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    style={{ ...inputStyle, flex: '1', minWidth: '200px' }}
                />
                <select
                    value={deptFilter}
                    onChange={e => setDeptFilter(e.target.value)}
                    style={{ ...inputStyle, color: '#94a3b8', cursor: 'pointer' }}
                >
                    <option value="">All Departments</option>
                    {depts.map(d => (
                        <option key={d.department} value={d.department}>{d.department}</option>
                    ))}
                </select>
                <select
                    value={typeFilter}
                    onChange={e => setTypeFilter(e.target.value)}
                    style={{ ...inputStyle, color: '#94a3b8', cursor: 'pointer' }}
                >
                    <option value="">All Types</option>
                    <option value="FTE">FTE</option>
                    <option value="PPO">PPO</option>
                    <option value="Intern">Intern</option>
                </select>
                {(search || deptFilter || typeFilter) && (
                    <button
                        onClick={() => { setSearch(''); setDeptFilter(''); setTypeFilter('') }}
                        style={{ ...inputStyle, backgroundColor: 'rgba(255,255,255,0.08)', color: '#94a3b8', cursor: 'pointer' }}
                    >
                        Clear
                    </button>
                )}
            </div>

            {/* ── Table ── */}
            {loading ? (
                <p style={{ color: '#64748b' }}>Loading...</p>
            ) : (
                <div style={{ overflowX: 'auto', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.07)' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                        <thead>
                            <tr style={{ backgroundColor: '#0f172a', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                                {['#', 'Name', 'Roll No', 'Dept', 'Company', 'Role', 'Type', 'CTC / Stipend', 'Date'].map(h => (
                                    <th key={h} style={{
                                        padding: '12px 14px', textAlign: 'left', color: '#64748b',
                                        fontWeight: 600, fontSize: '11px', textTransform: 'uppercase',
                                        letterSpacing: '0.05em', whiteSpace: 'nowrap'
                                    }}>
                                        {h}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {filtered.map((s, i) => (
                                <tr
                                    key={s.id ?? i}
                                    style={{
                                        borderBottom: '1px solid rgba(255,255,255,0.05)',
                                        backgroundColor: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)'
                                    }}
                                >
                                    <td style={{ padding: '10px 14px', color: '#475569' }}>{i + 1}</td>
                                    <td style={{ padding: '10px 14px', color: 'white', fontWeight: 500, whiteSpace: 'nowrap' }}>
                                        {s.name}
                                    </td>
                                    <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.roll_no || '—'}</td>
                                    <td style={{ padding: '10px 14px' }}>{badge(s.department, '#818cf8')}</td>
                                    <td style={{ padding: '10px 14px', color: '#e2e8f0', fontWeight: 500, whiteSpace: 'nowrap' }}>
                                        {s.company || '—'}
                                    </td>
                                    <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.role || '—'}</td>
                                    <td style={{ padding: '10px 14px' }}>
                                        {ppoLabel(s.ppo_type)
                                            ? badge(ppoLabel(s.ppo_type), ppoColor(s.ppo_type))
                                            : '—'
                                        }
                                    </td>
                                    <td style={{
                                        padding: '10px 14px',
                                        color: s.ctc_lpa ? '#fbbf24' : '#94a3b8',
                                        fontVariantNumeric: 'tabular-nums',
                                        fontWeight: 600,
                                        whiteSpace: 'nowrap'
                                    }}>
                                        {s.ctc_lpa
                                            ? `${s.ctc_lpa} LPA`
                                            : s.stipend
                                                ? `₹${s.stipend}/mo`
                                                : '—'
                                        }
                                    </td>
                                    <td style={{ padding: '10px 14px', color: '#64748b', whiteSpace: 'nowrap' }}>
                                        {formatDate(s.date)}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    {filtered.length === 0 && (
                        <div style={{ padding: '40px', textAlign: 'center', color: '#475569' }}>
                            No students match your filters.
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}