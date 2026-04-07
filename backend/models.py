from pydantic import BaseModel, Field
from typing import Optional


# ─── Overall Dashboard Stats ────────────────────────────────────────────────

class OverallStats(BaseModel):
    total_placed: int
    total_batch: int          # total batch strength across all depts
    placement_percentage: float
    median_ctc: float
    max_ctc: float
    min_ctc: float
    avg_ctc: float
    avg_stipend: float
    fte_count: int            # placed via direct FTE (no internship)
    ppo_count: int            # intern who got PPO (confirmed or pending)
    intern_count: int         # intern only (no PPO yet / 2M short-term)


# ─── Department-wise Stats ───────────────────────────────────────────────────

class DeptStats(BaseModel):
    department: str
    placed: int
    batch_strength: int       # total students in that dept
    percentage: float
    median_ctc: float
    max_ctc: Optional[float]
    avg_ctc: float
    avg_stipend: float
    fte_count: int
    ppo_count: int
    intern_count: int


# ─── Company Stats ───────────────────────────────────────────────────────────

class CompanyStats(BaseModel):
    company: str
    count: int
    avg_ctc: float
    avg_stipend: float
    departments: dict[str, int]   # e.g. {"CSE": 3, "DSC": 1}
    roles: list[str]              # distinct roles offered by this company


# ─── Timeline ────────────────────────────────────────────────────────────────

class TimelineStat(BaseModel):
    month: str      # e.g. "Oct 2025"
    count: int


# ─── CTC Distribution Bucket ─────────────────────────────────────────────────

class CtcBucket(BaseModel):
    range: str      # e.g. "10–15 LPA"
    count: int


# ─── Role Stats ──────────────────────────────────────────────────────────────

class RoleStat(BaseModel):
    role: str
    count: int


# ─── PPO / Intern Breakdown ───────────────────────────────────────────────────

class PpoInternBreakdown(BaseModel):
    type: str       # raw value e.g. "11M Intern+PPO", "2M Intern", "FTE"
    count: int


# ─── Individual Student ──────────────────────────────────────────────────────

class Student(BaseModel):
    id: int
    name: Optional[str]           = None
    roll_no: Optional[str]        = None
    department: Optional[str]     = None
    company: Optional[str]        = None
    role: Optional[str]           = None
    ppo_type: Optional[str]       = None   # classified: "FTE" | "PPO" | "Intern"
    ppo_type_raw: Optional[str]   = None   # raw Excel value: "11M Intern+PPO" etc.
    ppo_confirmed: Optional[str]  = None   # "PPO Confirmation Status" column
    ctc_lpa: Optional[float]      = None
    stipend_pm: Optional[float]   = None
    date: Optional[str]           = None
    batch_year: Optional[int]     = None


# ─── Multi-batch summary (for future /api/batches endpoint) ──────────────────

class BatchYearStats(BaseModel):
    batch_year: int
    total_placed: int
    total_batch: int
    placement_percentage: float
    avg_ctc: float
    median_ctc: float
    departments: list[str]