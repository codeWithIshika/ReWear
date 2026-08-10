from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from models.product import Product


cart_bp = Blueprint("cart", __name__)


# =========================
# VIEW CART
# =========================

@cart_bp.route("/cart")
def cart():

    cart_items = session.get("cart", {})

    items = []
    subtotal = 0

    for product_id, quantity in cart_items.items():

        product = Product.query.get(int(product_id))

        if not product:
            continue

        # Make sure quantity is valid
        quantity = int(quantity)

        # Prevent cart quantity from exceeding stock
        if quantity > product.stock:
            quantity = product.stock

            cart_items[str(product.id)] = quantity

        if quantity <= 0:
            continue

        item_total = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total
        })

        subtotal += item_total


    # Save corrected cart
    session["cart"] = cart_items
    session.modified = True


    # Free shipping above ₹999
    if subtotal == 0:
        shipping = 0

    elif subtotal >= 999:
        shipping = 0

    else:
        shipping = 49


    total = subtotal + shipping


    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )


# =========================
# ADD TO CART
# =========================

@cart_bp.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    # Check stock
    if product.stock <= 0:

        flash(
            "Sorry, this product is out of stock.",
            "error"
        )

        return redirect(
            url_for("shop.product_details",
                    product_id=product.id)
        )


    cart = session.get("cart", {})

    product_id = str(product_id)

    current_quantity = int(
        cart.get(product_id, 0)
    )


    # Don't allow quantity above stock
    if current_quantity < product.stock:

        cart[product_id] = current_quantity + 1

        session["cart"] = cart
        session.modified = True

        flash(
            f"{product.name} added to your cart!",
            "success"
        )

    else:

        flash(
            f"Only {product.stock} item(s) available.",
            "error"
        )


    return redirect(
        url_for("cart.cart")
    )


# =========================
# INCREASE QUANTITY
# =========================

@cart_bp.route("/cart/increase/<int:product_id>")
def increase_quantity(product_id):

    product = Product.query.get_or_404(product_id)

    cart = session.get("cart", {})

    product_id = str(product_id)

    current_quantity = int(
        cart.get(product_id, 0)
    )


    if current_quantity < product.stock:

        cart[product_id] = current_quantity + 1

        session["cart"] = cart
        session.modified = True

    else:

        flash(
            "You cannot add more than the available stock.",
            "error"
        )


    return redirect(
        url_for("cart.cart")
    )


# =========================
# DECREASE QUANTITY
# =========================

@cart_bp.route("/cart/decrease/<int:product_id>")
def decrease_quantity(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)


    if product_id in cart:

        current_quantity = int(
            cart[product_id]
        )


        if current_quantity > 1:

            cart[product_id] = current_quantity - 1

        else:

            del cart[product_id]


        session["cart"] = cart
        session.modified = True


    return redirect(
        url_for("cart.cart")
    )


# =========================
# REMOVE FROM CART
# =========================

@cart_bp.route("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)


    if product_id in cart:

        del cart[product_id]

        session["cart"] = cart
        session.modified = True

        flash(
            "Product removed from cart.",
            "success"
        )


    return redirect(
        url_for("cart.cart")
    )


# =========================
# CLEAR CART
# =========================

@cart_bp.route("/cart/clear")
def clear_cart():

    session["cart"] = {}

    session.modified = True

    flash(
        "Your cart has been cleared.",
        "success"
    )

    return redirect(
        url_for("cart.cart")
    )