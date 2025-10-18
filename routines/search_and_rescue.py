# routines/search_and_rescue.py

ROUTINES = {
    "noble-01": {
        "scan_area": ["sniff", "ping", "report"],
        "mark_survivor": ["tag", "signal", "log"]
    },
    "phantom-01": {
        "aerial_scan": ["ascend", "sweep", "report"]
    },
    "humanoid-01": {
        "lift_debris": ["brace", "lift", "clear"]
    },
    "warthog-01": {
        "evac_route": ["map", "drive", "extract"]
    }
}