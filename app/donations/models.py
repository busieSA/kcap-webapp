from enum import Enum
from app.core.extensions import db
from app.core.base_model import BaseModel, d_col

class DonationStatus(str,Enum):

    PENDING = "pending"
    PROCEESSING = "processing"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    CANCELLED =  "cancelled"
    REFUNDED = "refunded"  

class Donation(BaseModel):
    __tablename__ = "donations"

    reference = d_col(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    donor_name = d_col(
        db.String(150),
        nullable=False
    )

    donor_email = d_col(
        db.String(255),
        nullable=True,
        index=True
    )

    donor_phone = d_col(
        db.String(50),
        nullable=True
    )

    amount = d_col(
        db.Numeric(12,2),
        nullable=False
    )

    currency = d_col(
        db.String(3),
        nullable=False,
        default="ZAR"
    )

    purpose = d_col(
        db.String(255),
        nullable=True
    )

    message = d_col(
        db.Text,
        nullable=True
    )

    is_anonymous = d_col(
        db.Boolean,
        default=False,
        nullable=False
    )

    provider = d_col(
        db.String(50),
        nullable=True,
        index=True
    )

    provider_reference = d_col(
        db.String(255),
        nullable=True,
        index=True
    )

    provider_session_reference = d_col(
        db.String(255),
        nullable=True
    )

    status = d_col(
        db.Enum(
            DonationStatus,
            values_callback =lambda enum_cls: [
                item.value for item in enum_cls
            ],
            native_enum=False,
            lenght=20
        ),
        default=DonationStatus.PENDING,
        nullable=False,
        index=True
    )

    paid_at = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    failed_at = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    cancelled_at = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    refunded_at= d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    @property
    def is_pending(self):
        return(
            self.status == DonationStatus.PENDING
        )
    
    @property
    def is_successful(self):
        return (
            self.status == DonationStatus.SUCCESSFUL
        )
    
    @property
    def is_failed(self):
        return (
            self.status == DonationStatus.FAILED
        )
    
    @property
    def is_cancelled(self):
        return (
            self.status == DonationStatus.CANCELLED
        )
    
    @property
    def is_refunded(self):
        return (
            self.status == DonationStatus.REFUNDED
        )
    
    @property
    def donor_desplay_name(self):
        if self.is_anonymous:
            return "anonymous Donor"
        
        return (
            self.donor_name or "Donor"
        )
    
    def __repr__(self):

        return (
            f"<Donation "
            f"{self.reference} "
            f"{self.amount}"
            f"{self.currency}"
            f"{self.status.value} >"
        )
    
    