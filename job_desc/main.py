from fastapi import Depends, FastAPI, Request, status
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# from database import engine, SessionLocal, Base
import os

# from database import engine, SessionLocal
# from models import Base
# import models
#  연결한 DB엔진에 테이블 생성함.
#  models에 정의한 모든 클래스를 테이블로 생성함
# Base.metadata.create_all(bind=engine)

# FastAPI() 객체 생성
app = FastAPI()

abs_path = os.path.dirname(os.path.realpath(__file__))
# print(abs_path)
# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")

########################################
# llm과 관련된 사전 작업
## api key 환경변수 설정
from dotenv import load_dotenv
import os

load_dotenv(override=True)
api_key = os.environ["OPENAI_API_KEY"]
## llm 객체생성
llm = ChatOpenAI(model="gpt-5-nano", api_key=api_key)
## json 파서로 결과 받음
# BaseModel 상속 받기
class JobRoleDesc(BaseModel):
    job_role: str = Field(description="직군명")
    level: str = Field(description="숙련도 수준")
    core_skills: str = Field(description="핵심 기술 역량")
    tools: str = Field(description="필수 도구 및 기술 스택")
    soft_skills: str = Field(description="비기술 역량")
    explain: str = Field(description="직업 설명")

parser = JsonOutputParser(pydantic_object=JobRoleDesc)
## 프롬프트 만들기
prompt_template = PromptTemplate(
    template="""당신은 취업 컨설턴트 입니다.
    최신 정보를 반영한 직군에 대한 설명을 해주세요.
    \n{format_instructions}\n{job_role}, {level}\n
    """,
    input_variables=["job_role", "level"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
## chain 객체 만들기
chain = prompt_template | llm | parser
########################################


# todo 조회
# @app.get("/")
# async def home(request: Request, db: Session = Depends(get_db)):
#     # todos = db.query(models.Todo).order_by(models.Todo.id.desc())
#     return templates.TemplateResponse("index.html", 
#                                       {"request": request, 
#                                        "todos": todos})
@app.get("/")
async def home(request: Request):
    test = 100
    return templates.TemplateResponse("index.html", 
                                      {"request": request, 
                                       "test": test})
# llm 질문, 응답받고, 결과를 리턴
@app.post("/generate")
def generate(request: Request, 
             job_role: str = Form(...), 
             level: str = Form(...)):
    # llm에 질물한(클라이언트에서 넘어온) 키워드를 받음
    # gpt에 질문하고 응답받기
    input_data = {"job_role":job_role, "level":level}
    print("llm 요청시작")
    response = chain.invoke(input_data)
    print("llm 응답완료")
    print(response)
    return templates.TemplateResponse("index.html", 
                                      {"request": request, 
                                       "result": response})
