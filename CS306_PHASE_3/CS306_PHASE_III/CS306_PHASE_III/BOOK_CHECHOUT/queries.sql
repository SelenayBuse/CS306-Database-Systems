CREATE TABLE BOOK_COPY AS SELECT * FROM CS306.BOOK;
CREATE TABLE CHECKOUT_BOOK_COPY AS SELECT * FROM CS306.CHECKOUT_BOOK;

-- 1st

-- Before adding indexes

SET profiling = 1;

SELECT *

FROM BOOK_COPY
JOIN CHECKOUT_BOOK_COPY ON BOOK_COPY.ISBN = CHECKOUT_BOOK_COPY.ISBN
WHERE BOOK_COPY.NUM_COPIES > 10
AND CHECKOUT_BOOK_COPY.DUE_DATE > 2000-05-22

LIMIT 1000000;

SHOW PROFILE;


-- Adding indexes
CREATE INDEX idx_columna ON BOOK_COPY(NUM_COPIES);
CREATE INDEX idx_columnb ON CHECKOUT_BOOK_COPY(DUE_DATE);

-- After adding indexes

SET profiling = 1;

SELECT *

FROM BOOK_COPY
JOIN CHECKOUT_BOOK_COPY ON BOOK_COPY.ISBN = CHECKOUT_BOOK_COPY.ISBN
WHERE BOOK_COPY.NUM_COPIES > 10
AND CHECKOUT_BOOK_COPY.DUE_DATE > 2000-05-22
LIMIT 1000000;

SHOW PROFILE;

