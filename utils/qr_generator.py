import qrcode

def generate_qr(url, filename='static/qr_code.png'):
    """
    Generate a QR code image for the given URL and save it to filename.
    """
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

