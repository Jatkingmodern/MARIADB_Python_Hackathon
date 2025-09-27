import logging
from typing import Dict, List, Tuple
from .config import settings
from .db import get_database
from databases import Database

logger = logging.getLogger(__name__)

async def introspect_schema() -> Dict[str, List[Tuple[str, str]]]:
    """
    Return a mapping table -> list of (column_name, data_type)
    Only tables present in config.yaml allowed_columns are exposed.
    """
    db: Database = get_database()
    # Use information_schema to fetch columns safely
    query = """
    SELECT TABLE_NAME, COLUMN_NAME, COLUMN_TYPE
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = :schema
    """
    rows = await db.fetch_all(query=query, values={"schema": settings.db_name})
    result = {}
    for r in rows:
        t = r["TABLE_NAME"]
        result.setdefault(t, []).append((r["COLUMN_NAME"], r["COLUMN_TYPE"]))
    return result

def allowed_tables_from_config() -> Dict[str, str]:
    """
    returns alias -> actual table name mapping from config.yaml
    """
    aliases = settings.yaml_cfg.get("nl2sql", {}).get("table_aliases", {})
    return aliases or {}

def allowed_columns_for_table(table: str) -> List[str]:
    allowed = settings.yaml_cfg.get("nl2sql", {}).get("allowed_columns", {})
    if table in allowed:
        return allowed[table]
    # table might already be actual name but config uses table as key
    for k, v in allowed.items():
        if v == table:
            return allowed[k]
    return []
