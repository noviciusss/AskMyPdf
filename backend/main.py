from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask_question, prepare_video_context
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    youtube_url: str
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: list[str]


class PrepareRequest(BaseModel):
    youtube_url: str


@app.post("/prepare")
async def prepare(request: PrepareRequest) -> dict[str, str]:
    """Pre-build the vector index so later /ask calls are faster."""
    prepare_video_context(request.youtube_url)
    return {"status": "ready"}
    
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    answer, sources = ask_question(request.youtube_url, request.question)
    return AskResponse(answer=answer, sources=sources)

