import qrcode
import pyqrcode
import png
if 1==1:   
    s = f"""Bus:1234,
            From: bang,
            to:hyd,
            status: confirmed"""
    img=qrcode.make(s)
    destination = f"D:/Project_app/project/website/static/tickets/ticket.png"
    img.save(destination)