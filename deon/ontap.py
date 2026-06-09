def menu():
    print("""
========== QUẢN LÝ THÔNG TIN CHUYẾN XE ==========
1. Hiển thị danh sách chuyến xe
2. Khai báo xe mới
3. Cập nhật đặt vé
4. Hủy chuyến xe
5. Tìm kiếm chuyến xe
6. Thống kê trạng thái chuyến xe
7. Phân loại trạng thái tự động
8. Thoát chương trình
=================================================""")
    
def get_validate_input(prompt : str,type_input : str = "str"):
    while True:
        user_input = input(prompt)
        if not user_input:
            print("Không được để trống")
            continue

        if type_input == "int":
            if user_input.isdigit():
                value = int(user_input)
                return value
            else:
                print("Dữ liệu không hợp lệ")
                continue
        return user_input
    
def show_trip_list(list):
    if len(list) == 0:
        print("Không có chuyến xe")
    else:
        print(f"{'Mã CX':<7} | {'Tuyến đường':<20} | {'Giá vé':<10} | {'Ghế trống':<10} | {'Tổng số ghế':<12} | {'Doanh thu hiện tại':<20} | {'Trạng thái lắp đầy':<10}")
        for item in list:
            print(f"{item.get('id'):<7} | {item.get('route'):<20} | {item.get('price'):<10} | {item.get('empty_seats'):<10} | {item.get('total_seats'):<12} | {item.get('revenue'):<20} | {item.get('status'):<10}")

def declaring_trip(list):
    while True:
        id = get_validate_input("Nhập mã CX: ")
        for item in list:
            if item.get("id") == id:
                print("Mã chuyến xe không được trùng lặp")
                break
        else:
            break
    route = get_validate_input("Nhập tuyến đường: ")
    price = get_validate_input("Nhập giá vé: ","int")
    total_seats = get_validate_input("Nhập tổng số ghế: ","int")
    list.append({"id":id,"route":route,"price":price,"empty_seats":total_seats,"total_seats":total_seats,"revenue":0,"status":"Ế khách"})

def update_trip(list):
    id = get_validate_input("Nhập mã CX: ")
    for item in list:
        if item.get("id")==id:
            quantity_seats = get_validate_input("Nhập số ghế muốn đặt: ")
            if int(quantity_seats) > item.get("empty_seats"):
                print("Số vé nhiều hơn số ghế trống")
                break
            else:
                quantity_seats = int(quantity_seats)
                item["empty_seats"]=item.get("empty_seats")-quantity_seats
                item["revenue"]=item.get("price")*quantity_seats
                if item.get("empty_seats") == 0:
                    item["status"] = "Hết vé"
                elif item.get("empty_seats")/item.get("total_seats") < 0.15:
                    item["status"] = "Hút khách (Cần tăng cường)"
                elif item.get("empty_seats")/item.get("total_seats") >= 0.15 and item.get("empty_seats")/item.get("total_seats") <= 0.8:
                    item["status"] = "Bình thường"
                else:
                    item["status"] = "Ế khách"
                break

def main():
    trip_list=[
        {"id":"CX001","route":"Sài Gòn - Đà Lạt","price":300000,"empty_seats":5,"total_seats":40,"revenue":10500000,"status":"Hút khách"},
        {"id":"CX002","route":"Sài Gòn - Kon Tum","price":200000,"empty_seats":10,"total_seats":30,"revenue":14000000,"status":"Hút khách"}
    ]
    while True:
        menu()
        choice = input("Nhập lựa chọn: ")
        match choice:
            case "1":
                show_trip_list(trip_list)
            case "2":
                declaring_trip(trip_list)
            case "3":
                update_trip(trip_list)
            case "8":
                break
            case _:
                print("Lựa chọn không hợp lệ")
                
main()