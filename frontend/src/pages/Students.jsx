


// import { useEffect, useState, useMemo } from 'react'
// import { getStudents, getDepartments } from '../services/api'

// function badge(text, color) {
//     return (
//         <span style={{
//             display: 'inline-block',
//             padding: '2px 8px',
//             borderRadius: '4px',
//             fontSize: '10px',
//             fontWeight: 700,
//             backgroundColor: color + '15',
//             border: `1px solid ${color}44`,
//             color: color,
//             whiteSpace: 'nowrap',
//             textTransform: 'uppercase'
//         }}>
//             {text}
//         </span>
//     )
// }

// function formatDate(dateStr) {
//     if (!dateStr) return '—'
//     const d = String(dateStr).split(' ')[0].split('T')[0]
//     if (!d || d === 'None' || d === 'nan') return '—'
//     const parts = d.split('-')
//     if (parts.length === 3) return `${parts[2]}/${parts[1]}/${parts[0]}`
//     return d
// }

// function ppoColor(t) {
//     if (!t) return '#818cf8'
//     const val = t.toUpperCase()
//     if (val.includes('PPO')) return '#a3e635' // Lime for PPO
//     if (val.includes('INTERN')) return '#fb923c' // Orange for Intern
//     if (val.includes('FTE')) return '#22d3ee' // Cyan for FTE
//     return '#94a3b8'
// }

// export default function Students() {
//     const [students, setStudents] = useState([])
//     const [depts, setDepts] = useState([])
//     const [search, setSearch] = useState('')
//     const [deptFilter, setDeptFilter] = useState('')
//     const [typeFilter, setTypeFilter] = useState('')
//     const [loading, setLoading] = useState(true)
//     const [isMobile, setIsMobile] = useState(window.innerWidth < 640)

//     useEffect(() => {
//         const handleResize = () => setIsMobile(window.innerWidth < 640)
//         window.addEventListener('resize', handleResize)
//         return () => window.removeEventListener('resize', handleResize)
//     }, [])

//     useEffect(() => {
//         Promise.all([getStudents(), getDepartments()])
//             .then(([sRes, dRes]) => {
//                 setStudents(Array.isArray(sRes.data) ? sRes.data : [])
//                 setDepts(Array.isArray(dRes.data) ? dRes.data : [])
//             })
//             .catch(() => {
//                 setStudents([])
//                 setDepts([])
//             })
//             .finally(() => setLoading(false))
//     }, [])

//     // ... (keep badge and formatDate functions)

//     const filtered = useMemo(() => {
//         let result = [...students]
//         if (deptFilter) result = result.filter(s => s.department === deptFilter)

//         if (typeFilter) {
//             result = result.filter(s => {
//                 // We use the simplified 'ppo_type' (PPO, Intern, FTE) for the filter dropdown
//                 // while keeping the display as raw data.
//                 const type = (s.ppo_type || 'FTE').toUpperCase()
//                 if (typeFilter === 'FTE') return type === 'FTE'
//                 if (typeFilter === 'PPO') return type === 'PPO'
//                 if (typeFilter === 'Intern') return type === 'INTERN'
//                 return true
//             })
//         }

//         if (search) {
//             const q = search.toLowerCase()
//             result = result.filter(s =>
//                 s.name?.toLowerCase().includes(q) ||
//                 s.company?.toLowerCase().includes(q) ||
//                 s.role?.toLowerCase().includes(q)
//             )
//         }
//         return result
//     }, [search, deptFilter, typeFilter, students])



//     const inputStyle = {
//         padding: '8px 14px',
//         backgroundColor: '#0f172a',
//         border: '1px solid rgba(255,255,255,0.1)',
//         borderRadius: '8px',
//         color: 'white',
//         fontSize: '14px',
//         outline: 'none'
//     }

//     return (
//         <div>
//             <h1 style={{ color: 'white', fontSize: isMobile ? '18px' : '22px', fontWeight: 700, marginBottom: '8px' }}>
//                 All Students
//             </h1>
//             <p style={{ color: '#64748b', fontSize: '14px', marginBottom: '20px' }}>
//                 {filtered.length} of {students.length} students
//             </p>

