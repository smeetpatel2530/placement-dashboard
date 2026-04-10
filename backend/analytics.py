import json
import statistics
from database import fetch_all_students, fetch_students_filtered
from collections import defaultdict, Counter


with open("config.json") as f:
    CONFIG = json.load(f)

BATCH_STRENGTH = CONFIG["batch_strength"]

MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Full placement season: Oct 2025 → JUl 2027 (extend as needed)
TIMELINE_ORDER = [
    "Oct 2024", "Nov 2024", "Dec 2024",
    "Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025", "May 2025",
    "Jun 2025", "Jul 2025", "Aug 2025", "Sep 2025",
    "Oct 2025", "Nov 2025", "Dec 2025",
    "Jan 2026", "Feb 2026", "Mar 2026", "Apr 2026", "May 2026",
    "Jun 2026", "Jul 2026", "Aug 2026", "Sep 2026",
    "Oct 2026", "Nov 2026", "Dec 2026",
    "Jan 2027", "Feb 2027", "Mar 2027", "Apr 2027", "May 2027",
    "Jun 2027", "Jul 2027",
]


def _median(values):
    clean = [v for v in values if v is not None and v > 0]
    return round(statistics.median(clean), 2) if clean else 0.0


def _avg(values):
    clean = [v for v in values if v is not None and v > 0]
    return round(sum(clean) / len(clean), 2) if clean else 0.0


def _classify_offer(ppo_type_raw: str) -> str:
    """
    Normalize raw ppo_type values into: 'FTE', 'PPO', 'Intern'
    Handles: '11M Intern+PPO', '2M Intern', 'FTE', 'PPO', '-', None
    """
    val = (ppo_type_raw or "").strip().upper()
    if not val or val in ["-", "NAN", "NONE", ""]:
        return "FTE"
    if "PPO" in val and "INTERN" in val:
        return "PPO"        # Intern who converted to PPO
    if "INTERN" in val:
        return "Intern"
    if "PPO" in val:
        return "PPO"
    return "FTE"


def get_overall_stats() -> dict:
    students = fetch_all_students()
    total = len(students)
    total_batch = sum(BATCH_STRENGTH.values())

    ctc_list = [s["ctc_lpa"] for s in students if s.get("ctc_lpa") and s["ctc_lpa"] > 0]
    stipend_list = [s.get("stipend_pm") for s in students if s.get("stipend_pm") and s["stipend_pm"] > 0]

    fte_count = 0
    ppo_count = 0
    intern_count = 0
    for s in students:
        offer = _classify_offer(s.get("ppo_type"))
        if offer == "FTE":
            fte_count += 1
        elif offer == "PPO":
            ppo_count += 1
        else:
            intern_count += 1

    return {
        "total_placed": total,
        "total_batch": total_batch,
        "placement_percentage": round((total / total_batch) * 100, 1) if total_batch else 0,
        "median_ctc": _median(ctc_list),
        "max_ctc": round(max(ctc_list), 2) if ctc_list else 0,
        "min_ctc": round(min(ctc_list), 2) if ctc_list else 0,
        "avg_ctc": _avg(ctc_list),
        "avg_stipend": _avg(stipend_list),
        "fte_count": fte_count,
        "ppo_count": ppo_count,
        "intern_count": intern_count,
    }


def get_dept_stats() -> list:
    students = fetch_all_students()
    if not students:
        return []

    dept_map = defaultdict(list)
    for s in students:
        dept = (s.get("department") or "Unknown").strip().upper()
        dept_map[dept].append(s)

    result = []
    for dept, group in dept_map.items():
        if dept in ["UNKNOWN", "NAN", ""]:
            continue

        batch = BATCH_STRENGTH.get(dept, len(group))
        placed = len(group)

        fte_count = ppo_count = intern_count = 0
        for s in group:
            offer = _classify_offer(s.get("ppo_type"))
            if offer == "FTE":
                fte_count += 1
            elif offer == "PPO":
                ppo_count += 1
            else:
                intern_count += 1

        ctc_list = [s["ctc_lpa"] for s in group if s.get("ctc_lpa") and s["ctc_lpa"] > 0]
        stipend_list = [s.get("stipend_pm") for s in group if s.get("stipend_pm") and s["stipend_pm"] > 0]

        result.append({
            "department": dept,
            "placed": placed,
            "batch_strength": batch,
            "percentage": round((placed / batch) * 100, 1) if batch > 0 else 0,
            "median_ctc": _median(ctc_list),
            "max_ctc": round(max(ctc_list), 2) if ctc_list else None,
            "avg_ctc": _avg(ctc_list),
            "avg_stipend": _avg(stipend_list),
            "fte_count": fte_count,
            "ppo_count": ppo_count,
            "intern_count": intern_count,
        })

    return sorted(result, key=lambda x: -x["placed"])


