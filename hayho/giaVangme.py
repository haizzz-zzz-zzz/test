import httpx
from datetime import datetime

def gia_vang(date):
    # URL của API đã tìm thấy trong Burp Suite
    url = "https://sjc.com.vn/GoldPrice/Services/PriceService.ashx"  # Thay thế bằng URL thực tế

    # Gửi yêu cầu GET tới API
    response = httpx.get(url)
    
    # Kiểm tra xem yêu cầu có thành công không
    if response.status_code != 200:
        return {"error": "Không thể lấy dữ liệu từ API."}
    
    # Phân tích dữ liệu JSON
    data = response.json()
    
    # Kiểm tra xem dữ liệu có thành công không
    if not data.get("success"):
        return {"error": "Dữ liệu không hợp lệ."}
    
    # Khởi tạo biến để lưu giá vàng
    gia_vang_data = {}
    
    # Lấy ngày hôm nay
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Duyệt qua dữ liệu để tìm giá vàng
    for item in data["data"]:
        if item["BranchName"] == "Hồ Chí Minh" and item["TypeName"] == "Vàng SJC 1L, 10L, 1KG":
            # Lưu giá bán vào từ điển
            gia_vang_data[today] = int(item["SellValue"])
            break  # Chỉ cần lấy giá của ngày hôm nay

    return gia_vang_data

# Gọi hàm và in kết quả
date= today = datetime.now()
result = gia_vang(date)
print(result)