from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

def build_html_email(
    content: str,
    title: str,
    logo_url: str,
    button_title: str = None,
    button_link: str = None,
    footer_label: str = "USATA",
    additional_context: dict = None
) -> str:
    """
    Render the email HTML using the base template with dynamic content.
    """
    context = {
        "content": mark_safe(content),
        "button_title": button_title,
        "button_link": button_link,
        "title": title,
        "footer_label": footer_label,
        "logo_url": logo_url,
    }
    
    if additional_context:
        context.update(additional_context)

    return render_to_string("core/base_email_template.html", context)

def send_webinar_registration_email(registration):
    """
    Send a webinar registration confirmation email.
    """
    recipient_email = registration.email

    if not recipient_email:
        print("No recipient email provided.")
        return False

    subject = "USATA Webinar Registration Confirmation"
    
    # HTML content for the email body
    content = f"""
    <p>Dear {registration.first_name},</p>
    
    <p>Thank you for registering for Webinar 1 of the USATA Procurement Readiness Series for U.S. SMEs.</p>
    
    <h4>Webinar Details:</h4>
    <p><strong>Title:</strong> Opportunities under World Bank Financed Projects in Africa – Demystifying the Process</p>
    <p><strong>Date:</strong> Tuesday, July 29th, 2025</p>
    <p><strong>Time:</strong> 10:00am – 12:00pm EST</p>
    
    <p>Please find the agenda attached below.</p>
    """

    button_title = "Join Webinar on Teams"
    button_link = "https://teams.microsoft.com/l/meetup-join/your-meeting-link"
    logo_url = "https://mcusercontent.com/7a690cee9d1354cf49cc70330/images/2b2d0cde-34c4-f862-e000-e6a208d5415c.jpg"

    # Additional context for webinar-specific content
    additional_context = {
        "webinar_title": "USATA Procurement Readiness Series",
        "webinar_date": "July 29, 2025",
        "webinar_time": "10:00 AM - 12:00 PM EST"
    }

    # HTML version
    html_message = build_html_email(
        content=content,
        title="USATA Webinar Registration Confirmation",
        button_title=button_title,
        button_link=button_link,
        logo_url=logo_url,
        footer_label="U.S. African Trade Alliance (USATA)",
        additional_context=additional_context
    )

    # Plain text fallback
    plain_message = f"""Dear {registration.first_name},

Thank you for registering for the USATA webinar.

Webinar Details:
Title: Opportunities under World Bank Financed Projects in Africa
Date: July 29, 2025
Time: 10:00 AM - 12:00 PM EST

Join here: {button_link}
"""

    try:
        # For more complex emails with attachments, use EmailMessage
        email = EmailMessage(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient_email],
        )
        email.content_subtype = "html"  # Main content is HTML
        email.body = html_message
        email.send(fail_silently=False)
        
        return True
    except Exception as e:
        print(f"Failed to send webinar registration email: {e}")
        return False