def get_company_stats() -> list:
    students = fetch_all_students()
    company_map = defaultdict(list)
    for s in students:
        company = (s.get("company") or "").strip()
        if company and company.lower() not in ["unknown", "nan", ""]:
            company_map[company].append(s)

    result = []
    for company, group in sorted(company_map.items(), key=lambda x: -len(x[1])):
        ctc_list = [s["ctc_lpa"] for s in group if s.get("ctc_lpa") and s["ctc_lpa"] > 0]
        stipend_list = [s.get("stipend_pm") for s in group          # ← also fix: stipend_pm not stipend
                        if s.get("stipend_pm") and s["stipend_pm"] > 0]
        depts = Counter(s.get("department", "") for s in group)
        roles = list({(s.get("role") or "").strip() for s in group  # ← ADD THIS
                      if s.get("role") and s["role"].strip()})

        result.append({
            "company": company,
            "count": len(group),
            "avg_ctc": _avg(ctc_list),
            "avg_stipend": _avg(stipend_list),
            "departments": dict(depts),
            "roles": roles,                                          # ← ADD THIS
        })

    return result[:15]


def get_timeline_stats() -> list:
    students = fetch_all_students()
    month_counter = Counter()

    for s in students:
        date_raw = str(s.get("date") or "").strip()
        if not date_raw or date_raw.lower() in ["nan", "none", ""]:
            continue
        try:
            date_part = date_raw.split(" ")[0].split("T")[0]
            parts = date_part.replace("/", "-").split("-")
            if len(parts) == 3:
                if len(parts[0]) == 4:          # YYYY-MM-DD
                    year, month = int(parts[0]), int(parts[1])
                else:                            # DD-MM-YYYY
                    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                    if year < 100:
                        year += 2000
                if 1 <= month <= 12 and 2000 <= year <= 2030:
                    label = f"{MONTH_NAMES[month]} {year}"
                    month_counter[label] += 1
        except (ValueError, IndexError):
            continue

    return [{"month": m, "count": month_counter[m]}
            for m in TIMELINE_ORDER if m in month_counter]


def get_ctc_distribution() -> list:
    students = fetch_all_students()
    buckets = {
        "< 10 LPA": 0, "10–15 LPA": 0, "15–20 LPA": 0,
        "20–25 LPA": 0, "25–30 LPA": 0, "30+ LPA": 0,
        "Intern Only": 0,
    }
    for s in students:
        ctc = s.get("ctc_lpa")
        offer = _classify_offer(s.get("ppo_type"))

        # Intern-only rows (no CTC, just stipend)
        if offer == "Intern" and (ctc is None or ctc <= 0):
            buckets["Intern Only"] += 1
            continue

        if ctc is None or ctc <= 0:
            continue

        if ctc < 10:
            buckets["< 10 LPA"] += 1
        elif ctc < 15:
            buckets["10–15 LPA"] += 1
        elif ctc < 20:
            buckets["15–20 LPA"] += 1
        elif ctc < 25:
            buckets["20–25 LPA"] += 1
        elif ctc < 30:
            buckets["25–30 LPA"] += 1
        else:
            buckets["30+ LPA"] += 1

    # Only return buckets with data
    return [{"range": k, "count": v} for k, v in buckets.items() if v > 0]


def get_role_stats() -> list:
    students = fetch_all_students()
    if not students:
        return []
    role_counter = Counter()
    for s in students:
        role = (s.get("role") or "").strip()
        if role and role.lower() not in ["", "nan", "none"]:
            role_counter[role] += 1
    return [{"role": r, "count": c} for r, c in role_counter.most_common(10)]


def get_role_breakdown() -> list:
    students = fetch_all_students()
    ROLE_CATEGORIES = {
        "Software Engineer": ["software", "sde", "developer", "swe", "engineer"],
        "AI / ML / Data": ["ai", "ml", "data scientist", "data analyst",
                           "data engineering", "ai/ds", "ai/ml"],
        "Research / R&D": ["r&d", "research", "gte", "pgte"],
        "Embedded / Hardware": ["embedded", "vlsi", "hardware", "firmware"],
        "Analyst / Finance": ["analyst", "consulting", "consultant", "finance"],
        "Cybersecurity": ["security", "cyber", "soc", "penetration"],
        "Academic": ["professor", "asst.", "lecturer"],
        "Other": [],
    }

    category_counter = Counter()
    for s in students:
        role_raw = (s.get("role") or "").lower()
        assigned = "Other"
        for cat, keywords in ROLE_CATEGORIES.items():
            if any(kw in role_raw for kw in keywords):
                assigned = cat
                break
        category_counter[assigned] += 1

    return [{"role": k, "count": v} for k, v in category_counter.most_common()]


def get_ppo_intern_breakdown() -> list:
    """
    New endpoint for 2027: breakdown of Intern durations
    e.g. '11M Intern+PPO': 3, '2M Intern': 5
    """
    students = fetch_all_students()
    counter = Counter()
    for s in students:
        val = (s.get("ppo_type") or "").strip()
        if val and val not in ["-", "", "nan"]:
            counter[val] += 1
    return [{"type": k, "count": v} for k, v in counter.most_common()]