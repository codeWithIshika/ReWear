from flask import Flask, render_template

from flask_login import LoginManager

from config import Config
from models import db

from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order, OrderItem
from models.wishlist import Wishlist, WishlistItem

from routes.shop import shop_bp
from routes.cart import cart_bp
from routes.wishlist import wishlist_bp
from routes.auth import auth_bp
from routes.checkout import checkout_bp
from routes.admin import admin_bp
from routes.orders import orders_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)


    # =========================
    # DATABASE
    # =========================

    db.init_app(app)


    # =========================
    # LOGIN MANAGER
    # =========================

    login_manager = LoginManager()

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"


    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))


    # =========================
    # CREATE DATABASE TABLES
    # =========================

    with app.app_context():

        db.create_all()


    # =========================
    # BLUEPRINTS
    # =========================

    app.register_blueprint(shop_bp)

    app.register_blueprint(cart_bp)

    app.register_blueprint(wishlist_bp)

    app.register_blueprint(auth_bp)

    app.register_blueprint(checkout_bp)

    app.register_blueprint(admin_bp)

    app.register_blueprint(orders_bp)


    # =========================
    # HOME
    # =========================

    @app.route("/")
    def home():

        featured_products = Product.query.limit(4).all()

        return render_template(
            "home.html",
            featured_products=featured_products
        )


    # =========================
    # ABOUT US
    # =========================

    @app.route("/about")
    def about():

        return render_template(
            "info.html",
            title="About Us",
            subtitle="Discover the story behind ReWear.",
            page="about"
        )


    # =========================
    # CONTACT
    # =========================

    @app.route("/contact")
    def contact():

        return render_template(
            "info.html",
            title="Contact Us",
            subtitle="We're here to help.",
            page="contact"
        )


    # =========================
    # SHIPPING
    # =========================

    @app.route("/shipping")
    def shipping():

        return render_template(
            "info.html",
            title="Shipping",
            subtitle="Everything you need to know about delivery.",
            page="shipping"
        )


    # =========================
    # RETURNS
    # =========================

    @app.route("/returns")
    def returns():

        return render_template(
            "info.html",
            title="Returns & Exchanges",
            subtitle="Need to return something? Here's how.",
            page="returns"
        )


    # =========================
    # FAQ
    # =========================

    @app.route("/faq")
    def faq():

        return render_template(
            "info.html",
            title="Frequently Asked Questions",
            subtitle="Quick answers to common questions.",
            page="faq"
        )


    # =========================
    # SUSTAINABILITY
    # =========================

    @app.route("/sustainability")
    def sustainability():

        return render_template(
            "info.html",
            title="Sustainability",
            subtitle="Fashion that gives existing clothes another life.",
            page="sustainability"
        )


    # =========================
    # OUR STORY
    # =========================

    @app.route("/our-story")
    def our_story():

        return render_template(
            "info.html",
            title="Our Story",
            subtitle="How ReWear came to life.",
            page="story"
        )


    return app


app = create_app()


if __name__ == "__main__":

    app.run(debug=True)