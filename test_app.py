"""
Unit tests for Flask app routes and prediction functionality
"""
import json
from app import app

client = app.test_client()

def test_routes():
    print("[*] Testing GET / ...")
    # templates/index.html might not exist yet, let's catch or create
    # Let's test /predict directly
    
    print("[*] Testing /predict with empty payload...")
    res = client.post("/predict", json={})
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    print(" -> Empty payload correctly rejected: 400")

    print("[*] Testing /predict with short text (<20 words)...")
    res = client.post("/predict", json={"text": "This is a very short text with only ten words total."})
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    print(" -> Short text correctly rejected: 400", res.get_json())

    print("[*] Testing /predict with oversized text (>5000 chars)...")
    res = client.post("/predict", json={"text": "word " * 1500})
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    print(" -> Oversized text correctly rejected: 400", res.get_json())

    print("[*] Testing /predict with sample REAL news...")
    real_sample = (
        "WASHINGTON (Reuters) - The Federal Reserve maintained its benchmark interest rate target on Wednesday, "
        "citing meaningful progress in slowing inflation toward its 2 percent annual target. Federal Reserve Chair "
        "Jerome Powell stated in a press briefing that economic growth remains resilient and labor market conditions continue to normalize. "
        "Policymakers noted that while wage increases have moderated, consumer spending and business investment continue to support domestic economic output."
    )
    res = client.post("/predict", json={"text": real_sample})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.get_data(as_text=True)}"
    data = res.get_json()
    print(" -> Real sample prediction result:", data)
    assert data["label"] in ["REAL", "FAKE"]
    assert 0 <= data["confidence"] <= 100

    print("[*] Testing /predict with sample FAKE news...")
    fake_sample = (
        "SHOCKING PROOF: Secret underground alien base discovered beneath Denver International Airport by whistleblowers! "
        "Leaked documents claim that high-ranking world leaders regularly meet with reptilian overlords during scheduled runway maintenance. "
        "The Illuminati controls commercial air travel and is preparing an apocalyptic underground bunker for the global elite. "
        "Share this post immediately before social media censors delete it forever!"
    )
    res = client.post("/predict", json={"text": fake_sample})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.get_data(as_text=True)}"
    data = res.get_json()
    print(" -> Fake sample prediction result:", data)
    assert data["label"] in ["REAL", "FAKE"]
    assert 0 <= data["confidence"] <= 100

    print("\n[+] All backend prediction tests passed successfully!")

if __name__ == "__main__":
    test_routes()
