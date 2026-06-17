"""
Vietnam Payroll Calculator - main.py
File chạy chính. Nhập dữ liệu nhân viên và xuất báo cáo lương.

Cách dùng:
    python main.py

Output:
    payroll_report_YYYYMM.xlsx trong thư mục hiện tại
"""

from calculator import calculate_payroll
from report import generate_excel_report
from datetime import datetime

# ============================================================
# DỮ LIỆU NHÂN VIÊN MẪU
# ============================================================
# Mỗi nhân viên cần có:
#   id          : Mã nhân viên (string)
#   name        : Họ và tên đầy đủ
#   gross_salary: Lương gross tháng (đồng)
#   dependents  : Số người phụ thuộc đã đăng ký giảm trừ
#   allowance   : Phụ cấp miễn thuế (ăn ca, xăng xe, điện thoại...) — mặc định 0

EMPLOYEES = [
    {
        'id': 'NV001',
        'name': 'Nguyễn Văn An',
        'gross_salary': 8_000_000,
        'dependents': 0,
        'allowance': 700_000,       # Phụ cấp ăn ca 730k/tháng (miễn thuế ≤730k)
    },
    {
        'id': 'NV002',
        'name': 'Trần Thị Bình',
        'gross_salary': 15_000_000,
        'dependents': 1,
        'allowance': 730_000,
    },
    {
        'id': 'NV003',
        'name': 'Lê Minh Cường',
        'gross_salary': 25_000_000,
        'dependents': 2,
        'allowance': 1_500_000,    # Phụ cấp xăng + điện thoại
    },
    {
        'id': 'NV004',
        'name': 'Phạm Thu Hà',
        'gross_salary': 40_000_000,
        'dependents': 1,
        'allowance': 2_000_000,
    },
    {
        'id': 'NV005',
        'name': 'Hoàng Đức Long',
        'gross_salary': 60_000_000,
        'dependents': 3,
        'allowance': 2_000_000,
    },
    {
        'id': 'NV006',
        'name': 'Vũ Thị Mai',
        'gross_salary': 5_500_000,
        'dependents': 0,
        'allowance': 0,
    },
    {
        'id': 'NV007',
        'name': 'Đặng Quốc Tuấn',
        'gross_salary': 90_000_000,
        'dependents': 2,
        'allowance': 3_000_000,
    },
    {
        'id': 'NV008',
        'name': 'Bùi Lan Anh',
        'gross_salary': 12_000_000,
        'dependents': 0,
        'allowance': 730_000,
    },
]

# ============================================================
# CHẠY TÍNH LƯƠNG VÀ XUẤT BÁO CÁO
# ============================================================

def main():
    # Tháng tính lương — có thể thay đổi tại đây
    pay_month = datetime.now().month
    pay_year  = datetime.now().year

    print(f"🔄 Đang tính lương tháng {pay_month:02d}/{pay_year}...")
    print(f"   Tổng số nhân viên: {len(EMPLOYEES)}")
    print()

    # Bước 1: Tính lương
    results = calculate_payroll(EMPLOYEES)

    # Bước 2: In tóm tắt ra terminal
    print(f"{'Mã NV':<8} {'Họ Tên':<22} {'Gross':>14} {'BH':>10} {'TNCN':>12} {'NET':>14}")
    print("-" * 85)
    for r in results:
        print(f"{r['id']:<8} {r['name']:<22} "
              f"{r['gross_salary']:>14,.0f} "
              f"{r['total_insurance']:>10,.0f} "
              f"{r['pit']:>12,.0f} "
              f"{r['net_salary']:>14,.0f}")
    print("-" * 85)

    total_gross  = sum(r['gross_salary'] for r in results)
    total_ins    = sum(r['total_insurance'] for r in results)
    total_pit    = sum(r['pit'] for r in results)
    total_net    = sum(r['net_salary'] for r in results)
    print(f"{'TỔNG CỘNG':<30} {total_gross:>14,.0f} "
          f"{total_ins:>10,.0f} {total_pit:>12,.0f} {total_net:>14,.0f}")
    print()

    # Bước 3: Xuất Excel
    output_file = f"/mnt/user-data/outputs/payroll_report_{pay_year}{pay_month:02d}.xlsx"
    generate_excel_report(results, pay_month, pay_year, output_file)

if __name__ == "__main__":
    main()
