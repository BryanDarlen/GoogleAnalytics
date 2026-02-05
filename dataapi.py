from fastapi import FastApi
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

URL = "https://eqms.doe.gov.my/api3/publicmapproxy/PUBLIC_DISPLAY/CAQM_MCAQM_Current_Reading/MapServer/0/query?f=json&outFields=*&returnGeometry=false&spatialRel=esriSpatialRelIntersects&where=1%3D1"

#allow frontend to call this API (frontend like HTML)
#uses "*"" for simple local testing only (also "*" means allow any request)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/air")
def air():
    r = requests.get(DOE_URL, timeout=30)
    r.raise_for_status()
    raw = r.json()

    features = raw.get("features", [])
    stations = []
    for item in features:
        a = item.get("attributes", {})
        stations.append({
            "station_id": a.get("STATION_ID"),
            "place": a.get("PLACE"),
            "state": a.get("STATE_NAME"),
            "api": a.get("API"),
            "class": a.get("CLASS"),
            "datetime_ms": a.get("DATETIME"),
            "lat": a.get("LATITUDE"),
            "lng": a.get("LONGITUDE"),
            "param": a.get("PARAM_SELECTED"),
        })

    return {"count": len(stations), "stations": stations}