dataset = [
    # ─────────────────────────────────────────
    # 🟢 EASY — Direct retrieval, clear context
    # ─────────────────────────────────────────
    {
        "query": "Where should Epinephrine be injected?",
        "context": "Administer Epinephrine 0.3mg intramuscularly into the outer thigh.",
        "correct_answer": "Outer thigh",
        "difficulty": "easy"
    },
    {
        "query": "What position should an unconscious patient be placed in?",
        "context": "Place unconscious breathing patients in the recovery position on their side.",
        "correct_answer": "Recovery position on their side",
        "difficulty": "easy"
    },
    {
        "query": "How should an open chest wound be covered?",
        "context": "Seal open chest wounds with a vented chest seal or occlusive dressing.",
        "correct_answer": "Vented chest seal or occlusive dressing",
        "difficulty": "easy"
    },
    {
        "query": "What is the first step in treating a snake bite?",
        "context": "For snake bites, immobilize the affected limb and keep it below heart level.",
        "correct_answer": "Immobilize the affected limb and keep it below heart level",
        "difficulty": "easy"
    },
    {
        "query": "What should be done if a patient is choking?",
        "context": "If the patient is choking and cannot speak, perform the Heimlich maneuver immediately.",
        "correct_answer": "Perform the Heimlich maneuver",
        "difficulty": "easy"
    },
    {
        "query": "What drug is given for opioid overdose?",
        "context": "Administer Naloxone 0.4mg IV immediately for suspected opioid overdose.",
        "correct_answer": "Naloxone 0.4mg IV",
        "difficulty": "easy"
    },
    {
        "query": "What is the CPR compression rate?",
        "context": "Perform chest compressions at a rate of 100-120 per minute during CPR.",
        "correct_answer": "100-120 per minute",
        "difficulty": "easy"
    },
    {
        "query": "Where should a tourniquet be applied for leg bleeding?",
        "context": "Apply the tourniquet 5cm above the wound on the limb to control bleeding.",
        "correct_answer": "5cm above the wound",
        "difficulty": "easy"
    },
    {
        "query": "What is the safe ICU blood glucose range?",
        "context": "Maintain blood glucose between 140-180 mg/dL for ICU patients.",
        "correct_answer": "140-180 mg/dL",
        "difficulty": "easy"
    },
    {
        "query": "What should be given to a patient in anaphylactic shock?",
        "context": "Inject Epinephrine 0.5mg intramuscularly into the outer thigh for anaphylactic shock.",
        "correct_answer": "Epinephrine 0.5mg intramuscularly",
        "difficulty": "easy"
    },

    # ──────────────────────────────────────────────────────────────
    # 🟡 MEDIUM — Synonyms, partial info, mild negation, inference
    # ──────────────────────────────────────────────────────────────
    {
        "query": "Who should assess the patient first?",
        "context": "A physician must evaluate the patient immediately upon arrival.",
        "correct_answer": "Physician",
        "difficulty": "medium"
    },
    {
        "query": "What drug reverses opioid overdose?",
        "context": "Administer Narcan immediately if opioid overdose is suspected.",
        "correct_answer": "Naloxone",
        "difficulty": "medium"
    },
    {
        "query": "What should be given for anaphylaxis?",
        "context": "Inject adrenaline 0.5mg intramuscularly into the outer thigh.",
        "correct_answer": "Epinephrine",
        "difficulty": "medium"
    },
    {
        "query": "Should aspirin be given to a child with fever?",
        "context": "Never administer aspirin to children under 16 with viral illness due to risk of Reye syndrome.",
        "correct_answer": "No",
        "difficulty": "medium"
    },
    {
        "query": "Can a tourniquet be applied to the neck?",
        "context": "Tourniquets must never be applied to the neck, chest, or abdomen.",
        "correct_answer": "No",
        "difficulty": "medium"
    },
    {
        "query": "What is the compression depth for adult CPR?",
        "context": "For adult CPR, compress the chest at least 2 inches but no more than 2.4 inches.",
        "correct_answer": "2 to 2.4 inches",
        "difficulty": "medium"
    },
    {
        "query": "How often should Naloxone be repeated?",
        "context": "Administer Naloxone 0.4mg IV. Repeat every 2-3 minutes if no response.",
        "correct_answer": "Every 2-3 minutes",
        "difficulty": "medium"
    },
    {
        "query": "What is the maximum safe dose of Acetaminophen per day?",
        "context": "Do not exceed 4000mg of Acetaminophen in 24 hours to avoid liver damage.",
        "correct_answer": "4000mg",
        "difficulty": "medium"
    },
    {
        "query": "Should oxygen be given to a COPD patient in respiratory distress?",
        "context": "For COPD patients, administer controlled oxygen at 24-28% via Venturi mask.",
        "correct_answer": "Yes, controlled oxygen at 24-28%",
        "difficulty": "medium"
    },
    {
        "query": "What is the first action for a suspected spinal injury?",
        "context": "Do not move a patient with suspected spinal injury unless there is immediate danger.",
        "correct_answer": "Do not move the patient",
        "difficulty": "medium"
    },

    # ────────────────────────────────────────────────────────────────────
    # 🔴 HARD — Missing info, adversarial traps, LLM forced to hallucinate
    # ────────────────────────────────────────────────────────────────────
    {
        "query": "What is the exact Epinephrine dose for this patient?",
        "context": "Patient presents with severe allergic reaction after eating peanuts. BP is dropping.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "What antibiotic should be prescribed?",
        "context": "Patient has a high fever and sore throat. Throat appears red and inflamed.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "How many mg of Morphine should be administered?",
        "context": "Patient is in severe post-operative pain. Vitals are stable.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "Should vomiting be induced for bleach ingestion?",
        "context": "Do NOT induce vomiting if the patient has ingested bleach or corrosives.",
        "correct_answer": "No",
        "difficulty": "hard"
    },
    {
        "query": "What is the correct insulin dose for this diabetic patient?",
        "context": "Patient is a known diabetic presenting with confusion and sweating.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "Which specific vein should be used for IV access?",
        "context": "Establish IV access immediately for fluid resuscitation.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "What is the exact blood pressure target for this trauma patient?",
        "context": "Trauma patient with internal bleeding is brought to the ER. GCS is 12.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "Should CPR be stopped after 10 minutes if there is no response?",
        "context": "Continue CPR until the patient recovers, AED is available, or a physician declares death.",
        "correct_answer": "No",
        "difficulty": "hard"
    },
    {
        "query": "What sedative should be used before intubation?",
        "context": "Patient requires emergency intubation due to respiratory failure.",
        "correct_answer": "Not mentioned",
        "difficulty": "hard"
    },
    {
        "query": "Is it safe to remove an impaled object from the chest?",
        "context": "Do NOT remove impaled objects. Stabilize them in place and transport immediately.",
        "correct_answer": "No",
        "difficulty": "hard"
    }
]