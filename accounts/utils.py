# accounts/utils.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user):
    """Send welcome email after user registration"""
    try:
        subject = 'Welcome to Lwal Kuu Tech! 🚀'
        
        # HTML Email Template
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Welcome to Lwal Kuu Tech</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <tr>
                    <td align="center" style="padding: 50px 20px;">
                        <table width="500" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #4f46e5, #ec4899); padding: 40px 30px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 28px;">✨ Lwal Kuu Tech</h1>
                                    <p style="color: rgba(255,255,255,0.85); margin: 10px 0 0;">Innovation & Excellence</p>
                                </td>
                            </tr>
                            <!-- Body -->
                            <tr>
                                <td style="padding: 40px 35px;">
                                    <h2 style="color: #1e293b; margin-top: 0;">ကျေးဇူးတင်ပါတယ် {user.first_name or user.username}! 🎉</h2>
                                    <p style="color: #475569; line-height: 1.6;">Lwal Kuu Tech ရဲ့ မိသားစုဝင်အဖြစ် လက်ခံခန့်ညှားတဲ့အတွက် ကျေးဇူးအထူးတင်ရှိပါတယ်။</p>
                                    <p style="color: #475569; line-height: 1.6;">သင့်အကောင့်ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။ အောက်ပါအချက်များကို ယခုစတင်လုပ်ဆောင်နိုင်ပါပြီ:</p>
                                    <ul style="color: #475569; line-height: 1.8;">
                                        <li>ကျွန်ုပ်တို့ရဲ့ ဝန်ဆောင်မှုများကို လေ့လာခြင်း</li>
                                        <li>အောင်မြင်ခဲ့တဲ့ Project များကို ကြည့်ရှုခြင်း</li>
                                        <li>ကျွမ်းကျင်တဲ့ Developer များနှင့် ဆက်သွယ်ခြင်း</li>
                                    </ul>
                                    <div style="text-align: center; margin: 35px 0;">
                                        <a href="https://lwalkuu.vercel.app" style="background: linear-gradient(135deg, #4f46e5, #ec4899); color: white; padding: 12px 35px; text-decoration: none; border-radius: 30px; display: inline-block;">စတင်အသုံးပြုရန် →</a>
                                    </div>
                                    <div style="background-color: #f8fafc; border-radius: 12px; padding: 15px; text-align: center;">
                                        <p style="color: #475569; margin: 0; font-size: 14px;">💡 မေးစရာများရှိပါက <a href="mailto:lwalkuutech@gmail.com" style="color: #4f46e5;">lwalkuutech@gmail.com</a> သို့ ဆက်သွယ်နိုင်ပါသည်။</p>
                                    </div>
                                </td>
                            </tr>
                            <!-- Footer -->
                            <tr>
                                <td style="background-color: #f8fafc; padding: 25px; text-align: center; border-top: 1px solid #e2e8f0;">
                                    <p style="color: #94a3b8; margin: 0;">© 2025 Lwal Kuu Tech. All rights reserved.</p>
                                    <p style="color: #cbd5e1; margin: 10px 0 0; font-size: 12px;">Yangon, Myanmar</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
        print(f"✅ Welcome email sent to {user.email}")
        
    except Exception as e:
        print(f"❌ Failed to send email to {user.email}: {str(e)}")