//             <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' }}>
//                 <input
//                     type="text"
//                     placeholder="Search name, company, role..."
//                     value={search}
//                     onChange={e => setSearch(e.target.value)}
//                     style={{ ...inputStyle, flex: '1', minWidth: '200px' }}
//                 />
//                 <select
//                     value={deptFilter}
//                     onChange={e => setDeptFilter(e.target.value)}
//                     style={{ ...inputStyle, color: '#94a3b8', cursor: 'pointer' }}
//                 >
//                     <option value="">All Departments</option>
//                     {depts.map(d => (
//                         <option key={d.department} value={d.department}>{d.department}</option>
//                     ))}
//                 </select>
//                 <select
//                     value={typeFilter}
//                     onChange={e => setTypeFilter(e.target.value)}
//                     style={{ ...inputStyle, color: '#94a3b8', cursor: 'pointer' }}
//                 >
//                     <option value="">All Types</option>
//                     <option value="FTE">FTE</option>
//                     <option value="PPO">PPO</option>
//                     <option value="Intern">Intern</option>
//                 </select>
//             </div>

//             {loading ? (
//                 <p style={{ color: '#64748b' }}>Loading...</p>
//             ) : (
//                 <div style={{ overflowX: 'auto', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.07)' }}>
//                     <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
//                         <thead>
//                             <tr style={{ backgroundColor: '#0f172a', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
//                                 {['#', 'Name', 'Roll No', 'Dept', 'Company', 'Role', 'Type', 'CTC / Stipend', 'Date'].map(h => (
//                                     <th key={h} style={{
//                                         padding: '12px 14px', textAlign: 'left', color: '#64748b',
//                                         fontWeight: 600, fontSize: '11px', textTransform: 'uppercase',
//                                         letterSpacing: '0.05em', whiteSpace: 'nowrap'
//                                     }}>
//                                         {h}
//                                     </th>
//                                 ))}
//                             </tr>
//                         </thead>
//                         <tbody>
//                             {filtered.map((s, i) => (
//                                 <tr key={s.id ?? i} style={{
//                                     borderBottom: '1px solid rgba(255,255,255,0.05)',
//                                     backgroundColor: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)'
//                                 }}>
//                                     <td style={{ padding: '10px 14px', color: '#475569' }}>{i + 1}</td>
//                                     <td style={{ padding: '10px 14px', color: 'white', fontWeight: 500, whiteSpace: 'nowrap' }}>{s.name}</td>
//                                     <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.roll_no || '—'}</td>
//                                     <td style={{ padding: '10px 14px' }}>{badge(s.department, '#818cf8')}</td>
//                                     <td style={{ padding: '10px 14px', color: '#e2e8f0', fontWeight: 500, whiteSpace: 'nowrap' }}>{s.company || '—'}</td>
//                                     <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.role || '—'}</td>
//                                     <td style={{ padding: '10px 14px' }}>
//                                         {/* Always show the raw data from the Excel cell */}
//                                         {badge(s.ppo_type_raw || s.ppo_type || 'FTE', ppoColor(s.ppo_type_raw || s.ppo_type))}
//                                     </td>
//                                     <td style={{
//                                         padding: '10px 14px',
//                                         color: s.ctc_lpa ? '#fbbf24' : (s.stipend_pm ? '#22d3ee' : '#94a3b8'),
//                                         fontVariantNumeric: 'tabular-nums',
//                                         fontWeight: 600,
//                                         whiteSpace: 'nowrap'
//                                     }}>
//                                         {s.ctc_lpa
//                                             ? `${s.ctc_lpa} LPA`
//                                             : s.stipend_pm
//                                                 ? `₹${Number(s.stipend_pm).toLocaleString('en-IN')}K /mo`
//                                                 : '—'
//                                         }
//                                     </td>
//                                     <td style={{ padding: '10px 14px', color: '#64748b', whiteSpace: 'nowrap' }}>{formatDate(s.date)}</td>
//                                 </tr>
//                             ))}
//                         </tbody>
//                     </table>
//                 </div>
//             )}
//         </div>
//     )
// }

import { useEffect, useState, useMemo } from 'react'
import { getStudents, getDepartments } from '../services/api'

