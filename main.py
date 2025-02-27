from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from exception import ProcessingFailedError
from models import AnalysisRequest, AnalysisResponse, AnalysisResult
from process import analyze

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://0.0.0.0:8000'],
    allow_methods=['*']
)

"""
Endpoint that returns a json response containing the review ID
"""
@app.post('/analyze_sentiment', status_code=200)
async def analyze_sentiment(data: dict) -> JSONResponse:
    try:
        analyze_request: AnalysisRequest = AnalysisRequest(**data)
    except ValidationError as ve:
        for error in ve.errors():
            if error['type'] == 'empty_text' or error['type'] == 'empty_id':
                raise HTTPException(status_code=400, detail=error['msg'])
        raise HTTPException(status_code=400, detail=str(ve))

    try:
        analysis_result: AnalysisResult = await analyze(analyze_request.review_text)
    except ValidationError as ve:
        for error in ve.errors():
            if error['type'] == 'not_in_range':
                raise HTTPException(status_code=400, detail=error['msg'])
        raise HTTPException(status_code=400, detail=str(ve))
    except ProcessingFailedError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    response = AnalysisResponse(
        review_id=analyze_request.review_id,
        details=analysis_result
    )

    return JSONResponse(content=jsonable_encoder(response), status_code=200)

