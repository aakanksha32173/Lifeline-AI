# Lifeline AI - Setup Guide

## 🚀 Enhanced Features Implemented

### ✅ Backend Improvements
1. **Semantic Clustering** - Uses OpenAI embeddings for intelligent incident grouping (not just exact location matching)
2. **Geocoding** - Automatically converts location strings to lat/lng coordinates
3. **ASI:One API Integration** - Active AI-powered recommendations for emergency response
4. **Color-Coded Clusters** - Visual categorization by event type
5. **Browserbase Resource Search** - Enhanced resource finding capabilities

### ✅ Frontend Improvements
1. **Interactive Map View** - Leaflet-based map showing all incidents with color-coded markers
2. **Clusters Tab** - Organized view grouping incidents by category (medical, rescue, environmental, etc.)
3. **Enhanced Priority Queue** - Color-coded clusters with event categories
4. **Tab Navigation** - Easy switching between Priority Queue, Map View, and Clusters
5. **Auto-refresh** - Dashboard updates every 10 seconds

---

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Redis server
- ASI:One API key (already configured - handles both embeddings and recommendations)

---

## 🔧 Installation

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start Redis:**
```bash
# macOS (with Homebrew)
brew services start redis

# Linux
sudo systemctl start redis

# Or run directly
redis-server
```

6. **Run the backend:**
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run the development server:**
```bash
npm run dev
```

4. **Open browser:**
Navigate to `http://localhost:5173`

---

## 🎯 How It Works

### Semantic Clustering Flow
1. User submits crisis report with text and location
2. **Geocoding**: Location is converted to lat/lng coordinates
3. **Incident Extraction**: Text is analyzed for keywords (medical, rescue, flood, etc.)
4. **Semantic Similarity**: ASI:One embeddings compare new incident with existing ones
5. **Clustering**: Incidents are grouped if they have:
   - Semantic similarity > 70%
   - Geographic distance < 5km (or same location string)
6. **Priority Scoring**: Cluster priority calculated based on urgency, medical needs, vulnerable populations
7. **AI Recommendations**: ASI:One API generates actionable response plans

**Note**: All AI features use ASI:One API - no additional API keys needed!

### Color Coding System
- 🔴 **Red (#ef4444)**: Medical Emergency
- 🟠 **Orange (#f97316)**: Rescue Request
- 🔵 **Blue (#3b82f6)**: Flooding
- 🟡 **Yellow (#eab308)**: Power Outage
- 🟢 **Green (#22c55e)**: Shelter Update
- 🟣 **Purple (#6366f1)**: General Alert

---

## 🗺️ Using the Map View

1. Click **"🗺️ Map View"** tab
2. Incidents appear as colored circles (size = urgency level)
3. Click any marker to see incident details
4. Map auto-zooms to fit all incidents
5. Legend shows color meanings

---

## 🔗 Using the Clusters Tab

1. Click **"🔗 Clusters"** tab
2. View incidents grouped by category:
   - Medical Emergencies
   - Rescue Operations
   - Environmental Hazards
   - Infrastructure Issues
   - Shelter & Housing
   - General Alerts
3. Each cluster shows:
   - All related incidents
   - Priority score
   - AI-generated recommendations

---

## 🧪 Testing the System

### Test Case 1: Medical Emergency Clustering
```
Report 1:
Text: "My grandmother needs oxygen urgently, water is rising"
Location: "Berkeley, CA"

Report 2:
Text: "Elderly person trapped, requires medical assistance"
Location: "Berkeley, CA"
```
**Expected**: Both cluster together (semantic similarity + same location)

### Test Case 2: Different Locations
```
Report 1:
Text: "Flooding on Main Street"
Location: "Oakland, CA"

Report 2:
Text: "Water rising quickly"
Location: "San Francisco, CA"
```
**Expected**: Separate clusters (distance > 5km)

### Test Case 3: Color Coding
- Medical reports → Red
- Rescue requests → Orange
- Flooding → Blue
- Power outages → Yellow

---

## 🔑 API Endpoints

- `POST /events/process` - Submit new crisis report
- `GET /priority-queue` - Get sorted clusters by priority
- `GET /clusters` - Get all clusters (unsorted)
- `DELETE /memory` - Clear all clusters from Redis

---

## 🐛 Troubleshooting

### "Cannot find module 'react-leaflet'"
```bash
cd frontend
npm install
```

### Geocoding not working
- Check internet connection (uses Nominatim API)
- Rate limit: 1 request per second

### ASI:One API errors
- Verify `ASI_ONE_API_KEY` in `.env`
- Check API quota/limits

### Redis connection failed
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

### ASI:One Embedding errors
- Verify `ASI_ONE_API_KEY` in `.env`
- Check API quota/limits
- Fallback: System uses keyword-based embeddings if API fails

---

## 📊 Performance Notes

- **Semantic clustering**: ~1-2 seconds per incident (ASI:One embedding API call)
- **Geocoding**: ~0.5-1 second per location (Nominatim)
- **Map rendering**: Optimized for up to 100 incidents
- **Auto-refresh**: Every 10 seconds
- **Fallback mode**: Instant clustering using keyword-based embeddings if API unavailable

---

## 🚀 Production Deployment

1. Verify `ASI_ONE_API_KEY` in production environment
2. Use production Redis instance
3. Configure CORS for production domain
4. Build frontend: `npm run build`
5. Serve with nginx or similar
6. Use gunicorn for backend: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

---

## 📝 Environment Variables Reference

```bash
# Required
ASI_ONE_API_KEY=sk_...          # For embeddings AND AI recommendations (all-in-one!)
REDIS_HOST=localhost
REDIS_PORT=6379

# Optional
BROWSERBASE_API_KEY=bb_live_... # For resource search
BROWSERBASE_PROJECT_ID=...
DEEPGRAM_API_KEY=...            # For future audio processing
```

---

## 🎨 Customization

### Adjust Clustering Thresholds
Edit `backend/processing/incident_fusion.py`:
```python
semantic_threshold=0.70,      # 0.0-1.0 (higher = stricter)
distance_threshold_km=5.0     # kilometers
```

### Change Color Scheme
Edit `backend/processing/incident_fusion.py` → `get_cluster_color()`

### Modify Priority Scoring
Edit `backend/processing/priority_scorer.py` → `calculate_priority()`

---

## 📚 Architecture

```
Frontend (React + Leaflet)
    ↓
FastAPI Backend
    ↓
┌─────────────────────────────────┐
│ Incident Processing Pipeline    │
├─────────────────────────────────┤
│ 1. Geocoding (geopy)            │
│ 2. Extraction (keyword analysis)│
│ 3. Semantic Clustering (ASI:One)│
│ 4. Priority Scoring             │
│ 5. AI Recommendations (ASI:One) │
└─────────────────────────────────┘
    ↓
Redis (Cluster Storage)
```

---

## ✨ What's New vs Original

| Feature | Original | Enhanced |
|---------|----------|----------|
| Clustering | Exact string match | Semantic similarity + distance |
| Geocoding | None | Full lat/lng support |
| Map View | None | Interactive Leaflet map |
| Clusters Tab | None | Category-based grouping |
| Color Coding | None | 6 event categories |
| AI Recommendations | Unused | Active ASI:One integration |
| Resource Search | Mock data | Browserbase-ready |
| Auto-refresh | Manual | Every 10 seconds |

---

## 🤝 Support

For issues or questions, check:
1. Console logs (browser + terminal)
2. Redis connection: `redis-cli ping`
3. API keys are valid
4. All dependencies installed
