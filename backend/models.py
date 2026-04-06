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


class StudentRecord(BaseModel):
    id: int
    name: str
    roll_no: Optional[str]
    department: Optional[str]
    company: Optional[str]
    role: Optional[str]
    ctc_lpa: Optional[float]
    stipend: Optional[float]
    ppo_type: Optional[str]
    date: Optional[str]


class PpoInternBreakdown(BaseModel):
    type: str
    count: int