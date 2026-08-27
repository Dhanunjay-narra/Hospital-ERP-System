import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"

    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    registration_number = Column(String(100), nullable=True)
    tax_number = Column(String(100), nullable=True)
    logo_url = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    currency = Column(String(10), default="USD", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    settings = Column(JSON, nullable=True, default=dict)

    branches = relationship("HospitalBranch", back_populates="organization", cascade="all, delete-orphan")

class HospitalBranch(BaseModel):
    __tablename__ = "hospital_branches"

    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(50), index=True, nullable=False)
    is_main_branch = Column(Boolean, default=False, nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    organization = relationship("Organization", back_populates="branches")
    buildings = relationship("Building", back_populates="branch", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="branch", cascade="all, delete-orphan")

class Building(BaseModel):
    __tablename__ = "buildings"

    branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    total_floors = Column(Integer, default=1, nullable=False)

    branch = relationship("HospitalBranch", back_populates="buildings")
    floors = relationship("Floor", back_populates="building", cascade="all, delete-orphan")

class Floor(BaseModel):
    __tablename__ = "floors"

    building_id = Column(String(36), ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    floor_number = Column(Integer, nullable=False)

    building = relationship("Building", back_populates="floors")
    wards = relationship("Ward", back_populates="floor", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="floor", cascade="all, delete-orphan")

class Department(BaseModel):
    __tablename__ = "departments"

    branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=False)
    department_type = Column(String(50), default="CLINICAL", nullable=False) # CLINICAL, DIAGNOSTIC, ADMINISTRATIVE, SUPPORT
    head_of_department_id = Column(String(36), nullable=True)
    description = Column(Text, nullable=True)
    is_opd = Column(Boolean, default=True, nullable=False)
    is_ipd = Column(Boolean, default=True, nullable=False)
    is_emergency = Column(Boolean, default=False, nullable=False)

    branch = relationship("HospitalBranch", back_populates="departments")
    wards = relationship("Ward", back_populates="department")

class Ward(BaseModel):
    __tablename__ = "wards"

    branch_id = Column(String(36), ForeignKey("hospital_branches.id", ondelete="CASCADE"), nullable=False)
    floor_id = Column(String(36), ForeignKey("floors.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    gender_type = Column(String(20), default="ALL", nullable=False)  # MALE, FEMALE, PEDIATRIC, ALL
    ward_type = Column(String(50), default="GENERAL", nullable=False)  # GENERAL, ICU, CCU, NICU, POST_OP, PRIVATE

    floor = relationship("Floor", back_populates="wards")
    department = relationship("Department", back_populates="wards")
    rooms = relationship("Room", back_populates="ward", cascade="all, delete-orphan")
    beds = relationship("Bed", back_populates="ward", cascade="all, delete-orphan")

class Room(BaseModel):
    __tablename__ = "rooms"

    ward_id = Column(String(36), ForeignKey("wards.id", ondelete="SET NULL"), nullable=True)
    floor_id = Column(String(36), ForeignKey("floors.id", ondelete="SET NULL"), nullable=True)
    room_number = Column(String(50), nullable=False)
    room_type = Column(String(50), default="GENERAL", nullable=False) # GENERAL, SEMI_PRIVATE, PRIVATE, DELUXE, ICU
    daily_rate = Column(Integer, default=0, nullable=False)

    ward = relationship("Ward", back_populates="rooms")
    floor = relationship("Floor", back_populates="rooms")
    beds = relationship("Bed", back_populates="room", cascade="all, delete-orphan")

class Bed(BaseModel):
    __tablename__ = "beds"

    ward_id = Column(String(36), ForeignKey("wards.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(String(36), ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    bed_number = Column(String(50), nullable=False)
    status = Column(String(30), default="AVAILABLE", nullable=False) # AVAILABLE, RESERVED, OCCUPIED, CLEANING, BLOCKED, MAINTENANCE
    bed_type = Column(String(50), default="STANDARD", nullable=False) # STANDARD, ICU, ELECTRIC, PEDIATRIC
    current_patient_id = Column(String(36), nullable=True)
    current_admission_id = Column(String(36), nullable=True)

    ward = relationship("Ward", back_populates="beds")
    room = relationship("Room", back_populates="beds")
