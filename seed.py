#!/usr/bin/env python
"""Seed the database with initial North East England transport data.

Usage:
    python seed.py

Run this once after the database has been created. It is safe to re-run —
it exits early if operators already exist.
"""

import app.models  # noqa: F401 — must be imported before create_all
from app.database import Base, SessionLocal, engine
from app.models.location import Location
from app.models.operator import Operator
from app.models.ticket import Ticket
from app.models.zone import Zone


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Operator).count() > 0:
            print("Database already seeded — skipping.")
            return

        # ── Zones ────────────────────────────────────────────────────────────
        zone_a = Zone(
            name="Zone A",
            color="#0069FA",
            description="Newcastle City Centre and surrounding areas",
            areas=["Newcastle Central", "Monument", "Eldon Square", "Gateshead"],
            metro_stations=["Newcastle", "Monument", "Central Station", "St James", "Gateshead"],
        )
        zone_b = Zone(
            name="Zone B",
            color="#F57C00",
            description="Sunderland and surrounding areas — home of the University of Sunderland",
            areas=["Sunderland City Centre", "St Peter's", "Stadium of Light", "Pallion"],
            metro_stations=["Sunderland", "St Peter's", "Stadium of Light", "Park Lane"],
        )
        zone_c = Zone(
            name="Zone C",
            color="#4CAF50",
            description="North Tyneside — coastal towns and residential suburbs",
            areas=["Whitley Bay", "Tynemouth", "North Shields", "Wallsend"],
            metro_stations=["Whitley Bay", "Tynemouth", "North Shields", "Wallsend", "Cullercoats"],
        )
        zone_d = Zone(
            name="Zone D",
            color="#9C27B0",
            description="Airport and western corridor",
            areas=["Newcastle Airport", "Callerton", "Kingston Park", "Regent Centre"],
            metro_stations=["Airport", "Callerton Parkway", "Kingston Park", "Regent Centre"],
        )
        db.add_all([zone_a, zone_b, zone_c, zone_d])
        db.flush()

        # ── Operators ─────────────────────────────────────────────────────────
        go_north_east = Operator(
            name="Go North East",
            type="Bus",
            color="#E30613",
            description="The main bus operator serving Tyne and Wear and County Durham.",
            website="https://www.gonortheast.co.uk",
            sustainability_note=(
                "Investing in electric and hybrid buses to reduce emissions across the North East."
            ),
        )
        nexus = Operator(
            name="Nexus Metro",
            type="Metro",
            color="#FFD700",
            description=(
                "Tyne and Wear Metro — the rapid transit system connecting "
                "Sunderland, Newcastle, and the coast."
            ),
            website="https://www.nexus.org.uk",
            sustainability_note=(
                "The Metro produces 75% less CO\u2082 per passenger mile compared to a private car."
            ),
        )
        northern = Operator(
            name="Northern Trains",
            type="Train",
            color="#003366",
            description="Regional rail services connecting Sunderland to Newcastle, Durham, and beyond.",
            website="https://www.northernrailway.co.uk",
            sustainability_note="Rail travel produces up to 60% less CO\u2082 per passenger mile than driving.",
        )
        stagecoach = Operator(
            name="Stagecoach",
            type="Bus",
            color="#E37124",
            description="Bus services across Sunderland and the surrounding areas.",
            website="https://www.stagecoachbus.com",
            sustainability_note=(
                "One fully loaded bus takes up to 50 cars off the road, cutting congestion and emissions."
            ),
        )
        db.add_all([go_north_east, nexus, northern, stagecoach])
        db.flush()

        # ── Tickets ───────────────────────────────────────────────────────────
        tickets = [
            # Go North East
            Ticket(operator_id=go_north_east.id, ticket_type="Single", price=1.80, duration="Single", notes="Valid for one journey"),
            Ticket(operator_id=go_north_east.id, ticket_type="Day Saver", price=4.20, duration="Day", notes="Unlimited bus travel for one day"),
            Ticket(operator_id=go_north_east.id, ticket_type="Weekly", price=16.00, duration="Week", notes="7-day unlimited bus travel"),
            Ticket(operator_id=go_north_east.id, ticket_type="Monthly", price=52.00, duration="Month", notes="28-day unlimited bus travel"),
            # Nexus Metro
            Ticket(operator_id=nexus.id, ticket_type="Single (1 Zone)", price=1.80, duration="Single", notes="One zone, one journey"),
            Ticket(operator_id=nexus.id, ticket_type="Single (2 Zones)", price=2.30, duration="Single", notes="Two zones, one journey"),
            Ticket(operator_id=nexus.id, ticket_type="Day Saver (1 Zone)", price=3.80, duration="Day", notes="Unlimited Metro travel in one zone"),
            Ticket(operator_id=nexus.id, ticket_type="Day Saver (2 Zones)", price=5.10, duration="Day", notes="Unlimited Metro travel in two zones"),
            Ticket(operator_id=nexus.id, ticket_type="Weekly Pass", price=18.00, duration="Week", notes="7-day unlimited Metro travel"),
            Ticket(operator_id=nexus.id, ticket_type="Pop Card Monthly", price=45.00, duration="Month", notes="28-day unlimited Metro travel via Pop Card"),
            # Northern Trains
            Ticket(operator_id=northern.id, ticket_type="Single", price=3.50, duration="Single", notes="One-way journey"),
            Ticket(operator_id=northern.id, ticket_type="Off-Peak Return", price=7.00, duration="Return", notes="Travel after 09:30 — not valid on peak services"),
            Ticket(operator_id=northern.id, ticket_type="Weekly Season", price=32.00, duration="Week", notes="7-day rail pass"),
            Ticket(operator_id=northern.id, ticket_type="Monthly Season", price=120.00, duration="Month", notes="28-day rail pass"),
            # Stagecoach
            Ticket(operator_id=stagecoach.id, ticket_type="Single", price=2.00, duration="Single", notes="Single journey"),
            Ticket(operator_id=stagecoach.id, ticket_type="Day Rider", price=4.50, duration="Day", notes="Unlimited Stagecoach travel for one day"),
            Ticket(operator_id=stagecoach.id, ticket_type="Megarider 7", price=18.50, duration="Week", notes="7-day unlimited Stagecoach travel"),
            Ticket(operator_id=stagecoach.id, ticket_type="Megarider 28", price=65.00, duration="Month", notes="28-day unlimited Stagecoach travel"),
        ]
        db.add_all(tickets)

        # ── Locations ─────────────────────────────────────────────────────────
        locations = [
            Location(
                name="University of Sunderland (City Campus)",
                type="campus",
                lat=54.9070,
                lng=-1.3845,
                description="Main campus of the University of Sunderland in the city centre.",
                nearby_transport=["Sunderland Metro Station", "Park Lane Interchange"],
                zone_id=zone_b.id,
            ),
            Location(
                name="St Peter's Campus",
                type="campus",
                lat=54.9113,
                lng=-1.3769,
                description="Riverside campus on the banks of the River Wear.",
                nearby_transport=["St Peter's Metro Station"],
                zone_id=zone_b.id,
            ),
            Location(
                name="Sunderland Metro Station",
                type="metro",
                lat=54.9057,
                lng=-1.3814,
                description="Main Sunderland Metro stop, connecting to Newcastle and the coast.",
                nearby_transport=["Park Lane Bus Interchange"],
                zone_id=zone_b.id,
            ),
            Location(
                name="St Peter's Metro Station",
                type="metro",
                lat=54.9100,
                lng=-1.3758,
                description="Metro stop serving St Peter's campus and Stadium of Light.",
                nearby_transport=[],
                zone_id=zone_b.id,
            ),
            Location(
                name="Park Lane Interchange",
                type="bus",
                lat=54.9060,
                lng=-1.3830,
                description="Major bus interchange in Sunderland city centre.",
                nearby_transport=["Sunderland Metro Station"],
                zone_id=zone_b.id,
            ),
            Location(
                name="Sunderland Train Station",
                type="train",
                lat=54.9049,
                lng=-1.3806,
                description="Sunderland railway station with Northern Trains services to Newcastle and Durham.",
                nearby_transport=["Park Lane Bus Interchange", "Sunderland Metro Station"],
                zone_id=zone_b.id,
            ),
            Location(
                name="Newcastle Central Station",
                type="train",
                lat=54.9686,
                lng=-1.6178,
                description="Newcastle's main railway station with national and regional services.",
                nearby_transport=["Newcastle Metro Station", "Eldon Square Bus Station"],
                zone_id=zone_a.id,
            ),
            Location(
                name="Newcastle Monument Metro",
                type="metro",
                lat=54.9749,
                lng=-1.6143,
                description="Central Metro interchange at Monument, Newcastle.",
                nearby_transport=["Eldon Square Bus Station"],
                zone_id=zone_a.id,
            ),
            Location(
                name="Eldon Square Bus Station",
                type="bus",
                lat=54.9759,
                lng=-1.6153,
                description="Major bus station in Newcastle city centre.",
                nearby_transport=["Newcastle Monument Metro"],
                zone_id=zone_a.id,
            ),
            Location(
                name="Tynemouth Metro Station",
                type="metro",
                lat=55.0171,
                lng=-1.4232,
                description="Coastal Metro stop serving Tynemouth and North Shields.",
                nearby_transport=[],
                zone_id=zone_c.id,
            ),
        ]
        db.add_all(locations)

        db.commit()
        print(
            f"Seeded: 4 zones, 4 operators, {len(tickets)} tickets, {len(locations)} locations."
        )

    except Exception as exc:
        db.rollback()
        print(f"Seeding failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
