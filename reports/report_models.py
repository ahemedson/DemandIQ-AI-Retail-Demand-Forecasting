from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ==================================================
# KPI
# ==================================================

@dataclass
class KPI:
    title: str
    value: str
    status: Optional[str] = None


# ==================================================
# Executive Score
# ==================================================

@dataclass
class ExecutiveScore:
    title: str
    score: float
    grade: str
    description: str


# ==================================================
# Executive Alert
# ==================================================

@dataclass
class ExecutiveAlert:
    level: str
    title: str
    description: str


# ==================================================
# Report Table
# ==================================================

@dataclass
class ReportTable:
    title: str
    columns: List[str]
    rows: List[List[Any]]


# ==================================================
# Report Chart
# ==================================================

@dataclass
class ReportChart:
    title: str
    image_path: str = ""


# ==================================================
# Report Section
# ==================================================

@dataclass
class ReportSection:
    title: str
    subtitle: str = ""
    content: str = ""

    kpis: List[KPI] = field(default_factory=list)

    scores: List[ExecutiveScore] = field(default_factory=list)

    alerts: List[ExecutiveAlert] = field(default_factory=list)

    tables: List[ReportTable] = field(default_factory=list)

    charts: List[ReportChart] = field(default_factory=list)


# ==================================================
# Report Metadata
# ==================================================

@dataclass
class ReportMetadata:
    report_title: str
    generated_by: str
    generated_at: str
    ai_model: str
    version: str

    company: str = "DemandIQ"

    report_type: str = "Executive Intelligence Report"


# ==================================================
# Executive Report
# ==================================================

@dataclass
class ExecutiveReport:
    metadata: ReportMetadata

    sections: List[ReportSection] = field(default_factory=list)

    properties: Dict[str, Any] = field(default_factory=dict)