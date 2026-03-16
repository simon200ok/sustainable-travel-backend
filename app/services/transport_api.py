"""
Transport API integration service.

This module will handle fetching live data from an external transport API
(e.g. Traveline Data Service, Transport API, National Rail Enquiries).

When you're ready to integrate:
1. Add your API key to .env and config.py
2. Implement the fetch functions below
3. Call sync_operators() / sync_locations() from a scheduled job or on startup

The sync functions write directly to the DB so all existing endpoints
continue to work without any changes.
"""

import logging
from typing import Any

import httpx
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config — add to core/config.py and .env when you have a real API key:
#   TRANSPORT_API_KEY=your-key-here
#   TRANSPORT_API_BASE_URL=https://api.example.com/v1
# ---------------------------------------------------------------------------


class TransportAPIError(Exception):
    """Raised when the external transport API returns an unexpected response."""


async def _get(url: str, params: dict | None = None, api_key: str = "") -> Any:
    """
    Shared HTTP GET helper with timeout and error handling.
    Replace the headers/auth scheme to match whichever API you integrate.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise TransportAPIError(
            f"Transport API returned {response.status_code}: {response.text}"
        )

    return response.json()


# ---------------------------------------------------------------------------
# Sync functions — implement these when you have a real API
# ---------------------------------------------------------------------------


async def sync_operators(db: Session, base_url: str, api_key: str) -> int:
    """
    Fetch operators from the external API and upsert into the DB.
    Returns the number of operators synced.

    TODO: implement when API is available.
    Example flow:
        data = await _get(f"{base_url}/operators", api_key=api_key)
        for item in data["operators"]:
            existing = db.query(Operator).filter_by(name=item["name"]).first()
            if existing:
                existing.description = item["description"]
                ...
            else:
                db.add(Operator(...))
        db.commit()
    """
    logger.info("sync_operators: not yet implemented — using seeded data")
    return 0


async def sync_locations(db: Session, base_url: str, api_key: str) -> int:
    """
    Fetch stop/station locations from the external API and upsert into the DB.
    Returns the number of locations synced.

    TODO: implement when API is available.
    Traveline NaPTAN data and Transport API both provide stop coordinates
    that map directly onto the Location model (name, type, lat, lng).
    """
    logger.info("sync_locations: not yet implemented — using seeded data")
    return 0


async def sync_tickets(db: Session, base_url: str, api_key: str) -> int:
    """
    Fetch live ticket/fare data and upsert into the DB.
    Returns the number of tickets synced.

    TODO: implement when API is available.
    Note: not all APIs expose fares — you may need to combine sources
    (e.g. Nexus open data for Metro fares, National Rail for train fares).
    """
    logger.info("sync_tickets: not yet implemented — using seeded data")
    return 0


async def run_full_sync(db: Session, base_url: str, api_key: str) -> dict:
    """
    Run all sync jobs in sequence.
    Call this from a scheduled task (APScheduler, cron, etc.) when ready.

    Example — add to main.py for a startup sync:
        from app.services.transport_api import run_full_sync
        from app.database import SessionLocal
        from app.core.config import settings

        @app.on_event("startup")
        async def startup_sync():
            db = SessionLocal()
            try:
                await run_full_sync(db, settings.transport_api_base_url, settings.transport_api_key)
            finally:
                db.close()
    """
    try:
        operators = await sync_operators(db, base_url, api_key)
        locations = await sync_locations(db, base_url, api_key)
        tickets = await sync_tickets(db, base_url, api_key)
        logger.info("Full sync complete: %d operators, %d locations, %d tickets", operators, locations, tickets)
        return {"operators": operators, "locations": locations, "tickets": tickets}
    except TransportAPIError as exc:
        logger.error("Transport API sync failed: %s", exc)
        raise
