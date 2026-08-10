from flask import Blueprint, render_template, request

from models.product import Product


shop_bp = Blueprint("shop", __name__)


# =====================================================
# SHOP + SEARCH + CATEGORY FILTER
# =====================================================

@shop_bp.route("/shop")
def shop():

    category_name = request.args.get("category")
    search_query = request.args.get("search", "").strip()


    # Start query
    query = Product.query


    # CATEGORY FILTER
    if category_name:

        query = (
            query
            .join(Product.category)
            .filter(Product.category.has(name=category_name))
        )


    # SEARCH FILTER
    if search_query:

        search_text = f"%{search_query}%"

        query = query.filter(
            Product.name.ilike(search_text)
            |
            Product.brand.ilike(search_text)
        )


    products = query.all()


    return render_template(
        "shop.html",
        products=products,
        selected_category=category_name,
        search_query=search_query
    )


# =====================================================
# PRODUCT DETAILS
# =====================================================

@shop_bp.route("/product/<int:product_id>")
def product_details(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        "product_details.html",
        product=product
    )