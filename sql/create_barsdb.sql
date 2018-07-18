--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: book_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.book_no_seq
    START WITH 3200000
    INCREMENT BY 1
    MINVALUE 3200000
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_no_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: book_cross_index; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_cross_index (
    locator character(6) NOT NULL,
    origin_address character(7) NOT NULL,
    book_no integer DEFAULT nextval('public.book_no_seq'::regclass) NOT NULL,
    book_category character(1) NOT NULL,
    reply_poll_flag character(1),
    processing_flag character(1) NOT NULL,
    ext_locator character(6),
    codeshare_book_numb character(6),
    update_user character(5) NOT NULL,
    update_group character(12) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_cross_index OWNER TO postgres;

--
-- Name: book_fares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_fares (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    total_amount_curr character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(90),
    status_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_fares OWNER TO postgres;

--
-- Name: book_fares_pass; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_fares_pass (
    book_no integer NOT NULL,
    pax_code character(5) NOT NULL,
    total_amount_curr character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_fares_pass OWNER TO postgres;

--
-- Name: book_fares_paym; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_fares_paym (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    payment_code character(5) NOT NULL,
    fare_calc_code character(15) NOT NULL,
    fare_paymt_amt numeric(15,5) NOT NULL,
    currency_code character(3) NOT NULL,
    tax_code character(5),
    nation_code character(5),
    refund_stat_flag character(1) NOT NULL,
    exempt_stat_flag character(1) NOT NULL,
    refundable_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    net_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    private_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    flight_number character(7),
    board_date date,
    flight_origin character(5),
    flight_destination character(5),
    source_ref_id bigint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_fares_paym OWNER TO postgres;

--
-- Name: book_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_requests (
    book_no integer NOT NULL,
    rqst_sequence_no smallint NOT NULL,
    item_no smallint NOT NULL,
    indicator character(1),
    rqst_code character(4),
    carrier_code character(3),
    action_code character(2),
    actn_number character(3),
    processing_flag character(1) NOT NULL,
    rqr_count smallint,
    request_text character varying(255),
    all_pax_flag character(1) NOT NULL,
    all_itinerary_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_requests OWNER TO postgres;

--
-- Name: book_time_limits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.book_time_limits (
    book_no integer NOT NULL,
    timelmt_sequence_no smallint NOT NULL,
    timelmt_type character(1) NOT NULL,
    limit_time timestamp with time zone,
    cancel_flag character(1) NOT NULL,
    queue_code character(5),
    dest_branch character(12) NOT NULL,
    remark_text character(240),
    all_pax_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.book_time_limits OWNER TO postgres;

--
-- Name: booking_fare_segments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booking_fare_segments (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    selling_class character(5) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.booking_fare_segments OWNER TO postgres;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    book_no integer DEFAULT 0 NOT NULL,
    locator character(6),
    book_type character(2) NOT NULL,
    group_name character(53),
    no_of_seats smallint NOT NULL,
    book_category character(1) NOT NULL,
    group_wait_seats smallint,
    group_request_seats smallint,
    group_realtn_pcnt smallint,
    origin_branch_code character(12) NOT NULL,
    agency_code character(8),
    book_agency character(8),
    departure_city character(5),
    departure_nation character(2),
    origin_address character(10),
    record_locator character varying(69),
    received_from character varying(60) NOT NULL,
    tour_code character(20),
    payment_amount numeric(15,5),
    status_flag character(1) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    divide_from_no character(10),
    divide_to_nos character varying(110),
    first_segm_date date NOT NULL,
    last_segm_date date NOT NULL,
    reaccom_party smallint NOT NULL,
    dvd_process_flag character(1) NOT NULL,
    rdu_process_flag character(1) NOT NULL,
    grp_process_flag character(1) NOT NULL,
    nrl_process_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp with time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone,
    currency_code character(3)
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: fare_basis_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fare_basis_codes (
    company_code character(3) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    short_description character varying(30),
    description character varying(255),
    selling_class character(2) NOT NULL,
    fare_category character(4) NOT NULL,
    oneway_return_flag character(1) NOT NULL,
    acss_strt_auth_level smallint,
    acss_end_auth_level smallint,
    byps_strt_auth_level smallint,
    byps_end_auth_level smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.fare_basis_codes OWNER TO postgres;

--
-- Name: fee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fee_id_seq OWNER TO postgres;

--
-- Name: fees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fees (
    fee_id integer DEFAULT nextval('public.fee_id_seq'::regclass) NOT NULL,
    company_code character(3),
    fee_type_rcd character(10) NOT NULL,
    fee_code character(5) NOT NULL,
    description character varying(250) NOT NULL,
    valid_from_date_time timestamp with time zone NOT NULL,
    valid_until_date_time timestamp with time zone NOT NULL,
    fee_amount numeric(15,5) NOT NULL,
    fee_currency character(3),
    fee_percent_flag integer NOT NULL,
    tax_amount numeric(15,5),
    tax_percent_flag integer NOT NULL,
    selling_class_code character(2),
    days_before_departure integer,
    use_days_before_departure_flag integer NOT NULL,
    per_pax_flag integer,
    pax_code character(5),
    branch_code character varying(15),
    payment_type character(5),
    payment_form character(5),
    booking_category character(1),
    fare_basis_code character varying(15),
    create_user character(5) NOT NULL,
    create_time timestamp with time zone DEFAULT now() NOT NULL,
    inactivated_user_code character(5),
    inactivated_date_time timestamp with time zone,
    active_flag integer NOT NULL,
    international_domestic_indicator character(1) NOT NULL,
    ssr_code character(4),
    min_fee_amount numeric(15,5),
    max_fee_amount numeric(15,5),
    pnl_adl_identifier character varying(20) DEFAULT NULL::character varying,
    dcs_miscellaneous_charge_rcd character varying(20) DEFAULT NULL::character varying,
    allow_segment_association integer DEFAULT 0,
    exclude_branches_flag character(1) DEFAULT 'N'::bpchar,
    exclude_classes_flag character(1) DEFAULT 'N'::bpchar,
    exclude_fares_flag character(1) DEFAULT 'N'::bpchar,
    exclude_passengers_flag character(1) DEFAULT 'N'::bpchar,
    per_segment_flag integer DEFAULT 0 NOT NULL,
    inv_section character(1),
    CONSTRAINT fee_international_domestic_indicator_check CHECK ((international_domestic_indicator = ANY (ARRAY['I'::bpchar, 'D'::bpchar, 'A'::bpchar])))
);


ALTER TABLE public.fees OWNER TO postgres;

--
-- Name: itineraries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itineraries (
    book_no integer NOT NULL,
    route_no smallint NOT NULL,
    alt_itinerary_no smallint NOT NULL,
    itinerary_no smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_city character(5),
    arrival_city character(5),
    departure_airport character(5),
    arrival_airport character(5),
    departure_time time with time zone,
    arrival_time time with time zone,
    date_change_ind smallint,
    flight_path_code character(1),
    departure_terminal character(2),
    arrival_terminal character(2),
    city_pair integer,
    physical_class character(2),
    selling_class character(2),
    status_flag character(1),
    itinerary_type character(1),
    reserve_status character(5),
    request_nos character varying(1024),
    fare_nos smallint NOT NULL,
    contact_nos character varying(30),
    processing_flag character(1) NOT NULL,
    stopover_flag character(1),
    other_rloc character(30),
    rlr_rqr_count smallint,
    action_to_company character(3),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.itineraries OWNER TO postgres;

--
-- Name: passengers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.passengers (
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    pax_name character(53) NOT NULL,
    client_prfl_no character(15),
    request_nos character varying(1024),
    remark_nos character varying(30),
    fare_nos character varying(30),
    contact_nos character varying(30),
    timelmt_nos character varying(30),
    ticket_nos character varying(50),
    name_incl_type character(1),
    pax_code character(5) NOT NULL,
    processing_flag character(1) NOT NULL,
    tty_pax_line_no integer DEFAULT 0 NOT NULL,
    tty_pax_grp_no integer DEFAULT 0 NOT NULL,
    tty_pax_grp_seq integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone,
    birth_date date
);


ALTER TABLE public.passengers OWNER TO postgres;

--
-- Name: pax_contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pax_contact (
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    home_phone_no character varying(30),
    buss_phone_no character varying(30),
    contact_phone_no character varying(30),
    agent_phone_no character varying(30),
    home_address character varying(200),
    home_city character(25),
    home_state character(25),
    home_zip character(15),
    home_nation character(25),
    buss_address character varying(200),
    buss_city character(25),
    buss_state character(25),
    buss_zip character(15),
    buss_nation character(25),
    contact_address character varying(200),
    contact_city character(25),
    contact_state character(25),
    contact_zip character(15),
    contact_nation character(25),
    agent_address character varying(200),
    agent_city character(25),
    agent_state character(25),
    agent_zip character(15),
    agent_nation character(25),
    email_address character varying(150),
    fax_number character varying(30),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.pax_contact OWNER TO postgres;

--
-- Name: payment_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payment_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_no_seq OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    payment_no integer DEFAULT nextval('public.payment_no_seq'::regclass) NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    payment_amount numeric(15,5) NOT NULL,
    payment_date date NOT NULL,
    document_no character(25),
    cc_cid character(4),
    payment_mode character(1),
    document_date date,
    book_no integer,
    pax_name character(53),
    client_prfl_no character(15),
    pax_code character(5),
    book_agency_code character(8),
    origin_address character(10),
    origin_branch_code character(12) NOT NULL,
    contact_phone_no character varying(30),
    contact_address character varying(200),
    contact_city character(25),
    contact_state character(25),
    contact_zip character(15),
    contact_nation character(25),
    cc_approval_code character(6),
    cc_approval_type character(1),
    cc_expiry_date character(4),
    remarks_text character varying(60),
    record_locator character varying(69),
    received_from character varying(60) NOT NULL,
    currency_code character(3) NOT NULL,
    paid_flag character(1) NOT NULL,
    pay_stat_flag character(1) NOT NULL,
    recpt_stat_flag character(1) NOT NULL,
    invc_stat_flag character(1) NOT NULL,
    status_flag character(1) NOT NULL,
    voucher_no integer,
    credit_req_seq character varying(10),
    cc_cvv character varying(10),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp with time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: selling_conf; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.selling_conf (
    company_code character(3) NOT NULL,
    selling_class character(3) NOT NULL,
    cabin_code character(2) NOT NULL,
    parent_sell_cls character(3) NOT NULL,
    sell_cls_category character(2) NOT NULL,
    ffp_fact_mult numeric(5,2),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone,
    display_priority smallint
);


ALTER TABLE public.selling_conf OWNER TO postgres;

--
-- Name: service_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.service_requests (
    company_code character(3) NOT NULL,
    rqst_code character(4) NOT NULL,
    description character varying(120),
    rqst_type character(5) NOT NULL,
    misc_charge_code character(10),
    indicator character(1) NOT NULL,
    yy_flag character(1) NOT NULL,
    action_flag character(1) NOT NULL,
    number_flag character(1) NOT NULL,
    text_flag character(1) NOT NULL,
    auto_format_flag character(1) NOT NULL,
    reply_flag character(1) NOT NULL,
    segment_flag character(1) NOT NULL,
    pass_name_flag character(1) NOT NULL,
    handling_branch character(12) NOT NULL,
    cfm_queue_code character(5) NOT NULL,
    rqst_queue_code character(5) NOT NULL,
    canx_queue_code character(5),
    ttr_queue_code character(5),
    arpt_action_flag character(1) NOT NULL,
    rcfm_canx_flag character(1) NOT NULL,
    def_actn_code character(2),
    que_action_flag character(1) NOT NULL,
    fin_actn_code character(2),
    bilateral_carrs character varying(40),
    active_flag integer DEFAULT 1,
    validation_regexp character varying(100),
    remove_permission_flag character(1),
    validation_error_message character varying(250),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.service_requests OWNER TO postgres;
--
-- Name: city_pairs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE city_pairs (
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    city_pair integer NOT NULL,
    pair_indicator character(1) NOT NULL,
    distance integer,
    distance_uom character(3),
    points_value smallint,
    avl_forw_scan_days smallint,
    baggage_alownce character varying(35),
    pair_rule_no character(8),
    remarks character varying(80),
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.city_pairs OWNER TO postgres;

--
-- Name: city_pair_city_pair_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE city_pair_city_pair_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.city_pair_city_pair_seq OWNER TO postgres;

--
-- Name: city_pair_city_pair_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE city_pair_city_pair_seq OWNED BY city_pairs.city_pair;

CREATE TABLE public.flight_segment_dates (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    city_pair integer NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time time with time zone,
    arrival_time time with time zone,
    date_change_ind smallint NOT NULL,
    flight_path_code character(1) NOT NULL,
    departure_terminal character(2) NOT NULL,
    arrival_terminal character(2) NOT NULL,
    flgt_sched_status character(1) NOT NULL,
    no_of_stops smallint NOT NULL,
    aircraft_code character(3) NOT NULL,
    flight_closed_flag character(1) NOT NULL,
    flight_brdng_flag character(1) NOT NULL,
    leg_number smallint NOT NULL,
    segment_number character(22) NOT NULL,
    schedule_period_no smallint NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp with time zone
);

ALTER TABLE public.flight_segment_dates OWNER TO postgres;

CREATE UNIQUE INDEX flight_segm_date_fndda ON public.flight_segment_dates
USING btree (flight_number, flight_date, departure_airport, arrival_airport);


--
-- Name: inventry_segment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventry_segment (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    departure_city character(5) NOT NULL,
    arrival_city character(5) NOT NULL,
    leg_number smallint NOT NULL,
    segment_number character(22) NOT NULL,
    ob_profile_no character(5) NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    overbooking_percnt smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    nett_sngl_sold smallint NOT NULL,
    nett_sngl_wait smallint NOT NULL,
    nett_group_sold smallint NOT NULL,
    nett_group_wait smallint NOT NULL,
    nett_nrev_sold smallint NOT NULL,
    nett_nrev_wait smallint NOT NULL,
    segm_sngl_sold smallint NOT NULL,
    segm_sngl_wait smallint NOT NULL,
    segm_group_sold smallint NOT NULL,
    segm_group_wait smallint NOT NULL,
    segm_nrev_sold smallint NOT NULL,
    segm_nrev_wait smallint NOT NULL,
    segm_group_nrealsd smallint NOT NULL,
    segm_sngl_ticktd smallint NOT NULL,
    segm_group_ticktd smallint NOT NULL,
    segm_nrev_ticktd smallint NOT NULL,
    segment_closed_flag character(1) NOT NULL,
    wl_closed_flag character(1) NOT NULL,
    wl_clear_inhibit_flag character(1) NOT NULL,
    wl_release_party_flag character(1) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    display_priority smallint NOT NULL,
    schedule_period_no smallint NOT NULL,
    invt_update_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    group_name character(8) NOT NULL,
    update_time timestamp with time zone
);


ALTER TABLE public.inventry_segment OWNER TO postgres;


--
-- Name: book_no_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.book_no_seq', 3200167, true);


--
-- Name: fee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fee_id_seq', 11, true);


--
-- Name: payment_no_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payment_no_seq', 117, true);


--
-- Name: book_cross_index book_crs_index_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_cross_index
    ADD CONSTRAINT book_crs_index_pkey PRIMARY KEY (book_no);


--
-- Name: book_fares_pass book_fares_pass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_fares_pass
    ADD CONSTRAINT book_fares_pass_pkey PRIMARY KEY (book_no, pax_code);


--
-- Name: book_fares book_fares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_fares
    ADD CONSTRAINT book_fares_pkey PRIMARY KEY (book_no, fare_no, pax_code);


--
-- Name: bookings book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT book_pkey PRIMARY KEY (book_no);


--
-- Name: book_requests book_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.book_requests
    ADD CONSTRAINT book_requests_pkey PRIMARY KEY (book_no, rqst_sequence_no, item_no);


--
-- Name: itineraries itenary_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itineraries
    ADD CONSTRAINT itenary_pkey PRIMARY KEY (book_no, route_no, alt_itinerary_no, itinerary_no);


--
-- Name: pax_contact pax_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pax_contact
    ADD CONSTRAINT pax_contact_pkey PRIMARY KEY (book_no, pax_no);


--
-- Name: passengers pax_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.passengers
    ADD CONSTRAINT pax_pkey PRIMARY KEY (book_no, pax_no);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_no);


--
-- PostgreSQL database dump complete
--

