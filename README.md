# Vietnam Payroll Calculator

Hệ thống tính lương tự động theo quy định Việt Nam, xây dựng bằng Python.

## Chức năng

- Tính BHXH (8%), BHYT (1.5%), BHTN (1%) theo mức trần hiện hành
- Tính thuế TNCN theo biểu lũy tiến 5 bậc (Luật Thuế TNCN)
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

## Quy định pháp lý áp dụng (Luật Thuế TNCN 2025 (109/2025/QH15) & Nghị quyết 110/2025/UBTVQH15, kỳ tính thuế 2026)

| Khoản mục | Tỷ lệ | Mức trần |
|---|---|---|
| BHXH (hưu trí + tử tuất) | 8% | 50,600,000 đ/tháng | #(Mức cũ: 46,800,000 đ/tháng)
| BHYT | 1.5% |  50,600,000 đ/tháng | #Mức cũ: 46,800,000 đ/tháng)
| BHTN | 1% |  106,200,000 đ/tháng | #Mức cũ: 99,200,000 đ/tháng)
| Giảm trừ bản thân | — | 15,500,000 đ/tháng |
| Giảm trừ NPT | — | 6,200,000 đ/người/tháng |

## Biểu thuế TNCN (tính theo tháng)

| Bậc | Thu nhập chịu thuế | Thuế suất |
|---|---|---|
| 1 | ≤ 10 triệu | 5% |
| 2 | 10 – 30 triệu | 10% |
| 3 | 30 – 60 triệu | 20% |
| 4 | 60 – 100 triệu | 30% |
| 5 | > 100 triệu | 35% |

## Công thức tính

```
Thu nhập chịu thuế (TNCT) = Gross - BHXH - BHYT - BHTN
                           - Giảm trừ bản thân (15.5tr)
                           - Giảm trừ NPT (6.2tr × số NPT)
                           - Phụ cấp miễn thuế

Lương NET = Gross - (BHXH + BHYT + BHTN) - Thuế TNCN
```

## Tài liệu pháp lý tham chiếu

- Luật Thuế TNCN số 04/2007/QH12 và các văn bản sửa đổi
- Nghị định 65/2013/NĐ-CP hướng dẫn thi hành Luật Thuế TNCN
- Thông tư 111/2013/TT-BTC (sửa đổi bởi Nghị quyết 954/2020/UBTVQH14) - Thay thế bở NQ 110/2025/UBTVQH15
- Luật BHXH số 41/2024/QH15 - Luật BHXH
- Nghị định 293/2025/NĐ-CP — Lương tối thiểu vùng (Vùng I 5,310,000) thay đổi từ 1/7/2026, có hiệu lực từ 1/1/2026
- Lương cơ sở: ghi riêng "2,340,000 (NĐ 73/2024) đến 30/6/2026; # Dự thảo 2,530,000 từ 1/7/2026" .
- Quyết định 595/QĐ-BHXH 2017
- Luật 109/2025/QH15 - Luật thuế thu nhập cá nhân
