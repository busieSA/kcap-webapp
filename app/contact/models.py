import enum

from app.core.extensions import db
from app.core.base_model import BaseModel, utc_now, d_col


class EnquiryStatus(enum.Enum):
    NEW = "new"
    READ = "read"
    RESOLVED = "resolved"


class Enquiry(BaseModel):

    __tablename__ = "enquiries"

    name = d_col(
        db.String(255),
        nullable=False
    )

    email = d_col(
        db.String(255),
        nullable=False,
        index=True
    )

    phone = d_col(
        db.String(30),
        nullable=True
    )

    subject = d_col(
        db.String(255),
        nullable=True
    )

    message = d_col(
        db.Text,
        nullable=False
    )

    status = d_col(
        db.Enum(EnquiryStatus),
        default=EnquiryStatus.NEW,
        nullable=False,
        index=True
    )

    is_registered = d_col(
        db.Boolean,
        default=False,
        nullable=False
    )

    read_at = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    resolved_at = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    def mark_as_read(self):
        if self.status == EnquiryStatus.NEW:
            self.status = EnquiryStatus.READ

        if self.read_at is None:
            self.read_at = utc_now()

        return self

    def mark_as_resolved(self):
        if self.read_at is None:
            self.read_at = utc_now()

        self.status = EnquiryStatus.RESOLVED
        self.resolved_at = utc_now()

        return self

    def reopen(self):
        self.status = EnquiryStatus.READ
        self.resolved_at = None

        if self.read_at is None:
            self.read_at = utc_now()

        return self

    @property
    def is_new(self):
        return self.status == EnquiryStatus.NEW

    @property
    def is_resolved(self):
        return self.status == EnquiryStatus.RESOLVED

    def __repr__(self) -> str:
        return (
            f"<Enquiry "
            f"id={self.id} "
            f"email={self.email} "
            f"status={self.status.value}>"
        )