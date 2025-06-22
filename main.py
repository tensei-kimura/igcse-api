# ✅ STEP 1: FastAPI backend to serve IGCSE Science questions

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Allow frontend (e.g., localhost:3000 or deployed site)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extended question templates and content for more variety
TEMPLATES = {
    "Physics": [
        ("What is Newton's {law} law of motion?",
         "Newton's {law} law states that {content}.",
         "This means that {explanation}."),
        ("Why does a balloon expand when heated?",
         "A balloon expands when heated because {content}.",
         "This is due to {explanation}.")
    ],
    "Chemistry": [
        ("What is the chemical formula of {substance}?",
         "The formula is {formula}.",
         "This is because it contains {elements}."),
        ("Why is water a good solvent?",
         "Water is a good solvent because {content}.",
         "This is due to {explanation}.")
    ],
    "Biology": [
        ("What is the function of the {organelle}?",
         "The {organelle} is responsible for {function}.",
         "It plays a key role in {biological_process}."),
        ("How do enzymes affect reactions?",
         "Enzymes affect reactions by {content}.",
         "This helps in {explanation}.")
    ]
}

FILL_VALUES = {
    "law": ["first", "second", "third"],
    "content": [
        "an object in motion stays in motion unless acted upon",
        "force equals mass times acceleration",
        "every action has an equal and opposite reaction",
        "heating increases kinetic energy of particles",
        "polar molecules dissolve other polar molecules",
        "lowering the activation energy"
    ],
    "explanation": [
        "forces occur in pairs",
        "objects resist changes",
        "motion results from interactions",
        "particles move faster and exert more pressure",
        "water's polarity allows it to surround ions",
        "faster reaction rates"
    ],
    "substance": ["water", "carbon dioxide", "sodium chloride", "ammonia", "glucose"],
    "formula": ["H2O", "CO2", "NaCl", "NH3", "C6H12O6"],
    "elements": [
        "hydrogen and oxygen",
        "carbon and oxygen",
        "sodium and chlorine",
        "nitrogen and hydrogen",
        "carbon, hydrogen, and oxygen"
    ],
    "organelle": ["nucleus", "mitochondria", "ribosome", "chloroplast", "cell membrane"],
    "function": [
        "controlling cell activities",
        "producing energy",
        "synthesizing proteins",
        "photosynthesis",
        "regulating transport"
    ],
    "biological_process": [
        "metabolism",
        "respiration",
        "protein synthesis",
        "photosynthesis",
        "homeostasis"
    ]
}

# Utility to capitalize first letter
capitalize = lambda s: s[0].upper() + s[1:] if s else s

@app.get("/generate")
def generate_question(subject: str = Query(..., enum=["Physics", "Chemistry", "Biology"])):
    template = random.choice(TEMPLATES[subject])
    replacements = {key: random.choice(val) for key, val in FILL_VALUES.items()}
    replacements.update({k.capitalize(): capitalize(v) for k, v in replacements.items()})

    question = template[0].format(**replacements)
    answer = template[1].format(**replacements)
    explanation = template[2].format(**replacements)

    return {
        "subject": subject,
        "question": question,
        "answer": answer,
        "explanation": explanation
    }
