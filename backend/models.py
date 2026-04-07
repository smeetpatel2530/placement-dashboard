from pydantic import BaseModel
from typing import Optional


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


class CompanyStats(BaseModel):
    company: str
    count: int
    avg_ctc: float
    avg_stipend: float
    departments: dict


class TimelineStat(BaseModel):
    month: str
    count: int


class CtcBucket(BaseModel):
    range: str
    count: int


class RoleStat(BaseModel):
    role: str
    count: int


class Student(BaseModel):
    id: int
    name: Optional[str]
    roll_no: Optional[str]
    department: Optional[str]
    company: Optional[str]
    role: Optional[str]
    ppo_type: Optional[str]
    ppo_type_raw: Optional[str]
    ppo_confirmed: Optional[str]
    ctc_lpa: Optional[float]      
    stipend_pm: Optional[float]
    date: Optional[str]
    batch_year: Optional[int]


class PpoInternBreakdown(BaseModel):
    type: str
    count: int