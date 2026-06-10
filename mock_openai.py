import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/v1/chat/completions")
async def mock_stream():
    async def generate():
        # Notice how "Apple" is in the VERY FIRST chunk. This is what breaks LiteLLM!
        chunks = [
            {"choices": [{"delta": {"role": "assistant", "content": ""}}]},
            {"choices": [{"delta": {"content": "Apple"}}]},
            {"choices": [{"delta": {"content": " Banana"}}]},
            {"choices": [{"delta": {"content": " Cherry"}}]},
            {"choices": [{"delta": {}, "finish_reason": "stop"}]}
        ]
        for chunk in chunks:
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.1)
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")