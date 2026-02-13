import os
from src.main import app

# This file is used by Hugging Face Spaces to run your application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)