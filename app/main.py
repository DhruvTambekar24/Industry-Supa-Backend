# from fastapi import FastAPI, HTTPException
# from app.models import MentorQuery, ScenarioRequest, FeedbackRequest
# from app.mentor_ai import IndustryMentorAI
# from app.config import settings


# app = FastAPI()

# # Initialize the mentor AI with your API key
# MENTOR_AI = IndustryMentorAI(api_key=settings.gemini_api_key)

# @app.post("/get-mentor-response")
# async def get_mentor_response(mentor_query: MentorQuery):
#     try:
#         response = MENTOR_AI.get_mentor_response(mentor_query.mentor_type, mentor_query.query)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/generate-scenario")
# async def generate_scenario(scenario_request: ScenarioRequest):
#     try:
#         scenario = MENTOR_AI.generate_scenario(scenario_request.mentor_type, scenario_request.difficulty)
#         return scenario
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/provide-feedback")
# async def provide_feedback(feedback_request: FeedbackRequest):
#     try:
#         feedback = MENTOR_AI.provide_feedback(feedback_request.mentor_type, feedback_request.scenario, feedback_request.solution)
#         return feedback
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Run the FastAPI app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import MentorQuery, ScenarioRequest, FeedbackRequest
from app.mentor_ai import IndustryMentorAI
from app.config import settings

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the mentor AI with your API key
MENTOR_AI = IndustryMentorAI(api_key=settings.gemini_api_key)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.post("/get-mentor-response")
async def get_mentor_response(mentor_query: MentorQuery):
    try:
        response = MENTOR_AI.get_mentor_response(mentor_query.mentor_type, mentor_query.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-scenario")
async def generate_scenario(scenario_request: ScenarioRequest):
    try:
        scenario = MENTOR_AI.generate_scenario(scenario_request.mentor_type, scenario_request.difficulty)
        return scenario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/provide-feedback")
async def provide_feedback(feedback_request: FeedbackRequest):
    try:
        feedback = MENTOR_AI.provide_feedback(feedback_request.mentor_type, feedback_request.scenario, feedback_request.solution)
        return feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
