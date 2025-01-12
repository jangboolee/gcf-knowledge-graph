from datetime import datetime

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base class for ORM objects
class Base(DeclarativeBase):
    pass


# Core master tables
class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
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
        ForeignKey("project_size_dict.id"), nullable=False
    )
    ess_category_id: Mapped[int] = mapped_column(
        ForeignKey("ess_category_dict.id"), nullable=False
    )
    financing_usd: Mapped[int] = mapped_column(nullable=False)

    entity: Mapped["Entity"] = relationship(
        "Entity", back_populates="projects"
    )
    countries: Mapped[list["Country"]] = relationship(
        "Country", secondary="country_project", back_populates="projects"
    )
    modality: Mapped["ModalityDict"] = relationship("ModalityDict")
    sector: Mapped["SectorDict"] = relationship("SectorDict")
    theme: Mapped["ThemeDict"] = relationship("ThemeDict")
    project_size: Mapped["ProjectSizeDict"] = relationship("ProjectSizeDict")
    ess_category: Mapped["EssCategoryDict"] = relationship("EssCategoryDict")


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    is_dae: Mapped[bool] = mapped_column(Boolean, nullable=False)
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
    country: Mapped["Country"] = relationship("Country")
    sector: Mapped["SectorDict"] = relationship("SectorDict")
    entity_type: Mapped["EntityTypeDict"] = relationship("EntityTypeDict")
    stage: Mapped["StageDict"] = relationship("StageDict")


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    iso3: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    is_sids: Mapped[bool] = mapped_column(Boolean)
    is_ldc: Mapped[bool] = mapped_column(Boolean)

    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary="country_project", back_populates="countries"
    )


class Readiness(Base):
    __tablename__ = "readiness"

    id: Mapped[int] = mapped_column(primary_key=True)
    ref: Mapped[str] = mapped_column(nullable=False)
    readiness_type_id: Mapped[int] = mapped_column(
        ForeignKey("readiness_type_dict.id"), nullable=False
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


# Data dictionaries
class ModalityDict(Base):
    __tablename__ = "modality_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class SectorDict(Base):
    __tablename__ = "sector_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class ThemeDict(Base):
    __tablename__ = "theme_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class ProjectSizeDict(Base):
    __tablename__ = "project_size_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class EssCategoryDict(Base):
    __tablename__ = "ess_category_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class EntityTypeDict(Base):
    __tablename__ = "entity_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class StageDict(Base):
    __tablename__ = "stage_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class ReadinessTypeDict(Base):
    __tablename__ = "readiness_type_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class ReadinessStatusDict(Base):
    __tablename__ = "readiness_status_dict"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


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
