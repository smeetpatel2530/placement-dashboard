import pandas as pd
import re
import os
from database import clear_and_insert, init_db

EXCEL_PATH = os.environ.get("EXCEL_PATH", "data/placements.xlsx")

SHEET_MAP = {
    "DSC": "DSC", "SWE": "SWE", "CSE": "CSE",
    "ITY": "ITY", "AFI": "AFI", "Research": "Research",
    "CYS": "CYS", "RCO": "RCO", "RIT": "RIT", "RSE": "RSE",
}

# ← FIXED: added ALL real column name variants from the actual Excel
COL_NAME       = ["NAME", "Name"]
COL_ROLL       = ["ROLL NO", "Roll No", "ROLL_NO", "ROLL NO."]
COL_COMPANY    = ["COMPANY", "Company"]
COL_ROLE       = ["ROLE", "Role"]
COL_PPO_TYPE   = [
    "PPO / INTERN", "PPO/INTERN", "PPO_INTERN",
    "PPO INTERN",           # ← actual column in your Excel
    "PPO / INTERN ",
]
COL_PPO_STATUS = [
    "PPO Confirmation Status", "PPO Status", "PPO_Status",
    "PPO CONFIRMATION STATUS",
]
COL_CTC        = [
    "CTC (LPA)", "CTC(LPA)", "CTC",
    "CTC LPA",              # ← actual column in your Excel
    "CTC(LPA) ",
]
COL_STIPEND    = [
    "Stipend (PM)", "Stipend(PM)", "Stipend (k PM)", "STIPEND",
    "Stipend PM",           # ← actual column in your Excel
    "STIPEND PM",
]
COL_DATE       = ["Date", "DATE", "date"]


def _pick_col(df_cols, candidates):
    # exact match first
    for c in candidates:
        if c in df_cols:
            return c
    # case-insensitive fallback
    df_cols_upper = {c.upper(): c for c in df_cols}
    for c in candidates:
        if c.upper() in df_cols_upper:
            return df_cols_upper[c.upper()]
    return None


def _safe_float(val):
    if val is None or str(val).strip() in ["-", "–", "—", "NA", "na", "nan", ""]:
        return None
    try:
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def classify_offer_type(raw_val) -> str:
    if not raw_val or str(raw_val).strip() in ["-", "–", "—", "", "nan", "None"]:
        return "FTE"
    val = str(raw_val).strip().upper()
    if "PPO" in val:
        return "PPO"
    if "FTE" in val and "INTERN" in val:
        return "FTE_via_Intern"
    if "FTE" in val:
        return "FTE"
    if "INTERN" in val:
        return "Intern"
    return "FTE"


def _detect_batch_year(filepath: str) -> int:
    fname = os.path.basename(filepath).upper()
    if "2027" in fname:
        return 2027
    if "2026" in fname:
        return 2026
    return 2027


def parse_excel(filepath: str) -> list[dict]:
    init_db()
    records = []
    batch_year = _detect_batch_year(filepath)

    try:
        xf = pd.ExcelFile(filepath, engine="openpyxl")
    except Exception as e:
        print(f"[Parser] ERROR opening Excel: {e}")
        return []

    print(f"[Parser] Sheets found: {xf.sheet_names}")

    for sheet_name in xf.sheet_names:
        dept = SHEET_MAP.get(sheet_name.strip())
        if not dept:
            print(f"[Parser] Skipping unmapped sheet: '{sheet_name}'")
            continue

        try:
            df_raw = xf.parse(sheet_name, header=None)
        except Exception as e:
            print(f"[Parser] ERROR reading sheet '{sheet_name}': {e}")
            continue

        # Find header row containing "NAME" or "ROLL NO"
        header_row_idx = None
        for i, row in df_raw.iterrows():
            row_vals = [str(v).strip().upper() for v in row.values]
            if "NAME" in row_vals or "ROLL NO" in row_vals:
                header_row_idx = i
                break

        if header_row_idx is None:
            print(f"[Parser] No header found in sheet '{sheet_name}' — skipping")
            continue

        df = xf.parse(sheet_name, header=header_row_idx)
        df.columns = [str(c).strip() for c in df.columns]

        print(f"[Parser] Sheet '{sheet_name}' columns: {list(df.columns)}")  # ← debug log

        col_name       = _pick_col(df.columns, COL_NAME)
        col_roll       = _pick_col(df.columns, COL_ROLL)
        col_company    = _pick_col(df.columns, COL_COMPANY)
        col_role       = _pick_col(df.columns, COL_ROLE)
        col_ppo_type   = _pick_col(df.columns, COL_PPO_TYPE)
        col_ppo_status = _pick_col(df.columns, COL_PPO_STATUS)
        col_ctc        = _pick_col(df.columns, COL_CTC)
        col_stipend    = _pick_col(df.columns, COL_STIPEND)
        col_date       = _pick_col(df.columns, COL_DATE)

        if col_name is None:
            print(f"[Parser] WARNING: No NAME column found in '{sheet_name}'")
            continue

        sheet_count = 0
        for _, row in df.iterrows():
            name_val = str(row[col_name]).strip() if col_name else ""

            if not name_val or name_val.upper() in [
                "NAN", "NAME", "TOTAL", "COUNT", "", "-"
            ]:
                continue
            if re.match(r"^\d+$", name_val):  # skip row numbers
                continue

            raw_ppo = None
            if col_ppo_type:
                raw_val = str(row[col_ppo_type]).strip()
                raw_ppo = raw_val if raw_val not in ["nan", "-", ""] else None

            record = {
                "name":          name_val,
                "roll_no":       str(row[col_roll]).strip() if col_roll and str(row[col_roll]) != "nan" else None,
                "department":    dept,
                "company":       str(row[col_company]).strip() if col_company and str(row[col_company]) not in ["nan", ""] else "Unknown",
                "role":          str(row[col_role]).strip() if col_role and str(row[col_role]) != "nan" else None,
                "ppo_type":      classify_offer_type(raw_ppo),
                "ppo_type_raw":  raw_ppo,
                "ppo_confirmed": str(row[col_ppo_status]).strip() if col_ppo_status and str(row[col_ppo_status]) != "nan" else None,
                "ctc_lpa":       _safe_float(row[col_ctc]) if col_ctc else None,
                "stipend_pm":    _safe_float(row[col_stipend]) if col_stipend else None,
                "date":          str(row[col_date]).strip() if col_date and str(row[col_date]) != "nan" else None,
                "batch_year":    batch_year,
            }
            records.append(record)
            sheet_count += 1

        print(f"[Parser] Sheet '{sheet_name}' → {sheet_count} students")

    clear_and_insert(records)
    print(f"[Parser] ✅ Total {len(records)} students loaded (batch {batch_year})")
    return records