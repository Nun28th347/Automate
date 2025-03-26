import tkinter as tk            #GUI
import subprocess               #run cmd
import sys                      #OS pip install openpyxl
import os                       #path
from PIL import Image, ImageTk  # เพิ่มสำหรับใส่รูป
"""
    pip install playwright
    pip install pytest
    pip install pillow
    pip install openpyxl

"""


class PlaywrightTestUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playwright Test Runner")   #name window
        self.root.geometry("800x650")               # screen size
        self.root.configure(bg="#2C3E50")           # พื้นหลังสีเทา

        # โหลดและวางรูปจากโฟลเดอร์ที่กำหนด
        avatar1_path = r"C:\Users\Admin\Desktop\playwright_pytest\picture\avatar1.jpg"
        avatar2_path = r"C:\Users\Admin\Desktop\playwright_pytest\picture\avatar2.png"
        avatar3_path = r"C:\Users\Admin\Desktop\playwright_pytest\picture\avatar3.png"

        # size
        self.avatar1_img = ImageTk.PhotoImage(Image.open(avatar1_path).resize((100, 100)))
        self.avatar2_img = ImageTk.PhotoImage(Image.open(avatar2_path).resize((100, 100)))
        self.avatar3_img = ImageTk.PhotoImage(Image.open(avatar3_path).resize((100, 100)))

        # location  
        self.left_avatar_top = tk.Label(root, image=self.avatar1_img, bg="#2C3E50")
        self.left_avatar_top.place(x=50, y=40)

        self.right_avatar_top = tk.Label(root, image=self.avatar1_img, bg="#2C3E50")
        self.right_avatar_top.place(x=600, y=40)

        self.left_avatar_middle = tk.Label(root, image=self.avatar2_img, bg="#2C3E50")
        self.left_avatar_middle.place(x=50, y=270)

        self.right_avatar_middle = tk.Label(root, image=self.avatar2_img, bg="#2C3E50")
        self.right_avatar_middle.place(x=600, y=270)

        self.left_avatar_bottom = tk.Label(root, image=self.avatar3_img, bg="#2C3E50")
        self.left_avatar_bottom.place(x=50, y=500)

        self.right_avatar_bottom = tk.Label(root, image=self.avatar3_img, bg="#2C3E50")
        self.right_avatar_bottom.place(x=600, y=500)



        """ BTN start """
        
        # ปุ่มรัน login test
        self.login_button = tk.Button(
            root, text="Login Tests", command=self.run_login_tests, height=6, width=27,
            font=("Comic Sans MS", 14, "bold"), bg="#1ABC9C", fg="white", activebackground="#16A085",
            activeforeground="white", relief="raised", bd=4
        )
        self.login_button.pack(pady=15)

        # ปุ่มรัน logout test
        self.logout_button = tk.Button(
            root, text="Logout Test", command=self.run_logout_test, height=6, width=27,
            font=("Comic Sans MS", 14, "bold"), bg="#3498DB", fg="white", activebackground="#2980B9",
            activeforeground="white", relief="raised", bd=4
        )
        self.logout_button.pack(pady=15)

        # ปุ่มออกจากโปรแกรม
        self.exit_button = tk.Button(
            root, text="Close Programs", command=self.root.quit, height=6, width=27,
            font=("Comic Sans MS", 14, "bold"), bg="#E74C3C", fg="white", activebackground="#C0392B",
            activeforeground="white", relief="raised", bd=4
        )
        self.exit_button.pack(pady=15)
        
        """ BTN end """

    """ RUN command"""
    def run_login_tests(self):
        if sys.platform.startswith('win'):
            subprocess.Popen(["cmd", "/k", "pytest test_login01.py --headed"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", "pytest test_login01.py"])

    def run_logout_test(self):
        if sys.platform.startswith('win'):
            subprocess.Popen(["cmd", "/k", "pytest test_logout01.py --headed"])
        else:
            subprocess.Popen(["x-terminal-emulator", "-e", "pytest test_logout01.py"])

if __name__ == "__main__":            # start program
    root = tk.Tk()
    app = PlaywrightTestUI(root)
    root.mainloop()