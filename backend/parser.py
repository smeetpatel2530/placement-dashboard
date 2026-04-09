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

VALID_SHEETS = list(BATCH_STRENGTH.keys())

def classify_offer_type(val):
    if not val or str(val).strip().lower() in ['-', '', 'nan', 'none']:
        return 'FTE'
    v = str(val).upper()
    if 'PPO' in v and 'INTERN' in v:
        return 'PPO'
    if 'INTERN' in v:
        return 'Intern'
    return 'FTE'

def find_header_row(df):
    """Find the row index that contains NAME or S.NO as header."""
    for i, row in df.iterrows():
        vals = [str(v).strip().upper() for v in row if pd.notna(v) and str(v).strip()]
        if 'NAME' in vals or 'S.NO' in vals or 'SNO' in vals:
            return i
    return None

def parse_excel(filepath: str) -> list[dict]:
    all_students = []
    try:
        xl = pd.ExcelFile(filepath)
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

    for sheet_name in xl.sheet_names:
        dept = sheet_name.strip().upper()
        if dept not in VALID_SHEETS:
            print(f"Skipping unknown sheet: {sheet_name}")
            continue

        try:
            raw = xl.parse(sheet_name, header=None)
        except Exception as e:
            print(f"Error parsing sheet {sheet_name}: {e}")
            continue

        header_row = find_header_row(raw)
        if header_row is None:
            print(f"No header found in sheet: {sheet_name}")
            continue

        df = xl.parse(sheet_name, header=header_row)
        df.columns = [str(c).strip().upper().replace('\n', ' ') for c in df.columns]

        # Map columns flexibly
        col_map = {}
        for c in df.columns:
            cu = c.upper()
            if 'NAME' in cu and 'COMPANY' not in cu:
                col_map[c] = 'name'
            elif 'ROLL' in cu or 'ENROLL' in cu:
                col_map[c] = 'roll_no'
            elif 'COMPANY' in cu or 'ORGANISATION' in cu or 'ORGANIZATION' in cu:
                col_map[c] = 'company'
            elif 'ROLE' in cu or 'DESIGNATION' in cu or 'PROFILE' in cu:
                col_map[c] = 'role'
            elif 'PPO' in cu and 'INTERN' in cu:
                col_map[c] = 'ppo_intern'
            elif 'CTC' in cu or 'PACKAGE' in cu:
                col_map[c] = 'ctc'
            elif 'STIPEND' in cu:
                col_map[c] = 'stipend'
            elif 'DATE' in cu:
                col_map[c] = 'date'

        df = df.rename(columns=col_map)

        if 'name' not in df.columns:
            continue

        for _, row in df.iterrows():
            name = str(row.get('name', '')).strip()
            if not name or name.lower() in ['nan', '-', '', 'name'] or name.upper() in ['TOTAL'] or name.isdigit():
                continue

            # Parse CTC
            ctc = None
            ctc_raw = row.get('ctc')
            if ctc_raw is not None and str(ctc_raw).strip() not in ['-', 'nan', '', 'None']:
                try:
                    ctc = float(ctc_raw)
                except (ValueError, TypeError):
                    ctc = None

            # Parse Date
            date_str = None
            date_raw = row.get('date')
            if date_raw is not None and str(date_raw).strip() not in ['-', 'nan', '', 'None']:
                try:
                    date_obj = pd.to_datetime(date_raw, dayfirst=True, errors='coerce')
                    if pd.notna(date_obj):
                        date_str = date_obj.strftime('%Y-%m-%d')
                except Exception:
                    date_str = None

            raw_type_val = str(row.get('ppo_intern', '')).strip()

            all_students.append({
                'name': name,
                'roll_no': str(row.get('roll_no', '')).strip(),
                'department': dept,
                'company': str(row.get('company', '')).strip() if str(row.get('company')) != 'nan' else '',
                'role': str(row.get('role', '')).strip() if str(row.get('role')) != 'nan' else '',
                'ctc': ctc,
                'ppo_type': classify_offer_type(raw_type_val),
                'ppo_type_raw': raw_type_val if raw_type_val.lower() not in ['nan', 'none', '-'] else 'FTE',
                'date': date_str,
                'batch_year': 2027,
            })

    return all_students