function badge(text, color) {
    return (
        <span style={{
            display: 'inline-block',
            padding: '2px 8px',
            borderRadius: '4px',
            fontSize: '10px',
            fontWeight: 700,
            backgroundColor: color + '15',
            border: `1px solid ${color}44`,
            color: color,
            whiteSpace: 'nowrap',
            textTransform: 'uppercase'
        }}>
            {text || '—'}
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

function typeColor(raw) {
    const t = String(raw || '').toUpperCase()
    if (!t) return '#94a3b8'
    if (t.includes('INTERN')) return '#fb923c'
    if (t.includes('PPO')) return '#a3e635'
    if (t.includes('FTE')) return '#22d3ee'
    if (t.includes('GTE')) return '#60a5fa'
    return '#c084fc'
}

function normalizeType(value) {
    if (value == null) return ''
    return String(value).trim()
}

export default function Students() {
    const [students, setStudents] = useState([])
    const [depts, setDepts] = useState([])
    const [types, setTypes] = useState([])
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

    async function loadAll() {
        setLoading(true)
        try {
            const [sRes, dRes] = await Promise.all([
                getStudents(),
                getDepartments(),
            ])
            setStudents(Array.isArray(sRes.data) ? sRes.data : [])
            setDepts(Array.isArray(dRes.data) ? dRes.data : [])

            const rawTypes = Array.isArray(sRes.data)
                ? [...new Set(sRes.data.map(s => normalizeType(s.type || s.ppo_type_raw || s.ppo_type)).filter(Boolean))].sort((a, b) => a.localeCompare(b))
                : []
            setTypes(rawTypes)
        } catch {
            setStudents([])
            setDepts([])
            setTypes([])
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadAll()
    }, [])

    const filtered = useMemo(() => {
        let result = [...students]

        if (deptFilter) result = result.filter(s => s.department === deptFilter)

        if (typeFilter) {
            result = result.filter(s => normalizeType(s.type || s.ppo_type_raw || s.ppo_type) === typeFilter)
        }

        if (search.trim()) {
            const q = search.toLowerCase()
            result = result.filter(s =>
                String(s.name || '').toLowerCase().includes(q) ||
                String(s.company || '').toLowerCase().includes(q) ||
                String(s.role || '').toLowerCase().includes(q) ||
                String(s.roll_no || '').toLowerCase().includes(q) ||
                String(s.department || '').toLowerCase().includes(q) ||
                String(s.type || s.ppo_type_raw || s.ppo_type || '').toLowerCase().includes(q)
            )
        }

        // ── Sort: LPA students first (highest to lowest), then stipend students (highest to lowest)
        result.sort((a, b) => {
            const aHasCtc = a.ctc_lpa != null && a.ctc_lpa !== ''
            const bHasCtc = b.ctc_lpa != null && b.ctc_lpa !== ''

            if (aHasCtc && bHasCtc) return Number(b.ctc_lpa) - Number(a.ctc_lpa)  // both LPA → higher first
            if (aHasCtc && !bHasCtc) return -1  // a has LPA, b doesn't → a comes first
            if (!aHasCtc && bHasCtc) return 1   // b has LPA, a doesn't → b comes first

            // Both have only stipend → sort by stipend descending
            const aStipend = a.stipend_pm != null && a.stipend_pm !== '' ? Number(a.stipend_pm) : -1
            const bStipend = b.stipend_pm != null && b.stipend_pm !== '' ? Number(b.stipend_pm) : -1
            return bStipend - aStipend
        })

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
                    {types.map(t => (
                        <option key={t} value={t}>{t}</option>
                    ))}
                </select>
            </div>

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
                            {filtered.map((s, i) => {
                                const rawType = normalizeType(s.type || s.ppo_type_raw || s.ppo_type)
                                return (
                                    <tr key={s.id ?? i} style={{
                                        borderBottom: '1px solid rgba(255,255,255,0.05)',
                                        backgroundColor: i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.01)'
                                    }}>
                                        <td style={{ padding: '10px 14px', color: '#475569' }}>{i + 1}</td>
                                        <td style={{ padding: '10px 14px', color: 'white', fontWeight: 500, whiteSpace: 'nowrap' }}>{s.name || '—'}</td>
                                        <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.roll_no || '—'}</td>
                                        <td style={{ padding: '10px 14px' }}>{badge(s.department, '#818cf8')}</td>
                                        <td style={{ padding: '10px 14px', color: '#e2e8f0', fontWeight: 500, whiteSpace: 'nowrap' }}>{s.company || '—'}</td>
                                        <td style={{ padding: '10px 14px', color: '#94a3b8' }}>{s.role || '—'}</td>
                                        <td style={{ padding: '10px 14px' }}>
                                            {badge(rawType || '—', typeColor(rawType))}
                                        </td>
                                        <td style={{
                                            padding: '10px 14px',
                                            color: s.ctc_lpa != null && s.ctc_lpa !== '' ? '#fbbf24' : (s.stipend_pm != null && s.stipend_pm !== '' ? '#22d3ee' : '#94a3b8'),
                                            fontVariantNumeric: 'tabular-nums',
                                            fontWeight: 600,
                                            whiteSpace: 'nowrap'
                                        }}>
                                            {s.ctc_lpa != null && s.ctc_lpa !== ''
                                                ? `${s.ctc_lpa} LPA`
                                                : s.stipend_pm != null && s.stipend_pm !== ''
                                                    ? `₹${Number(s.stipend_pm).toLocaleString('en-IN')} /mo`
                                                    : '—'
                                            }
                                        </td>
                                        <td style={{ padding: '10px 14px', color: '#64748b', whiteSpace: 'nowrap' }}>{formatDate(s.date)}</td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}