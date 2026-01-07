# class JobRoleDesc(BaseModel):
#     id = Column(Integer, primary_key=True, index=True)
#     job_role = Field(String, description="직군명")
#     level = Field(String, description="숙련도 수준")
#     core_skills = Field(String, description="핵심 기술 역량")
#     tools = Field(String, description="필수 도구 및 기술 스택")
#     soft_skills = Field(String, description="비기술 역량")
#     explain = Field(String, description="직업 설명")