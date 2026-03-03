BÀI1
a)  
SELECT HoTen, CB#
FROM CANBO
WHERE GioiTinh = 'Nam' AND QueQuan = 'Hà Giang';
b)
SELECT TenNN
FROM NGOAINGU;
C)
SELECT CB.HoTen
FROM CANBO CB, DONVI DV
WHERE CB.CB# = DV.TruongĐV 
  AND DV.ĐV# = 'P1';
D
SELECT DV.TenĐV
FROM CANBO CB, DONVI DV
WHERE CB.ĐV# = DV.ĐV# 
  AND CB.CB# = 'CB05';
E
SELECT CB.HoTen
FROM CANBO CB, DONVI DV
WHERE CB.ĐV# = DV.ĐV# 
  AND DV.TenĐV = 'Phòng Tổ chức';
bài2
a
SELECT DS#,TENS
FROM DAUSACH
WWHERE TENTG='Vũ Trọng Phụng';
b
SELECT TENNXB
FROM NHAXUATBAN
WHERE DIACHI ='HANOI';
C
SELECT DS.TenS
FROM DAUSACH DS, THELOAISACH TL
WHERE DS.TheLoai# = TL.TheLoai# AND TL.NgonNgu = 'Tiếng Nga';
d
SELECT DS.DS#
FROM DAUSACH DS, THELOAISACH TL
WHERE DS.TheLoai# = TL.TheLoai# AND DS.NXB# = 'NXB01' AND TL.NgonNgu = 'Tiếng Hàn';
e
SELECT DS.DS#
FROM DAUSACH DS, THELOAISACH TL
WHERE DS.TheLoai# = TL.TheLoai# AND DS.NXB# = 'NXB01' AND TL.NgonNgu = 'Tiếng Hàn' AND DS.NamXB = 2025;
f
SELECT TenNXB 
FROM NHAXUATBAN 
WHERE NXB# IN (SELECT NXB# FROM DAUSACH WHERE TenS = 'Số đỏ') AND NXB# IN (SELECT NXB# FROM DAUSACH WHERE TenS = 'Đất vỡ hoang');
g
SELECT DS.TenS
FROM DAUSACH DS, NHAXUATBAN NXB, THELOAISACH TL
WHERE DS.NXB# = NXB.NXB# AND DS.TheLoai# = TL.TheLoai#AND NXB.TenNXB = 'Nhà xuất bản Hội nhà văn' AND TL.NgonNgu = 'Tiếng Nga';
h
SELECT NXB.TenNXB
FROM NHAXUATBAN NXB, DAUSACH DS, THELOAISACH TL
WHERE NXB.NXB# = DS.NXB# AND DS.TheLoai# = TL.TheLoai#AND TL.NgonNgu = 'Tiếng Pháp';
i
SELECT TenNXB 
FROM NHAXUATBAN 
WHERE NXB# IN (SELECT DS.NXB# FROM DAUSACH DS, THELOAISACH TL WHERE DS.TheLoai# = TL.TheLoai# AND TL.NgonNgu = 'Tiếng Pháp')
AND NXB# NOT IN (SELECT DS.NXB# FROM DAUSACH DS, THELOAISACH TL WHERE DS.TheLoai# = TL.TheLoai# AND TL.NgonNgu = 'Tiếng Anh');
/*
LƯỢC ĐỒ CSDL GIẢ ĐỊNH:

DOCGIA(MaDG, HoTen, NgaySinh, SDT, DiaChi)
SACH(MaSach, TenSach, MaNXB, MaTG, MaTL)
TACGIA(MaTG, TenTG, QuocTich)
NXB(MaNXB, TenNXB, DiaChi)
THELOAI(MaTL, TenTL)
PHIEUMUON(MaPM, MaDG, NgayMuon)
CTPM(MaPM, MaSach)
*/


/* =======================
   CÂU 1
   Lấy tất cả thông tin độc giả
   ======================= */
SELECT *
FROM DOCGIA;


/* =======================
   CÂU 2
   Tên và địa chỉ NXB có mã 'NXB01'
   ======================= */
SELECT TenNXB, DiaChi
FROM NXB
WHERE MaNXB = 'NXB01';


/* =======================
   CÂU 3
   Liệt kê tên tất cả các sách
   ======================= */
SELECT TenSach
FROM SACH;


/* =======================
   CÂU 4
   Cho biết tên sách và tên NXB của sách "Số đỏ"
   ======================= */
SELECT S.TenSach, N.TenNXB
FROM SACH S, NXB N
WHERE S.MaNXB = N.MaNXB
  AND S.TenSach = N'Số đỏ';


/* =======================
   CÂU 5
   Liệt kê tên tác giả, quốc tịch có quốc tịch = 'QT02'
   ======================= */
SELECT TenTG, QuocTich
FROM TACGIA
WHERE QuocTich = 'QT02';


/* =======================
   CÂU 6
   Tên và SĐT độc giả mượn sách ngày 15/12/2025
   ======================= */
SELECT DG.HoTen, DG.SDT
FROM DOCGIA DG, PHIEUMUON PM
WHERE DG.MaDG = PM.MaDG
  AND PM.NgayMuon = '2025-12-15';


/* =======================
   CÂU 7
   Mã sách và tên sách thuộc thể loại mã 'TL01'
   ======================= */
SELECT MaSach, TenSach
FROM SACH
WHERE MaTL = 'TL01';


/* =======================
   CÂU 8
   Tên độc giả và mã sách mượn ngày 15/12/2025
   ======================= */
SELECT DG.HoTen, CT.MaSach
FROM DOCGIA DG, PHIEUMUON PM, CTPM CT
WHERE DG.MaDG = PM.MaDG
  AND PM.MaPM = CT.MaPM
  AND PM.NgayMuon = '2025-12-15';


/* =======================
   CÂU 9
   Tên sách và tên tác giả của sách do NXB ở Hà Nội xuất bản
   ======================= */
SELECT S.TenSach, TG.TenTG
FROM SACH S, TACGIA TG, NXB N
WHERE S.MaTG = TG.MaTG
  AND S.MaNXB = N.MaNXB
  AND N.DiaChi = N'Hà Nội';


/* =======================
   CÂU 10
   Tên độc giả đã mượn sách có mã 'MTG07'
   ======================= */
SELECT DISTINCT DG.HoTen
FROM DOCGIA DG, PHIEUMUON PM, CTPM CT
WHERE DG.MaDG = PM.MaDG
  AND PM.MaPM = CT.MaPM
  AND CT.MaSach = 'MTG07';


