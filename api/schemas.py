"""
schemas.py

Définition des schémas Pydantic utilisés par l'API.

Ce fichier contient :
- les modèles d'entrée et de sortie ;
- les énumérations des valeurs autorisées ;
- les règles de validation métier.
"""

from enum import Enum
from pydantic import BaseModel, Field, model_validator

class PrimaryPropertyTypeEnum(str, Enum):
    """Types principaux de bâtiments autorisés par l'API."""

    DISTRIBUTION_CENTER = "Distribution Center"
    HOSPITAL = "Hospital"
    HOTEL = "Hotel"
    K12_SCHOOL = "K-12 School"
    LABORATORY = "Laboratory"
    LARGE_OFFICE = "Large Office"
    LOW_RISE_MULTIFAMILY = "Low-Rise Multifamily"
    MEDICAL_OFFICE = "Medical Office"
    MIXED_USE_PROPERTY = "Mixed Use Property"
    OFFICE = "Office"
    OTHER = "Other"
    REFRIGERATED_WAREHOUSE = "Refrigerated Warehouse"
    RESIDENCE_HALL = "Residence Hall"
    RESTAURANT = "Restaurant"
    RETAIL_STORE = "Retail Store"
    SELF_STORAGE_FACILITY = "Self-Storage Facility"
    SENIOR_CARE_COMMUNITY = "Senior Care Community"
    SMALL_AND_MID_SIZED_OFFICE = "Small- and Mid-Sized Office"
    SUPERMARKET_OR_GROCERY_STORE = "Supermarket / Grocery Store"
    UNIVERSITY = "University"
    WAREHOUSE = "Warehouse"
    WORSHIP_FACILITY = "Worship Facility"

class LargestPropertyUseTypeEnum(str, Enum):
    """Usages principaux autorisés par l'API."""

    ADULT_EDUCATION = "Adult Education"
    AUTOMOBILE_DEALERSHIP = "Automobile Dealership"
    BANK_BRANCH = "Bank Branch"
    COLLEGE_UNIVERSITY = "College/University"
    CONVENTION_CENTER = "Convention Center"
    COURTHOUSE = "Courthouse"
    DATA_CENTER = "Data Center"
    DISTRIBUTION_CENTER = "Distribution Center"
    FINANCIAL_OFFICE = "Financial Office"
    FIRE_STATION = "Fire Station"
    FITNESS_CENTER_HEALTH_CLUB_GYM = "Fitness Center/Health Club/Gym"
    FOOD_SERVICE = "Food Service"
    HOSPITAL_GENERAL_MEDICAL_SURGICAL = "Hospital (General Medical & Surgical)"
    HOTEL = "Hotel"
    K12_SCHOOL = "K-12 School"
    LABORATORY = "Laboratory"
    LIBRARY = "Library"
    LIFESTYLE_CENTER = "Lifestyle Center"
    MANUFACTURING_INDUSTRIAL_PLANT = "Manufacturing/Industrial Plant"
    MEDICAL_OFFICE = "Medical Office"
    MOVIE_THEATER = "Movie Theater"
    MULTIFAMILY_HOUSING = "Multifamily Housing"
    MUSEUM = "Museum"
    NON_REFRIGERATED_WAREHOUSE = "Non-Refrigerated Warehouse"
    OFFICE = "Office"
    OTHER = "Other"
    OTHER_EDUCATION = "Other - Education"
    OTHER_ENTERTAINMENT_PUBLIC_ASSEMBLY = "Other - Entertainment/Public Assembly"
    OTHER_LODGING_RESIDENTIAL = "Other - Lodging/Residential"
    OTHER_MALL = "Other - Mall"
    OTHER_PUBLIC_SERVICES = "Other - Public Services"
    OTHER_RECREATION = "Other - Recreation"
    OTHER_RESTAURANT_BAR = "Other - Restaurant/Bar"
    OTHER_SERVICES = "Other - Services"
    OTHER_UTILITY = "Other - Utility"
    OTHER_SPECIALTY_HOSPITAL = "Other/Specialty Hospital"
    PARKING = "Parking"
    PERFORMING_ARTS = "Performing Arts"
    PERSONAL_SERVICES = "Personal Services (Health/Beauty, Dry Cleaning, etc)"
    POLICE_STATION = "Police Station"
    PRESCHOOL_DAYCARE = "Pre-school/Daycare"
    PRISON_INCARCERATION = "Prison/Incarceration"
    REFRIGERATED_WAREHOUSE = "Refrigerated Warehouse"
    REPAIR_SERVICES = "Repair Services (Vehicle, Shoe, Locksmith, etc)"
    RESIDENCE_HALL_DORMITORY = "Residence Hall/Dormitory"
    RESIDENTIAL_CARE_FACILITY = "Residential Care Facility"
    RESTAURANT = "Restaurant"
    RETAIL_STORE = "Retail Store"
    SELF_STORAGE_FACILITY = "Self-Storage Facility"
    SENIOR_CARE_COMMUNITY = "Senior Care Community"
    SOCIAL_MEETING_HALL = "Social/Meeting Hall"
    STRIP_MALL = "Strip Mall"
    SUPERMARKET_GROCERY_STORE = "Supermarket/Grocery Store"
    URGENT_CARE_CLINIC_OUTPATIENT = "Urgent Care/Clinic/Other Outpatient"
    WHOLESALE_CLUB_SUPERCENTER = "Wholesale Club/Supercenter"
    WORSHIP_FACILITY = "Worship Facility"

class BuildingInput(BaseModel):
    """Informations métier fournies par le propriétaire du bâtiment."""

    PropertyGFATotal: float = Field(
        ...,
        gt=0,
        description="Surface totale du bâtiment en pieds carrés.",
        examples=[50000],
    )

    PropertyGFAParking: float = Field(
        ...,
        ge=0,
        description="Surface consacrée au parking en pieds carrés.",
        examples=[5000],
    )

    NumberofFloors: int = Field(
        ...,
        ge=1,
        le=100,
        description="Nombre d'étages du bâtiment.",
        examples=[5],
    )

    YearBuilt: int = Field(
        ...,
        ge=1800,
        le=2016,
        description="Année de construction du bâtiment.",
        examples=[1985],
    )

    Latitude: float = Field(
        ...,
        ge=47.0,
        le=48.0,
        description="Latitude du bâtiment dans la zone de Seattle.",
        examples=[47.61],
    )

    Longitude: float = Field(
        ...,
        ge=-123.0,
        le=-121.0,
        description="Longitude du bâtiment dans la zone de Seattle.",
        examples=[-122.33],
    )

    PrimaryPropertyType: PrimaryPropertyTypeEnum = Field(
        ...,
        description="Type principal du bâtiment.",
        examples=["Office"],
    )

    LargestPropertyUseType: LargestPropertyUseTypeEnum = Field(
        ...,
        description="Usage occupant la plus grande surface.",
        examples=["Office"],
    )

    
    @model_validator(mode="after")
    def validate_surfaces(self) -> "BuildingInput":
        if self.PropertyGFAParking > self.PropertyGFATotal:
            raise ValueError(
                "PropertyGFAParking ne peut pas dépasser PropertyGFATotal."
            )
        return self


class PredictionOutput(BaseModel):
    """Réponse renvoyée par l'API."""

    predicted_site_energy_kbtu: float = Field(
        ...,
        description="Consommation énergétique annuelle prédite du bâtiment en kBtu.",
    )