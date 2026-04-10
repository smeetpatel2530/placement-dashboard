# import pandas as pd
# from datetime import datetime

# BATCH_STRENGTH = {
#     'CSE': 28, 'AFI': 33, 'CYS': 29, 'DSC': 30,
#     'SWE': 25, 'ITY': 25, 'RCO': 12, 'RIT': 9, 'RSE': 15
# }

# VALID_SHEETS = list(BATCH_STRENGTH.keys())

# def classify_offer_type(val):
#     if not val or str(val).strip().lower() in ['-', '', 'nan', 'none']:
#         return 'FTE'
#     v = str(val).upper()
#     if 'PPO' in v and 'INTERN' in v:
#         return 'PPO'
#     if 'INTERN' in v:
#         return 'Intern'
#     return 'FTE'

# def find_header_row(df):
#     """Find the row index that contains NAME or S.NO as header."""
#     for i, row in df.iterrows():
#         vals = [str(v).strip().upper() for v in row if pd.notna(v) and str(v).strip()]
#         if 'NAME' in vals or 'S.NO' in vals or 'SNO' in vals:
#             return i
#     return None

# def parse_excel(filepath: str) -> list[dict]:
#     all_students = []
#     try:
#         xl = pd.ExcelFile(filepath)
#     except Exception as e:
#         print(f"Error opening file: {e}")
#         return []

#     for sheet_name in xl.sheet_names:
#         dept = sheet_name.strip().upper()
#         if dept not in VALID_SHEETS:
#             print(f"Skipping unknown sheet: {sheet_name}")
#             continue

#         try:
#             raw = xl.parse(sheet_name, header=None)
#         except Exception as e:
#             print(f"Error parsing sheet {sheet_name}: {e}")
#             continue

#         header_row = find_header_row(raw)
#         if header_row is None:
#             print(f"No header found in sheet: {sheet_name}")
#             continue

#         df = xl.parse(sheet_name, header=header_row)
#         # Normalize column names
#         df.columns = [str(c).strip().upper().replace('\n', ' ') for c in df.columns]
#         print(f"Sheet {dept} columns: {list(df.columns)}")

#         # Map columns flexibly
#         col_map = {}
#         for c in df.columns:
#             cu = c.upper()
#             if 'NAME' in cu and 'COMPANY' not in cu:
#                 col_map[c] = 'name'
#             elif 'ROLL' in cu or 'ENROLL' in cu:
#                 col_map[c] = 'roll_no'
#             elif 'COMPANY' in cu or 'ORGANISATION' in cu or 'ORGANIZATION' in cu:
#                 col_map[c] = 'company'
#             elif 'ROLE' in cu or 'DESIGNATION' in cu or 'PROFILE' in cu:
#                 col_map[c] = 'role'
#             elif 'PPO' in cu and 'INTERN' in cu:
#                 col_map[c] = 'ppo_intern'
#             elif 'CTC' in cu or 'PACKAGE' in cu:
#                 col_map[c] = 'ctc'
#             elif 'STIPEND' in cu:
#                 col_map[c] = 'stipend'
#             elif 'DATE' in cu:
#                 col_map[c] = 'date'

#         df = df.rename(columns=col_map)

#         if 'name' not in df.columns:
#             print(f"No 'name' column found in sheet {dept} after mapping")
#             continue

#         for _, row in df.iterrows():
#             name = str(row.get('name', '')).strip()
#             # Skip blank/header/total rows
#             if (not name or name.lower() in ['nan', '-', '', 'name'] 
#                     or name.upper() in ['TOTAL', 'S.NO', 'SNO']
#                     or name.isdigit()):
#                 continue

#             # Parse CTC
#             ctc = None
#             ctc_raw = row.get('ctc')
#             if ctc_raw is not None and str(ctc_raw).strip() not in ['-', 'nan', '', 'None']:
#                 try:
#                     ctc = float(ctc_raw)
#                 except (ValueError, TypeError):
#                     ctc = None

