from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import login_required, current_user

from models import db
from models.product import Product
from models.order import Order, OrderItem

import uuid


checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():

    cart_items = session.get("cart", {})

    if not cart_items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.cart"))


    items = []
    subtotal = 0


    for product_id, quantity in cart_items.items():

        product = Product.query.get(int(product_id))

        if product:

            item_total = product.price * quantity

            items.append({
                "product": product,
                "quantity": quantity,
                "item_total": item_total
            })

            subtotal += item_total


    shipping = 0 if subtotal >= 999 else 49
    total = subtotal + shipping


    if request.method == "POST":

        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        pincode = request.form.get("pincode")


        order_number = "RW-" + uuid.uuid4().hex[:8].upper()


        order = Order(
            order_number=order_number,
            user_id=current_user.id,
            total_amount=total,
            shipping_fee=shipping,
            status="Pending",
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )


        db.session.add(order)


        for item in items:

            order_item = OrderItem(
                order=order,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
            )

            db.session.add(order_item)

            item["product"].stock -= item["quantity"]


        db.session.commit()


        session["cart"] = {}
        session.modified = True


        return redirect(
            url_for(
                "checkout.order_success",
                order_number=order_number
            )
        )


    return render_template(
        "checkout.html",
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        total=total
    )


@checkout_bp.route("/order-success/<order_number>")
@login_required
def order_success(order_number):

    order = Order.query.filter_by(
        order_number=order_number,
        user_id=current_user.id
    ).first_or_404()


    return render_template(
        "order_success.html",
        order=order
    )