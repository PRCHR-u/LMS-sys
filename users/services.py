import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    """
    Creates a product in Stripe.
    """
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(product_id, amount):
    """
    Creates a price for a product in Stripe.
    """
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # Convert to cents
        currency="usd",
    )
    return price


def create_stripe_session(price_id):
    """
    Creates a checkout session in Stripe and returns the payment link.
    """
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session
