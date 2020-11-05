--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bills (
    id integer NOT NULL,
    date date NOT NULL,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL
);


ALTER TABLE public.bills OWNER TO postgres;

--
-- Name: bills_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bills_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bills_id_seq OWNER TO postgres;

--
-- Name: bills_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bills_id_seq OWNED BY public.bills.id;


--
-- Name: bills_with_number; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.bills_with_number AS
 WITH monthly_ids AS (
         SELECT bills_1.id,
            count(bills_cmp.id) AS month_id
           FROM (public.bills bills_cmp
             JOIN public.bills bills_1 ON (((bills_cmp.id <= bills_1.id) AND (date_trunc('month'::text, (bills_1.date)::timestamp with time zone) <= bills_cmp.date))))
          GROUP BY bills_1.id
        )
 SELECT bills.id,
    (((date_part('year'::text, bills.date))::text || lpad((date_part('month'::text, bills.date))::text, 2, '0'::text)) || lpad((monthly_ids.month_id)::text, 2, '0'::text)) AS number,
    bills.date,
    bills.sender_id,
    bills.receiver_id
   FROM (public.bills
     JOIN monthly_ids ON ((monthly_ids.id = bills.id)));


ALTER TABLE public.bills_with_number OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    bill_id integer NOT NULL,
    quantity integer NOT NULL,
    description text NOT NULL,
    unitary_price numeric(15,2) NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: receivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.receivers (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address_part_1 character varying(255),
    address_part_2 character varying(255)
);


ALTER TABLE public.receivers OWNER TO postgres;

--
-- Name: receivers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.receivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.receivers_id_seq OWNER TO postgres;

--
-- Name: receivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.receivers_id_seq OWNED BY public.receivers.id;


--
-- Name: senders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.senders (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    address_part_1 character varying(255) NOT NULL,
    address_part_2 character varying(255) NOT NULL,
    phone character varying(15),
    email character varying(255) NOT NULL,
    siren character(9) NOT NULL,
    bank_details_name character varying(255) NOT NULL,
    bank_details_bank character varying(255) NOT NULL,
    bank_details_iban character varying(34) NOT NULL,
    bank_details_bic character varying(11) NOT NULL
);


ALTER TABLE public.senders OWNER TO postgres;

--
-- Name: senders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.senders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.senders_id_seq OWNER TO postgres;

--
-- Name: senders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.senders_id_seq OWNED BY public.senders.id;


--
-- Name: bills id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bills ALTER COLUMN id SET DEFAULT nextval('public.bills_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: receivers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receivers ALTER COLUMN id SET DEFAULT nextval('public.receivers_id_seq'::regclass);


--
-- Name: senders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.senders ALTER COLUMN id SET DEFAULT nextval('public.senders_id_seq'::regclass);


--
-- Name: bills bills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bills
    ADD CONSTRAINT bills_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: receivers receivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receivers
    ADD CONSTRAINT receivers_pkey PRIMARY KEY (id);


--
-- Name: senders senders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.senders
    ADD CONSTRAINT senders_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

