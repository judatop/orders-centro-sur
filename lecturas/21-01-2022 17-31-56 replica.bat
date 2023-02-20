cd C:\replica
mysqldump -h localhost -u root -pgatojuda orden > orden.sql
mysql -h localhost -u root -pgatojuda orden2 < orden.sql

mysqldump -P 33663 -h 190.154.48.250 -u root -pcentrosur orden > orden.sql