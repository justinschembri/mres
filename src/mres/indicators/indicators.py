"""Base classes representing the Multi-hazard resilience indicators."""

#stdlib
from pydantic import BaseModel, Field
from typing import Union
from abc import ABC, abstractmethod
from enum import Enum
#external

class HazardType(Enum):
    HEAT = "heat"
    SEISMIC = "seismic"
    FLOOD = "flood"
    WIND = "wind"

class ResilienceIndicator(BaseModel, ABC):

    id: int

    def __repr__(self) -> str:
        return self.__class__.__name__ + (f"(Building ID: {str(self.id)})")

    @abstractmethod
    def calculate_rrl(self, *args, **kwargs) -> float:
        ""
        pass

class HeatResilienceIndicators(ResilienceIndicator):
    """A set of indicators for calculating heat resilience of a building."""
    res_1: Union[int, float] = Field(..., gt=0, le=1, description="First heat resistance indicator")
    res_2: Union[int, float] = Field(..., gt=0, le=1, description="Second heat resistance indicator")
    res_3: Union[int, float] = Field(..., gt=0, le=1, description="Third heat resistance indicator")
    rec_1: Union[int, float] = Field(..., gt=0, le=1, description="Heat recovery indicator")
    e_f: Union[int, float] = Field(..., gt=0, le=1, description="Heat efficiency indicator")
    m_1: Union[int, float] = Field(..., gt=0, le=1, description="Resilience indicator weighting")
    m_2: Union[int, float] = Field(..., gt=0, le=1, description="Recovery indicator weighting")
    
    res_readiness_level: float | None = Field(
        default=None,
        description="Calculated resilience readiness level"
    )

    def calculate_rrl(self) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            ((1 - self.res_1 * self.res_2 * self.res_3) * self.m_1) +
            ((1 - self.rec_1) * self.m_2)
        ) * self.e_f
        return self.res_readiness_level

class SeismicResilienceIndicators(ResilienceIndicator):
    """A set of indicators for calculating seismic resilience of a building."""
    res_1: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 1")
    res_2: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 2")
    res_3: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 3")
    res_4: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 4")
    rec_1: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 1")
    rec_2: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 2")
    rec_3: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 3")
    n_1: Union[int, float] = Field(..., ge=0, le=1, description="...")
    n_2: Union[int, float] = Field(..., ge=0, le=1, description="...")
    n_3: Union[int, float] = Field(..., ge=0, le=1, description="...")
    n_4: Union[int, float] = Field(..., ge=0, le=1, description="...")
    n_5: Union[int, float] = Field(..., ge=0, le=1, description="...") 
    n_6: Union[int, float] = Field(..., ge=0, le=1, description="...")
    n_7: Union[int, float] = Field(..., ge=0, le=1, description="...")
    m_1: Union[int, float] = Field(..., ge=0, le=1, description="...")
    m_2: Union[int, float] = Field(..., ge=0, le=1, description="...")

    res_readiness_level: float | None = Field(
        default=None,
        description="Calculated resilience readiness level"
    )

    def calculate_rrl(
        self,
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.res_1**self.n_1 *
                    self.res_2**self.n_2 *
                    self.res_3**self.n_3 *
                    self.res_4**self.n_4
                )
            ) * self.m_1
            +
            (
                1 - (
                    self.rec_1**self.n_5 *
                    self.rec_2**self.n_6 *
                    self.rec_3**self.n_7
                )
            ) * self.m_2
        )
        return self.res_readiness_level #type: ignore

class WindResilienceIndicators(ResilienceIndicator):
    """A set of indicators for calculating wind resilience of a building."""
    res_1: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 1")
    res_2: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 2")
    res_3: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 3")
    rec_1: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 1")
    rec_2: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 2")
    rec_3: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 3")
    n_1: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_2: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_3: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_4: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_5: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_6: Union[int, float] = Field(..., gt=0, le=1, description="...")
    m_1: Union[int, float] = Field(..., gt=0, le=1, description="...")
    m_2: Union[int, float] = Field(..., gt=0, le=1, description="...")

    res_readiness_level: float | None = Field(
        default=None,
        description="Calculated resilience readiness level"
    )

    def calculate_rrl(
        self,
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.res_1**self.n_1 *
                    self.res_2**self.n_2 *
                    self.res_3**self.n_3
                )
            ) * self.m_1
            +
            (
                1 - (
                    self.rec_1**self.n_4 *
                    self.rec_2**self.n_5 *
                    self.rec_3**self.n_6
                )
            ) * self.m_2
        )
        return self.res_readiness_level #type: ignore

class FloodResilienceIndicators(ResilienceIndicator):
    """A set of indicators for calculating flood resilience of a building."""
    res_1: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 1")
    res_2: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 2")
    res_3: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 3")
    res_4: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 4")
    res_5: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 5")
    rec_1: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 1")
    rec_2: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 2")
    rec_3: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 3")
    rec_4: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 4")
    n_1: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_2: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_3: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_4: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_5: Union[int, float] = Field(..., gt=0, le=1, description="...") 
    n_6: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_7: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_8: Union[int, float] = Field(..., gt=0, le=1, description="...")
    n_9: Union[int, float] = Field(..., gt=0, le=1, description="...")
    m_1: Union[int, float] = Field(..., gt=0, le=1, description="...")
    m_2: Union[int, float] = Field(..., gt=0, le=1, description="...")

    res_readiness_level: float | None = Field(
        default=None,
        description="Calculated resilience readiness level"
    )

    def calculate_rrl(
        self
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.res_1**self.n_1 *
                    self.res_2**self.n_2 *
                    self.res_3**self.n_3 *
                    self.res_4**self.n_4 *
                    self.res_5**self.n_5
                )
            ) * self.m_1
            +
            (
                1 - (
                    self.rec_1**self.n_6 *
                    self.rec_2**self.n_7 *
                    self.rec_3**self.n_8 *
                    self.rec_4**self.n_9
                )
            ) * self.m_2
        )
        return self.res_readiness_level #type: ignore
