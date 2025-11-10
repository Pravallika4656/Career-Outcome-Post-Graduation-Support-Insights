from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .agent import AgentWrapper 
from .database import db   

app = FastAPI()

# Initialize AgentWrapper
agent = None
try:
    agent = AgentWrapper()
    print("INFO: AgentWrapper initialized successfully.")
except Exception as e:
    print(f"ERROR: Could not initialize AgentWrapper. Error: {e}")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Career Insight Bot API Running ✅ Use /api/chat or /api/parent_insights"}


# -------------------------------
# ✅ Chatbot Endpoint
# -------------------------------

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):

    if agent is None:
        return {"reply": "Error: Backend AI failed to initialize."}

    try:
        response = agent.ask(req.message)

        # Save to DB
        await db.chats.insert_one({
            "user_message": req.message,
            "bot_reply": response
        })

        return {"reply": response}

    except Exception as e:
        print(f"FATAL ERROR IN /api/chat: {e}")
        return {"reply": "Server error. Please try again."}


# -------------------------------
# ✅ Parent Career Insight Endpoint (Updated with ROI)
# -------------------------------

class ParentInsightsRequest(BaseModel):
    major: str
    academic_strength: str
    interest_area: str
    investment: float
    placement: float

@app.post("/api/parent_insights")
async def parent_insights_endpoint(req: ParentInsightsRequest):

    if agent is None:
        return {"insight": "Backend agent failed to initialize."}

    try:
        result = agent.generate_parent_insights(
            req.major,
            req.academic_strength,
            req.interest_area,
            req.investment,
            req.placement
        )

        # Save to DB
        await db.parent_insights.insert_one({
            "major": req.major,
            "academic_strength": req.academic_strength,
            "interest_area": req.interest_area,
            "investment": req.investment,
            "placement": req.placement,
            "generated_insight": result
        })

        return {"insight": result}

    except Exception as e:
        print(f"FATAL ERROR IN /api/parent_insights: {e}")
        return {"insight": "Something went wrong while generating insights. Try again!"}
