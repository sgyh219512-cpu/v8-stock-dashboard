import os, requests
from flask import Flask, jsonify, send_from_directory
app=Flask(__name__,static_folder="static")
BASE=os.getenv("KIWOOM_BASE_URL","https://api.kiwoom.com")
KEY=os.getenv("KIWOOM_APP_KEY",""); SECRET=os.getenv("KIWOOM_SECRET_KEY","")
@app.get("/")
def index(): return send_from_directory("static","index.html")
@app.get("/api/health")
def health(): return jsonify(ok=True,credentials_configured=bool(KEY and SECRET))
@app.get("/api/kiwoom/token-test")
def token_test():
    try:
        r=requests.post(BASE+"/oauth2/token",headers={"Content-Type":"application/json;charset=UTF-8"},json={"grant_type":"client_credentials","appkey":KEY,"secretkey":SECRET},timeout=15)
        r.raise_for_status(); d=r.json()
        if d.get("return_code") not in (0,"0",None): raise RuntimeError(d.get("return_msg","인증 실패"))
        return jsonify(ok=True,message="키움 REST API 인증 성공",token_type=d.get("token_type"),expires_dt=d.get("expires_dt"))
    except Exception as e: return jsonify(ok=False,message=str(e)),500
@app.get("/api/dashboard")
def dashboard(): return jsonify(sectors=[],leaders=[],closing_bets=[],notice="인증 확인 후 실제 시세 선별 로직 연결 예정")
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","10000")))
