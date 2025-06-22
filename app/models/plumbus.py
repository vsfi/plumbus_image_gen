from pydantic import BaseModel, Field
from typing import Optional


class PlumbusModel(BaseModel):
    size: str = Field("M", enum=["XS", "S", "M", "L", "XL", "XXL", "nano"])
    color: str = Field("pink", enum=["pink", "deep_pink", "red", "blue", "green", "yellow", "purple", "orange", "cyan", "lime", "teal", "brown"])
    shape: str = Field("smooth", enum=["uglovatiy", "multi-uglovatiy", "smooth"])
    weight: str = Field("medium", enum=["heavy", "medium", "light", "ultralight"])
    wrapping: str = Field("default", enum=["default", "gift", "limited"])

