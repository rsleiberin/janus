from backend import create_app
from backend.models import db, User, Admin, Log, Analytics, Security

app = create_app()

with app.app_context():
    # Add sample users
    user1 = User(username="john_doe", email="john@example.com", password_hash="hashedpassword1", role="user")
    user2 = User(username="admin_user", email="admin@example.com", password_hash="hashedpassword2", role="admin")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Add admins
    admin1 = Admin(user_id=user2.id, admin_level="superadmin")
    db.session.add(admin1)
    db.session.commit()

    # Add logs
    log1 = Log(action="Logged in", user_id=user1.id)
    db.session.add(log1)
    db.session.commit()

    # Add analytics data
    analytics1 = Analytics(data={"metric": "value1"})
    db.session.add(analytics1)
    db.session.commit()

    # Add security events
    security1 = Security(user_id=user1.id, action="Failed login attempt")
    db.session.add(security1)
    db.session.commit()

    print("Seed data inserted successfully!")
