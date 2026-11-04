# Website Vân Phong

Trang web Công ty TNHH Kỹ thuật và Thương mại Vân Phong – https://www.vanphongtechco.com.vn

Web gồm 3 thứ tiếng: tiếng Việt (`/`), tiếng Anh (`/en/`), tiếng Trung (`/zh/`).
Mỗi lần đẩy thay đổi lên nhánh `main`, web tự cập nhật sau khoảng 1–2 phút (GitHub Pages).

---

## 1. Nguyên tắc quan trọng nhất

**Chỉ sửa bản tiếng Việt. Không sửa trực tiếp `en/index.html` và `zh/index.html`.**
Hai file này được sinh tự động từ `index.html` (tiếng Việt). Sửa tay vào đó thì lần cập nhật sau sẽ bị ghi đè.

Luôn **lấy bản mới nhất trước khi sửa** (`git pull`), vì nhiều người cùng sửa web.

---

## 2. Các file chính

| Muốn sửa | Sửa ở đâu |
|---|---|
| Chữ, menu, giới thiệu, dịch vụ, liên hệ (tiếng Việt) | `index.html` |
| Danh sách sản phẩm | `index.html` → mảng `PRODUCTS` (mỗi dòng 1 sản phẩm) |
| Nhóm / mục con sản phẩm | `index.html` → mảng `CATS` |
| Bản dịch tiếng Anh, tiếng Trung | `_tools/i18n.py` → bảng `P` |
| Tin tức | `_tools/news.py` (đủ 3 thứ tiếng trong 1 chỗ) |
| Ban lãnh đạo | `_tools/leaders.py` |
| Đối tác – khách hàng | `_tools/partners.py` |
| Bài báo khoa học, sáng chế | `_tools/papers/meta.json`, `_tools/papers/patent.json` |
| Catalog PDF sản phẩm | `_tools/catalog.py` |
| Ảnh sản phẩm | thư mục `anh-san-pham/` (tên file = trường `img` của sản phẩm, `.jpg`, nên vuông nền trắng ~640×640) |
| Ảnh tin tức, lãnh đạo, logo đối tác | `tin-tuc/`, `lanh-dao/`, `logo-doi-tac/` |
| PDF bài báo, bản vẽ, catalog, video | `bai-bao/`, `ban-ve/`, `catalog/`, `video/` |

---

## 3. Cách làm (trên máy tính)

### Cài một lần
1. Cài **Git**: https://git-scm.com/downloads
2. Cài **Python 3**: https://www.python.org/downloads/ (Windows: tích ô *Add Python to PATH*).
3. Tải web về máy:
   ```
   git clone https://github.com/vanphongtechco/vanphongtechco.github.io.git
   cd vanphongtechco.github.io
   ```
   (Có thể dùng GitHub Desktop thay cho dòng lệnh nếu quen giao diện hơn.)

### Mỗi lần sửa
```
git pull                      # 1. lấy bản mới nhất
# 2. sửa file (xem bảng ở mục 2)
python3 _tools/build.py       # 3. cập nhật cả 3 thứ tiếng  (Windows: python _tools/build.py)
python3 -m http.server 8000   # 4. xem thử tại http://localhost:8000  (Ctrl+C để dừng)
git add -A
git commit -m "Mô tả ngắn việc đã sửa"
git push                      # 5. đưa lên web
```

Sau khi push, chờ 1–2 phút rồi mở https://www.vanphongtechco.com.vn (nhấn Ctrl+F5) để kiểm tra cả 3 thứ tiếng.

### Khi `build.py` báo `MISSING: ...`
Nghĩa là bạn vừa sửa/thêm một đoạn chữ tiếng Việt trong `index.html` mà bảng dịch chưa có.
Mở `_tools/i18n.py`, tìm dòng có đoạn tiếng Việt cũ (hoặc thêm dòng mới) theo mẫu:
```python
('đoạn tiếng Việt y hệt trong index.html', 'English text', '中文'),
```
rồi chạy lại `python3 _tools/build.py` đến khi báo **XONG**.

Dòng `leftover` (chữ tiếng Việt còn sót trên trang EN/ZH) liệt kê ra là bình thường nếu đó là tên gốc bài báo, tên tạp chí, chữ "Vân Phong" trong logo.

---

## 4. Thêm một sản phẩm

Trong `index.html`, mảng `PRODUCTS`, thêm 1 dòng, ví dụ:
```js
{c:'tn', s:2, n:'Tên sản phẩm', code:'MÃ-MODEL', img:'ma-model', d:'Mô tả ngắn, thông số chính. Hãng ...', i:'balance'},
```
- `c`: nhóm (`cn` công nghiệp, `yt` y tế, `tn` thí nghiệm, `dt` điện – tự động hóa, `th` tin học); `s`: số thứ tự mục con trong `CATS` (bắt đầu từ 0).
- `img`: tên ảnh trong `anh-san-pham/` (không ghi `.jpg`).
- Tùy chọn: `pdf` (catalog), `art` (bài báo), `dwg` (bản vẽ), `vid` (video), `hot:1` (đưa lên đầu).

Sau đó thêm dòng dịch tương ứng vào `_tools/i18n.py` (chép mẫu của sản phẩm khác: phần từ `n:'...` đến hết `d:'...'`), rồi chạy `build.py`.

## 5. Thêm một tin tức

Mở `_tools/news.py`, chép một khối `dict(...)` có sẵn lên đầu danh sách `N` (tin mới nhất ở trên), sửa nội dung cả 3 thứ tiếng, đặt ảnh vào `tin-tuc/`, rồi chạy `build.py`.
Có thể thêm `video="/video/ten.mp4"` (ảnh `img` dùng làm ảnh bìa video) và `links=` để gắn nút tải PDF.

---

## 6. Quy định nội dung

- Hotline trên web: **08.9999.0683**.
- Không đưa lên web: số CCCD, ngày sinh, địa chỉ nhà riêng, ghi chú nội bộ, nhận xét kiểu "đang cập nhật", "tạm thời"...
- Nội dung khách hàng đọc phải gọn, chuyên nghiệp.
- Bài báo khoa học: không ghi đơn vị công tác cũ của tác giả, trừ khi bài gốc yêu cầu giữ nguyên.

## 7. Phân quyền

Người sửa web được mời bằng tài khoản GitHub riêng (Settings → Collaborators). Không chia sẻ mật khẩu tài khoản công ty.
