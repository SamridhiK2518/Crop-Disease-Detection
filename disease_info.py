"""Disease descriptions, treatment and prevention tips.

Keys match PlantVillage folder names (Crop___Disease). Anything not listed
falls back to generic advice, so the app never breaks on a new class.
"""

DISEASE_INFO = {
    "Tomato___Early_blight": {
        "description": "A fungal disease causing dark brown spots with concentric rings on older leaves.",
        "treatment": [
            "Remove and destroy infected leaves.",
            "Spray a copper-based or chlorothalonil fungicide.",
            "Avoid overhead watering.",
        ],
        "prevention": ["Rotate crops every 2-3 years.", "Mulch the soil and keep plants well spaced."],
    },
    "Tomato___Late_blight": {
        "description": "A fast-spreading disease causing water-soaked, dark patches on leaves and fruit.",
        "treatment": [
            "Remove infected plants immediately.",
            "Apply a mancozeb or metalaxyl fungicide.",
            "Do not compost infected material.",
        ],
        "prevention": ["Use resistant varieties.", "Keep foliage dry and ensure good air flow."],
    },
    "Tomato___Leaf_Mold": {
        "description": "Pale yellow spots on the upper leaf surface with olive-green mold underneath.",
        "treatment": ["Improve ventilation.", "Apply a suitable fungicide.", "Remove affected leaves."],
        "prevention": ["Reduce humidity in greenhouses.", "Water at the base of the plant."],
    },
    "Tomato___Bacterial_spot": {
        "description": "Small dark, greasy-looking spots on leaves and fruit caused by bacteria.",
        "treatment": ["Spray copper-based bactericide.", "Remove severely infected plants."],
        "prevention": ["Use disease-free seeds.", "Avoid working with wet plants."],
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "A virus spread by whiteflies, causing curled, yellow leaves and stunted growth.",
        "treatment": ["Control whiteflies with neem oil or insecticidal soap.", "Remove infected plants."],
        "prevention": ["Use reflective mulches.", "Plant resistant varieties."],
    },
    "Potato___Early_blight": {
        "description": "Dark spots with concentric rings on older potato leaves.",
        "treatment": ["Apply a fungicide such as mancozeb.", "Remove infected foliage."],
        "prevention": ["Practice crop rotation.", "Make sure plants get enough nutrients and water."],
    },
    "Potato___Late_blight": {
        "description": "Water-soaked lesions that turn brown and spread quickly in cool, wet weather.",
        "treatment": ["Apply a protective fungicide immediately.", "Destroy infected plants and tubers."],
        "prevention": ["Plant certified seed tubers.", "Avoid overhead irrigation."],
    },
    "Corn_(maize)___Common_rust_": {
        "description": "Small reddish-brown pustules on both sides of corn leaves.",
        "treatment": ["Apply a fungicide if infection is severe.", "Remove heavily infected leaves."],
        "prevention": ["Plant resistant hybrids.", "Plant early in the season."],
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Long, cigar-shaped gray-green lesions on corn leaves.",
        "treatment": ["Apply fungicide at early signs.", "Remove crop residue after harvest."],
        "prevention": ["Use resistant hybrids.", "Rotate with non-host crops."],
    },
    "Apple___Apple_scab": {
        "description": "Olive-green to brown scabby spots on leaves and fruit.",
        "treatment": ["Apply fungicide during early spring.", "Rake and destroy fallen leaves."],
        "prevention": ["Prune for air circulation.", "Choose scab-resistant varieties."],
    },
    "Grape___Black_rot": {
        "description": "Brown circular leaf spots and shriveled black fruit mummies.",
        "treatment": ["Remove mummified fruit.", "Spray a fungicide before and after bloom."],
        "prevention": ["Prune for airflow.", "Keep the vineyard floor clean."],
    },
    "Pepper,_bell___Bacterial_spot": {
        "description": "Small, water-soaked spots that turn brown on leaves and fruit.",
        "treatment": ["Use copper-based sprays.", "Remove infected plants."],
        "prevention": ["Use clean seed.", "Avoid overhead watering."],
    },
}

GENERIC_DISEASE = {
    "description": "A plant disease was detected. Symptoms and spread depend on the cause (fungal, bacterial or viral).",
    "treatment": [
        "Isolate and remove the affected leaves or plants.",
        "Consult a local agriculture officer before using any pesticide.",
        "Avoid overhead watering and improve air circulation.",
    ],
    "prevention": ["Rotate crops each season.", "Use certified, disease-free seeds.", "Keep tools and field clean."],
}

HEALTHY = {
    "description": "The leaf looks healthy. No visible signs of disease were detected.",
    "treatment": ["No treatment needed."],
    "prevention": [
        "Keep monitoring the crop regularly.",
        "Maintain balanced watering and fertilisation.",
        "Remove weeds and fallen debris.",
    ],
}


def split_label(label: str):
    """'Tomato___Early_blight' -> ('Tomato', 'Early blight')."""
    if "___" in label:
        crop, disease = label.split("___", 1)
    else:
        crop, disease = "Unknown", label
    crop = crop.replace("_", " ").replace(",", "").strip()
    disease = disease.replace("_", " ").strip()
    return crop, disease


def get_info(label: str):
    crop, disease = split_label(label)
    is_healthy = "healthy" in label.lower()
    info = HEALTHY if is_healthy else DISEASE_INFO.get(label, GENERIC_DISEASE)
    return {
        "crop": crop,
        "disease": "Healthy" if is_healthy else disease,
        "is_healthy": is_healthy,
        **info,
    }
