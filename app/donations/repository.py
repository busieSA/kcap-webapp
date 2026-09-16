from sqlalchemy import func
from app.core.extensions import db
from app.core.base_repository import BaseRepository

from app.donations.models import Donation, DonationStatus

class DonationRepository(BaseRepository):

    model = Donation

    @classmethod
    def get_by_reference(cls, reference):

        return (
            cls.model.query.filter(
                cls.model.reference == reference
            ).first()
        )
    
    @classmethod
    def get_by_provider_reference(
        cls,
        provider_reference
    ):
        return (
            cls.model.query.filter(
                cls.model.provider_reference == provider_reference
            ).first()
        )
    
    @classmethod
    def get_by_provider_session_reference(cls, session_reference):

        return (
            cls.model.query.filter(
                cls.model.provider_session_reference == session_reference
            ).first()
        )
    
    @classmethod
    def get_pending(cls):
        
        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.PENDING,
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def get_processing(cls):

        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.PROCEESSING,
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def get_successful(cls):

        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.SUCCESSFUL,
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    classmethod
    def get_failed(cls):

        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.FAILED,
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def get_recent(cls, limit=10):

        return (
            cls.model.query.filter(
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).limit(limit).all()
        )
    
    @classmethod
    def get_recent_successful(
        cls, limit=10
    ):
        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.SUCCESSFUL,
                cls.model.is_deleted.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).limit(limit).all()
        )

    @classmethod
    def count_success(cls):

        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.SUCCESSFUL,
                cls.model.is_deleted.is_(False)
            ).count()
        )
    
    @classmethod
    def count_pending(cls):

        return (
            cls.model.query.filter(
                cls.model.status == DonationStatus.PENDING,
                cls.model.is_deleted.is_(False)
            ).count()
        )
    
    @classmethod
    def total_successful_amount(cls, currency="ZAR"):

        total = (
            db.session.query(
                func.coalesce(
                    func.sum(
                        cls.model.amount
                    ),0
                )
            ).filter(
                cls.model.status == DonationStatus.SUCCESSFUL,
                cls.model.currency == currency.upper(),
                cls.model.is_deleted.is_(False)
            ).scalar()
        )

        return total
    
    @classmethod
    def reference_exists(cls,reference):

        return (
            cls.model.query.filter(
                cls.model.reference == reference
            ).first()
            is not None
        )
    
    

        