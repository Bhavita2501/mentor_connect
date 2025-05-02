# Import blueprints directly
from .main import main
from .auth import auth
from .profile import profile
from .booking import booking
from .payment import payment

# Make blueprints available for import
__all__ = ['main', 'auth', 'profile', 'booking', 'payment']