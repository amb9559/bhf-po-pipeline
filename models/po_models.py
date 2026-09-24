"""Data models for purchase-order processing."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class POHeader:
    po_number: Optional[str] = None
    vendor_name: Optional[str] = None
    buyer: Optional[str] = None
    ship_date: Optional[str] = None
    ship_terms: Optional[str] = None
    ref_po: Optional[str] = None


@dataclass
class POLineItem:
    sku: Optional[str] = None
    upc: Optional[str] = None
    department: Optional[str] = None
    vendor_part: Optional[str] = None
    description: Optional[str] = None
    retail: Optional[float] = None
    cost: Optional[float] = None
    cartons: Optional[int] = None
    case_pack: Optional[int] = None
    ext_qty: Optional[int] = None
    ext_cost: Optional[float] = None
    cube: Optional[float] = None
    kilograms: Optional[float] = None
    issues: List[str] = field(default_factory=list)


@dataclass
class PORecord:
    header: POHeader = field(default_factory=POHeader)
    line_items: List[POLineItem] = field(default_factory=list)
    source_file: Optional[str] = None
    issues: List[str] = field(default_factory=list)
