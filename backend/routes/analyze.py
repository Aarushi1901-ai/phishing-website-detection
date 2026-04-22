from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import json

from services.feature_extractor import extract_features, get_feature_names
from services.domain_utils import get_domain_intelligence
from services.model_service import predict, get_model
from services.explain_service import generate_explanation

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: str

class Location(BaseModel):
    country: str
    city: str

class AnalyzeResponse(BaseModel):
    prediction: str
    probability: float
    domain_age: int
    location: Location
    explanation: list[str]

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_url(req: AnalyzeRequest):
    url = req.url
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        # 1. Feature Extraction
        features = extract_features(url)
        feature_names = get_feature_names()
        
        # 2. Domain Intelligence
        domain_intel = get_domain_intelligence(url)
        
        # 3. Model Prediction
        prediction_result = predict(features)
        
        # 4. SHAP Explanation
        model = get_model()
        explanation = generate_explanation(model, features, feature_names)
        
        # 5. Build Response
        return AnalyzeResponse(
            prediction=prediction_result["class"],
            probability=prediction_result["probability"],
            domain_age=domain_intel["domain_age"],
            location=Location(
                country=domain_intel["country"],
                city=domain_intel["city"]
            ),
            explanation=explanation
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
