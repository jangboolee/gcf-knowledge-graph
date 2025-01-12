from datetime import datetime

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base class for ORM objects
class Base(DeclarativeBase):
    pass


# Core master tables
class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ref: Mapped[str] = mapped_column(nullable=False)
    modality_id: Mapped[int] = mapped_column(
        ForeignKey("modality_dict.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    entity_id: Mapped[int] = mapped_column(ForeignKey("entity.id"))
    bm: Mapped[int] = mapped_column(nullable=False)
    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sector_dict.id"), nullable=False
    )
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("theme_dict.id"), nullable=False
    )
    project_size_id: Mapped[int] = mapped_column(
        ForeignKey("project_size_dict.id"), nullable=True
    )
    ess_category_id: Mapped[int] = mapped_column(
        ForeignKey("ess_category_dict.id"), nullable=False
    )
    financing_usd: Mapped[int] = mapped_column(nullable=False)

    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="projects"
    )
    countries: Mapped[list["Country"]] = relationship(
        "Country", secondary="country_project", back_populates="projects"
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
    project_size: Mapped["ProjectSizeDict"] = relationship(
        "ProjectSizeDict", back_populates="projects"
    )
    ess_category: Mapped["EssCategoryDict"] = relationship(
        "EssCategoryDict", back_populates="projects"
    )


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    is_DAE: Mapped[bool] = mapped_column(Boolean, nullable=False)
    entity_type_id: Mapped[int] = mapped_column(
        ForeignKey("entity_type_dict.id"), nullable=False
    )
    stage_id: Mapped[int] = mapped_column(
        ForeignKey("stage_dict.id"), nullable=False
    )
    bm: Mapped[int] = mapped_column(nullable=False)
    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sector_dict.id"), nullable=False
    )

    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary="entity_project", back_populates="entities"
    )
    country: Mapped["Country"] = relationship(
        "Country", back_populates="entities"
    )
    sector: Mapped["SectorDict"] = relationship(
        "SectorDict", back_populates="entities"
    )
    entity_type: Mapped["EntityTypeDict"] = relationship(
        "EntityTypeDict", back_populates="entities"
    )
    stage: Mapped["StageDict"] = relationship(
        "StageDict", back_populates="entities"
    )


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    countries: Mapped[list["Country"]] = relationship(
        "Country", back_populates="region"
    )
    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="region"
    )


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    iso3: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    is_sids: Mapped[bool] = mapped_column(Boolean)
    is_ldc: Mapped[bool] = mapped_column(Boolean)

    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary="country_project", back_populates="countries"
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="country"
    )
    region: Mapped["Region"] = relationship(
        "Region", back_populates="countries"
    )
    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="country"
    )


class Readiness(Base):
    __tablename__ = "readiness"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ref: Mapped[str] = mapped_column(nullable=False)
    activity_type_id: Mapped[int] = mapped_column(
        ForeignKey("activity_type_dict.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    delivery_partner: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(
        ForeignKey("region.id"), nullable=False
    )
    is_sids: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_ldc: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_nap: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status_id: Mapped[int] = mapped_column(
        ForeignKey("readiness_status_dict.id"), nullable=False
    )
    approved_date: Mapped[datetime] = mapped_column(nullable=False)
    financing_usd: Mapped[int] = mapped_column(nullable=False)

    country: Mapped["Country"] = relationship(
        "Country", back_populates="readinesses"
    )
    region: Mapped["Region"] = relationship(
        "Region", back_populates="readinesses"
    )
    activity_type: Mapped["ActivityTypeDict"] = relationship(
        "ActivityTypeDict", back_populates="readinesses"
    )
    status: Mapped["ReadinessStatusDict"] = relationship(
        "ReadinessStatusDict", back_populates="readinesses"
    )


# Data dictionaries
class ModalityDict(Base):
    __tablename__ = "modality_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="modality"
    )


class SectorDict(Base):
    __tablename__ = "sector_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="sector"
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="sector"
    )


class ThemeDict(Base):
    __tablename__ = "theme_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="theme"
    )


class ProjectSizeDict(Base):
    __tablename__ = "project_size_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="project_size"
    )


class EssCategoryDict(Base):
    __tablename__ = "ess_category_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="ess_category"
    )


class EntityTypeDict(Base):
    __tablename__ = "entity_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="entity_type"
    )


class StageDict(Base):
    __tablename__ = "stage_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    entities: Mapped[list["Entity"]] = relationship(
        "Entity", back_populates="stage"
    )


class ActivityTypeDict(Base):
    __tablename__ = "activity_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="activity_type"
    )


class ReadinessStatusDict(Base):
    __tablename__ = "readiness_status_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    readinesses: Mapped[list["Readiness"]] = relationship(
        "Readiness", back_populates="status"
    )


# Join tables
class CountryProject(Base):
    __tablename__ = "country_project"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=False
    )


class EntityProject(Base):
    __tablename__ = "entity_project"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=False
    )
