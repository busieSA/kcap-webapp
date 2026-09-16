from app.core.base_service import BaseService
from app.core.email_service import EmailService
from app.core.errors import NotFoundError

from app.contact.models import Enquiry
from app.contact.repository import EnquiryRepository

class EnquiryService(BaseService):

    repository = EnquiryRepository

    @classmethod
    def submit_enquiry(cls,data):

        enquiry = Enquiry(
            name = data["name"].strip(),
            email=data["email"].strip().lower(),
            phone =(
                data.get("phone","").strip() or None
            ),
            message = data["message"].strip()
        )

        cls.repository.add(enquiry)

        email_sent = True

        try:
            EmailService.send_enquiry_notification(
                enquiry
            )
        except Exception:
            email_sent = False
        
        return enquiry, email_sent
    
    @classmethod
    def get_enquiry(cls, enquiry_id):
        enquiry = cls.repository.get_by_id(
            enquiry_id
        )

        if not enquiry or enquiry.is_deleted:
            raise NotFoundError(
                "Enquiry not Found..."
            )
        
        return enquiry
    
    @classmethod
    def mark_as_read(cls, enquiry_id):
        enquiry = cls.get_enquiry(
            enquiry_id
        )

        enquiry.mark_as_read()
        cls.repository.save()

        return enquiry
    
    @classmethod
    def resolve(cls, enquiry_id):

        enquiry = cls.get_enquiry(
            enquiry_id
        )

        enquiry.mark_as_resolved()

        cls.repository.save()

        return enquiry
    
    @classmethod
    def reopen(cls, enquiry_id):
        enquiry = cls.get_enquiry(
            enquiry_id
        )

        enquiry.reopen()

        cls.repository.save()

        return enquiry
    
    @classmethod
    def archive(cls, enquiry_id):

        enquiry = cls.get_enquiry(
            enquiry_id
        )

        enquiry.soft_delete(
            commit=False
        )

        cls.repository.save()

        return enquiry
    
    