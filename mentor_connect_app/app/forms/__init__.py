# Import form classes directly
from .auth import LoginForm, RegistrationForm
from .profile import ProfileForm, MentorProfileForm
from .booking import BookingForm, SessionFeedbackForm

# Make forms available for import
__all__ = [
    'LoginForm', 
    'RegistrationForm',
    'ProfileForm', 
    'MentorProfileForm',
    'BookingForm', 
    'SessionFeedbackForm'
]