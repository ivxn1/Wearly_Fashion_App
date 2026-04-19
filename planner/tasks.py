import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.timezone import localdate

logger = logging.getLogger(__name__)
UserModel = get_user_model()


def _build_digest_html(profile, entries):

    rows = ""
    for entry in entries:
        garment_names = ", ".join(g.title for g in entry.outfit.garments.all())
        rows += f"""
        <tr>
          <td style="padding: 14px 18px; border-bottom: 1px solid #f0f0f0; font-size: 14px; color: #1a1a1a; font-weight: 600;">
            {entry.date.strftime("%A, %b %d")}
          </td>
          <td style="padding: 14px 18px; border-bottom: 1px solid #f0f0f0;">
            <span style="font-size: 14px; color: #1a1a1a; font-weight: 500;">{entry.outfit.title}</span>
            <br>
            <span style="font-size: 12px; color: #8a8a8a;">{entry.outfit.occasion} &middot; {entry.outfit.season.title() if entry.outfit.season else ""}</span>
            {f'<br><span style="font-size: 12px; color: #6a6a6a; font-style: italic;">{garment_names}</span>' if garment_names else ""}
          </td>
          <td style="padding: 14px 18px; border-bottom: 1px solid #f0f0f0; font-size: 12px; color: #8a8a8a; text-align: right;">
            {f"<em>{entry.note}</em>" if entry.note else "&mdash;"}
          </td>
        </tr>"""

    if not rows:
        rows = """
        <tr>
          <td colspan="3" style="padding: 40px 18px; text-align: center; color: #8a8a8a; font-size: 14px;">
            No outfits planned for the upcoming week. Time to schedule some looks!
          </td>
        </tr>"""

    today = localdate()
    end = today + timedelta(days=7)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 40px 20px;">
        <tr>
          <td align="center">

            <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.06);">

              <!-- Header -->
              <tr>
                <td style="background-color: #1a1a1a; padding: 32px 40px; text-align: center;">
                  <h1 style="margin: 0; font-size: 28px; font-weight: 300; letter-spacing: 3px; color: #ffffff; text-transform: uppercase;">
                    Wearly
                  </h1>
                  <p style="margin: 8px 0 0; font-size: 13px; letter-spacing: 1px; color: rgba(255,255,255,0.6); text-transform: uppercase;">
                    Weekly Outfit Digest
                  </p>
                </td>
              </tr>

              <!-- Greeting -->
              <tr>
                <td style="padding: 32px 40px 16px;">
                  <h2 style="margin: 0; font-size: 20px; font-weight: 500; color: #1a1a1a;">
                    Hi {profile.first_name},
                  </h2>
                  <p style="margin: 10px 0 0; font-size: 14px; color: #6a6a6a; line-height: 1.6;">
                    Here's your outfit plan for <strong>{today.strftime("%b %d")}</strong> &ndash; <strong>{end.strftime("%b %d, %Y")}</strong>.
                  </p>
                </td>
              </tr>

              <!-- Divider -->
              <tr>
                <td style="padding: 0 40px;">
                  <hr style="border: none; border-top: 1px solid #eee; margin: 0;">
                </td>
              </tr>

              <!-- Plan table -->
              <tr>
                <td style="padding: 24px 40px;">
                  <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse;">
                    <tr>
                      <th style="padding: 10px 18px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #8a8a8a; font-weight: 600; border-bottom: 2px solid #1a1a1a;">
                        Day
                      </th>
                      <th style="padding: 10px 18px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #8a8a8a; font-weight: 600; border-bottom: 2px solid #1a1a1a;">
                        Outfit
                      </th>
                      <th style="padding: 10px 18px; text-align: right; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #8a8a8a; font-weight: 600; border-bottom: 2px solid #1a1a1a;">
                        Note
                      </th>
                    </tr>
                    {rows}
                  </table>
                </td>
              </tr>

              <!-- Summary -->
              <tr>
                <td style="padding: 0 40px 24px;">
                  <div style="background-color: #fafafa; border-radius: 8px; padding: 16px 20px; text-align: center;">
                    <span style="font-size: 13px; color: #6a6a6a;">
                      <strong style="color: #1a1a1a;">{len(entries)}</strong> outfit{"s" if len(entries) != 1 else ""} planned this week
                    </span>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background-color: #fafafa; padding: 24px 40px; text-align: center; border-top: 1px solid #eee;">
                  <p style="margin: 0; font-size: 12px; color: #aaa; line-height: 1.6;">
                    You're receiving this because you're a Wearly Premium member.
                    <br>
                    Sent with care from your wardrobe assistant.
                  </p>
                </td>
              </tr>

            </table>

          </td>
        </tr>
      </table>

    </body>
    </html>
    """


@shared_task
def send_weekly_digest(user_id):
    """Send a weekly outfit digest email to a single user."""
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        logger.warning("Weekly digest: user %s not found", user_id)
        return

    profile = user.profile
    today = localdate()
    entries = list(
        user.plans.select_related("outfit")
        .prefetch_related("outfit__garments")
        .filter(date__gte=today, date__lt=today + timedelta(days=7))
        .order_by("date")
    )

    html_body = _build_digest_html(profile, entries)
    plain_body = (
        f"Hi {profile.first_name}, you have {len(entries)} outfit(s) planned this week. "
        f"Log in to Wearly to see the details."
    )

    send_mail(
        subject="Your Weekly Outfit Digest - Wearly",
        message=plain_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_body,
        fail_silently=False,
    )
    logger.info("Weekly digest sent to %s (%d entries)", user.email, len(entries))


@shared_task
def send_weekly_digest_to_all_premiums():
    """Dispatch individual digest tasks for all Premium users."""
    premium_users = UserModel.objects.filter(is_premium=True, is_active=True)
    count = 0
    for user in premium_users:
        send_weekly_digest.delay(user.id)
        count += 1
    logger.info("Dispatched weekly digests for %d premium users", count)
