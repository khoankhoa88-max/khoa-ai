from sympy import *
import re

x = symbols('x')

print("=" * 50)
print("AI TOÁN + VẬT LÝ MINI")
print("Gõ 'thoat' để thoát")
print("=" * 50)

while True:

    cau_hoi = input("\nBạn: ").lower().strip()

    if cau_hoi == "thoat":
        print("AI: Tạm biệt!")
        break

    try:

        # PHƯƠNG TRÌNH
        if "giải" in cau_hoi and "=" in cau_hoi:

            pt = cau_hoi.replace("giải", "").strip()

            trai, phai = pt.split("=")

            eq = Eq(sympify(trai), sympify(phai))

            kq = solve(eq, x)

            print("AI:", kq)

        # ĐẠO HÀM
        elif "đạo hàm" in cau_hoi:

            bieu_thuc = cau_hoi.replace("đạo hàm", "").strip()

            expr = sympify(bieu_thuc)

            print("AI:", diff(expr, x))

        # TÍCH PHÂN
        elif "tích phân" in cau_hoi:

            bieu_thuc = cau_hoi.replace("tích phân", "").strip()

            expr = sympify(bieu_thuc)

            print("AI:", integrate(expr, x))

        # VẬN TỐC
        elif cau_hoi == "vận tốc":

            s = float(input("Quãng đường (m): "))
            t = float(input("Thời gian (s): "))

            print("AI: Vận tốc =", s / t, "m/s")

        # LỰC
        elif cau_hoi == "lực":

            m = float(input("Khối lượng (kg): "))
            a = float(input("Gia tốc (m/s²): "))

            print("AI: Lực =", m * a, "N")

        # CÔNG
        elif cau_hoi == "công":

            F = float(input("Lực (N): "))
            s = float(input("Quãng đường (m): "))

            print("AI: Công =", F * s, "J")

        # TOÁN CƠ BẢN
        elif re.search(r'[0-9]', cau_hoi):

            kq = eval(cau_hoi)

            print("AI:", kq)

        # CHÀO HỎI
        elif "xin chào" in cau_hoi:
            print("AI: Xin chào!")

        elif "bạn là ai" in cau_hoi:
            print("AI: Tôi là AI Toán và Vật Lý Mini.")

        else:
            print("AI: Tôi chưa hiểu câu hỏi.")

    except Exception as e:
        print("AI: Lỗi:", e)