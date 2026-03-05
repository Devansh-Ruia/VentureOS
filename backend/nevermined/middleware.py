"""FastAPI middleware for Nevermined payment validation."""
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nevermined.seller import get_payments_instance


class NeverminedPaymentMiddleware(BaseHTTPMiddleware):
    """Validates payment-signature header for protected endpoints."""
    
    async def dispatch(self, request: Request, call_next):
        # Only protect /api/run endpoint
        if request.url.path != "/api/run" or request.method != "POST":
            return await call_next(request)
        
        agent_id = os.getenv("NVM_AGENT_ID")
        plan_id = os.getenv("NVM_PLAN_ID")
        
        # If Nevermined not configured, allow unauthenticated access
        if not agent_id or not plan_id:
            return await call_next(request)
        
        # Check for payment signature
        payment_signature = request.headers.get("payment-signature")
        
        if not payment_signature:
            return JSONResponse(
                status_code=402,
                content={"error": "Payment required", "plan_id": plan_id}
            )
        
        # Validate access token
        try:
            payments = get_payments_instance()
            valid = payments.ai_query_api.validate_access_token(
                access_token=payment_signature,
                agent_id=agent_id
            )
            
            if not valid:
                return JSONResponse(
                    status_code=402,
                    content={"error": "Invalid payment signature", "plan_id": plan_id}
                )
            
            # Process request
            response = await call_next(request)
            
            # Burn credits after successful response
            try:
                payments.ai_query_api.burn_credits(
                    access_token=payment_signature,
                    credits_used=1,
                    agent_id=agent_id
                )
            except Exception as e:
                print(f"Credit burn error: {e}")
            
            return response
            
        except Exception as e:
            print(f"Payment validation error: {e}")
            return JSONResponse(
                status_code=402,
                content={"error": "Payment validation failed", "plan_id": plan_id}
            )
