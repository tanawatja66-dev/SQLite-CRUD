-- ══════════════════════════════════════════════
--  เฉลย Question จากสไลด์ SQLite Integration
-- ══════════════════════════════════════════════

-- ── Q1: คำสั่งที่ใช้ เพิ่ม ข้อมูล ──────────────
INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');


-- ── Q2: คำสั่งที่ใช้ ตรวจสอบข้อมูลที่เป็นค่าว่าง ──
SELECT CustomerName, ContactName, Address
FROM Customers
WHERE Address IS NULL;


-- ── Q3: คำสั่งที่ใช้ แก้ไข ข้อมูล ──────────────
UPDATE Customers
SET ContactName = 'Alfred Schmidt', City = 'Frankfurt'
WHERE CustomerID = 1;


-- ── Q4: คำสั่งที่ใช้ ลบ ข้อมูล ─────────────────
DELETE FROM Customers
WHERE CustomerName = 'Alfreds Futterkiste';


-- ── Q5: คำสั่งที่ใช้ เลือกข้อมูลเฉพาะ 3 แถวแรก ─
SELECT * FROM Customers
LIMIT 3;


-- ── Q6: คำสั่งที่ใช้ ค้นหาข้อมูลที่มีค่า ต่ำสุด ──
SELECT MIN(Price) AS SmallestPrice, CategoryID
FROM Products
GROUP BY CategoryID;


-- ── Q7: คำสั่งที่ใช้ นับจำนวน ข้อมูล ───────────
SELECT COUNT(ProductID)
FROM Products
WHERE Price > 20;


-- ── Q8: คำสั่งที่ใช้ เชื่อมข้อมูลระหว่าง 2 ตาราง ─
SELECT Products.ProductID, Products.ProductName, Categories.CategoryName
FROM Products
INNER JOIN Categories ON Products.CategoryID = Categories.CategoryID;


-- ── Q9: คำสั่งที่ใช้ ลบฐานข้อมูล ───────────────
DROP DATABASE databasename;


-- ── Q10: คำสั่งที่ใช้ สร้างตารางเสมือน (View) ──
CREATE VIEW [Brazil Customers] AS
SELECT CustomerName, ContactName
FROM Customers
WHERE Country = 'Brazil';
