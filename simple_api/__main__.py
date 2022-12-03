import uvicorn
from simple_api.app import app

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, loop='uvloop', log_level='info')
