"""
Vietnam Payroll Calculator - calculator.py
Tính lương theo quy định Việt Nam (cập nhật 7/2026)

Tài liệu pháp lý:
- Luật Thuế TNCN số 04/2007/QH12 và các văn bản sửa đổi
- Nghị định 65/2013/NĐ-CP hướng dẫn thi hành Luật Thuế TNCN
- Thông tư 111/2013/TT-BTC (sửa đổi bởi Nghị quyết 954/2020/UBTVQH14) - Thay thế bở NQ 110/2025/UBTVQH15
- Luật BHXH số 41/2024/QH15 - Luật BHXH
- Nghị định 293/2025/NĐ-CP — Lương tối thiểu vùng (Vùng I 5,310,000) thay đổi từ 1/7/2026, có hiệu lực từ 1/1/2026
- NĐ 161/2026/NĐ-CP - Lương cơ sở: 2,340,000 (NĐ 73/2024) đến 30/6/2026; từ 1/7/2026: 2,530,000.
- Quyết định 595/QĐ-BHXH 2017
- Luật 109/2025/QH15 - Luật thuế thu nhập cá nhân
"""

# ============================================================
# HẰNG SỐ THEO QUY ĐỊNH PHÁP LUẬT (cập nhật 7/2024)
# ============================================================

# Giảm trừ gia cảnh (Thông tư 111/2013/TT-BTC, sửa đổi 2020)
PERSONAL_DEDUCTION = 15_500_000     # 15 triệu 500 đồng/tháng (bản thân)
DEPENDENT_DEDUCTION = 6_200_000     # 6.2 triệu đồng/tháng/người phụ thuộc

# Mức đóng BHXH/BHYT/BHTN (phần người lao động)
BHXH_RATE = 0.08    # 8% vào quỹ hưu trí và tử tuất
BHYT_RATE = 0.015   # 1.5% bảo hiểm y tế
BHTN_RATE = 0.01    # 1% bảo hiểm thất nghiệp

# Mức trần đóng BHXH/BHYT = 20 × lương cơ sở (2,340,000 từ 1/7/2024)
BHXH_CAP = 20 * 2_340_000   # 46,800,000 đồng/tháng

# Mức trần đóng BHTN = 20 × lương tối thiểu vùng I (4,960,000 từ 1/7/2024)
BHTN_CAP = 20 * 4_960_000   # 99,200,000 đồng/tháng

# Biểu thuế TNCN lũy tiến từng phần (Điều 22, Luật Thuế TNCN)
# Mỗi phần tử: (khoảng thu nhập chịu thuế của bậc, thuế suất)
# Tính theo tháng (bằng 1/12 biểu thuế năm)
PIT_BRACKETS = [
    (10_000_000,     0.05),   # Bậc 1: ≤ 10 triệu → 5%
    (20_000_000,     0.10),   # Bậc 2: 10–30 triệu → 10%
    (30_000_000,     0.20),   # Bậc 3: 30–60 triệu → 20%
    (40_000_000,    0.30),   # Bậc 4: 60–100 triệu → 30%
    (float('inf'), 0.35),   # Bậc 7: > 100 triệu → 35%
]


# ============================================================
# HÀM TÍNH BẢO HIỂM XÃ HỘI
# ============================================================

def calculate_insurance(gross_salary: float) -> dict:
    """
    Tính các khoản trừ bảo hiểm (phần người lao động đóng).

    Args:
        gross_salary: Lương gross tháng (đồng)

    Returns:
        dict với bhxh, bhyt, bhtn, total
    """
    # Áp dụng mức trần trước khi nhân tỷ lệ
    bhxh_base = min(gross_salary, BHXH_CAP)
    bhtn_base = min(gross_salary, BHTN_CAP)

    bhxh = bhxh_base * BHXH_RATE
    bhyt = bhxh_base * BHYT_RATE   # BHYT dùng cùng trần với BHXH
    bhtn = bhtn_base * BHTN_RATE

    return {
        'bhxh': bhxh,
        'bhyt': bhyt,
        'bhtn': bhtn,
        'total': bhxh + bhyt + bhtn,
    }


# ============================================================
# HÀM TÍNH THUẾ TNCN (7 BẬC LŨY TIẾN)
# ============================================================

def calculate_pit(taxable_income: float) -> float:
    """
    Tính thuế TNCN theo phương pháp lũy tiến từng phần.

    Args:
        taxable_income: Thu nhập chịu thuế sau giảm trừ (đồng)

    Returns:
        Số thuế TNCN phải nộp (đồng)
    """
    if taxable_income <= 0:
        return 0.0

    pit = 0.0
    remaining = taxable_income

    for bracket_size, rate in PIT_BRACKETS:
        if remaining <= 0:
            break
        # Phần thu nhập tính thuế tại bậc này
        taxable_at_bracket = min(remaining, bracket_size)
        pit += taxable_at_bracket * rate
        remaining -= taxable_at_bracket

    return pit


# ============================================================
# HÀM TÍNH LƯƠNG CHO TỪNG NHÂN VIÊN
# ============================================================

def calculate_employee_payroll(employee: dict) -> dict:
    """
    Tính toàn bộ bảng lương cho một nhân viên.

    Args:
        employee: dict với các key:
            - id (str): Mã nhân viên
            - name (str): Họ và tên
            - gross_salary (float): Lương gross tháng
            - dependents (int): Số người phụ thuộc đã đăng ký
            - allowance (float, optional): Phụ cấp không tính thuế (mặc định 0)

    Returns:
        dict chứa toàn bộ kết quả tính lương
    """
    gross = float(employee['gross_salary'])
    dependents = int(employee.get('dependents', 0))
    allowance = float(employee.get('allowance', 0))  # Phụ cấp miễn thuế (ăn ca, xăng xe...)

    # Bước 1: Tính bảo hiểm
    insurance = calculate_insurance(gross)

    # Bước 2: Tính thu nhập chịu thuế
    # TNCT = Gross - Bảo hiểm - Giảm trừ bản thân - Giảm trừ người phụ thuộc - Phụ cấp miễn thuế
    deduction_personal = PERSONAL_DEDUCTION
    deduction_dependent = dependents * DEPENDENT_DEDUCTION
    taxable_income = gross - insurance['total'] - deduction_personal - deduction_dependent - allowance
    taxable_income = max(0, taxable_income)  # Không âm

    # Bước 3: Tính thuế TNCN
    pit = calculate_pit(taxable_income)

    # Bước 4: Tính lương net
    net_salary = gross - insurance['total'] - pit

    return {
        'id':                   employee['id'],
        'name':                 employee['name'],
        'gross_salary':         gross,
        'allowance':            allowance,
        'bhxh':                 insurance['bhxh'],
        'bhyt':                 insurance['bhyt'],
        'bhtn':                 insurance['bhtn'],
        'total_insurance':      insurance['total'],
        'deduction_personal':   deduction_personal,
        'deduction_dependent':  deduction_dependent,
        'dependents':           dependents,
        'taxable_income':       taxable_income,
        'pit':                  pit,
        'net_salary':           net_salary,
    }


# ============================================================
# XỬ LÝ TOÀN BỘ DANH SÁCH NHÂN VIÊN
# ============================================================

def calculate_payroll(employees: list) -> list:
    """
    Tính lương cho toàn bộ danh sách nhân viên.

    Args:
        employees: List các dict nhân viên

    Returns:
        List kết quả tính lương từng người
    """
    return [calculate_employee_payroll(emp) for emp in employees]
