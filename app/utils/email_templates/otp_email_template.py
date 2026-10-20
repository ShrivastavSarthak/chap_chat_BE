def get_otp_email_template(otp: str, app_name: str = "Chap Chat") -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Your Verification Code</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #333333;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;">
        <tr>
          <td align="center" style="padding: 40px 10px;">
            <!-- Main Container Card -->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); overflow: hidden; border: 1px solid #e5e7eb;">
              
              <!-- Brand Header -->
              <tr>
                <td align="center" style="padding: 32px 20px 10px 20px;">
                  <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #111827; letter-spacing: -0.5px;">
                    {app_name}
                  </h1>
                </td>
              </tr>

              <!-- Body Message -->
              <tr>
                <td align="center" style="padding: 10px 30px;">
                  <p style="margin: 0; font-size: 15px; line-height: 24px; color: #4b5563;">
                    Use the verification code below to verify your email address and sign in.
                  </p>
                </td>
              </tr>

              <!-- OTP Highlight Box -->
              <tr>
                <td align="center" style="padding: 24px 30px;">
                  <div style="background-color: #f3f4f6; border-radius: 8px; padding: 18px 24px; display: inline-block; border: 1px dashed #d1d5db;">
                    <span style="font-size: 32px; font-weight: 800; letter-spacing: 10px; color: #1f2937; font-family: monospace;">
                      {otp}
                    </span>
                  </div>
                </td>
              </tr>

              <!-- Expiration Warning -->
              <tr>
                <td align="center" style="padding: 0 30px 24px 30px;">
                  <p style="margin: 0; font-size: 13px; color: #6b7280; line-height: 20px;">
                    This code is valid for <strong>5 minutes</strong>.<br>
                    If you did not request this verification, you can safely ignore this email.
                  </p>
                </td>
              </tr>

              <!-- Divider -->
              <tr>
                <td style="padding: 0 30px;">
                  <div style="border-top: 1px solid #f3f4f6;"></div>
                </td>
              </tr>

              <!-- Footer -->
              <tr>
                <td align="center" style="padding: 20px 30px; font-size: 12px; color: #9ca3af;">
                  <p style="margin: 0;">
                    &copy; {app_name}. All rights reserved.
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