VALID_TAGS = [
    "Long_Duration_(>2_Hrs)",
    "Short_Duration_(<2_Hrs)",
    "Labor_Intensive",
    "Construction",
    "Moving",
    "Food_Bank"
    ]

DISPLAY_TAGS = [entry.replace('_', ' ') for entry in VALID_TAGS]

NUM_TAGS = len(VALID_TAGS)