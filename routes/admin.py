from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import login_required, current_user

from models import db
from models.product import Product
from models.category import Category
from models.order import Order
from models.user import User


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================================
# ADMIN PROTECTION
# ==========================================

def admin_required():

    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    if not current_user.is_admin:
        flash(
            "You do not have permission to access the admin area.",
            "error"
        )

        return redirect(url_for("home"))

    return None


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin_bp.route("/")
@login_required
def dashboard():

    protection = admin_required()

    if protection:
        return protection

    total_products = Product.query.count()

    total_users = User.query.count()

    total_orders = Order.query.count()

    total_revenue = db.session.query(
        db.func.sum(Order.total_amount)
    ).scalar() or 0

    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders
    )


# ==========================================
# PRODUCTS
# ==========================================

@admin_bp.route("/products")
@login_required
def products():

    protection = admin_required()

    if protection:
        return protection

    products = Product.query.order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "admin/products.html",
        products=products
    )


# ==========================================
# ADD PRODUCT
# ==========================================

@admin_bp.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    protection = admin_required()

    if protection:
        return protection

    categories = Category.query.all()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get(
            "description",
            ""
        ).strip()

        category_id = request.form.get(
            "category_id"
        )

        price = request.form.get("price")
        original_price = request.form.get(
            "original_price"
        )

        size = request.form.get(
            "size",
            ""
        ).strip()

        brand = request.form.get(
            "brand",
            ""
        ).strip()

        condition = request.form.get(
            "condition",
            ""
        ).strip()

        stock = request.form.get("stock")

        image_url = request.form.get(
            "image_url",
            ""
        ).strip()


        # Basic validation

        if not name or not price or not category_id:

            flash(
                "Please fill all required fields.",
                "error"
            )

            return render_template(
                "admin/add_product.html",
                categories=categories
            )


        try:

            price = float(price)

            original_price = (
                float(original_price)
                if original_price
                else None
            )

            stock = int(stock or 0)

            category_id = int(category_id)

        except ValueError:

            flash(
                "Please enter valid numeric values.",
                "error"
            )

            return render_template(
                "admin/add_product.html",
                categories=categories
            )


        product = Product(

            name=name,

            description=description,

            category_id=category_id,

            price=price,

            original_price=original_price,

            size=size,

            brand=brand,

            condition=condition,

            stock=stock,

            image_url=image_url
        )


        db.session.add(product)

        db.session.commit()


        flash(
            "Product added successfully!",
            "success"
        )

        return redirect(
            url_for("admin.products")
        )


    return render_template(
        "admin/add_product.html",
        categories=categories
    )


# ==========================================
# EDIT PRODUCT
# ==========================================

@admin_bp.route(
    "/products/edit/<int:product_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(product_id):

    protection = admin_required()

    if protection:
        return protection

    product = Product.query.get_or_404(
        product_id
    )

    categories = Category.query.all()


    if request.method == "POST":

        product.name = request.form.get(
            "name",
            ""
        ).strip()

        product.description = request.form.get(
            "description",
            ""
        ).strip()

        product.category_id = int(
            request.form.get("category_id")
        )

        product.price = float(
            request.form.get("price")
        )

        original_price = request.form.get(
            "original_price"
        )

        product.original_price = (
            float(original_price)
            if original_price
            else None
        )

        product.size = request.form.get(
            "size",
            ""
        ).strip()

        product.brand = request.form.get(
            "brand",
            ""
        ).strip()

        product.condition = request.form.get(
            "condition",
            ""
        ).strip()

        product.stock = int(
            request.form.get("stock", 0)
        )

        product.image_url = request.form.get(
            "image_url",
            ""
        ).strip()


        db.session.commit()


        flash(
            "Product updated successfully!",
            "success"
        )

        return redirect(
            url_for("admin.products")
        )


    return render_template(
        "admin/edit_product.html",
        product=product,
        categories=categories
    )


# ==========================================
# DELETE PRODUCT
# ==========================================

@admin_bp.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
@login_required
def delete_product(product_id):

    protection = admin_required()

    if protection:
        return protection

    product = Product.query.get_or_404(
        product_id
    )


    db.session.delete(product)

    db.session.commit()


    flash(
        "Product deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.products")
    )


# ==========================================
# ORDERS
# ==========================================

@admin_bp.route("/orders")
@login_required
def orders():

    protection = admin_required()

    if protection:
        return protection

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin/orders.html",
        orders=orders
    )


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@admin_bp.route(
    "/orders/<int:order_id>/status",
    methods=["POST"]
)
@login_required
def update_order_status(order_id):

    protection = admin_required()

    if protection:
        return protection

    order = Order.query.get_or_404(
        order_id
    )

    status = request.form.get(
        "status"
    )

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:

        flash(
            "Invalid order status.",
            "error"
        )

        return redirect(
            url_for("admin.orders")
        )


    order.status = status

    db.session.commit()


    flash(
        "Order status updated.",
        "success"
    )

    return redirect(
        url_for("admin.orders")
    )


# ==========================================
# USERS
# ==========================================

@admin_bp.route("/users")
@login_required
def users():

    protection = admin_required()

    if protection:
        return protection

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )