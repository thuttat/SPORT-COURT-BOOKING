import datetime
import hashlib
import hmac

import urllib



def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def calculate_duration(start_time, end_time):
    dummy_date = datetime.datetime.today()
    dt_start = datetime.datetime.combine(dummy_date, start_time)
    dt_end = datetime.datetime.combine(dummy_date, end_time)  
    if dt_end < dt_start:
        dt_end += datetime.timedelta(days=1)
    return (dt_end - dt_start).total_seconds() / 3600.0

####################################
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_IMAGE_SIZE = 20 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    if not file or not file.filename:
        return False, "No file provided"

    if not allowed_file(file.filename):
        return False, "Invalid file type! Only PNG, JPG, JPEG are allowed."

    file.seek(0, 2)         
    size = file.tell()      
    file.seek(0)             

    if size > MAX_IMAGE_SIZE:
        return False, "This picture is too big"

    if size == 0:
        return False, "File is empty!"

    return True, None




#################################################################

def generate_vnpay_url(booking, ip_address):
    vnp_TmnCode = "IVN0ZMWM"
    vnp_HashSecret = "DWNZDYT99VTGXXDDMD59VNBGR6ROY5HP"
    vnp_Url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    vnp_Returnurl = "http://127.0.0.1:5000/payment" 
    
    inputData = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": vnp_TmnCode,
        "vnp_Amount": int(booking.total_price * 100), 
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": str(booking.id), 
        "vnp_OrderInfo": f"Thanh toan san bong don hang {booking.id}",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": vnp_Returnurl,
        "vnp_IpAddr": ip_address,
        "vnp_CreateDate": datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    }

    keys = sorted(inputData.keys())
    qs = ''
    hasData = ''
    for key in keys:
        value = str(inputData[key])
        qs = qs + urllib.parse.quote_plus(key) + '=' + urllib.parse.quote_plus(value) + '&'
        hasData = hasData + str(key) + '=' + str(value) + '&'
    
    hasData = hasData[:-1]
    qs = qs[:-1]

    hashValue = hmac.new(bytes(vnp_HashSecret, 'utf-8'), bytes(qs, 'utf-8'), hashlib.sha512).hexdigest()
    return vnp_Url + "?" + qs + '&vnp_SecureHash=' + hashValue


