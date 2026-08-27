from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.pagination import PaginationParams, PaginatedResponse
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.users.models import User
from app.modules.ot.schemas import OTRoomCreate, OTRoomResponse, SurgeryBookingCreate, SurgeryBookingResponse
from app.modules.ot.service import OTService

router = APIRouter(prefix="/ot", tags=["Operation Theatre"])

@router.get("/rooms", response_model=List[OTRoomResponse])
def list_ot_rooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return OTService.get_rooms(db)

@router.post("/rooms", response_model=OTRoomResponse)
def create_ot_room(
    room_in: OTRoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN"))
):
    return OTService.create_room(db, room_in)

@router.get("/surgeries", response_model=PaginatedResponse[SurgeryBookingResponse])
def list_surgeries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    ot_room_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size)
    surgeries, total = OTService.get_surgeries(db, skip=params.skip, limit=params.limit, ot_room_id=ot_room_id, status=status)
    return PaginatedResponse.create(items=surgeries, total=total, params=params)

@router.post("/surgeries", response_model=SurgeryBookingResponse)
def book_surgery(
    surg_in: SurgeryBookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "HOSPITAL_ADMIN", "DOCTOR"))
):
    return OTService.book_surgery(db, surg_in, created_by=current_user.id)
