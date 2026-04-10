from pydantic import BaseModel, Field
from typing import Optional


# ─── Overall Dashboard Stats ────────────────────────────────────────────────

class OverallStats(BaseModel):
    total_placed: int
    total_batch: int          
    placement_percentage: float
    median_ctc: float
    max_ctc: float
    min_ctc: float
    avg_ctc: float
    avg_stipend: float
    fte_count: int            
    ppo_count: int            
    intern_count: int         


# ─── Department-wise Stats ───────────────────────────────────────────────────

class DeptStats(BaseModel):
    department: str
    placed: int
    batch_strength: int      
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
    departments: dict[str, int]   
    roles: list[str]              


# ─── Timeline ────────────────────────────────────────────────────────────────

class TimelineStat(BaseModel):
    month: str     
    count: int


# ─── CTC Distribution Bucket ─────────────────────────────────────────────────

class CtcBucket(BaseModel):
    range: str      
    count: int


# ─── Role Stats ──────────────────────────────────────────────────────────────

class RoleStat(BaseModel):
    role: str
    count: int


# ─── PPO / Intern Breakdown ───────────────────────────────────────────────────

class PpoInternBreakdown(BaseModel):
    type: str      
    count: int


# ─── Individual Student ──────────────────────────────────────────────────────

class Student(BaseModel):
    id: int
    name: Optional[str]           = None
    roll_no: Optional[str]        = None
    department: Optional[str]     = None
    company: Optional[str]        = None
    role: Optional[str]           = None
    ppo_type: Optional[str]       = None   
    ppo_type_raw: Optional[str]   = None   
    ppo_confirmed: Optional[str]  = None   
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