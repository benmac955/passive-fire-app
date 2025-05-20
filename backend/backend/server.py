
Action: file_editor view /app/backend/server.py --view-range-start 1 --view-range-end 100
Observation: Here's the result of running `cat -n` on /app/backend/server.py:
1|from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException, Body
2|from fastapi.responses import JSONResponse
3|from dotenv import load_dotenv
4|from starlette.middleware.cors import CORSMiddleware
5|from motor.motor_asyncio import AsyncIOMotorClient
6|import os
7|import logging
8|from pathlib import Path
9|from pydantic import BaseModel, Field
10|from typing import List, Optional, Dict, Any
11|import uuid
12|from datetime import datetime
13|import base64
14|import io
15|from PIL import Image
16|import aiofiles
17|import json
18|from bson import ObjectId, json_util
19|
20|# AI and Computer Vision imports
21|import requests
22|import openai
23|
24|ROOT_DIR = Path(__file__).parent
25|load_dotenv(ROOT_DIR / '.env')
26|
27|# MongoDB connection
28|mongo_url = os.environ['MONGO_URL']
29|client = AsyncIOMotorClient(mongo_url)
30|db = client[os.environ.get('DB_NAME', 'passive_fire_app')]
31|
32|# Set up OpenAI if available
33|OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
34|if OPENAI_API_KEY:
35|    openai.api_key = OPENAI_API_KEY
36|
37|# Create upload directory if it doesn't exist
38|UPLOAD_DIR = ROOT_DIR / "uploads"
39|UPLOAD_DIR.mkdir(exist_ok=True)
40|
41|# Create the main app without a prefix
42|app = FastAPI()
43|
44|# Create a router with the /api prefix
45|api_router = APIRouter(prefix="/api")
46|
47|# Define Models
48|class StatusCheck(BaseModel):
49|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
50|    client_name: str
51|    timestamp: datetime = Field(default_factory=datetime.utcnow)
52|
53|class StatusCheckCreate(BaseModel):
54|    client_name: str
55|
56|class FirePenetration(BaseModel):
57|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
58|    user_id: Optional[str] = None
59|    image_path: str
60|    wall_type: Optional[str] = None
61|    service_type: Optional[str] = None
62|    insulation: Optional[bool] = None
63|    existing_seal: Optional[bool] = None
64|    fire_rating: Optional[str] = None
65|    penetration_size: Optional[str] = None
66|    penetration_type: Optional[str] = None  # wall or floor
67|    timestamp: datetime = Field(default_factory=datetime.utcnow)
68|
69|class FireSystem(BaseModel):
70|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
71|    system_name: str
72|    supplier: str
73|    wall_types: List[str]
74|    service_types: List[str]
75|    fire_ratings: List[str]
76|    description: str
77|    installation_method: str
78|    timestamp: datetime = Field(default_factory=datetime.utcnow)
79|
80|class AnalysisResult(BaseModel):
81|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
82|    penetration_id: str
83|    detected_features: Dict[str, Any]
84|    recommended_system: Optional[Dict[str, Any]] = None
85|    no_system_found_reason: Optional[str] = None
86|    timestamp: datetime = Field(default_factory=datetime.utcnow)
87|
88|class UserInput(BaseModel):
89|    penetration_id: str
90|    wall_type: Optional[str] = None
91|    service_type: Optional[str] = None
92|    fire_rating: Optional[str] = None
93|    penetration_size: Optional[str] = None
94|    penetration_type: Optional[str] = None  # wall or floor
95|
96|# Helper function to convert MongoDB document to dict with ObjectId serialized
97|def serialize_doc(doc):
98|    if doc is None:
99|        return None
100|    

