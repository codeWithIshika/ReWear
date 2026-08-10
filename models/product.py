from models import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=True)

    size = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    condition = db.Column(db.String(100), nullable=False)

    stock = db.Column(db.Integer, default=0, nullable=False)

    image_url = db.Column(db.String(500), nullable=True)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    category = db.relationship(
        "Category",
        back_populates="products"
    )

    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )

    wishlist_items = db.relationship(
        "WishlistItem",
        back_populates="product"
    )

    def __repr__(self):
        return f"<Product {self.name}>"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = (
                (self.original_price - self.price)
                / self.original_price
            ) * 100

            return round(discount)

        return 0