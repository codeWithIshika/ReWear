from app import create_app
from models import db
from models.user import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(
        email="admin@rewear.com"
    ).first()

    if user:
        user.is_admin = True
    else:
        user = User(
            name="ReWear Admin",
            email="admin@rewear.com",
            is_admin=True
        )

        user.set_password("Admin@123")

        db.session.add(user)

    db.session.commit()

    print("Admin account ready!")