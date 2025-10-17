# dashboard/motions.py

"""
🧠 Hector Motion Routines

This file defines symbolic motion frames for each routine.
To remix or add new routines:
- Use emoji + action text for clarity
- Keep frame order expressive and teachable
- Avoid long delays or ambiguous steps

Example:
motions["wave"] = [
    "👋 raise hand",
    "👋 sweep left",
    "👋 sweep right",
    "👋 return to idle"
]
"""

motions = {
    "ballet": [
        "🩰 base sweep →",
        "🩰 arm extension ↑",
        "🩰 wrist flourish ✨",
        "🩰 gentle grip 🤏"
    ],
    "kata": [
        "🥋 guard stance 🛡️",
        "🥋 strike ➡️",
        "🥋 block ⛔",
        "🥋 bow 🙇"
    ],
    "intercept": [
        "🛡️ scanning perimeter",
        "🛡️ posture shift",
        "🛡️ signal sent",
        "🛡️ stance locked"
    ],
    "saluting": [
        "🫡 posture align",
        "🫡 hand raise",
        "🫡 hold position",
        "🫡 return to idle"
    ]
}