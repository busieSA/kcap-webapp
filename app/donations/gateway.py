from abc import ABC , abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

@dataclass
class CheckoutSession:

    provider: str

    session_reference:str

    payment_reference:str | None

    checkout_url:str

    raw_data: dict[str, Any] | None=None


@dataclass
class PaymentVerification:

    provider:str

    verified: bool
    
    status:str

    payment_reference: str | None

    session_reference: str | None

    amount: Decimal | None

    currency:str | None

    raw_data: dict[str, Any] | None=None

class PaymentGateway(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique provider name.

        example :

                stripe
                payfast
        """
        raise NotImplementedError
    
    @abstractmethod
    def create_checkout(
        self,
        *,
        reference:str,
        amount:Decimal,
        currency:str,
        donor_email:str,
        donor_name:str | None=None, 
        success_url:str,
        cancel_url: str
    ) -> CheckoutSession:
        
        """
            create a provider-hosted payment session.
        
        """

        raise NotImplementedError
    
    @abstractmethod
    def verify_webhook(
        self, 
        *,
        payload: bytes,
        headers: dict
    ) -> PaymentVerification:
        
        raise NotImplementedError
    
    @abstractmethod
    def retrieve_payment(
        self,
        *,
        provider_reference:str
    ) -> PaymentVerification:
        
        raise NotImplementedError
    
class PaymentGatewayError(Exception):

    pass 

class CheckoutCreationError(PaymentGatewayError):

    pass 

class WebhookVerificationError(PaymentGatewayError):

    pass

class PaymentRetrievalError(PaymentGatewayError):

    pass

