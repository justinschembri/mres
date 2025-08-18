"""Base classes representing the Multi-hazard resilience indicators."""

#stdlib
from pydantic import BaseModel, Field
from typing import Union
#external

class HeatResilienceIndicators(BaseModel):
    """A set of indicators for calculating heat resilience of a building."""
    heat_res1: Union[int, float] = Field(..., ge=0, le=1, description="First heat resistance indicator")
    heat_res2: Union[int, float] = Field(..., ge=0, le=1, description="Second heat resistance indicator")
    heat_res3: Union[int, float] = Field(..., ge=0, le=1, description="Third heat resistance indicator")
    heat_rec: Union[int, float] = Field(..., ge=0, le=1, description="Heat recovery indicator")
    heat_ef: Union[int, float] = Field(..., ge=0, le=1, description="Heat efficiency indicator")

    res_readiness_level: float | None = Field(
        default=None,
        description="Calculated resilience readiness level"
    )

    def calculate_rrl(self, m1: float, m2: float) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            ((1 - self.heat_res1 * self.heat_res2 * self.heat_res3) * m1) +
            ((1 - self.heat_rec) * m2)
        )
        return self.res_readiness_level

class SeismicResilienceIndicators(BaseModel):
    """A set of indicators for calculating seismic resilience of a building."""
    seismic_res1: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 1")
    seismic_res2: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 2")
    seismic_res3: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 3")
    seismic_res4: Union[int, float] = Field(..., ge=0, le=1, description="Seismic resistance indicator 4")
    seismic_rec1: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 1")
    seismic_rec2: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 2")
    seismic_rec3: Union[int, float] = Field(..., ge=0, le=1, description="Seismic recovery indicator 3")

    def calculate_rrl(
        self,
        n1: float,
        n2: float,
        n3: float,
        n4: float,
        n5: float, 
        n6: float,
        n7: float,
        m1: float,
        m2: float
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.seismic_res1**n1 *
                    self.seismic_res2**n2 *
                    self.seismic_res3**n3 *
                    self.seismic_res4**n4
                )
            ) * m1
            +
            (
                1 - (
                    self.seismic_rec1**n5 *
                    self.seismic_rec2**n6 *
                    self.seismic_rec3**n7
                )
            ) * m2
        )
        return self.res_readiness_level

class WindResilienceIndicators(BaseModel):
    """A set of indicators for calculating wind resilience of a building."""
    wind_res1: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 1")
    wind_res2: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 2")
    wind_res3: Union[int, float] = Field(..., ge=0, le=1, description="Wind resistance indicator 3")
    wind_rec1: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 1")
    wind_rec2: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 2")
    wind_rec3: Union[int, float] = Field(..., ge=0, le=1, description="Wind recovery indicator 3")

    def calculate_rrl(
        self,
        n1: float,
        n2: float,
        n3: float,
        n4: float,
        n5: float,
        n6: float,
        m1: float,
        m2: float
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.wind_res1**n1 *
                    self.wind_res2**n2 *
                    self.wind_res3**n3
                )
            ) * m1
            +
            (
                1 - (
                    self.wind_rec1**n4 *
                    self.wind_rec2**n5 *
                    self.wind_rec3**n6
                )
            ) * m2
        )
        return self.res_readiness_level

class FloodResilienceIndicators(BaseModel):
    """A set of indicators for calculating flood resilience of a building."""
    flood_res1: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 1")
    flood_res2: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 2")
    flood_res3: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 3")
    flood_res4: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 4")
    flood_res5: Union[int, float] = Field(..., ge=0, le=1, description="Flood resistance indicator 5")
    flood_rec1: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 1")
    flood_rec2: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 2")
    flood_rec3: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 3")
    flood_rec4: Union[int, float] = Field(..., ge=0, le=1, description="Flood recovery indicator 4")

    def calculate_rrl(
        self,
        n1: float,
        n2: float,
        n3: float,
        n4: float,
        n5: float, 
        n6: float,
        n7: float,
        n8: float,
        n9: float,
        m1: float,
        m2: float
    ) -> float:
        """Calculate the resilience readiness level based on the indicators."""
        self.res_readiness_level = (
            (
                1 - (
                    self.flood_res1**n1 *
                    self.flood_res2**n2 *
                    self.flood_res3**n3 *
                    self.flood_res4**n4 *
                    self.flood_res5**n5
                )
            ) * m1
            +
            (
                1 - (
                    self.flood_rec1**n6 *
                    self.flood_rec2**n7 *
                    self.flood_rec3**n8 *
                    self.flood_rec4**n9
                )
            ) * m2
        )
        return self.res_readiness_level
