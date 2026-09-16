from decimal import Decimal
from uuid import uuid4

from app.core.base_service import BaseService
from app.core.errors import (
    NotFoundError,
    ValidationError
)

from app.core.base_model import utc_now
from app.donations.models import Donation, DonationStatus

from app.donations.repository import DonationRepository
from app.donations.gateway import (
    PaymentGateway,
    CheckoutCreationError,
    WebhookVerificationError
)

class DonationService(BaseService):

    repository = DonationRepository

    @classmethod
    def generate_reference(cls):

        """
            Generate an internal KCAP donation reference.
            kcap-don-12334asdad
        """

        while True:

            reference = (
                f"KCAP-DON-"
                f"{uuid4().hex[:8].upper()}"
            )

            if not cls.repository.reference_exists(
                reference
            ):
                return reference

    @classmethod
    def create_donation(
        cls,
        data
    ):
        
        """
            create donation local before contacting the any payment provider
        """

        amount = Decimal(
            str(data["amount"])
        )

        if amount <=0:
            raise ValidationError(
                "Donation amount must be "
                "greater than zero"
            )
        
        donation = Donation(
            reference = cls.generate_reference(),

            donor_name = data.get(
                "donor_name"
            ),
            donor_email = data.get(
                "donor_email"
            ),

            donor_phone = data.get(
                "donor_phone"
            ),
            amount=amount,

            currency = (
                data.get(
                    "currency",
                    "ZAR"
                ).upper()
            ),
            purpose=data.get(
                "purpose"
            ),
            message = data.get(
                "message"
            ),
            is_anonymous = data.get(
                "is_anonymous",
                False
            ),
            status= DonationStatus.PENDING

        )

        return cls.repository.add(donation)

    @classmethod
    def start_checkout(
        cls,
        *,
        donation,
        gateway: PaymentGateway,
        success_url,
        cancel_url
    ):
        if donation.is_successful:

            raise ValidationError(
                "This donation has already been paid."
            )
        if donation.is_refunded:

            raise ValidationError(
                "A refunded donation cannot"
                "start another checkout"
            )
        
        try:
            checkout = (
                gateway.create_checkout(
                    reference=donation.reference,
                    amount=donation.amount,
                    currency=donation.currency,
                    donor_email=(
                        donation.donor_email
                    ),
                    donor_name=(
                        donation.donor_name
                    ),
                    success_url=success_url,
                    cancel_url=cancel_url
                )
            )

        except Exception as error:

            if isinstance(
                error,
                CheckoutCreationError
            ):
                
                raise
            raise CheckoutCreationError(
                "Unable to create payment"
                "checkout"
            ) from error

        donation.provider = (
            checkout.provider
        )

        donation.provider_session_reference = (
            checkout.session_reference
        )

        donation.provider_reference = (
            checkout.payment_reference
        )

        donation.status = (
            DonationStatus.PROCEESSING
        )

        cls.repository.save(
            donation
        )

        return checkout
    
    @classmethod
    def create_and_start_checkout(
        cls,
        *,
        data,
        gateway:PaymentGateway,
        success_url,
        cancel_url
    ):
        
        donation = (
            cls.create_donation(
                data
            )
        )

        checkout = (
            cls.start_checkout(
                donation=donation,
                gateway=gateway,
                success_url=success_url,
                cancel_url=cancel_url
            )
        )

        return donation, checkout

    @classmethod
    def get_by_reference(cls, reference):
        donation = (
            cls.repository.get_by_reference(
                reference
            )
        )

        if not donation:
            raise NotFoundError(
                "Donation not found."
            )
        return donation
    
    @classmethod
    def get_by_procider_reference(cls, provider_reference):

        donation = (
            cls.repository.get_by_provider_reference(
                provider_reference
            )
        )

        if not donation:
            raise NotFoundError(
                "Donation not found..."
            )
        
        return donation
    

    @classmethod
    def get_by_session_reference(cls, session_reference):

        donation = (
            cls.repository.get_by_provider_session_reference(
                session_reference
            )
        )


        if not donation:
            raise NotFoundError(
                "Donation not found..."
            )
        
        return donation
    
    @classmethod
    def process_webhook(
        cls,
        *,
        gateway: PaymentGateway,
        payload: bytes,
        headers:dict
    ):
        
        try:
            verification = (
                gateway.verify_webhook(
                    payload=payload,
                    headers=headers
                )
            )
        except WebhookVerificationError:
            raise

        if not verification.verified:

            raise WebhookVerificationError(
                "Payment webhook could not"
                "be verified."
            )
        
        donation = (
            cls._find_donation_from_verification(
                verification
            )
        )

        cls._validate_payment_amount(
            donation=donation,
            verification=verification
        )

        cls._apply_payment_status(
            donation=donation,
            verification=verification
        )

        cls.repository.save(
            donation
        )

        return donation
    

    @classmethod
    def _find_donation_from_verification(cls, verification):

        donation = None

        if verification.payement_reference:
            donation = (
                cls.repository.get_by_provider_reference(
                    verification.payment_reference
                )
            )
        
        if (
            donation in None and verification.session_reference
        ):
            donation = (
                cls.repository.get_by_provider_session_reference(
                    verification.session_reference
                )
            )

        if donation in None:

            raise NotFoundError(
                " No Donation matches this payment transaction."
            )
        
        return donation
    

    @classmethod
    def _validate_payment_amount(
        cls,
        *,
        donation,
        verification
    ):
        if verification.amount is not None:
            if Decimal(
                str(
                    verification.amount
                )
            ) != Decimal(
                str(donation.amount)
            ):
                raise ValidationError(
                    "Payment amount does not"
                    "match the donation"
                )
            
        if verification.currency:

            if(
                verification.currency.upper() != donation.currency.upper()
            ):
                
                raise ValidationError(
                    "Payment Currency does not "
                    "match the donation."
                )
            
    @classmethod
    def _apply_payment_status(
        cls,
        *,
        donation,
        verification
    ):
        
        status = (
            verification.status.strip().lower()
        )

        if status == "successful":

            donation.status = (
                DonationStatus.SUCCESSFUL
            )

            donation.paid_at = (
                donation.paid_at or utc_now()
            )

            if (
                verification.payment_reference
            ):
                donation.provider_reference = (
                    verification.payment_reference
                )
                return 
        
        if status == "processing":
            donation.status = (
                DonationStatus.PROCEESSING
            )

            return
        
        if status == "failed":
            donation.status = (
                DonationStatus.FAILED
            )

            donation.failed_at = ( utc_now )

            return
        
        if status == "cancelled":

            donation.status = (
                DonationStatus.CANCELLED
            )

            donation.cancelled_at = (
                utc_now()
            )

            return
        
        if status == "refunded":
            donation.status = (
                DonationStatus.REFUNDED
            )

            donation.refunded_at = (
                utc_now()
            )

            return 
        
        raise ValidationError(
            f"Unsupported payment status : "
            f"{status}"
        )

