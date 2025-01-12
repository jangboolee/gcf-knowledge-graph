from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey


class Base(DeclarativeBase):
    pass


"""
Master tables containing key GCF data
"""


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    ref: Mapped[str] = mapped_column(nullable=False)
    modality_id: Mapped[int] = mapped_column(
        ForeignKey("modality_dict.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id"), nullable=False
    )
    bm: Mapped[int] = mapped_column(nullable=False)
    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sector_dict.id"), nullable=False
    )
    theme_id: Mapped[int] = mapped_column(
        ForeignKey("theme_dict.id"), nullable=False
    )
    project_size_id: Mapped[str] = mapped_column(
        ForeignKey("project_size_dict.id"), nullable=False
    )
    ess_category_id: Mapped[str] = mapped_column(
        ForeignKey("ess_category_dict.id"), nullable=False
    )

    # One-to-many relationship with data dictionaries
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
    # One-to-many relationship with Entities
    entity: Mapped["Entity"] = relationship(
        "Entity", back_populates="projects"
    )
    # Many-to-many relationships with Country and Entity
    countries: Mapped[list["Country"]] = relationship(
        "Country",
        secondary="country_project",
        back_populates="projects",
    )
    entities: Mapped[list["Entity"]] = relationship(
        "Entity",
        secondary="entity_project",
        back_populates="projects",
    )


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    region_id: Mapped[int] = mapped_column(
        ForeignKey("region_dict.id"), nullable=False
    )
    is_SIDS: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_LDC: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # One-to-many relationship with data dictionary
    region: Mapped["RegionDict"] = relationship(
        "RegionDict", back_populates="countries"
    )

    # Many-to-many relationship with Project via country_project
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary="country_project",
        back_populates="countries",
    )


class Entity(Base):
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    is_DAE: Mapped[bool] = mapped_column(Boolean, nullable=False)
    type: Mapped[str]

    # One-to-many relationship
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="entity"
    )
    # Many-to-many relationship with Project via entity_project
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary="entity_project",
        back_populates="entities",
    )


class Readiness(Base):
    __tablename__ = "readiness"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)


"""
Data dictionaries for ID to name mapping within the GCF taxonomy
"""


class ModalityDict(Base):
    __tablename__ = "modality_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Project
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="modality"
    )


class SectorDict(Base):
    __tablename__ = "sector_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Project
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="sector"
    )


class ThemeDict(Base):
    __tablename__ = "theme_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Project
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="theme"
    )


class ProjectSizeDict(Base):
    __tablename__ = "project_size_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Project
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="project_size"
    )


class EssCategoryDict(Base):
    __tablename__ = "ess_category_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Project
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="ess_category"
    )


class RegionDict(Base):
    __tablename__ = "region_dict"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Country
    countries: Mapped[list["Country"]] = relationship(
        "Country", back_populates="region"
    )


"""
Join tables to represent many-to-many relationships
"""


class CountryProject(Base):
    __tablename__ = "country_project"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=False
    )


class EntityProject(Base):
    __tablename__ = "entity_project"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    entity_id: Mapped[int] = mapped_column(
        ForeignKey("entity.id"), nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"), nullable=False
    )
