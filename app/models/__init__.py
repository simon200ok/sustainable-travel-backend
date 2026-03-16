# Import all models so SQLAlchemy registers them with Base.metadata
# before create_all() is called in main.py
from app.models.user import User
from app.models.zone import Zone
from app.models.location import Location
from app.models.operator import Operator
from app.models.ticket import Ticket
from app.models.favourite import Favourite
from app.models.travel_log import TravelLog

__all__ = ["User", "Zone", "Location", "Operator", "Ticket", "Favourite", "TravelLog"]
