from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives

from core.models import Member


class Command(BaseCommand):

    help = 'Send pregnancy alert when delivery is within 2 days'

    def handle(self, *args, **kwargs):

        today = date.today()
        alert_end_date = today + timedelta(days=2)

        women = Member.objects.filter(
            gender='Female',
            currently_pregnant=True,
            expected_delivery_date__gte=today,
            expected_delivery_date__lte=alert_end_date,
            pregnancy_alert_sent=False
        ).select_related(
            'family',
            'family__village'
        )

        count = 0

        for woman in women:

            days_remaining = (
                woman.expected_delivery_date - today
            ).days

            if days_remaining == 0:
                alert_title = "Delivery Expected Today"
                alert_message = "Immediate follow-up is recommended."
                alert_class = "urgent"
            elif days_remaining == 1:
                alert_title = "Delivery Expected Tomorrow"
                alert_message = "Please contact and follow up with the family."
                alert_class = "warning"
            else:
                alert_title = "Delivery Expected in 2 Days"
                alert_message = "Please plan a follow-up with the family."
                alert_class = "notice"

            subject = f"ASHA Care Alert: {alert_title} - {woman.name}"

            text_message = f"""
ASHA CARE
Pregnancy Follow-up Alert

{alert_title}

Pregnant Woman:
{woman.name}

Family:
{woman.family.family_name}

Village:
{woman.family.village.name}

House Number:
{woman.family.house_number}

Mobile Number:
{woman.mobile_number}

Expected Delivery Date:
{woman.expected_delivery_date.strftime('%d-%m-%Y')}

Days Remaining:
{days_remaining}

{alert_message}

Please ensure timely follow-up and necessary medical care.

This is an automatic notification from ASHA Care.
"""

            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body style="
    margin:0;
    padding:0;
    background:#f3f6f9;
    font-family:Arial, Helvetica, sans-serif;
">

<div style="
    max-width:650px;
    margin:30px auto;
    background:#ffffff;
    border-radius:14px;
    overflow:hidden;
    box-shadow:0 4px 18px rgba(0,0,0,0.10);
