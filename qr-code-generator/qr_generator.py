
import qrcode

x = qrcode.QRCode()
msg = "HEY BUDDY BE HAPPY"

x.add_data(msg)
x.make(fit=True)

res = x.make_image(fill_color="black", back_color="white")
res.save("Alwina.png")

print("CREATED SUCCESSFULLY!!!")
