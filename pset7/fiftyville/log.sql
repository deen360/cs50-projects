-- Keep a log of any SQL queries you execute as you solve the mystery.

--check the crime Scene report
 SELECT description FROM crime_scene_reports WHERE day = 28 AND Month = 7 AND street = "Chamberlin Street";.
sqlite> SELECT id FROM crime_scene_reports WHERE day = 28 AND Month = 7 AND street = "Chamberlin Street";

-- Read the interviews
SELECT transcript,year,month,day FROM interviews WHERE transcript LIKE "%courthouse%" AND month >= 7;

--checks the courthouse log and track people details through license plate 

SELECT name FROM people WHERE license_plate IN
(
    SELECT license_plate 
    FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND month = 7 AND hour = 10 AND activity ="exit" AND minute > 15 AND minute < 25
);

--account numbers on that atm for that day
SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";


---id of all the people that withdrew money on 28th 
SELECT person_id FROM bank_accounts WHERE account_number IN 
(
    SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"
);

----names of all people that made withdrawals
SELECT name FROM people WHERE id IN
(
SELECT person_id FROM bank_accounts WHERE account_number IN 
(
    SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"
)
);

---callers,receiver fitting the description 
SELECT caller,receiver FROM phone_calls WHERE year = 2020 AND Month = 7 AND day = 28 AND duration < 60;

--name of people that made phone calls 
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND Month = 7 AND day = 28 AND duration < 60);

--name of people that received phone call to book flight 
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE year = 2020 AND Month = 7 AND day = 28 AND duration < 60);

---Airport details 
SELECT abbreviation,full_name FROM airports WHERE city = "Fiftyville";
SELECT id FROM airports WHERE city = "Fiftyville";

--flight taken 
SELECT destination_airport_id,hour,minute 
FROM flights WHERE origin_airport_id IN 
(
    SELECT id FROM airports WHERE city = "Fiftyville"
) 
AND year = 2020 AND month = 7 AND day = 29 ;

--flight destination 
SELECT city FROM airports WHERE id IN
(
SELECT destination_airport_id 
FROM flights WHERE origin_airport_id IN 
(
    SELECT id FROM airports WHERE city = "Fiftyville"
) 
AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1
);

--tracking paasenger in flight

SELECT passport_number FROM passengers WHERE flight_id IN 
(
SELECT destination_airport_id 
FROM flights WHERE origin_airport_id IN 
(
    SELECT id FROM airports WHERE city = "Fiftyville"
) 
AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT  1
)

---name of people to london flight 
SELECT name FROM people WHERE passport_number IN
(
SELECT passport_number FROM passengers WHERE flight_id IN 
(
SELECT destination_airport_id 
FROM flights WHERE origin_airport_id IN 
(
    SELECT id FROM airports WHERE city = "Fiftyville"
) 
AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT  1
)
)
