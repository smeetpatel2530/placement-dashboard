# DTU M.Tech Placements 2026 Dashboard

Real-time placement analytics dashboard for DTU M.Tech batch 2024-2026.

## Stack
- **Backend:** FastAPI + Python + SQLite
- **Frontend:** React + Vite + Tailwind + Recharts

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Features
- Real-time placement stats from Excel
- Department-wise breakdown with progress bars
- Company hiring charts
- CTC distribution analytics
- Full student table with search & filter
- Placement timeline chart