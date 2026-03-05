import os
import stripe


def create_payment_link(product_name: str, price_cents: int) -> dict:
    """
    Create a Stripe payment link in test mode.
    Creates Product, Price, and Payment Link.
    Returns payment link URL and product ID.
    """
    try:
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        product = stripe.Product.create(
            name=product_name,
            description=f"Early access to {product_name}",
        )
        
        price = stripe.Price.create(
            product=product.id,
            unit_amount=price_cents,
            currency="usd",
        )
        
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
        )
        
        return {
            "payment_link_url": payment_link.url,
            "product_id": product.id,
        }
    
    except Exception as e:
        return {"error": str(e)}
