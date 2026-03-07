from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv(Path(__file__).parent.parent / ".env")

from payments_py import Payments, PaymentOptions

payments = Payments(PaymentOptions(
    nvm_api_key=os.getenv("NVM_API_KEY"),
    environment="sandbox"
))

ADAGENT_PLAN_ID = "43955667645714568092057142565359274237259428265532767327265493246604990476175"
ADAGENT_AGENT_ID = "23914165245228865506529334228547597361447900285168247629778996230188006229083"

result = payments.x402.get_x402_access_token(
    plan_id=ADAGENT_PLAN_ID,
    agent_id=ADAGENT_AGENT_ID
)
print(result)
