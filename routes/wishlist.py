from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import login_required, current_user

from models import db
from models.product import Product
from models.wishlist import Wishlist, WishlistItem


wishlist_bp = Blueprint("wishlist", __name__)


# =========================
# GET OR CREATE WISHLIST
# =========================

def get_user_wishlist():

    wishlist = Wishlist.query.filter_by(
        user_id=current_user.id
    ).first()

    if not wishlist:

        wishlist = Wishlist(
            user_id=current_user.id
        )

        db.session.add(wishlist)
        db.session.commit()

    return wishlist


# =========================
# VIEW WISHLIST
# =========================

@wishlist_bp.route("/wishlist")
@login_required
def wishlist():

    wishlist = get_user_wishlist()

    return render_template(
        "wishlist.html",
        wishlist=wishlist
    )


# =========================
# ADD TO WISHLIST
# =========================

@wishlist_bp.route(
    "/wishlist/add/<int:product_id>"
)
@login_required
def add_to_wishlist(product_id):

    product = Product.query.get_or_404(product_id)

    wishlist = get_user_wishlist()


    # Check if already in wishlist

    existing_item = WishlistItem.query.filter_by(
        wishlist_id=wishlist.id,
        product_id=product.id
    ).first()


    if existing_item:

        flash(
            "This product is already in your wishlist.",
            "error"
        )

        return redirect(
            url_for(
                "shop.product_details",
                product_id=product.id
            )
        )


    wishlist_item = WishlistItem(
        wishlist_id=wishlist.id,
        product_id=product.id
    )

    db.session.add(wishlist_item)

    db.session.commit()


    flash(
        f"{product.name} added to your wishlist!",
        "success"
    )


    return redirect(
        url_for(
            "shop.product_details",
            product_id=product.id
        )
    )


# =========================
# REMOVE FROM WISHLIST
# =========================

@wishlist_bp.route(
    "/wishlist/remove/<int:product_id>"
)
@login_required
def remove_from_wishlist(product_id):

    wishlist = get_user_wishlist()


    item = WishlistItem.query.filter_by(
        wishlist_id=wishlist.id,
        product_id=product_id
    ).first()


    if item:

        db.session.delete(item)

        db.session.commit()

        flash(
            "Product removed from wishlist.",
            "success"
        )


    return redirect(
        url_for("wishlist.wishlist")
    )


# =========================
# MOVE TO CART
# =========================

@wishlist_bp.route(
    "/wishlist/move-to-cart/<int:product_id>"
)
@login_required
def move_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    wishlist = get_user_wishlist()


    # Check wishlist item

    item = WishlistItem.query.filter_by(
        wishlist_id=wishlist.id,
        product_id=product.id
    ).first()


    if not item:

        flash(
            "Product is not in your wishlist.",
            "error"
        )

        return redirect(
            url_for("wishlist.wishlist")
        )


    # Check stock

    if product.stock <= 0:

        flash(
            "Sorry, this product is currently out of stock.",
            "error"
        )

        return redirect(
            url_for("wishlist.wishlist")
        )


    # Get session cart

    cart = session.get("cart", {})

    product_id_str = str(product.id)

    current_quantity = int(
        cart.get(product_id_str, 0)
    )


    # Add one item to cart

    if current_quantity < product.stock:

        cart[product_id_str] = current_quantity + 1

        session["cart"] = cart
        session.modified = True


        # Remove from wishlist

        db.session.delete(item)

        db.session.commit()


        flash(
            f"{product.name} moved to your cart!",
            "success"
        )

    else:

        flash(
            "You already have the maximum available quantity in your cart.",
            "error"
        )


    return redirect(
        url_for("wishlist.wishlist")
    )