">

    <!-- HEADER -->

    <div style="
        background:#15803d;
        padding:24px 28px;
        color:white;
    ">

        <div style="
            font-size:14px;
            font-weight:bold;
            letter-spacing:1px;
            margin-bottom:8px;
        ">
            ASHA CARE
        </div>

        <div style="
            font-size:25px;
            font-weight:bold;
        ">
            Pregnancy Alert
        </div>

        <div style="
            font-size:14px;
            margin-top:7px;
            opacity:0.92;
        ">
            Maternal health follow-up notification
        </div>

    </div>


    <!-- ALERT -->

    <div style="
        margin:24px 28px 10px 28px;
        padding:18px;
        border-radius:10px;
        background:#fff4f4;
        border-left:5px solid #dc2626;
    ">

        <div style="
            color:#b91c1c;
            font-size:20px;
            font-weight:bold;
            margin-bottom:6px;
        ">
            {alert_title}
        </div>

        <div style="
            color:#7f1d1d;
            font-size:14px;
            line-height:1.5;
        ">
            {alert_message}
        </div>

    </div>


    <!-- WOMAN DETAILS -->

    <div style="padding:10px 28px 0 28px;">

        <div style="
            color:#1f2937;
            font-size:18px;
            font-weight:bold;
            margin-bottom:14px;
        ">
            Patient Information
        </div>


        <table width="100%" cellpadding="0" cellspacing="0"
               style="
                    border-collapse:collapse;
                    border:1px solid #e5e7eb;
                    border-radius:10px;
                    overflow:hidden;
               ">

            <tr>
                <td style="
                    padding:13px;
                    background:#f8fafc;
                    color:#64748b;
                    font-size:13px;
                    width:42%;
                    border-bottom:1px solid #e5e7eb;
                ">
                    Name
                </td>

                <td style="
                    padding:13px;
                    color:#111827;
                    font-size:14px;
                    font-weight:bold;
                    border-bottom:1px solid #e5e7eb;
                ">
                    {woman.name}
                </td>
            </tr>


            <tr>
                <td style="
                    padding:13px;
                    background:#f8fafc;
                    color:#64748b;
                    font-size:13px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    Family
                </td>

                <td style="
                    padding:13px;
                    color:#111827;
                    font-size:14px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    {woman.family.family_name}
                </td>
            </tr>


            <tr>
                <td style="
                    padding:13px;
                    background:#f8fafc;
                    color:#64748b;
                    font-size:13px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    Village
                </td>

                <td style="
                    padding:13px;
                    color:#111827;
                    font-size:14px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    {woman.family.village.name}
                </td>
            </tr>


            <tr>
                <td style="
                    padding:13px;
                    background:#f8fafc;
                    color:#64748b;
                    font-size:13px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    House Number
                </td>

                <td style="
                    padding:13px;
                    color:#111827;
                    font-size:14px;
                    border-bottom:1px solid #e5e7eb;
                ">
                    {woman.family.house_number}
                </td>
            </tr>


            <tr>
                <td style="
                    padding:13px;
                    background:#f8fafc;
                    color:#64748b;
                    font-size:13px;
                ">
                    Mobile Number
                </td>

                <td style="
                    padding:13px;
                    color:#111827;
                    font-size:14px;
                    font-weight:bold;
                ">
                    {woman.mobile_number}
                </td>
            </tr>

        </table>

    </div>


    <!-- DELIVERY INFORMATION -->

    <div style="
        margin:24px 28px;
        padding:20px;
        background:#f0fdf4;
        border:1px solid #bbf7d0;
        border-radius:10px;
        text-align:center;
    ">

        <div style="
            color:#166534;
            font-size:13px;
            font-weight:bold;
            text-transform:uppercase;
            letter-spacing:0.5px;
        ">
            Expected Delivery Date
        </div>

        <div style="
            color:#14532d;
            font-size:26px;
            font-weight:bold;
            margin-top:8px;
        ">
            {woman.expected_delivery_date.strftime('%d-%m-%Y')}
        </div>

        <div style="
            margin-top:12px;
            color:#166534;
            font-size:15px;
            font-weight:bold;
        ">
            {days_remaining} day(s) remaining
        </div>

    </div>


    <!-- ACTION -->

    <div style="
        margin:0 28px 24px 28px;
        padding:18px;
        background:#fffbeb;
        border:1px solid #fde68a;
        border-radius:10px;
    ">

        <div style="
            color:#92400e;
            font-size:15px;
            font-weight:bold;
            margin-bottom:7px;
        ">
            Follow-up Required
        </div>

        <div style="
            color:#78350f;
            font-size:14px;
            line-height:1.6;
        ">
            Please contact the family and ensure timely follow-up,
            necessary medical care, and preparation for delivery.
        </div>

    </div>


    <!-- FOOTER -->

    <div style="
        background:#f8fafc;
        border-top:1px solid #e5e7eb;
        padding:18px 28px;
        text-align:center;
    ">

        <div style="
            color:#15803d;
            font-size:16px;
            font-weight:bold;
        ">
            ASHA Care
        </div>

        <div style="
            color:#64748b;
            font-size:12px;
            margin-top:5px;
        ">
            Healthcare & Family Monitoring System
        </div>

        <div style="
            color:#94a3b8;
            font-size:11px;
            margin-top:10px;
        ">
            This is an automatic notification. Please do not reply to this email.
        </div>

    </div>

</div>

</body>
</html>
"""

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=None,
                to=[
                    'parth27052002@gmail.com',
                    'ashaanursing2026@gmail.com'
                ]
            )

            email.attach_alternative(
                html_message,
                "text/html"
            )

            email.send(fail_silently=False)

            woman.pregnancy_alert_sent = True

            woman.save(
                update_fields=['pregnancy_alert_sent']
            )

            count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Pregnancy alert sent for {woman.name} - '
                    f'{days_remaining} day(s) remaining.'
                )
            )

        if count == 0:

            self.stdout.write(
                self.style.SUCCESS(
                    'No pregnancy alerts required today.'
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    f'{count} pregnancy alert(s) sent successfully.'
                )
            )