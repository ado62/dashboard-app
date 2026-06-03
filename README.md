# CSV Dashboard

A Python-only web dashboard using Streamlit to read CSV source data.

## Features

- 📊 Interactive line chart with Plotly
- 🗺️ Map visualization with Folium
- 📋 Data table preview
- 📝 Log panel
- ⚡ No Node.js required (Python only)

## Quick Start

1. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Run the dashboard:

```powershell
streamlit run streamlit_app.py
```

3. Open the browser at `http://localhost:8501`

## Data

- Add your CSV files to the `data/` folder
- Update the paths in `streamlit_app.py` if needed
- Supported columns: `date`, `category`, `region`, `value`, `latitude`, `longitude`, `note`

## Alternative: FastAPI + React Stack

For the interactive React + FastAPI dashboard instead of Streamlit:

### Backend
```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` when the frontend is ready.

---

## Deployment

### Frontend (Vercel) — Easiest
1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repo → Deploy (auto-rebuilds on push)
4. Set environment variable: `VITE_API_URL=https://your-backend-url`

### Backend (Render) — Free tier
1. Go to [render.com](https://render.com)
2. New → Web Service → Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Copy the deployed URL and set it in frontend env vars

### Docker (Local testing)
```bash
docker-compose up
```

### GitHub Actions (Auto-deploy on push)
1. Create GitHub secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
   - `RENDER_SERVICE_ID`
   - `RENDER_API_KEY`
2. Push to `main` branch → Auto-deploys to Vercel + Render
