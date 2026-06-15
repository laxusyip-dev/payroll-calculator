# Vietnam Payroll Calculator

Hệ thống tính lương tự động theo quy định Việt Nam, xây dựng bằng Python.

## Chức năng

- Tính BHXH (8%), BHYT (1.5%), BHTN (1%) theo mức trần hiện hành
- Tính thuế TNCN theo biểu lũy tiến 7 bậc (Luật Thuế TNCN)
- Hỗ trợ giảm trừ gia cảnh và người phụ thuộc (NPT)
- Hỗ trợ phụ cấp miễn thuế (ăn ca, xăng xe, điện thoại...)
- Xuất báo cáo Excel chuyên nghiệp: Bảng lương tổng hợp + Phiếu lương cá nhân

## Cấu trúc dự án

```
vietnam-payroll-calculator/
├── calculator.py   # Logic tính lương (BHXH, BHYT, BHTN, PIT)
├── report.py       # Xuất báo cáo Excel (openpyxl)
├── main.py         # File chạy chính — nhập dữ liệu NV tại đây
└── README.md
```

## Cài đặt

```bash
pip install openpyxl
python main.py
```

## Quy định pháp lý áp dụng (cập nhật 7/2024)

| Khoản mục | Tỷ lệ | Mức trần |
|---|---|---|
| BHXH (hưu trí + tử tuất) | 8% | 46,800,000 đ/tháng |
| BHYT | 1.5% | 46,800,000 đ/tháng |
| BHTN | 1% | 99,200,000 đ/tháng |
| Giảm trừ bản thân | — | 11,000,000 đ/tháng |
| Giảm trừ NPT | — | 4,400,000 đ/người/tháng |

## Biểu thuế TNCN (tính theo tháng)

| Bậc | Thu nhập chịu thuế | Thuế suất |
|---|---|---|
| 1 | ≤ 5 triệu | 5% |
| 2 | 5 – 10 triệu | 10% |
| 3 | 10 – 18 triệu | 15% |
| 4 | 18 – 32 triệu | 20% |
| 5 | 32 – 52 triệu | 25% |
| 6 | 52 – 80 triệu | 30% |
| 7 | > 80 triệu | 35% |

## Công thức tính

```
Thu nhập chịu thuế (TNCT) = Gross - BHXH - BHYT - BHTN
                           - Giảm trừ bản thân (11tr)
                           - Giảm trừ NPT (4.4tr × số NPT)
                           - Phụ cấp miễn thuế

Lương NET = Gross - (BHXH + BHYT + BHTN) - Thuế TNCN
```

## Tài liệu pháp lý tham chiếu

- Luật Thuế TNCN số 04/2007/QH12 và các văn bản sửa đổi
- Nghị định 65/2013/NĐ-CP hướng dẫn thi hành Luật Thuế TNCN
- Thông tư 111/2013/TT-BTC (sửa đổi bởi Nghị quyết 954/2020/UBTVQH14)
- Luật BHXH số 58/2014/QH13
- Nghị định 74/2024/NĐ-CP — Lương tối thiểu vùng từ 1/7/2024
- Nghị định 73/2024/NĐ-CP — Lương cơ sở 2,340,000đ từ 1/7/2024
