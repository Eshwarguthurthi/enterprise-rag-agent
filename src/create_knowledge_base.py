from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


documents = {

    "hr/leave_policy.pdf": {
        "title": "Employee Leave Policy",
        "content": [
            ("1. Purpose",
             "This document defines the leave rules and procedures applicable to employees."),

            ("2. Casual Leave",
             "Employees are entitled to 12 casual leave days per calendar year. "
             "Casual leave may be used for personal matters, urgent requirements, "
             "or short-term absence."),

            ("3. Sick Leave",
             "Employees are entitled to 10 sick leave days per calendar year. "
             "Medical documentation may be requested for extended periods of absence."),

            ("4. Annual Leave",
             "Employees receive 18 annual leave days per year. "
             "Unused annual leave may be carried forward according to applicable company rules."),

            ("5. Leave Application",
             "Employees should submit leave requests through the employee portal. "
             "Planned leave should normally be submitted at least two working days "
             "before the requested leave date."),

            ("6. Emergency Leave",
             "Emergency leave may be submitted after the absence when circumstances "
             "prevent advance submission. Manager approval is required."),

            ("7. Leave Approval",
             "Leave requests are subject to manager approval and organizational requirements.")
        ]
    },

    "hr/employee_policy.pdf": {
        "title": "Employee Policy",
        "content": [
            ("1. Purpose",
             "This document describes general workplace policies and employee responsibilities."),

            ("2. Working Hours",
             "Standard working hours are 9:00 AM to 6:00 PM from Monday through Friday. "
             "Employees are expected to follow their assigned work schedules."),

            ("3. Attendance",
             "Employees should maintain regular attendance and inform their manager "
             "when they are unable to attend work."),

            ("4. Employee Responsibilities",
             "Employees are responsible for completing assigned work, protecting "
             "organizational information, and following workplace procedures."),

            ("5. Code of Conduct",
             "Employees are expected to behave professionally and respectfully "
             "toward colleagues, customers, and business partners."),

            ("6. Identification",
             "Employees must carry their organization-issued identification card "
             "when accessing company premises.")
        ]
    },

    "hr/work_from_home_policy.pdf": {
        "title": "Work From Home Policy",
        "content": [
            ("1. Purpose",
             "This document defines the organization's work-from-home guidelines."),

            ("2. Eligibility",
             "Employees may work remotely when their role permits remote work "
             "and the arrangement has been approved."),

            ("3. Approval",
             "Employees should obtain manager approval before working remotely."),

            ("4. Working Hours",
             "Employees working remotely are expected to remain available during "
             "their assigned working hours."),

            ("5. Equipment",
             "Employees are responsible for taking reasonable care of company "
             "equipment used for remote work."),

            ("6. Information Security",
             "Employees must use approved systems and secure network connections "
             "when accessing organizational information remotely.")
        ]
    },

    "it/password_reset.pdf": {
        "title": "Password Reset Procedure",
        "content": [
            ("1. Purpose",
             "This document explains how employees can reset their organization password."),

            ("2. Password Requirements",
             "Passwords should contain at least eight characters and include "
             "a combination of letters, numbers, and special characters."),

            ("3. Password Reset",
             "Open the employee account portal and select the Password Reset option. "
             "Complete identity verification and create a new password."),

            ("4. Account Lockout",
             "An account may be temporarily locked after multiple unsuccessful "
             "login attempts."),

            ("5. OTP Verification",
             "Identity verification may require a one-time password sent to "
             "the employee's registered contact method."),

            ("6. IT Helpdesk",
             "If the password reset process fails, contact the IT helpdesk "
             "with the employee account identifier and a description of the problem.")
        ]
    },

    "it/vpn_support.pdf": {
        "title": "VPN Support Guide",
        "content": [
            ("1. Purpose",
             "This document provides guidance for connecting to the organization's VPN."),

            ("2. VPN Installation",
             "Install the organization-approved VPN client on the assigned device."),

            ("3. VPN Login",
             "Open the VPN client, enter the organization credentials, "
             "complete any required verification, and select Connect."),

            ("4. Connection Problems",
             "If the VPN does not connect, verify the internet connection, "
             "restart the VPN client, and try again."),

            ("5. Authentication Problems",
             "Employees should verify that their credentials are current "
             "and that required multi-factor authentication is completed."),

            ("6. Escalation",
             "If troubleshooting does not resolve the problem, contact the IT support team.")
        ]
    },

    "it/account_management.pdf": {
        "title": "Account Management Policy",
        "content": [
            ("1. Purpose",
             "This document describes procedures for managing employee accounts."),

            ("2. Account Creation",
             "New employee accounts are created after the required employee "
             "information and access approvals have been received."),

            ("3. Account Activation",
             "Employees must complete the required identity verification "
             "before accessing organizational systems."),

            ("4. Access Requests",
             "Access to restricted applications requires approval from the "
             "appropriate manager or system owner."),

            ("5. Account Locking",
             "Accounts may be temporarily locked when suspicious activity "
             "or repeated unsuccessful authentication attempts are detected."),

            ("6. Account Deactivation",
             "Employee accounts should be deactivated when access is no longer required.")
        ]
    },

    "support/ticket_escalation.pdf": {
        "title": "Support Ticket Escalation Procedure",
        "content": [
            ("1. Purpose",
             "This document defines support ticket priority levels and escalation procedures."),

            ("2. Priority 1",
             "Priority 1 incidents represent critical issues affecting major services "
             "or a large number of users. These incidents require immediate escalation."),

            ("3. Priority 2",
             "Priority 2 incidents represent significant issues that affect important "
             "functionality but do not cause a complete service outage."),

            ("4. Priority 3",
             "Priority 3 incidents are lower-impact issues, general requests, "
             "or problems with available workarounds."),

            ("5. Escalation",
             "Support agents should escalate tickets when the issue requires "
             "specialist assistance or cannot be resolved within the applicable "
             "support process."),

            ("6. Escalation Information",
             "The escalation should include the ticket number, problem description, "
             "impact, troubleshooting already performed, and relevant evidence.")
        ]
    },

    "support/customer_support_sop.pdf": {
        "title": "Customer Support Standard Operating Procedure",
        "content": [
            ("1. Purpose",
             "This SOP defines the standard process for handling customer support requests."),

            ("2. Customer Greeting",
             "Support agents should greet the customer professionally and confirm "
             "the customer's request."),

            ("3. Ticket Creation",
             "A support ticket should contain the customer information, issue description, "
             "priority, and relevant supporting details."),

            ("4. Issue Classification",
             "Agents should classify the issue according to its type, impact, "
             "and applicable support category."),

            ("5. Resolution",
             "Agents should investigate the issue, provide appropriate troubleshooting, "
             "and document the resolution."),

            ("6. Ticket Closure",
             "Tickets should be closed after the issue has been resolved and "
             "the required closure information has been recorded.")
        ]
    },

    "support/complaint_handling.pdf": {
        "title": "Customer Complaint Handling Procedure",
        "content": [
            ("1. Purpose",
             "This document defines the process for receiving and resolving customer complaints."),

            ("2. Complaint Registration",
             "Every customer complaint should be recorded in the support system "
             "with the relevant customer and issue details."),

            ("3. Complaint Classification",
             "Complaints should be classified according to the type and severity of the issue."),

            ("4. Initial Response",
             "The support team should acknowledge the complaint and communicate "
             "the next steps to the customer."),

            ("5. Escalation",
             "Complaints requiring specialist review should be escalated "
             "to the appropriate team."),

            ("6. Resolution",
             "The final resolution and actions taken should be documented "
             "before the complaint is closed.")
        ]
    },

    "products/product_manual.pdf": {
        "title": "Product User Manual",
        "content": [
            ("1. Product Overview",
             "This manual provides general instructions for using the organization's product."),

            ("2. Installation",
             "Follow the installation instructions supplied with the product "
             "and verify that the required environment is available."),

            ("3. Configuration",
             "After installation, configure the required settings before using the product."),

            ("4. Basic Usage",
             "Users should sign in with their authorized account and follow "
             "the product workflow for their assigned tasks."),

            ("5. Troubleshooting",
             "For common problems, restart the application, verify the configuration, "
             "and consult the troubleshooting documentation."),

            ("6. Support",
             "If the issue remains unresolved, contact customer support with "
             "the product information and description of the problem.")
        ]
    },

    "products/product_faq.pdf": {
        "title": "Product Frequently Asked Questions",
        "content": [
            ("1. What is the product?",
             "The product is an organization-supported solution designed "
             "to provide users with business functionality."),

            ("2. Who can use the product?",
             "Authorized customers and employees with appropriate access "
             "may use the product."),

            ("3. How do I access the product?",
             "Users should use their authorized credentials through the "
             "organization's supported access method."),

            ("4. What should I do if I cannot log in?",
             "Verify your credentials and follow the password reset procedure "
             "if the password is no longer valid."),

            ("5. Where can I get support?",
             "Users can contact the customer support team when they need assistance.")
        ]
    },

    "products/warranty_policy.pdf": {
        "title": "Product Warranty Policy",
        "content": [
            ("1. Purpose",
             "This document defines the general warranty rules for eligible products."),

            ("2. Warranty Period",
             "Eligible products are covered by a standard warranty period "
             "of twelve months from the date of purchase."),

            ("3. Covered Issues",
             "Manufacturing defects and qualifying product failures occurring "
             "during the warranty period may be covered."),

            ("4. Non-Covered Issues",
             "Damage caused by misuse, unauthorized modification, accidents, "
             "or normal wear may not be covered."),

            ("5. Warranty Claim",
             "Customers requesting warranty service should provide proof of purchase "
             "and relevant product information."),

            ("6. Replacement",
             "If a qualifying warranty claim is approved, the organization "
             "may repair or replace the affected product according to the applicable procedure.")
        ]
    }
}


def create_pdf(relative_path, title, sections):
    output_path = DATA_DIR / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocumentTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        leading=16,
        spaceAfter=10,
    )

    story = []

    story.append(Paragraph(title, title_style))

    for heading, text in sections:
        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 5))

    doc.build(story)


def main():
    for path, document in documents.items():
        create_pdf(
            path,
            document["title"],
            document["content"]
        )
        print(f"Created: {path}")

    print("\nKnowledge base created successfully.")


if __name__ == "__main__":
    main()