import time 
import torch 
from fastapi import FastAPI, HTTPException 
from fastapi.concurrency import run_in_threadpool 
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS
from pydantic import BaseModel 
from contextlib import asynccontextmanager 
from transformers import T5Tokenizer, T5ForConditionalGeneration 

# ========================================== 
# CONFIG 
# ========================================== 

MODEL_NAME = "dxv39/tone" 
ml_resources = {} 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 

# ========================================== 
# LIFESPAN 
# ========================================== 

@asynccontextmanager 
async def lifespan(app: FastAPI): 
    print("⚡ Loading model...") 

    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME) 
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME) 

    model.to(device) 
    model.eval() 

    ml_resources["tokenizer"] = tokenizer 
    ml_resources["model"] = model 

    print("✅ Model loaded!") 
    yield 
    ml_resources.clear() 

app = FastAPI(lifespan=lifespan) 

# ========================================== 
# CORS CONFIGURATION - ADD THIS SECTION
# ========================================== 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tone-forge-ai.vercel.app", 
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================== 
# REQUEST / RESPONSE MODELS 
# ========================================== 

class EmailRequest(BaseModel): 
    subject: str 
    recipient: str 
    sender: str 
    body: str 
    mode: str  # formal or casual 

class EmailResponse(BaseModel): 
    formatted_email: str 
    latency_ms: float 

# ========================================== 
# GENERATION 
# ========================================== 

def rewrite_body(body: str, mode: str): 
    tokenizer = ml_resources["tokenizer"] 
    model = ml_resources["model"] 

    input_text = f"{mode}: {body}" 

    inputs = tokenizer( 
        input_text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True 
    ).to(device) 

    with torch.no_grad(): 
        outputs = model.generate( 
            inputs.input_ids, 
            max_length=256, 
            num_beams=5, 
            temperature=0.7, 
            early_stopping=True 
        ) 

    return tokenizer.decode(outputs[0], skip_special_tokens=True) 

# ========================================== 
# ROUTES 
# ========================================== 

@app.post("/transform-email", response_model=EmailResponse) 
async def transform_email(request: EmailRequest): 

    if request.mode.lower() not in ["formal", "casual"]: 
        raise HTTPException( 
            status_code=400, 
            detail="Mode must be either 'formal' or 'casual'" 
        ) 

    start_time = time.time() 

    rewritten_body = await run_in_threadpool( 
        rewrite_body, 
        request.body, 
        request.mode.lower() 
    ) 

    formatted_email = f"""Subject: {request.subject} 
Hi {request.recipient}, 
{rewritten_body} 
Thanks, 
{request.sender} 
""" 

    latency = round((time.time() - start_time) * 1000, 2) 

    return EmailResponse( 
        formatted_email=formatted_email, 
        latency_ms=latency 
    ) 

@app.get("/") 
def health(): 
    return {"status": "online", "model": "T5-tone-formalizer"}
