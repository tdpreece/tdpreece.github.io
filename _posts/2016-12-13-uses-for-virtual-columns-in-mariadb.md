---
layout: post
title: "Uses for Virtual columns in MariaDB"
date: 2016-12-13
---

The examples shown used MariaDB 10.1.19.

A [virtual column](https://mariadb.com/kb/en/mariadb/virtual-computed-columns/)
is a column in a table that has its value automatically calculated using
a deterministic expression.  This expression cannot include data from
outside the row (no subqueries) and cannot use stored functions.

There are two types of virtual columns: PERSISTENT,
which are stored in the table, and VIRTUAL, which are
generated when the table is queried.  Indexes can only be based on
PERSISTENT virtual columns.

I like to keep domain logic out of the database and only store in the
database what is necessary.  One reason that I might me tempted to use virtual
columns would be for performance (if this was really required).  Thus,
I'm only interested in PERSISTENT virtual columns,
which can be indexed and might offer some performance benefit.

If I want to query on a particular value that isn't stored in the database
I adjust my query to use the columns in the database that do exist.
I can then keep business logic in the code and out of the database.

For example, I created the following table (formula taken from a recent
[webinar](https://www.percona.com/resources/technical-presentations/virtual-columns-mysql-and-mariadb-percona-mysql-webinar)
by Federico Goncalvez on virtual columns).

```sql
CREATE TABLE `goods` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `price` decimal(65,2) unsigned DEFAULT NULL,
  `taxed_price` decimal(65,2) unsigned AS (price + (price / 100 * 20)) PERSISTENT,
  PRIMARY KEY (`id`),
  KEY `price` (`price`),
  KEY `taxed_price` (`taxed_price`)
) ENGINE=InnoDB

INSERT INTO goods (price) VALUES (10), (20), (30), (40), (50), (60);
```

and wanted to query goods with taxed price equal to 24, I could 
query against price or taxed_price, e.g.

```sql
MariaDB [tpreece_test]> explain SELECT * FROM goods WHERE taxed_price = 24.00;                                                                  
+------+-------------+-------+------+---------------+-------------+---------+-------+------+-------+
| id   | select_type | table | type | possible_keys | key         | key_len | ref   | rows | Extra |
+------+-------------+-------+------+---------------+-------------+---------+-------+------+-------+
|    1 | SIMPLE      | goods | ref  | taxed_price   | taxed_price | 30      | const |    1 |       |
+------+-------------+-------+------+---------------+-------------+---------+-------+------+-------+
1 row in set (0.00 sec)

MariaDB [tpreece_test]> explain SELECT * FROM goods WHERE price = 20.00;                                                                        
+------+-------------+-------+------+---------------+-------+---------+-------+------+-------+
| id   | select_type | table | type | possible_keys | key   | key_len | ref   | rows | Extra |
+------+-------------+-------+------+---------------+-------+---------+-------+------+-------+
|    1 | SIMPLE      | goods | ref  | price         | price | 30      | const |    1 |       |
+------+-------------+-------+------+---------------+-------+---------+-------+------+-------+
1 row in set (0.00 sec)
```

As we can see, both queries use an index and both columns will have the
same cardinality (each value of `price` corresponds to exactly one value
of `taxed_price`) so there doesn't seem to be any performance
benefit from introducing the taxed_price virtual column.

Consider a different example in which the virtual column is a function
of two other columns.

```sql
CREATE TABLE journey (
    id bigint NOT NULL AUTO_INCREMENT,
    distance_in_metres DOUBLE,
    time_in_seconds DOUBLE,
    speed_in_metres_per_second DOUBLE AS (distance_in_metres/time_in_seconds) PERSISTENT,
    PRIMARY KEY (id),
    KEY `distance_time` (`distance_in_metres`, `time_in_seconds`),
    KEY `speed` (`speed_in_metres_per_second`)
) ENGINE=InnoDB;

INSERT INTO journey (distance_in_metres, time_in_seconds)
VALUES (4,1), (8,2), (16, 4), (16, 3), (16, 2);
```

Let's say that I wanted to find the rows with `speed = 8m/s`.
This can be done using either of the queries explained below.

```sql
MariaDB [tpreece_test]> explain select id from journey where distance_in_metres/time_in_seconds = 8;
+------+-------------+---------+-------+---------------+---------------+---------+------+------+--------------------------+
| id   | select_type | table   | type  | possible_keys | key           | key_len | ref  | rows | Extra                    |
+------+-------------+---------+-------+---------------+---------------+---------+------+------+--------------------------+
|    1 | SIMPLE      | journey | index | NULL          | distance_time | 18      | NULL |    5 | Using where; Using index |
+------+-------------+---------+-------+---------------+---------------+---------+------+------+--------------------------+
1 row in set (0.00 sec)

MariaDB [tpreece_test]> explain select id from journey where speed_in_metres_per_second = 8;
+------+-------------+---------+------+---------------+-------+---------+-------+------+-------------+
| id   | select_type | table   | type | possible_keys | key   | key_len | ref   | rows | Extra       |
+------+-------------+---------+------+---------------+-------+---------+-------+------+-------------+
|    1 | SIMPLE      | journey | ref  | speed         | speed | 9       | const |    1 | Using index |
+------+-------------+---------+------+---------------+-------+---------+-------+------+-------------+
1 row in set (0.00 sec)
```

For the first query, [type = index](https://mariadb.com/kb/en/mariadb/explain/#type-column) indicates a
full scan over the index will take place.  This is because the B-tree
index is of no use for finding values where the ratio of the two key
parts are `8`.

For the second query [type = ref](https://mariadb.com/kb/en/mariadb/explain/#type-column)
indicates that the
index is used to find the rows.  Thus, selects for `speed` will be faster using
the virtual column.  The fact that the calculation of `speed` is done at write
time would probably also make the the query using the virtual column more
efficient.

Virtual columns may help
boost efficiency for reads from a B-tree index
for any `WHERE`/`JOIN ON` clause that can be written in
the form, `column=C [AND|OR another_column=C' ...]'`, where `C` and `C'`
represent constant values (the '`=`' could be any other operator that
the given index supports see [here](https://mariadb.com/kb/en/mariadb/storage-engine-index-types/)).

Another example of where select statements cannot use indexs effectively are
queries involving the day of the week of a datetime column [[1]](#dayOfWeekEg1)
[[2]](#dayOfWeekEg2).

## References
* <a name="dayOfWeekEg1">1</a>: [MariaDB 5.2: What would you use virtual columns for? - hingo](http://openlife.cc/blogs/2010/october/what-would-you-use-virtual-columns)
* <a name="dayOfWeekEg2">2</a>: [Putting Virtual Columns to good use - Anders Karlsson](https://mariadb.com/resources/blog/putting-virtual-columns-good-use)
