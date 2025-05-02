from app import create_app, db
from app.models.user import Skill

def init_database():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Insert default skills
        Skill.insert_default_skills()
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()