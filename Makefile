run: 
	@uvicorn main:app --reload --port 8000 --log-level trace