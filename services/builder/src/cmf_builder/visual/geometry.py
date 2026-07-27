"""Exact deterministic geometry normalization for ST-02.01."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from cmf_builder.visual.ontology import SyntaxContractError, canonical_sha256


class GeometryInvalid(SyntaxContractError):
    code = "GeometryInvalid"


@dataclass(frozen=True, slots=True)
class PixelBox:
    x: int
    y: int
    width: int
    height: int

    def validate(self, *, canvas_width: int, canvas_height: int) -> None:
        if canvas_width <= 0 or canvas_height <= 0:
            raise GeometryInvalid("source canvas dimensions must be positive")
        if self.x < 0 or self.y < 0 or self.width <= 0 or self.height <= 0:
            raise GeometryInvalid(
                "pixel boxes require non-negative origins and positive dimensions"
            )
        if self.x + self.width > canvas_width or self.y + self.height > canvas_height:
            raise GeometryInvalid(
                "pixel box exceeds the governed source canvas",
                canvas_width=canvas_width,
                canvas_height=canvas_height,
            )

    def as_dict(self) -> dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True, slots=True)
class ExactRatio:
    numerator: int
    denominator: int

    def __post_init__(self) -> None:
        if self.denominator <= 0 or self.numerator < 0:
            raise GeometryInvalid("normalized ratios require a non-negative value")
        reduced = Fraction(self.numerator, self.denominator)
        if reduced > 1:
            raise GeometryInvalid("normalized ratios cannot exceed one")
        object.__setattr__(self, "numerator", reduced.numerator)
        object.__setattr__(self, "denominator", reduced.denominator)

    @classmethod
    def create(cls, numerator: int, denominator: int) -> "ExactRatio":
        return cls(numerator=numerator, denominator=denominator)

    def as_dict(self) -> dict[str, int]:
        return {"numerator": self.numerator, "denominator": self.denominator}


@dataclass(frozen=True, slots=True)
class NormalizedBox:
    x: ExactRatio
    y: ExactRatio
    width: ExactRatio
    height: ExactRatio
    source_width_px: int
    source_height_px: int

    @property
    def geometry_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "x": self.x.as_dict(),
            "y": self.y.as_dict(),
            "width": self.width.as_dict(),
            "height": self.height.as_dict(),
            "source_width_px": self.source_width_px,
            "source_height_px": self.source_height_px,
        }


def normalize_box(
    box: PixelBox, *, canvas_width: int, canvas_height: int
) -> NormalizedBox:
    """Return an exact rational representation; no floating-point state enters identity."""

    box.validate(canvas_width=canvas_width, canvas_height=canvas_height)
    return NormalizedBox(
        x=ExactRatio.create(box.x, canvas_width),
        y=ExactRatio.create(box.y, canvas_height),
        width=ExactRatio.create(box.width, canvas_width),
        height=ExactRatio.create(box.height, canvas_height),
        source_width_px=canvas_width,
        source_height_px=canvas_height,
    )
