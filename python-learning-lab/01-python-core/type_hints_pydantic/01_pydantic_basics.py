"""
Exercise 01 — Pydantic v2 and Type Hints
==========================================
Goal: use Pydantic to validate data and manage configuration.

Pydantic is fundamental in the modern Python ecosystem:
  - FastAPI uses it to validate requests and responses
  - LangChain uses it to configure chains and agents
  - You will use it to validate data in ETL pipelines

Install: pip install pydantic pydantic-settings
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ─────────────────────────────────────────────
# LEVEL 1 — Basic model with validation
# ─────────────────────────────────────────────

class Sector(str, Enum):
    TECH = "tech"
    FINANCE = "finance"
    HEALTH = "health"
    OTHER = "other"


class Company(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sector: Sector
    employees: int = Field(gt=0)
    revenue_eur: Optional[float] = Field(default=None, ge=0)
    founded_year: int = Field(ge=1800, le=datetime.now().year)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode="after")
    def revenue_required_for_large_companies(self) -> "Company":
        if self.employees > 1000 and self.revenue_eur is None:
            raise ValueError("Companies with >1000 employees must provide revenue")
        return self


class Portfolio(BaseModel):
    """Model representing an investment portfolio."""
    owner: str
    companies: list[Company]
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def total_employees(self) -> int:
        return sum(c.employees for c in self.companies)

    @property
    def by_sector(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for company in self.companies:
            result.setdefault(company.sector, []).append(company.name)
        return result


# ─────────────────────────────────────────────
# LEVEL 2 — Settings from environment variables
# ─────────────────────────────────────────────

class DatabaseSettings(BaseSettings):
    """
    Reads configuration from environment variables or a .env file.
    Variables use the prefix DB_ (e.g. DB_HOST=localhost).
    """
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"
    user: str = "postgres"
    password: str = ""

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "python-learning-lab"
    debug: bool = False
    api_key: str = ""
    db: DatabaseSettings = DatabaseSettings()


# ─────────────────────────────────────────────
# LEVEL 3 — Serialisation and parsing
# ─────────────────────────────────────────────

def parse_companies_from_dict(data: list[dict]) -> list[Company]:
    """Parses and validates a list of companies from raw data."""
    return [Company.model_validate(item) for item in data]


# ─────────────────────────────────────────────
# EXERCISE — implement this yourself
# ─────────────────────────────────────────────

class Transaction(BaseModel):
    """
    TODO: Create a model for an investment transaction with:
    - ticker: str (e.g. "AAPL", max 5 chars, uppercase)
    - shares: float (must be positive)
    - price_eur: float (must be positive)
    - transaction_type: Enum with BUY / SELL
    - date: datetime

    Add a `total_value` property that returns shares * price_eur.
    Add a validator that automatically converts ticker to uppercase.
    """
    pass


# ─────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("LEVEL 1 — Pydantic models")
    print("=" * 50)

    raw_data = [
        {"name": "Anthropic", "sector": "tech", "employees": 800, "founded_year": 2021},
        {"name": "Polar Capital", "sector": "finance", "employees": 200, "founded_year": 2001},
    ]

    companies = parse_companies_from_dict(raw_data)
    portfolio = Portfolio(owner="Ruben", companies=companies)

    print(f"Portfolio owner: {portfolio.owner}")
    print(f"Total employees: {portfolio.total_employees}")
    print(f"By sector: {portfolio.by_sector}")
    print("\nPortfolio JSON:")
    print(portfolio.model_dump_json(indent=2))

    print("\n" + "=" * 50)
    print("LEVEL 2 — Validation fails correctly")
    print("=" * 50)

    try:
        bad = Company(
            name="BigCorp",
            sector="tech",
            employees=5000,  # >1000 employees without revenue → error
            founded_year=2020,
        )
    except Exception as e:
        print(f"Expected error: {e}")

    print("\n" + "=" * 50)
    print("LEVEL 3 — Settings")
    print("=" * 50)
    settings = AppSettings()
    print(f"App: {settings.app_name}")
    print(f"DB URL: {settings.db.url}")