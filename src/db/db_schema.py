from datetime import datetime

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base class for ORM objects
class Base(DeclarativeBase):
    pass


# Key data tables
class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ref: Mapped[str] = mapped_column(nullable=False)
    modality_id: Mapped[int] = mapped_column(
        ForeignKey("modality_dict.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id"), nullable=True
    )
    bm_id: Mapped[int] = mapped_column(
        ForeignKey("bm_dict.id"), nullable=False
    )

    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sector_dict.id"), nullable=False
    )
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("theme_dict.id"), nullable=False
    )
    size_id: Mapped[int] = mapped_column(
        ForeignKey("size_dict.id"), nullable=True
    )
    ess_category_id: Mapped[int] = mapped_column(
        ForeignKey("ess_category_dict.id"), nullable=False
    )
    financing_usd: Mapped[int] = mapped_column(nullable=False)

    # Data dictionary relationships
    countries: Mapped[list["CountryDict"]] = relationship(
        "CountryDict", secondary="project_country", back_populates="projects"
    )
    modality: Mapped["ModalityDict"] = relationship(
        "ModalityDict", back_populates="projects"
    )
    sector: Mapped["SectorDict"] = relationship(
        "SectorDict", back_populates="projects"
    )
    theme: Mapped["ThemeDict"] = relationship(
        "ThemeDict", back_populates="projects"
    )
    size: Mapped["SizeDict"] = relationship(
        "SizeDict", back_populates="projects"
    )
    ess_category: Mapped["EssCategoryDict"] = relationship(
        "EssCategoryDict", back_populates="projects"
    )
    bm: Mapped["BmDict"] = relationship("BmDict", back_populates="projects")


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country_dict.id"), nullable=False
    )
    is_dae: Mapped[bool] = mapped_column(Boolean, nullable=False)
    entity_type_id: Mapped[int] = mapped_column(
        ForeignKey("entity_type_dict.id"), nullable=False
    )
    stage_id: Mapped[int] = mapped_column(
        ForeignKey("stage_dict.id"), nullable=False
    )
    bm_id: Mapped[int] = mapped_column(ForeignKey("bm_dict.id"), nullable=True)
    size_id: Mapped[int] = mapped_column(
        ForeignKey("size_dict.id"), nullable=False
    )
    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sector_dict.id"), nullable=False
    )

    # Data dictionary relationships
    country: Mapped["CountryDict"] = relationship(
        "CountryDict", back_populates="entities"
    )
    entity_type: Mapped["EntityTypeDict"] = relationship(
        "EntityTypeDict", back_populates="entities"
    )
    stage: Mapped["StageDict"] = relationship(
        "StageDict", back_populates="entities"
    )
    size: Mapped["SizeDict"] = relationship(
        "SizeDict", back_populates="entities"
    )
    sector: Mapped["SectorDict"] = relationship(
        "SectorDict", back_populates="entities"
    )
    bm: Mapped["BmDict"] = relationship("BmDict", back_populates="entities")


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    iso3: Mapped[str] = mapped_column(
        ForeignKey("country_dict.iso3"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("region_dict.id"))
    is_sids: Mapped[bool] = mapped_column(Boolean)
    is_ldc: Mapped[bool] = mapped_column(Boolean)

    # Data dictionary relationships
    region: Mapped["RegionDict"] = relationship(
        "RegionDict", back_populates="countries"
    )
    dictionary: Mapped["CountryDict"] = relationship(
        "CountryDict", back_populates="country", uselist=False
    )


class Readiness(Base):
    __tablename__ = "readiness"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ref: Mapped[str] = mapped_column(nullable=True)
    activity_type_id: Mapped[int] = mapped_column(
        ForeignKey("activity_type_dict.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    delivery_partner_id: Mapped[int] = mapped_column(
        ForeignKey("delivery_partner_dict.id"), nullable=False
    )
    region_id: Mapped[int] = mapped_column(
        ForeignKey("region_dict.id"), nullable=True
    )
    has_sids: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_ldc: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_nap: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("status_dict.id"), nullable=False
    )
    approved_date: Mapped[datetime] = mapped_column(nullable=False)
    financing_usd: Mapped[int] = mapped_column(nullable=False)

    # Data dictionary relationships
    region: Mapped["RegionDict"] = relationship(
        "RegionDict", back_populates="readinesses"
    )
    activity_type: Mapped["ActivityTypeDict"] = relationship(
        "ActivityTypeDict", back_populates="readinesses"
    )
    status: Mapped["StatusDict"] = relationship(
        "StatusDict", back_populates="readinesses"
    )
    countries: Mapped[list["CountryDict"]] = relationship(
        "CountryDict",
        secondary="readiness_country",
        back_populates="readinesses",
    )
    delivery_partner: Mapped["DeliveryPartnerDict"] = relationship(
        "DeliveryPartnerDict", back_populates="readinesses"
    )


# Data dictionaries
class RegionDict(Base):
    __tablename__ = "region_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    countries: Mapped[list["Country"]] = relationship(
        "Country", back_populates="region"
    )
    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="region"
    )


class CountryDict(Base):
    __tablename__ = "country_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    iso2: Mapped[str] = mapped_column(unique=True, nullable=False)
    iso3: Mapped[str] = mapped_column(unique=True, nullable=False)
    code: Mapped[int] = mapped_column(unique=True, nullable=False)

    # Data table relationships
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="country"
    )
    country: Mapped["Country"] = relationship(
        "Country", back_populates="dictionary", uselist=False
    )
    # Join table relationships
    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary="project_country", back_populates="countries"
    )
    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness",
        secondary="readiness_country",
        back_populates="countries",
    )


class ModalityDict(Base):
    __tablename__ = "modality_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="modality"
    )


class SectorDict(Base):
    __tablename__ = "sector_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="sector"
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="sector"
    )


class ThemeDict(Base):
    __tablename__ = "theme_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="theme"
    )


class SizeDict(Base):
    __tablename__ = "size_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="size"
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="size"
    )


class EssCategoryDict(Base):
    __tablename__ = "ess_category_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="ess_category"
    )


class EntityTypeDict(Base):
    __tablename__ = "entity_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="entity_type"
    )


class StageDict(Base):
    __tablename__ = "stage_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="stage"
    )


class ActivityTypeDict(Base):
    __tablename__ = "activity_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="activity_type"
    )


class StatusDict(Base):
    __tablename__ = "status_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="status"
    )


class DeliveryPartnerDict(Base):
    __tablename__ = "delivery_partner_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Relationships
    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="delivery_partner"
    )


class BmDict(Base):
    __tablename__ = "bm_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="bm"
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="bm"
    )


# Join tables
class ProjectCountry(Base):
    __tablename__ = "project_country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=False
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country_dict.id"), nullable=False
    )


class ReadinessCountry(Base):
    __tablename__ = "readiness_country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    readiness_id: Mapped[int] = mapped_column(
        ForeignKey("readiness.id"), nullable=False
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country_dict.id"), nullable=False
    )
