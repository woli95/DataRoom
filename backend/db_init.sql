        ----------------------------------------------------
        -----------             MODEL            -----------
        ----------------------------------------------------

CREATE TABLE client(
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50),
    second_name VARCHAR(50),
    birth_date DATE,
    phone VARCHAR(9),
    created_date DATE,
    password VARCHAR(50) NOT NULL,
    current_session_token VARCHAR(20)
);
CREATE TABLE client_password_reset_token (
    client_id INT UNIQUE,
    token VARCHAR(20) NOT NULL,
    CONSTRAINT fk_client_password_reset_token_client
        FOREIGN KEY (client_id)
        REFERENCES client (id)
);

        ----------------------------------------------------
        ----------- AUTH AND CLIENT MANIPULATION -----------
        ----------------------------------------------------
CREATE OR REPLACE PROCEDURE save_password_reset_token(TOKEN VARCHAR(20), EMAIL VARCHAR(50))
LANGUAGE SQL
AS $$
    INSERT INTO client_password_reset_token VALUES
        ((SELECT id FROM client WHERE client.email=$2), $1)
$$;

CREATE OR REPLACE FUNCTION verify_password_reset_token(TOKEN VARCHAR(20), EMAIL VARCHAR(50))
RETURNS INT
LANGUAGE plpgsql
AS $$
    BEGIN
        IF      (SELECT COUNT(*)
                 FROM client_password_reset_token
                 WHERE client_password_reset_token.token=$1 AND client_id=(SELECT id FROM client WHERE client.email=$2)) <> 1 THEN RETURN -1;
        ELSE RETURN 1;
        END IF;
    END;
$$;
CREATE OR REPLACE PROCEDURE delete_password_reset_token(EMAIL VARCHAR(50))
LANGUAGE SQL
AS $$
    DELETE FROM client_password_reset_token
    WHERE client_id=(SELECT id FROM client WHERE email=$1)
$$;

CREATE OR REPLACE PROCEDURE create_client(EMAIL VARCHAR(50), PASSWORD VARCHAR(50))
LANGUAGE SQL
AS $$
    INSERT INTO client (email, password, created_date) VALUES
        ($1, $2, NOW())
$$;

CREATE OR REPLACE FUNCTION is_email_free(EMAIL VARCHAR(50))
RETURNS INT
LANGUAGE plpgsql
AS $$
    BEGIN
        IF      (SELECT COUNT(*)
                FROM client
                WHERE client.email=$1) <> 0
            THEN return -1;
        ELSE return 1;
        END IF;
    END;
$$;

CREATE OR REPLACE FUNCTION verify_credentials(EMAIL VARCHAR(50), PASSWORD VARCHAR(50))
RETURNS INT
LANGUAGE plpgsql
AS $$
    BEGIN
    IF EXISTS(SELECT *
              FROM client
              WHERE client.email=$1 AND client.password=$2) THEN RETURN 1;
    ELSE RETURN -1;
    END IF;
    END;
$$;

CREATE OR REPLACE PROCEDURE save_session_token (EMAIL VARCHAR(50), TOKEN VARCHAR(20))
LANGUAGE SQL
AS $$
    UPDATE client SET current_session_token=$2 WHERE email=$1
$$;

CREATE OR REPLACE PROCEDURE delete_session_token (TOKEN VARCHAR(20))
LANGUAGE SQL
AS $$
    UPDATE client set current_session_token='' WHERE client.current_session_token=$1
$$;

CREATE OR REPLACE PROCEDURE update_client_email (EMAIL VARCHAR(50), TOKEN VARCHAR(20))
LANGUAGE SQL
AS $$
    UPDATE client
    SET email=$1
    WHERE current_session_token=$2
$$;

CREATE OR REPLACE PROCEDURE update_client_password (PASSWORD VARCHAR(50), TOKEN VARCHAR(20))
LANGUAGE SQL
AS $$
    UPDATE client
    SET password=$1
    WHERE current_session_token=$2
$$;

CREATE OR REPLACE PROCEDURE update_client_profile(FIRSTNAME VARCHAR(20), SECONDNAME VARCHAR(20), PHONENUMBER VARCHAR(9), BIRTHDATE DATE, TOKEN VARCHAR(20))
LANGUAGE SQL
AS $$
    UPDATE client
    SET first_name=$1,
        second_name=$2,
        phone=$3,
        birth_date=$4
    WHERE current_session_token=$5
$$;

CREATE OR REPLACE FUNCTION get_client_profile(TOKEN VARCHAR(20))
RETURNS TABLE (email VARCHAR(50),
               first_name VARCHAR(50),
               second_name VARCHAR(50),
               phone VARCHAR(9),
               birth_date DATE,
               created_date DATE)
LANGUAGE plpgsql
AS $$
    BEGIN
        RETURN QUERY SELECT
                        client.email,
                        client.first_name,
                        client.second_name,
                        client.phone,
                        client.birth_date,
                        client.created_date
                    FROM client
                    WHERE current_session_token=$1;
    END;
$$;






























CREATE TABLE building (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    xml_document XML
);

CREATE TABLE building_client (
    client_id INT,
    building_id INT,
    CONSTRAINT fk_building_client_client
        FOREIGN KEY (client_id)
        REFERENCES client(id),
    CONSTRAINT fk_building_client_building
        FOREIGN KEY (building_id)
        REFERENCES building(id)
);

CREATE TABLE floor (
    id SERIAL PRIMARY KEY,
    building_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    xml_document XML,
    CONSTRAINT fk_floor_building
        FOREIGN KEY (building_id)
        REFERENCES building(id)
);
