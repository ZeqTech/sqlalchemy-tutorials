-- INNER JOIN
SELECT *
FROM users
    JOIN addresses ON users.id = addresses.user_id
WHERE
    users.id = addresses.user_id;

--ANTI INNER JOIN - Inverse
SELECT *
FROM users
    FULL OUTER JOIN addresses ON users.id = addresses.user_id
WHERE
    0 = 1;

--LEFT OUTER JOIN
SELECT users.*, addresses.*
FROM users
    LEFT OUTER JOIN addresses ON users.id = addresses.user_id;

--ANTI LEFT OUTER JOIN - Inverse
SELECT users.*, addresses.*
FROM users
    LEFT OUTER JOIN addresses ON users.id = addresses.user_id
WHERE
    NOT (
        EXISTS (
            SELECT 1
            FROM addresses
            WHERE
                users.id = addresses.user_id
        )
    );

--RIGHT OUTER JOIN
SELECT *
FROM addresses
    LEFT OUTER JOIN users ON users.id = addresses.user_id;

--ANTI RIGHT OUTER JOIN - Inverse
SELECT *
FROM addresses
    LEFT OUTER JOIN users ON users.id = addresses.user_id
WHERE
    addresses.user_id IS NULL;

--FULL JOIN
SELECT *
FROM (
        SELECT users.*, addresses.*
        FROM users
            LEFT OUTER JOIN addresses ON users.id = addresses.user_id
        UNION
        SELECT users.*, addresses.*
        FROM addresses
            LEFT OUTER JOIN users ON users.id = addresses.user_id
    );

--FULL JOIN
SELECT users.*, addresses.*
FROM users
    FULL OUTER JOIN addresses ON users.id = addresses.user_id;
