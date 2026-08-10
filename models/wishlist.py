from models import db


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="wishlist"
    )

    items = db.relationship(
        "WishlistItem",
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Wishlist User {self.user_id}>"


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey("wishlists.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    wishlist = db.relationship(
        "Wishlist",
        back_populates="items"
    )

    product = db.relationship(
        "Product",
        back_populates="wishlist_items"
    )

    def __repr__(self):
        return f"<WishlistItem {self.id}>"