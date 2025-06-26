import sys
print(sys.executable)
print(sys.version)

import qrcode

upi_id = input("Enter your UPI ID: ")

phonepe_url = f"upi://pay?pa={upi_id}&pn=PhonePe&mc=1234&tid=1234567890&am=1.00&cu=INR&url=https://www.phonepe.com"
google_pay_url = f"upi://pay?pa={upi_id}&pn=Google Pay&mc=1234&tid=1234567890&am=1.00&cu=INR&url=https://pay.google.com"
paytm_url = f"upi://pay?pa={upi_id}&pn=Paytm&mc=1234&tid=1234567890&am=1.00&cu=INR&url=https://paytm.com"

# Generate QR codes
phonepe_qr = qrcode.make(phonepe_url)
google_pay_qr = qrcode.make(google_pay_url) 
paytm_qr = qrcode.make(paytm_url)

# Save QR codes to files
phonepe_qr.save("phonepe_qr.png")
google_pay_qr.save("google_pay_qr.png")
paytm_qr.save("paytm_qr.png")

phonepe_qr.show()
google_pay_qr.show()
paytm_qr.show()
