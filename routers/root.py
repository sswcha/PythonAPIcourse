from fastapi import APIRouter


router = APIRouter(tags=["Root"])

##########################################  ROOT  ##########################################


@router.get("/")
def root():
    return {"message": "Hey broooo:3"}
