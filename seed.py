from app import app
from models import db
from models.category import Category
from models.product import Product


categories = [
    ("Dresses", "dresses"),
    ("Tops", "tops"),
    ("Bottoms", "bottoms"),
    ("Jackets", "jackets"),
    ("Shirts", "shirts"),
    ("Accessories", "accessories"),
]


products = [
    {
        "name": "Vintage Denim Jacket",
        "slug": "vintage-denim-jacket",
        "description": "Classic blue denim jacket with a relaxed vintage fit.",
        "price": 699,
        "original_price": 1499,
        "size": "M",
        "brand": "Roadster",
        "condition": "Excellent",
        "stock": 3,
        "image_url": "vintage-denim-jacket.jpg",
        "category": "Jackets",
    },
    {
        "name": "Oversized Graphic Tee",
        "slug": "oversized-graphic-tee",
        "description": "Comfortable oversized graphic t-shirt with a streetwear look.",
        "price": 399,
        "original_price": 899,
        "size": "L",
        "brand": "H&M",
        "condition": "Very Good",
        "stock": 5,
        "image_url": "oversized-graphic-tee.jpg",
        "category": "Tops",
    },
    {
        "name": "Brown Corduroy Pants",
        "slug": "brown-corduroy-pants",
        "description": "Retro-inspired brown corduroy pants with a comfortable fit.",
        "price": 599,
        "original_price": 1299,
        "size": "M",
        "brand": "Zara",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "brown-corduroy-pants.jpg",
        "category": "Bottoms",
    },
    {
        "name": "Floral Midi Dress",
        "slug": "floral-midi-dress",
        "description": "Elegant floral midi dress perfect for casual outings.",
        "price": 749,
        "original_price": 1699,
        "size": "S",
        "brand": "ONLY",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "floral-midi-dress.jpg",
        "category": "Dresses",
    },
    {
        "name": "Classic White Shirt",
        "slug": "classic-white-shirt",
        "description": "Minimal white button-down shirt with a timeless silhouette.",
        "price": 499,
        "original_price": 999,
        "size": "M",
        "brand": "Uniqlo",
        "condition": "Very Good",
        "stock": 4,
        "image_url": "classic-white-shirt.jpg",
        "category": "Shirts",
    },
    {
        "name": "Y2K Ribbed Crop Top",
        "slug": "y2k-ribbed-crop-top",
        "description": "Trendy ribbed crop top inspired by early 2000s fashion.",
        "price": 299,
        "original_price": 699,
        "size": "S",
        "brand": "Forever 21",
        "condition": "Excellent",
        "stock": 5,
        "image_url": "y2k-ribbed-crop-top.jpg",
        "category": "Tops",
    },
    {
        "name": "Black Straight Fit Jeans",
        "slug": "black-straight-fit-jeans",
        "description": "Versatile black straight-fit jeans for everyday wear.",
        "price": 649,
        "original_price": 1399,
        "size": "M",
        "brand": "Levis",
        "condition": "Very Good",
        "stock": 3,
        "image_url": "black-straight-fit-jeans.jpg",
        "category": "Bottoms",
    },
    {
        "name": "Beige Oversized Blazer",
        "slug": "beige-oversized-blazer",
        "description": "Sophisticated oversized blazer in a neutral beige shade.",
        "price": 899,
        "original_price": 2199,
        "size": "M",
        "brand": "Zara",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "beige-oversized-blazer.jpg",
        "category": "Jackets",
    },
    {
        "name": "Striped Casual Shirt",
        "slug": "striped-casual-shirt",
        "description": "Relaxed striped shirt that works perfectly with denim.",
        "price": 449,
        "original_price": 999,
        "size": "L",
        "brand": "Westside",
        "condition": "Very Good",
        "stock": 4,
        "image_url": "striped-casual-shirt.jpg",
        "category": "Shirts",
    },
    {
        "name": "Vintage Floral Skirt",
        "slug": "vintage-floral-skirt",
        "description": "Flowy floral skirt with a charming vintage aesthetic.",
        "price": 499,
        "original_price": 1099,
        "size": "S",
        "brand": "Forever New",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "vintage-floral-skirt.jpg",
        "category": "Bottoms",
    },
    {
        "name": "Black Slip Dress",
        "slug": "black-slip-dress",
        "description": "Elegant black slip dress with a simple minimalist design.",
        "price": 699,
        "original_price": 1499,
        "size": "S",
        "brand": "Mango",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "black-slip-dress.jpg",
        "category": "Dresses",
    },
    {
        "name": "Pastel Knit Cardigan",
        "slug": "pastel-knit-cardigan",
        "description": "Soft pastel cardigan perfect for layering.",
        "price": 599,
        "original_price": 1299,
        "size": "M",
        "brand": "H&M",
        "condition": "Very Good",
        "stock": 3,
        "image_url": "pastel-knit-cardigan.jpg",
        "category": "Jackets",
    },
    {
        "name": "Graphic Streetwear Tee",
        "slug": "graphic-streetwear-tee",
        "description": "Bold graphic tee inspired by modern streetwear.",
        "price": 349,
        "original_price": 799,
        "size": "L",
        "brand": "Urbanic",
        "condition": "Excellent",
        "stock": 5,
        "image_url": "graphic-streetwear-tee.jpg",
        "category": "Tops",
    },
    {
        "name": "High-Waisted Blue Jeans",
        "slug": "high-waisted-blue-jeans",
        "description": "Classic high-waisted blue jeans with a flattering fit.",
        "price": 649,
        "original_price": 1399,
        "size": "S",
        "brand": "Levis",
        "condition": "Very Good",
        "stock": 3,
        "image_url": "high-waisted-blue-jeans.jpg",
        "category": "Bottoms",
    },
    {
        "name": "Checked Overshirt",
        "slug": "checked-overshirt",
        "description": "Warm checked overshirt that adds a relaxed layered look.",
        "price": 549,
        "original_price": 1199,
        "size": "L",
        "brand": "Roadster",
        "condition": "Excellent",
        "stock": 4,
        "image_url": "checked-overshirt.jpg",
        "category": "Shirts",
    },
    {
        "name": "Satin Party Dress",
        "slug": "satin-party-dress",
        "description": "Elegant satin dress suitable for parties and special occasions.",
        "price": 799,
        "original_price": 1799,
        "size": "M",
        "brand": "Mango",
        "condition": "Excellent",
        "stock": 2,
        "image_url": "satin-party-dress.jpg",
        "category": "Dresses",
    },
    {
        "name": "Cropped Denim Jacket",
        "slug": "cropped-denim-jacket",
        "description": "Trendy cropped denim jacket with a modern silhouette.",
        "price": 649,
        "original_price": 1499,
        "size": "S",
        "brand": "ONLY",
        "condition": "Very Good",
        "stock": 3,
        "image_url": "cropped-denim-jacket.jpg",
        "category": "Jackets",
    },
    {
        "name": "Minimal Black Tee",
        "slug": "minimal-black-tee",
        "description": "Simple black t-shirt that belongs in every wardrobe.",
        "price": 299,
        "original_price": 599,
        "size": "M",
        "brand": "H&M",
        "condition": "Excellent",
        "stock": 6,
        "image_url": "minimal-black-tee.jpg",
        "category": "Tops",
    },
    {
        "name": "Vintage Denim Skirt",
        "slug": "vintage-denim-skirt",
        "description": "Classic denim skirt with a vintage-inspired wash.",
        "price": 449,
        "original_price": 999,
        "size": "S",
        "brand": "Levis",
        "condition": "Very Good",
        "stock": 2,
        "image_url": "vintage-denim-skirt.jpg",
        "category": "Bottoms",
    },
    {
        "name": "Canvas Tote Bag",
        "slug": "canvas-tote-bag",
        "description": "Reusable canvas tote bag for everyday essentials.",
        "price": 249,
        "original_price": 499,
        "size": "One Size",
        "brand": "ReWear",
        "condition": "Excellent",
        "stock": 8,
        "image_url": "canvas-tote-bag.jpg",
        "category": "Accessories",
    },
]


def seed_database():

    with app.app_context():

        Product.query.delete()
        Category.query.delete()

        db.session.commit()

        category_objects = {}

        for name, slug in categories:

            category = Category(
                name=name,
                slug=slug
            )

            db.session.add(category)

            category_objects[name] = category

        db.session.commit()

        for product_data in products:

            category_name = product_data.pop("category")

            product = Product(
                **product_data,
                category=category_objects[category_name]
            )

            db.session.add(product)

        db.session.commit()

        print("Database seeded successfully!")
        print(f"Added {len(categories)} categories")
        print(f"Added {len(products)} products")


if __name__ == "__main__":
    seed_database()