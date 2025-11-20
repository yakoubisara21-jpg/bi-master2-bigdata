SELECT CustomerID, EmployeeID, month(orderdate) AS OrderMonth, year(orderdate) AS OrderYear,
Count(CASE WHEN Shippeddate IS NOT NULL THEN OrderID END) AS Shipped,
Count(CASE WHEN Shippeddate IS NULL THEN OrderID END) AS NotShipped
FROM Orders
GROUP BY CustomerID, EmployeeID, month(orderdate), year(orderdate);