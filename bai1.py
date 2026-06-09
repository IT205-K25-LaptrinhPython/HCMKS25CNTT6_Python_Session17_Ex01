# Tại sao maketrans và translate lại nhanh hơn vòng lặp thông thường?
# Vòng lặp for + replace(): Khi bạn dùng vòng lặp duyệt qua từng ký tự rác (ví dụ: !, @, #, $) và gọi 
# replace(), Python sẽ phải quét lại toàn bộ chuỗi string từ đầu đến cuối cho mỗi ký tự cần xóa. 
# Điều này tạo ra độ phức tạp 
# .str.maketrans() và str.translate(): * maketrans tạo ra một bảng ánh xạ (mapping table) 
# (dưới dạng dictionary nối các mã Unicode của ký tự với giá trị đích - ở đây là None nếu muốn xóa).
#  Khi gọi translate(), Python sẽ đẩy tác vụ này xuống tầng ngôn ngữ C (ngôn ngữ lõi của Python). Trình 
# thông dịch C chỉ quét qua chuỗi đúng một lần duy nhất ($O(N)$). Với mỗi ký tự, nó tra cứu (look-up) 
# trong bảng ánh xạ với tốc độ cực nhanh ($O(1)$) để quyết định giữ lại hay loại bỏ ký tự đó. Do đó, 
# kỹ thuật này tối ưu hơn hẳn về mặt bộ nhớ và thời gian thực thi, đặc biệt khi xử lý hàng triệu dòng log.


raw_logs = []
processed_logs = []

def clean_raw_logs(input_string):
    """
    (Chức năng 1)
    Làm sạch dữ liệu log thô bằng str.maketrans và str.translate để loại bỏ '!@#$'.
    Tách các log bằng split(';') và lưu vào danh sách raw_logs.
    """
    global raw_logs
    
    translation_table = str.maketrans('', '', '!@#$')
    
    cleaned_string = input_string.translate(translation_table)
    
    raw_logs = [log.strip() for log in cleaned_string.split(';') if log.strip()]
    
    print(f"Đã làm sạch và lưu {len(raw_logs)} dòng log vào hệ thống.")

def filter_critical_logs():
    """
    (Chức năng 2)
    Sử dụng List Comprehension để lọc ra các log chứa 'ERROR' hoặc 'CRITICAL'.
    Xử lý Edge Case: Cảnh báo nếu raw_logs rỗng.
    """
    global raw_logs, processed_logs
    
    if not raw_logs:
        print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.")
        return

    processed_logs = [
        log for log in raw_logs 
        if "ERROR" in log.upper() or "CRITICAL" in log.upper()
    ]
    
    print("--- LỌC CẢNH BÁO ---")
    print(f"Tìm thấy {len(processed_logs)} cảnh báo nguy hiểm:")
    for log in processed_logs:
        print(f"- {log}")

def is_ip_address(word):
    """
    Hàm phụ trợ: Kiểm tra xem một chuỗi có mang định dạng IPv4 không.
    """
    parts = word.split('.')
    return len(parts) == 4 and all(part.isdigit() for part in parts)

def mask_ip_addresses():
    """
    (Chức năng 3)
    Duyệt processed_logs, tách chuỗi để tìm IP, mã hóa 2 dải số cuối (*.*).
    Xử lý Edge Case: Báo lỗi nếu chưa có raw_logs, không làm sập chương trình nếu không có IP.
    """
    global raw_logs, processed_logs
    
    if not raw_logs:
        print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1.")
        return []
    
    masked_logs = []
    
    for log in processed_logs:
        words = log.split()
        masked_log = log
        
        for word in words:
            if is_ip_address(word):
                # Tách IP ra để ghép lại theo format masking
                parts = word.split('.')
                masked_ip = ".".join([parts[0], parts[1], "*", "*"])
                # Thay thế IP gốc bằng IP đã được che giấu
                masked_log = masked_log.replace(word, masked_ip)
        
        masked_logs.append(masked_log)
    
    print("--- MÃ HÓA IP ---")
    print("Báo cáo log an toàn:")
    if not masked_logs:
         print("(Không có dữ liệu log cảnh báo để mã hóa)")
    else:
        for i, log in enumerate(masked_logs, 1):
            print(f"{i}. {log}")
            
    return masked_logs

def run_system():
    """
    (Chức năng 4)
    Vòng lặp giao diện dòng lệnh (CLI) chính của hệ thống.
    """
    while True:
        print("\n============= SECURITY LOG ANALYZER =============")
        print("1. Nhập và làm sạch dữ liệu Log thô")
        print("2. Lọc các Log cảnh báo mức độ cao (ERROR/CRITICAL)")
        print("3. Mã hóa địa chỉ IP (Masking)")
        print("4. Đóng hệ thống")
        print("=================================================")
        
        choice = input("Chọn chức năng (1-4): ")
        match choice:
            case '1':
                print("--- NẠP DỮ LIỆU LOG ---")
                raw_data = input("Nhập chuỗi log thô (cách nhau bởi dấu ;): ")
                clean_raw_logs(raw_data)
                
            case '2':
                filter_critical_logs()
                
            case '3':
                mask_ip_addresses()
                
            case '4':
                print("Đang đóng hệ thống... Hoàn tất.")
                break
                
            case _:
                print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 4.")

run_system()