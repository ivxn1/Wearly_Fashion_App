import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import send_mail

UserModel = get_user_model()
logger = logging.getLogger(__name__)

PREMIUM_SALT = "premium-activation"
PREMIUM_TOKEN_MAX_AGE = 60 * 60 * 24 * 3  # 3 days


def _build_premium_email_html(profile, activation_url):
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
                    Premium Activation
                  </p>
                </td>
              </tr>

              <!-- Greeting -->
              <tr>
                <td style="padding: 36px 40px 16px;">
                  <h2 style="margin: 0; font-size: 22px; font-weight: 500; color: #1a1a1a;">
                    Hi {profile.first_name},
                  </h2>
                  <p style="margin: 14px 0 0; font-size: 15px; color: #4a4a4a; line-height: 1.7;">
                    You've requested to upgrade to <strong style="color: #b8860b;">Wearly Premium</strong>.
                    Click the button below to confirm your activation and unlock exclusive features.
                  </p>
                </td>
              </tr>

              <!-- Divider -->
              <tr>
                <td style="padding: 0 40px;">
                  <hr style="border: none; border-top: 1px solid #eee; margin: 0;">
                </td>
              </tr>

              <!-- Benefits -->
              <tr>
                <td style="padding: 28px 40px 8px;">
                  <h3 style="margin: 0 0 16px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px; color: #8a8a8a; font-weight: 600;">
                    What you'll unlock
                  </h3>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding: 10px 0; font-size: 14px; color: #1a1a1a; border-bottom: 1px solid #f0f0f0;">
                        <span style="margin-right: 10px; color: #b8860b; font-size: 16px;">&#9733;</span>
                        Weekly outfit digest emails
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 10px 0; font-size: 14px; color: #1a1a1a; border-bottom: 1px solid #f0f0f0;">
                        <span style="margin-right: 10px; color: #b8860b; font-size: 16px;">&#9733;</span>
                        Priority style recommendations
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 10px 0; font-size: 14px; color: #1a1a1a; border-bottom: 1px solid #f0f0f0;">
                        <span style="margin-right: 10px; color: #b8860b; font-size: 16px;">&#9733;</span>
                        Unlimited wardrobe collections
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 10px 0; font-size: 14px; color: #1a1a1a;">
                        <span style="margin-right: 10px; color: #b8860b; font-size: 16px;">&#9733;</span>
                        Early access to new features
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- CTA Button -->
              <tr>
                <td style="padding: 32px 40px;" align="center">
                  <a href="{activation_url}"
                     style="display: inline-block; background-color: #b8860b; color: #ffffff; text-decoration: none;
                            padding: 16px 48px; border-radius: 8px; font-size: 16px; font-weight: 600;
                            letter-spacing: 0.5px; text-transform: uppercase;">
                    Activate Premium
                  </a>
                </td>
              </tr>

              <!-- Fallback link -->
              <tr>
                <td style="padding: 0 40px 28px; text-align: center;">
                  <p style="margin: 0; font-size: 12px; color: #aaa; line-height: 1.6;">
                    If the button doesn't work, copy and paste this link into your browser:
                    <br>
                    <a href="{activation_url}" style="color: #b8860b; word-break: break-all;">{activation_url}</a>
                  </p>
                </td>
              </tr>

              <!-- Expiry notice -->
              <tr>
                <td style="padding: 0 40px 24px;">
                  <div style="background-color: #fafafa; border-radius: 8px; padding: 16px 20px; text-align: center;">
                    <span style="font-size: 13px; color: #6a6a6a;">
                      This link expires in <strong style="color: #1a1a1a;">3 days</strong>.
                      If it expires, simply request a new one from your profile.
                    </span>
                  </div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td style="background-color: #fafafa; padding: 24px 40px; text-align: center; border-top: 1px solid #eee;">
                  <p style="margin: 0; font-size: 12px; color: #aaa; line-height: 1.6;">
                    If you didn't request this upgrade, you can safely ignore this email.
                    <br>
                    Sent with care from the Wearly team.
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
def send_premium_registration_email(user_id: int, activation_url: str):
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        logger.warning("Premium email: user %s not found", user_id)
        return

    profile = user.profile
    html_body = _build_premium_email_html(profile, activation_url)
    plain_body = (
        f"Hi {profile.first_name}, you've requested to upgrade to Wearly Premium! "
        f"Visit the following link to activate: {activation_url}"
    )

    send_mail(
        subject="Activate Your Wearly Premium Account",
        message=plain_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_body,
        fail_silently=False,
    )
    logger.info("Premium activation email sent to %s", user.email)

@shared_task
def send_password_reset_email(
    subject,
    message,
    from_email,
    recipient_list,
    html_message=None,
):
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )
