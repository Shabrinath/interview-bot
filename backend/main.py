from fastapi import FastAPI
from pydantic import BaseModel
from interview_logic import get_question, evaluate_answer

app = FastAPI()

class InterviewRequest(BaseModel):
    role: str
    difficulty: str
    topic: str
    tone: str

class AnswerRequest(BaseModel):
    question: str
    answer: str
    role: str
    difficulty: str
    topic: str
    tone: str

@app.post("/start")
def start_interview(req: InterviewRequest):
    question = get_question(req.role, req.difficulty, req.topic, req.tone)
    return {"question": question}

@app.post("/answer")
def answer(req: AnswerRequest):
    feedback = evaluate_answer(req.question, req.answer, req.role, req.difficulty, req.topic, req.tone)
    return {"feedback": feedback}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
