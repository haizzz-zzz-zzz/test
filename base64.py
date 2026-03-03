import os

def decode_hex_to_file(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Lỗi: Không tìm thấy file '{input_file}'")
        return

    try:
        # 1. Đọc chuỗi Hex từ file
        with open(input_file, 'r', encoding='utf-8') as f_in:
            # Đọc toàn bộ file
            hex_data = f_in.read()
            
            # QUAN TRỌNG: Loại bỏ khoảng trắng và xuống dòng (nếu có) 
            # để đảm bảo chuỗi Hex liền mạch.
            hex_data = hex_data.replace(' ', '').replace('\n', '').replace('\r', '')

        # 2. Giải mã Hex sang Bytes
        # Hàm bytes.fromhex() rất mạnh, nó tự chuyển chuỗi Hex thành dữ liệu gốc
        decoded_bytes = bytes.fromhex(hex_data)

        # 3. Ghi dữ liệu gốc ra file out.txt
        # Dùng 'wb' (Write Binary) để an toàn cho mọi loại file (ảnh, exe, text...)
        with open(output_file, 'wb') as f_out:
            f_out.write(decoded_bytes)

        print(f"✅ Đã giải mã Hex thành công! Kiểm tra file '{output_file}'")

    except ValueError:
        print("❌ Lỗi: Chuỗi trong in.txt không phải là Hex hợp lệ (hoặc độ dài bị lẻ).")
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")

# Chạy hàm
decode_hex_to_file('in.txt', 'out.txt')