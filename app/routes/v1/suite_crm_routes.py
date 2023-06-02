from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core.config import app_settings
from app.core.suite_crm.SuiteCrm import SuiteCrm
from app.db.models import lead as service
from app.schema import lead_schema

suite_crm_router = APIRouter(tags=["suite_crm_router"], prefix="/api/v1/suite-crm")


@suite_crm_router.get(
    "/all",
    response_model=list[lead_schema.LeadOut],
)
def get_all_leads(
    suite_crud: service.LeadCrud = Depends(service.get_lead_crud),
):
    return suite_crud.get_all()


@suite_crm_router.get("/save-all")
def save_all_leads(
    suite_crud: service.LeadCrud = Depends(service.get_lead_crud),
):
    suite_crm = SuiteCrm(
        module_name=app_settings.module_name,
        name=app_settings.api_username,
        password=app_settings.api_password,
        url=app_settings.api_url,
    )
    results = suite_crm.entries
    suite_crud.save_all(results)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "saved"}
    )
