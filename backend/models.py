from pydantic import BaseModel
from typing import Optional, List

class Student(BaseModel):
    id: int
    name: str
    roll_no: Optional[str]
    department: str
    company: Optional[str]
    role: Optional[str]
    ppo_type: Optional[str]       
    ppo_type_raw: Optional[str]   
    ppo_confirmed: Optional[str]
    ctc_lpa: Optional[float]
    stipend_pm: Optional[float]   
    date: Optional[str]
    batch_year: Optional[int]
 
class DeptStat(BaseModel):
    department: str
    placed: int
    batch_strength: int
    percentage: float
    median_ctc: Optional[float] = None
    max_ctc: Optional[float] = None
    avg_ctc: Optional[float] = None
    fte_count: Optional[int] = None
    ppo_count: Optional[int] = None
    intern_count: Optional[int] = None
    fte_intern_count: int 

class CompanyStat(BaseModel):
    company: str
    count: int
    avg_ctc: Optional[float]

class TimelineStat(BaseModel):
    month: str
    count: int

class CTCBucket(BaseModel):
    range: str
    count: int

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