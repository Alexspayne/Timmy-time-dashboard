"""Lightning invoice creation and payment verification.

Provides a mock implementation that will be replaced with real LND gRPC
calls in the roadmap's "Real Lightning" milestone.  The mock allows the
full L402 flow to be tested end-to-end without a running Lightning node.

When LIGHTNING_BACKEND=lnd is set in the environment, the handler will
attempt to connect to a local LND instance via gRPC.
"""

import hashlib
import hmac
import logging
import os
import secrets
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

# Secret key for HMAC-based invoice verification (mock mode)
_HMAC_SECRET_DEFAULT = "timmy-sovereign-sats"
_HMAC_SECRET_RAW = os.environ.get("L402_HMAC_SECRET", _HMAC_SECRET_DEFAULT)
_HMAC_SECRET = _HMAC_SECRET_RAW.encode()

if _HMAC_SECRET_RAW == _HMAC_SECRET_DEFAULT:
    logger.warning(
        "SEC: L402_HMAC_SECRET is using the default value — set a unique "
        "secret in .env before deploying to production."
    )


@dataclass
class Invoice:
    payment_hash: str
    payment_request: str  # bolt11 invoice string
    amount_sats: int
    memo: str = ""
    created_at: float = field(default_factory=time.time)
    settled: bool = False
    preimage: Optional[str] = None


class PaymentHandler:
    """Creates and verifies Lightning invoices.

    Currently uses a mock implementation.  The interface is designed to
    be a drop-in replacement for real LND gRPC calls.
    """

    def __init__(self) -> None:
        self._invoices: dict[str, Invoice] = {}
        self._backend = os.environ.get("LIGHTNING_BACKEND", "mock")
        logger.info("PaymentHandler initialized — backend: %s", self._backend)

    def create_invoice(self, amount_sats: int, memo: str = "") -> Invoice:
        """Create a new Lightning invoice."""
        preimage = secrets.token_hex(32)
        payment_hash = hashlib.sha256(bytes.fromhex(preimage)).hexdigest()

        # Mock bolt11 — in production this comes from LND
        payment_request = (
            f"lnbc{amount_sats}n1mock"
            f"{hmac.new(_HMAC_SECRET, payment_hash.encode(), hashlib.sha256).hexdigest()[:20]}"
        )

        invoice = Invoice(
            payment_hash=payment_hash,
            payment_request=payment_request,
            amount_sats=amount_sats,
            memo=memo,
            preimage=preimage,
        )
        self._invoices[payment_hash] = invoice
        logger.info(
            "Invoice created: %d sats — %s (hash: %s…)",
            amount_sats, memo, payment_hash[:12],
        )
        return invoice

    def check_payment(self, payment_hash: str) -> bool:
        """Check whether an invoice has been paid.

        In mock mode, invoices are auto-settled after creation.
        In production, this queries LND for the invoice state.
        """
        invoice = self._invoices.get(payment_hash)
        if invoice is None:
            return False

        if self._backend == "mock":
            # Auto-settle in mock mode for development
            invoice.settled = True
            return True

        # TODO: Real LND gRPC lookup
        return invoice.settled

    def settle_invoice(self, payment_hash: str, preimage: str) -> bool:
        """Manually settle an invoice with a preimage (for testing)."""
        invoice = self._invoices.get(payment_hash)
        if invoice is None:
            return False
        expected = hashlib.sha256(bytes.fromhex(preimage)).hexdigest()
        if expected != payment_hash:
            logger.warning("Preimage mismatch for invoice %s", payment_hash[:12])
            return False
        invoice.settled = True
        invoice.preimage = preimage
        return True

    def get_invoice(self, payment_hash: str) -> Optional[Invoice]:
        return self._invoices.get(payment_hash)

    def list_invoices(self, settled_only: bool = False) -> list[Invoice]:
        invoices = list(self._invoices.values())
        if settled_only:
            return [i for i in invoices if i.settled]
        return invoices


# Module-level singleton
payment_handler = PaymentHandler()