#             # Parse date
#             date_str = None
#             date_raw = row.get('date')
#             if date_raw is not None and str(date_raw).strip() not in ['-', 'nan', '', 'None']:
#                 try:
#                     date_obj = pd.to_datetime(date_raw, dayfirst=True, errors='coerce')
#                     if pd.notna(date_obj):
#                         date_str = date_obj.strftime('%Y-%m-%d')
#                 except Exception:
#                     date_str = None

#             company = str(row.get('company', '')).strip()
#             if company.lower() in ['nan', 'none', '-']:
#                 company = ''

#             role = str(row.get('role', '')).strip()
#             if role.lower() in ['nan', 'none', '-']:
#                 role = ''

#             all_students.append({
#                 'name': name,
#                 'roll_no': str(row.get('roll_no', '')).strip(),
#                 'department': dept,
#                 'company': company,
#                 'role': role,
#                 'ctc': ctc,
#                 'ppo_type': classify_offer_type(row.get('ppo_intern')),
#                 'date': date_str,
#                 'batch_year': 2027,
#                 'is_placed': bool(company and company not in ['', '-']),
#             })

#         print(f"Sheet {dept}: loaded {len([s for s in all_students if s['department'] == dept])} students")

#     print(f"Total students loaded: {len(all_students)}")
#     return all_students

import pandas as pd
from datetime import datetime


BATCH_STRENGTH = {
    'CSE': 28, 'AFI': 33, 'CYS': 29, 'DSC': 30,
    'SWE': 25, 'ITY': 25, 'RCO': 12, 'RIT': 9, 'RSE': 15
}

VALID_SHEETS = [k.upper() for k in BATCH_STRENGTH.keys()]


def classify_offer_type(val):
    if not val or str(val).strip().lower() in ['-', '', 'nan', 'none']:
        return 'FTE'
    v = str(val).upper()
    if 'PPO' in v and 'INTERN' in v: return 'PPO'
    if 'PPO' in v: return 'PPO'
    if 'INTERN' in v: return 'Intern'
    return 'FTE'


def find_header_row(df):
    for i, row in df.iterrows():
        vals = [str(v).strip().upper() for v in row if pd.notna(v)]
        if any(x in vals for x in ['NAME', 'S.NO', 'SNO', 'ROLL NO']):
            return i
    return None


def safe_str(val):
    """Safely convert a cell value to string, handling Series objects"""
    if val is None:
        return ''
    # If pandas accidentally gives us a Series, take the first element
    if isinstance(val, pd.Series):
        val = val.iloc[0] if len(val) > 0 else ''
    if pd.isna(val) if not isinstance(val, str) else False:
        return ''
    s = str(val).strip()
    if s.lower() in ['nan', 'none', 'nat']:
        return ''
    return s


