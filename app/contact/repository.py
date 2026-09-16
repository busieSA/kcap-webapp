from app.core.base_repository import BaseRepository
from app.contact.models import (
    Enquiry,
    EnquiryStatus
)

class EnquiryRepository(BaseRepository):
    model = Enquiry

    @classmethod
    def get_all_ordered(cls):
        return (
            cls.model.query.filter_by(
                is_deleted=False
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def get_new(cls):
        return (
            cls.model.query.filter_by(
                status=EnquiryStatus.NEW,
                is_deleted=False
            ).order_by(
                cls.model.created_at.esc()
            ).all()
        )
    
    @classmethod
    def get_read(cls):
        return (
            cls.model.query.filter_by(
                status=EnquiryStatus.READ,
                is_deleted=False
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def get_resolved(cls):

        return (
            cls.model.query.filter_by(
                status=EnquiryStatus.RESOLVED,
                is_deleted=False
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    
    @classmethod
    def search_enquiries(cls,keyword):
        if not keyword:
            return cls.model.query.filter_by(
                is_deleted=False
            )
        return (
            cls.model.search(
                keyword,
                "name",
                "email",
                "phone",
                "subject",
                "message"
            ).filter_by(
                is_deleted=False
            )
        )
    
    @classmethod
    def count_new(cls):
        return (
            cls.model.query.filter_by(
                status=EnquiryStatus.NEW,
                is_deleted=False
            ).count()
        )
    
    @classmethod
    def count_resolved(cls):
        return (

            cls.model.query.filter_by(
                status=EnquiryStatus.RESOLVED,
                is_deleted=False
            ).count()
        )
    
    