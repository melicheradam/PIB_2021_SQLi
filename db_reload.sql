-- SEQUENCE: public.users_id_seq

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;

CREATE SEQUENCE public.users_id_seq
    INCREMENT 1
    START 1
    MINVALUE 0
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE public.users_id_seq
    OWNER TO xmelicher;



-- Table: public.users

CREATE TABLE public.users
(
    id bigint NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username character varying COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_unique_username UNIQUE (username)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to xmelicher;

INSERT INTO public.users (username, password) VALUES('adam', 'adam');
INSERT INTO public.users (username, password) VALUES('test', 'test');
INSERT INTO public.users (username, password) VALUES('prepared', 'prepared');
INSERT INTO public.users (username, password) VALUES('user1', 'user1');
INSERT INTO public.users (username, password) VALUES('user2', 'user2');
INSERT INTO public.users (username, password) VALUES('user3', 'user3');
INSERT INTO public.users (username, password) VALUES('user4', 'user4');
INSERT INTO public.users (username, password) VALUES('user5', 'user5');