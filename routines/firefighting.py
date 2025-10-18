# routines/firefighting.py

ROUTINES = {
    "humanoid-01": {
        "hose_deploy": ["grab", "aim", "spray"],
        "door_breach": ["scan", "kick", "enter"]
    },
    "arm-01": {
        "valve_twist": ["align", "grip", "rotate"]
    },
    "pelican-01": {
        "water_drop": ["ascend", "position", "release"]
    }
}