def parse_excel(filepath: str) -> list[dict]:
    all_students = []
    try:
        xl = pd.ExcelFile(filepath)
    except Exception as e:
        print(f"[Parser] Failed to open file: {e}")
        return []

    for sheet_name in xl.sheet_names:
        dept = sheet_name.strip().upper()
        if dept not in VALID_SHEETS:
            continue

        try:
            raw = xl.parse(sheet_name, header=None)
            header_idx = find_header_row(raw)
            if header_idx is None:
                print(f"[Parser] No header found in sheet: {sheet_name}")
                continue

            df = xl.parse(sheet_name, header=header_idx)
            df.columns = [str(c).strip().upper().replace('\n', ' ') for c in df.columns]

            print(f"[Parser] Sheet '{sheet_name}' columns: {list(df.columns)}")

            # Build col_map — only take FIRST match for each logical field
            col_map = {}
            already_mapped = set()

            for c in df.columns:
                cu = c.upper()
                if 'NAME' in cu and 'COMPANY' not in cu and 'name' not in already_mapped:
                    col_map[c] = 'name'; already_mapped.add('name')
                elif ('ROLL' in cu or 'ENROLL' in cu) and 'roll_no' not in already_mapped:
                    col_map[c] = 'roll_no'; already_mapped.add('roll_no')
                elif ('COMPANY' in cu or 'ORGANISATION' in cu) and 'company' not in already_mapped:
                    col_map[c] = 'company'; already_mapped.add('company')
                elif ('ROLE' in cu or 'DESIGNATION' in cu) and 'role' not in already_mapped:
                    col_map[c] = 'role'; already_mapped.add('role')
                elif ('PPO' in cu or 'INTERN' in cu or 'TYPE' in cu or 'OFFER' in cu) and 'ppo_raw_col' not in already_mapped:
                    col_map[c] = 'ppo_raw_col'; already_mapped.add('ppo_raw_col')
                elif ('CTC' in cu or 'PACKAGE' in cu) and 'ctc_col' not in already_mapped:
                    col_map[c] = 'ctc_col'; already_mapped.add('ctc_col')
                elif 'STIPEND' in cu and 'stipend_col' not in already_mapped:
                    col_map[c] = 'stipend_col'; already_mapped.add('stipend_col')
                elif 'DATE' in cu and 'date_col' not in already_mapped:
                    col_map[c] = 'date_col'; already_mapped.add('date_col')

            print(f"[Parser] col_map for '{sheet_name}': {col_map}")

            df = df.rename(columns=col_map)

            for _, row in df.iterrows():
                name = safe_str(row.get('name'))
                if not name or name.lower() in ['nan', 'total', 'name', 'sl.no', 's.no']:
                    continue

                # Extract raw PPO/type value safely
                raw_ppo_val = safe_str(row.get('ppo_raw_col'))
                if not raw_ppo_val or raw_ppo_val.lower() in ['nan', 'none', '-', '']:
                    raw_ppo_val = 'FTE'

                # CTC parsing
                ctc = None
                ctc_raw = row.get('ctc_col')
                if ctc_raw is not None:
                    if isinstance(ctc_raw, pd.Series):
                        ctc_raw = ctc_raw.iloc[0] if len(ctc_raw) > 0 else None
                    if ctc_raw is not None and not (isinstance(ctc_raw, float) and pd.isna(ctc_raw)):
                        try:
                            ctc = float(str(ctc_raw).replace(',', '').strip())
                        except:
                            ctc = None

                # Stipend parsing
                stipend = None
                stipend_raw = row.get('stipend_col')
                if stipend_raw is not None:
                    if isinstance(stipend_raw, pd.Series):
                        stipend_raw = stipend_raw.iloc[0] if len(stipend_raw) > 0 else None
                    if stipend_raw is not None and not (isinstance(stipend_raw, float) and pd.isna(stipend_raw)):
                        try:
                            s_val = str(stipend_raw).lower().replace(',', '').replace('k', '000').strip()
                            stipend = float(''.join(filter(lambda x: x.isdigit() or x == '.', s_val)))
                        except:
                            stipend = None

                # Date parsing
                date_val = None
                date_raw = row.get('date_col')
                if date_raw is not None:
                    if isinstance(date_raw, pd.Series):
                        date_raw = date_raw.iloc[0] if len(date_raw) > 0 else None
                    if date_raw is not None:
                        date_str = safe_str(date_raw)
                        if date_str and date_str not in ['nan', 'none', '']:
                            # Normalize date to YYYY-MM-DD
                            try:
                                if isinstance(date_raw, (pd.Timestamp, datetime)):
                                    date_val = date_raw.strftime('%Y-%m-%d')
                                else:
                                    # Try parsing common formats
                                    for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y']:
                                        try:
                                            date_val = datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                                            break
                                        except:
                                            continue
                                    if not date_val:
                                        date_val = date_str  # fallback: store raw
                            except:
                                date_val = date_str

                all_students.append({
                    'name': name,
                    'roll_no': safe_str(row.get('roll_no')),
                    'department': dept,
                    'company': safe_str(row.get('company')),
                    'role': safe_str(row.get('role')),
                    'ctc': ctc,
                    'stipend_pm': stipend,
                    'ppo_type': classify_offer_type(raw_ppo_val),
                    'ppo_type_raw': raw_ppo_val,
                    'date': date_val,
                    'batch_year': 2027
                })

        except Exception as e:
            print(f"[Parser] Error in sheet '{sheet_name}': {e}")

    print(f"[Parser] Total students parsed: {len(all_students)}")
    return all_students