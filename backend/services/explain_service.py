import shap
import numpy as np

def generate_explanation(model, features, feature_names):
    """
    Generate SHAP explanations for the prediction.
    """
    explainer = shap.TreeExplainer(model)
    # SHAP values for the given features
    shap_values = explainer.shap_values(np.array(features))
    
    # TreeExplainer might return a list of arrays (one for each class)
    if isinstance(shap_values, list):
        # We look at the explanation for the predicted class
        # (For binary, index 1 is often the positive/phishing class)
        # Note: In newer SHAP versions shap_values is an array.
        shap_vals = shap_values[1][0]
    else:
        # In case of newer SHAP versions where it returns 3D arrays or direct values
        if len(shap_values.shape) == 3:
            shap_vals = shap_values[0, :, 1]
        else:
            shap_vals = shap_values[0]

    # Convert to standard format
    feature_impacts = []
    features_flat = features[0]
    
    for i in range(len(feature_names)):
        feature_impacts.append({
            "feature": feature_names[i],
            "value": features_flat[i],
            "shap_value": shap_vals[i]
        })
        
    # Sort by absolute impact magnitude
    feature_impacts.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
    
    explanations = []
    # Take top 3 most impactful features for explanation
    for impact in feature_impacts[:3]:
        sh_val = impact["shap_value"]
        feat = impact["feature"]
        val = impact["value"]
        
        # Human readable translations
        if feat == "URL length":
            desc = "unusually high" if val > 50 else "standard"
            if sh_val > 0: explanations.append(f"URL length ({val}) is {desc}, increasing phishing risk.")
            else: explanations.append(f"URL length ({val}) appears safe.")
        elif feat == "Number of dots":
            if sh_val > 0: explanations.append(f"Contains too many dots ({val}), commonly used to mislead users.")
            else: explanations.append(f"Number of dots ({val}) is typical for safe domains.")
        elif feat == "HTTPS usage":
            if val == 0: explanations.append("Does not use HTTPS (insecure), strongly indicating potential risk.")
            else: explanations.append("Uses HTTPS, providing secure communication.")
        elif feat == "Presence of '@'":
            if val == 1: explanations.append("Contains '@' symbol, a common technique to mask URLs.")
            else: explanations.append("Does not use masking characters like '@'.")
        elif feat == "Number of subdomains":
            if sh_val > 0: explanations.append(f"Too many subdomains ({val}) might indicate spoofing.")
            else: explanations.append(f"Subdomain count ({val}) is normal.")
        elif feat == "Presence of '-'":
            if sh_val > 0: explanations.append("Hyphenated domains are occasionally used to spoof legitimate sites.")
            else: explanations.append("No hyphens detected in domain.")
            
    # Guarantee at least something is returned
    if not explanations:
        explanations = ["Model determined prediction based on typical feature thresholds.", "No strong anomalies detected.", "Domain traits align with prediction confidence."]
            
    return explanations
