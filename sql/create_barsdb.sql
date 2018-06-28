--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases
--

DROP DATABASE barsdb;




--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION;






--
-- Database creation
--

CREATE DATABASE barsdb WITH TEMPLATE = template0 OWNER = postgres;
REVOKE ALL ON DATABASE template1 FROM PUBLIC;
REVOKE ALL ON DATABASE template1 FROM postgres;
GRANT ALL ON DATABASE template1 TO postgres;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect barsdb

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: acc_sales_revenue; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE acc_sales_revenue (
    branch_code character(12) NOT NULL,
    open_date_time timestamp WITH time zone NOT NULL,
    transaction_type character(1) NOT NULL,
    document_type character(1) NOT NULL,
    document_number character(20) NOT NULL,
    ticket_type character(1),
    valid_void_flag character(1) NOT NULL,
    locator character(6) NOT NULL,
    pax_name character(38) NOT NULL,
    pax_code character(5) NOT NULL,
    tour_code character(20),
    ticket_sequence_no smallint NOT NULL,
    payment_amount numeric(15,5) NOT NULL,
    currency_code character(3) NOT NULL,
    payment_form character(3) NOT NULL,
    cc_approval_code character(6),
    tax1_code character(3),
    tax1_amount numeric(15,5),
    tax1_currency character(3),
    tax2_code character(3),
    tax2_amount numeric(15,5),
    tax2_currency character(3),
    tax3_code character(3),
    tax3_amount numeric(15,5),
    tax3_currency character(3),
    equiv_fare_paid bigint,
    equiv_fare_curr character(3),
    agency_commission bigint,
    agency_comm_curr character(3),
    issued_in_exch character(13),
    book_agent_code character(10) NOT NULL,
    issue_agent_code character(10) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.acc_sales_revenue OWNER TO postgres;

--
-- Name: action_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE action_codes (
    company_code character(3) NOT NULL,
    action_code character(2) NOT NULL,
    display_priority smallint NOT NULL,
    short_description character(12),
    description character varying(255),
    action_category character(1) DEFAULT 'N'::bpchar,
    seat_request_type character(1) DEFAULT 'N'::bpchar,
    tty_flag character(1) DEFAULT 'N'::bpchar,
    inter_sys_avail_flag character(1) DEFAULT 'N'::bpchar,
    action_flag character(1) DEFAULT 'N'::bpchar,
    group_flag character(1) DEFAULT 'N'::bpchar,
    ssr_flag character(1) DEFAULT 'N'::bpchar,
    authority_level smallint NOT NULL,
    to_action_codes character varying(45),
    to_auth_levels character varying(75),
    to_airline_type character varying(30),
    ttyo_cancel_code character(2),
    tty_time_flag character(1),
    tty_disptn_flag character(1) DEFAULT 'N'::bpchar,
    tty_agrmnt_flag character(1) DEFAULT 'N'::bpchar,
    tty_altsegm_flag character(1) DEFAULT 'N'::bpchar,
    tty_condhold_flag character(1) DEFAULT 'N'::bpchar,
    tty_ackno_flag character(1) DEFAULT 'N'::bpchar,
    sell_to_code character(2),
    waitlist_to_code character(2),
    final_to_code character(2),
    ticket_to_code character(2),
    schedchange_to_code character(2),
    timechg_to_code character(2),
    tty_sell_code character(2),
    schedchange_sell_to character(2),
    tty_wl_code character(2),
    tty_final_code character(2),
    tty_schd_canx character(2),
    tty_schd_sell character(2),
    final_queue_flag character(1) DEFAULT 'N'::bpchar,
    tran_type character(1),
    rts_group_code character(2),
    rts_unable_flag character(1),
    rts_unable_code character(2),
    rts_unable_wl_code character(2),
    rts_unable_branch character(12),
    rts_unable_queue character(5),
    tty_group_code character(2),
    tty_unable_flag character(1),
    tty_unable_code character(2),
    tty_unable_wl_code character(2),
    tty_unable_branch character(12),
    tty_unable_queue character(5),
    pnl_adl_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.action_codes OWNER TO postgres;

--
-- Name: adl_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE adl_rule (
    pnl_adl_rule_code character(5) NOT NULL,
    adl_sequence_no smallint NOT NULL,
    adl_gen_type character(1) NOT NULL,
    adl_start_range smallint NOT NULL,
    adl_end_range smallint NOT NULL,
    adl_interval smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.adl_rule OWNER TO postgres;

--
-- Name: agency_book_agency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_book_agency (
    agency_code character(8) NOT NULL,
    auth_agency_code character(8) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.agency_book_agency OWNER TO postgres;

--
-- Name: agency_comm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_comm (
    agency_code character(8) NOT NULL,
    commission_type character(1) NOT NULL,
    commission_code character(16) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.agency_comm OWNER TO postgres;

--
-- Name: agency_fare_modifier; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_fare_modifier (
    agency_fare_modifier_id bigint NOT NULL,
    agency_code character varying(255) NOT NULL,
    change_type character(1) NOT NULL,
    change_amount numeric(15,5) NOT NULL,
    invalidated_user character(5),
    invalid_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.agency_fare_modifier OWNER TO postgres;

--
-- Name: agency_fare_modifier_agency_fare_modifier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE agency_fare_modifier_agency_fare_modifier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agency_fare_modifier_agency_fare_modifier_id_seq OWNER TO postgres;

--
-- Name: agency_fare_modifier_agency_fare_modifier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE agency_fare_modifier_agency_fare_modifier_id_seq OWNED BY agency_fare_modifier.agency_fare_modifier_id;


--
-- Name: agency_hierarchy; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_hierarchy (
    agency_code character(8) NOT NULL,
    agency_hierarchy character varying(135) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.agency_hierarchy OWNER TO postgres;

--
-- Name: agency_office_status_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_office_status_ref (
    agency_office_status_rcd character(2) NOT NULL,
    name character varying(100) NOT NULL,
    active_flag integer NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.agency_office_status_ref OWNER TO postgres;

--
-- Name: agency_route_fare_modifier; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_route_fare_modifier (
    agency_route_fare_modifier_id bigint NOT NULL,
    route_id bigint NOT NULL,
    agency_code character varying(255) NOT NULL,
    change_type character(1) NOT NULL,
    change_amount numeric(15,5) NOT NULL,
    invalidated_user character(5),
    invalid_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.agency_route_fare_modifier OWNER TO postgres;

--
-- Name: agency_route_fare_modifier_agency_route_fare_modifier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE agency_route_fare_modifier_agency_route_fare_modifier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agency_route_fare_modifier_agency_route_fare_modifier_id_seq OWNER TO postgres;

--
-- Name: agency_route_fare_modifier_agency_route_fare_modifier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE agency_route_fare_modifier_agency_route_fare_modifier_id_seq OWNED BY agency_route_fare_modifier.agency_route_fare_modifier_id;


--
-- Name: agency_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE agency_user (
    agency_code character(8) NOT NULL,
    agent_code character(5) NOT NULL,
    agent_name character varying(30),
    passwd_expiry_date date,
    account_expired_flag integer DEFAULT 0,
    password_hash character varying(45),
    failed_logins smallint,
    alt_agent_code character varying(255),
    department character varying(30),
    mail_address1 character varying(30),
    mail_address2 character varying(30),
    mail_city character varying(25),
    mail_state character(2),
    mail_zip character varying(10),
    mail_nation character varying(25),
    email_address character varying(150),
    contact_phone_no character varying(30),
    contact_mobile_no character varying(30),
    user_type character varying(20),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.agency_user OWNER TO postgres;


--
-- Name: aig_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE aig_transaction (
    transaction_id integer NOT NULL,
    message_id character varying(24) NOT NULL,
    transaction_type character varying(10) NOT NULL,
    book_no integer NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    policy_number character varying(10) DEFAULT ''::character varying,
    failure_flag character(1) DEFAULT 'N'::bpchar,
    request_data character varying(16000),
    reply_data character varying(16000),
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    update_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.aig_transaction OWNER TO postgres;

--
-- Name: aig_transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE aig_transaction_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.aig_transaction_transaction_id_seq OWNER TO postgres;

--
-- Name: aig_transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE aig_transaction_transaction_id_seq OWNED BY aig_transaction.transaction_id;


--
-- Name: aircraft_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE public.aircraft_config (
    config_table character(5) NOT NULL,
    company_code character(3) NOT NULL,
    selling_class character(2) NOT NULL,
    aircraft_code character(3) NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    gen_flag_invt character(1) NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);

ALTER TABLE public.aircraft_config OWNER TO postgres;

-- NEW TABLE

CREATE TABLE equipment_config (
    company_code character(3) NOT NULL,
    aircraft_code character(3) NOT NULL,
    config_table character(5) NOT NULL,
    tail_number character varying(20),
    cabin_code character(2) NOT NULL,
    seat_capacity smallint NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.equipment_config OWNER TO postgres;

--
-- Name: airport; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport (
    airport_code character(5) NOT NULL,
    city_code character(5) NOT NULL,
    airport_name character varying(60),
    city_name character varying(60),
    country_code character varying(2),
    local_time_zone character varying(12),
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport OWNER TO postgres;

--
-- Name: airport_device; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_device (
    airport_device_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(255),
    airport_device_type_rcd character varying(5),
    airport_workstation_id integer,
    device_status_rcd character varying(5),
    device_status_updated timestamp WITH time zone,
    active_flag character(1) NOT NULL,
    last_retrieved_adq_id integer,
    wait_for_response_flag character(1),
    device_mode character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_device OWNER TO postgres;

--
-- Name: airport_device_airport_device_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE airport_device_airport_device_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.airport_device_airport_device_id_seq OWNER TO postgres;

--
-- Name: airport_device_airport_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE airport_device_airport_device_id_seq OWNED BY airport_device.airport_device_id;


--
-- Name: airport_device_queue; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_device_queue (
    airport_device_queue_id integer NOT NULL,
    airport_device_id integer NOT NULL,
    airport_device_queue_entry_type_rcd character varying(5) NOT NULL,
    original_message_id integer,
    processed_flag character(1),
    queued_date_time timestamp WITH time zone,
    processed_date_time timestamp WITH time zone,
    message_data character varying(31000),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_device_queue OWNER TO postgres;

--
-- Name: airport_device_queue_airport_device_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE airport_device_queue_airport_device_queue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.airport_device_queue_airport_device_queue_id_seq OWNER TO postgres;

--
-- Name: airport_device_queue_airport_device_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE airport_device_queue_airport_device_queue_id_seq OWNED BY airport_device_queue.airport_device_queue_id;


--
-- Name: airport_device_queue_entry_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_device_queue_entry_type_ref (
    airport_device_queue_entry_type_rcd character varying(5) NOT NULL,
    description character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_device_queue_entry_type_ref OWNER TO postgres;

--
-- Name: airport_device_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_device_type_ref (
    airport_device_type_rcd character varying(5) NOT NULL,
    description character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_device_type_ref OWNER TO postgres;

--
-- Name: airport_workstation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_workstation (
    airport_workstation_id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(255),
    airport_code character varying(5) NOT NULL,
    branch_code character varying(20),
    airport_workstation_type_rcd character varying(5),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_workstation OWNER TO postgres;

--
-- Name: airport_workstation_airport_workstation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE airport_workstation_airport_workstation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.airport_workstation_airport_workstation_id_seq OWNER TO postgres;

--
-- Name: airport_workstation_airport_workstation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE airport_workstation_airport_workstation_id_seq OWNED BY airport_workstation.airport_workstation_id;


--
-- Name: airport_workstation_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE airport_workstation_type_ref (
    airport_workstation_type_rcd character varying(5) NOT NULL,
    description character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.airport_workstation_type_ref OWNER TO postgres;

--
-- Name: allotment_detail; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE allotment_detail (
    allotment_id bigint NOT NULL,
    flight_date date NOT NULL,
    allotment_book_no integer,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.allotment_detail OWNER TO postgres;

--
-- Name: allotment_header; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE allotment_header (
    allotment_id integer NOT NULL,
    allotment_description character(50),
    flight_number character(7) NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    origin_branch_code character(12) NOT NULL,
    allotment_type character(2) NOT NULL,
    allotment_seat_qty smallint NOT NULL,
    allotment_fare bigint,
    allotment_currency character(3),
    allotment_agency character(8),
    allotment_carrier character(3),
    allotment_release_days integer,
    allotment_release_interval character(1) DEFAULT 'D'::bpchar,
    allotment_status character(1) DEFAULT 'A'::bpchar,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.allotment_header OWNER TO postgres;

--
-- Name: allotment_header_allotment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE allotment_header_allotment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.allotment_header_allotment_id_seq OWNER TO postgres;

--
-- Name: allotment_header_allotment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE allotment_header_allotment_id_seq OWNED BY allotment_header.allotment_id;


--
-- Name: arpt_terminal; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE arpt_terminal (
    airport_code character(5) NOT NULL,
    start_terminal character(2) NOT NULL,
    end_terminal character(2) NOT NULL,
    conn_time_mins smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.arpt_terminal OWNER TO postgres;

--
-- Name: asr_reconcile_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE asr_reconcile_history (
    action_id integer NOT NULL,
    flight_date_leg_id integer NOT NULL,
    action_detail character varying(255),
    update_user character varying(5) NOT NULL,
    update_group character varying(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.asr_reconcile_history OWNER TO postgres;

--
-- Name: asr_reconcile_history_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE asr_reconcile_history_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.asr_reconcile_history_action_id_seq OWNER TO postgres;

--
-- Name: asr_reconcile_history_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE asr_reconcile_history_action_id_seq OWNED BY asr_reconcile_history.action_id;


--
-- Name: atm_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE atm_history (
    trans_name character(10) NOT NULL,
    payment_code character varying(20) NOT NULL,
    payment_no integer,
    cust_id character varying(20),
    bank_code character(3),
    branch_code character(4),
    terminal_code character(4),
    trans_ch character(4),
    trans_datetime character varying(14),
    trans_amt character varying(13),
    trans_type character(1),
    trans_result character varying(20),
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.atm_history OWNER TO postgres;

--
-- Name: attribute_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE attribute_rule (
    attribute_rule_id integer NOT NULL,
    seat_attribute_rcd character varying(5),
    pax_code character varying(5),
    request_code character varying(5),
    selling_class character varying(2),
    allow_flag integer DEFAULT 0 NOT NULL,
    invalid_time timestamp WITH time zone,
    invalidated_user character varying(5),
    remark character varying(240),
    create_time timestamp WITH time zone,
    create_user character varying(5)
);


ALTER TABLE public.attribute_rule OWNER TO postgres;

--
-- Name: attribute_rule_attribute_rule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE attribute_rule_attribute_rule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attribute_rule_attribute_rule_id_seq OWNER TO postgres;

--
-- Name: attribute_rule_attribute_rule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE attribute_rule_attribute_rule_id_seq OWNED BY attribute_rule.attribute_rule_id;


--
-- Name: authority_levels; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE authority_levels (
    company_code character(3) NOT NULL,
    duty_code character(3) NOT NULL,
    description character varying(160),
    authority_level smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.authority_levels OWNER TO postgres;

--
-- Name: availability_activity; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE availability_activity (
    origin character(3),
    destination character(3),
    start_date date,
    end_date date,
    return_flag character(1),
    fares_flag character(1),
    seat_count smallint,
    available_only_flag character(1),
    branch character(20),
    duration_ms integer,
    rows_returned smallint,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.availability_activity OWNER TO postgres;

--
-- Name: availbty_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE availbty_rule (
    pair_rule_no character(8) NOT NULL,
    default_depr_time smallint,
    max_journey_hrs smallint,
    max_stopovr_hrs smallint,
    no_of_days_forw smallint,
    no_of_days_back smallint,
    no_of_flights smallint,
    no_of_flts_back smallint,
    max_no_of_stops smallint,
    max_no_of_conns smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.availbty_rule OWNER TO postgres;

--
-- Name: avs_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE avs_history (
    avs_history_id bigint NOT NULL,
    departure_airport character varying(5) NOT NULL,
    arrival_airport character varying(5) NOT NULL,
    origin_address character varying(10) NOT NULL,
    dest_address character varying(10) NOT NULL,
    flight_number character varying(7) NOT NULL,
    board_date date NOT NULL,
    class character varying(2) NOT NULL,
    message character varying(1024) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.avs_history OWNER TO postgres;

--
-- Name: avs_history_avs_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE avs_history_avs_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.avs_history_avs_history_id_seq OWNER TO postgres;

--
-- Name: avs_history_avs_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE avs_history_avs_history_id_seq OWNED BY avs_history.avs_history_id;


--
-- Name: bbl_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE bbl_transaction (
    bbl_transaction_id integer NOT NULL,
    locator character varying(10),
    approved character(1) DEFAULT 'N'::bpchar NOT NULL,
    request text,
    request_data text,
    reply text,
    rqst_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    rply_date_time timestamp WITH time zone,
    settled character(1) DEFAULT 'N'::bpchar NOT NULL,
    sett_request text,
    sett_request_data text,
    sett_reply text,
    sett_request_date_time timestamp WITH time zone,
    sett_reply_date_time timestamp WITH time zone,
    external_tran_id character varying(30)
);


ALTER TABLE public.bbl_transaction OWNER TO postgres;

--
-- Name: bbl_transaction_bbl_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bbl_transaction_bbl_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bbl_transaction_bbl_transaction_id_seq OWNER TO postgres;

--
-- Name: bbl_transaction_bbl_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bbl_transaction_bbl_transaction_id_seq OWNED BY bbl_transaction.bbl_transaction_id;


--
-- Name: bilatrl_actn_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE bilatrl_actn_codes (
    company_code character(3) NOT NULL,
    carrier_code character(3) NOT NULL,
    action_code character(2) NOT NULL,
    description character(30),
    update_user character(5),
    update_group character(8),
    update_time character(19)
);


ALTER TABLE public.bilatrl_actn_codes OWNER TO postgres;

--
-- Name: blocked_seat_update_queue; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE blocked_seat_update_queue (
    seat_map_id integer NOT NULL,
    change_date_time timestamp WITH time zone NOT NULL,
    active_flag character(1) NOT NULL,
    processed_date_time timestamp WITH time zone,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT blocked_seat_update_queue_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.blocked_seat_update_queue OWNER TO postgres;

--
-- Name: boarding_control_number; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE boarding_control_number (
    boarding_control_number_id integer NOT NULL,
    flight_date_leg_id integer NOT NULL,
    bcn_no smallint NOT NULL,
    active_flag character(1),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone,
    CONSTRAINT boarding_control_number_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.boarding_control_number OWNER TO postgres;

--
-- Name: boarding_control_number_boarding_control_number_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE boarding_control_number_boarding_control_number_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.boarding_control_number_boarding_control_number_id_seq OWNER TO postgres;

--
-- Name: boarding_control_number_boarding_control_number_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE boarding_control_number_boarding_control_number_id_seq OWNED BY boarding_control_number.boarding_control_number_id;


--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE bookings (
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
    departure_airport character(5),
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
    create_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: book_additional_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_additional_data (
    book_additional_data_id integer NOT NULL,
    agency_code character varying(8),
    branch_code character varying(12),
    booking_category_code character(1),
    description character varying(255) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_additional_data OWNER TO postgres;

--
-- Name: book_additional_data_book_additional_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_additional_data_book_additional_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_additional_data_book_additional_data_id_seq OWNER TO postgres;

--
-- Name: book_additional_data_book_additional_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_additional_data_book_additional_data_id_seq OWNED BY book_additional_data.book_additional_data_id;


--
-- Name: book_additional_data_field; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_additional_data_field (
    book_additional_data_field_id integer NOT NULL,
    book_additional_data_id integer NOT NULL,
    field_control_type_rcd character varying(5),
    application_field_code character varying(30),
    field_name character varying(50) NOT NULL,
    field_caption character varying(100) NOT NULL,
    mandatory_flag character(1) NOT NULL,
    seq_no smallint,
    validation_regexp character varying(255),
    parse_regexp character varying(255),
    allow_manual_edit character(1) DEFAULT 'Y'::bpchar NOT NULL,
    allow_multiple_values character(1) DEFAULT 'Y'::bpchar NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_additional_data_field OWNER TO postgres;

--
-- Name: book_additional_data_field_book_additional_data_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_additional_data_field_book_additional_data_field_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_additional_data_field_book_additional_data_field_id_seq OWNER TO postgres;

--
-- Name: book_additional_data_field_book_additional_data_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_additional_data_field_book_additional_data_field_id_seq OWNED BY book_additional_data_field.book_additional_data_field_id;


--
-- Name: book_additional_data_field_value; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_additional_data_field_value (
    book_additional_data_field_value_id integer NOT NULL,
    book_additional_data_field_id integer NOT NULL,
    book_no integer NOT NULL,
    field_value_string character varying(255),
    field_value_int integer,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_additional_data_field_value OWNER TO postgres;

--
-- Name: book_additional_data_field_va_book_additional_data_field_va_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_additional_data_field_va_book_additional_data_field_va_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_additional_data_field_va_book_additional_data_field_va_seq OWNER TO postgres;

--
-- Name: book_additional_data_field_va_book_additional_data_field_va_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_additional_data_field_va_book_additional_data_field_va_seq OWNED BY book_additional_data_field_value.book_additional_data_field_value_id;


--
-- Name: book_category_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_category_ref (
    book_category_rcd character(10) NOT NULL,
    description character varying(250) NOT NULL,
    user_code character(5) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.book_category_ref OWNER TO postgres;

--
-- Name: book_commission; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_commission (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    comm_amount numeric(15,5) NOT NULL,
    commission_descr character varying(80),
    commission_sent numeric(15,5),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_commission OWNER TO postgres;

--
-- Name: book_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_no_seq
    START WITH 3200000
    INCREMENT BY 1
    MINVALUE 3200000
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_no_seq OWNER TO postgres;

--
-- Name: book_cross_index; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_cross_index (
    locator character(6) NOT NULL,
    origin_address character(7) NOT NULL,
    book_no integer DEFAULT nextval('book_no_seq'::regclass) NOT NULL,
    book_category character(1) NOT NULL,
    reply_poll_flag character(1),
    processing_flag character(1) NOT NULL,
    ext_locator character(6),
    codeshare_book_numb character(6),
    update_user character(5) NOT NULL,
    update_group character(12) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_cross_index OWNER TO postgres;

--
-- Name: book_fares; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_fares (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(90),
    status_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_fares OWNER TO postgres;

--
-- Name: book_fares_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_fares_pass (
    book_no integer NOT NULL,
    pax_code character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_fares_pass OWNER TO postgres;

--
-- Name: book_fares_paym; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_fares_paym (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    payment_code character(5) NOT NULL,
    fare_calc_code character(15) NOT NULL,
    fare_paymt_amount numeric(15,5) NOT NULL,
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_fares_paym OWNER TO postgres;

--
-- Name: booking_fare_segments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_fare_segments (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.booking_fare_segments OWNER TO postgres;

--
-- Name: book_fares_tckt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_fares_tckt (
    book_no integer NOT NULL,
    fare_sequence_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    ticket_sequence_no smallint NOT NULL,
    baggage_alownce character varying(35),
    before_date character varying(35),
    after_date character varying(35),
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_fares_tckt OWNER TO postgres;

--
-- Name: book_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_history (
    book_no integer NOT NULL,
    create_time character(19) NOT NULL,
    hist_sequence_no smallint NOT NULL,
    history_code character(3) NOT NULL,
    tran_type character(2) NOT NULL,
    item_sequence_no smallint NOT NULL,
    item_text character varying(255) NOT NULL,
    received_from character varying(60) NOT NULL,
    processing_flag character(1),
    duty_code character(5) NOT NULL,
    branch_code character(12) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL
);


ALTER TABLE public.book_history OWNER TO postgres;

--
-- Name: book_paymt_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_paymt_pass (
    book_no integer NOT NULL,
    pay_sequence_no smallint NOT NULL,
    pax_no smallint,
    fare_sequence_no smallint,
    pax_code character(5),
    flight_no character(7),
    board_date date,
    departure_airport character(5),
    arrival_airport character(5),
    start_airport character(5),
    end_airport character(5),
    book_paymt_amount numeric(15,5) NOT NULL,
    dep_pay_sequence_no smallint NOT NULL,
    payment_code character(10) NOT NULL,
    fare_calc_code character(45) NOT NULL,
    currency_code character(3) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_paymt_pass OWNER TO postgres;

--
-- Name: book_paymt_tckt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_paymt_tckt (
    book_no integer NOT NULL,
    ticket_sequence_no smallint NOT NULL,
    payment_no integer NOT NULL,
    transaction_no smallint,
    transaction_type character(1),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    payment_amount numeric(15,5) NOT NULL,
    document_no character(25),
    cc_expiry_date character(4),
    ticket_no character varying(20) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE public.book_paymt_tckt OWNER TO postgres;

--
-- Name: book_reinstate_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_reinstate_log (
    book_reinstate_log_no integer NOT NULL,
    record_locator character varying(6),
    reinstated_date_time timestamp WITH time zone,
    requested_by character varying(20)
);


ALTER TABLE public.book_reinstate_log OWNER TO postgres;

--
-- Name: book_reinstate_log_book_reinstate_log_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_reinstate_log_book_reinstate_log_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_reinstate_log_book_reinstate_log_no_seq OWNER TO postgres;

--
-- Name: book_reinstate_log_book_reinstate_log_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_reinstate_log_book_reinstate_log_no_seq OWNED BY book_reinstate_log.book_reinstate_log_no;


--
-- Name: book_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_requests (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_requests OWNER TO postgres;

--
-- Name: book_requests_old; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_requests_old (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_requests_old OWNER TO postgres;

--
-- Name: book_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_serial_nos (
    book_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.book_serial_nos OWNER TO postgres;

--
-- Name: book_serial_nos_book_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_serial_nos_book_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_serial_nos_book_no_seq OWNER TO postgres;

--
-- Name: book_serial_nos_book_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_serial_nos_book_no_seq OWNED BY book_serial_nos.book_no;


--
-- Name: book_summary_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_summary_history (
    book_no integer NOT NULL,
    book_summary_history_rcd character(10) NOT NULL,
    sent_date_time timestamp WITH time zone NOT NULL,
    user_code character(5) NOT NULL,
    email_address character varying(150),
    link_id bigint,
    ackn_timestamp timestamp WITH time zone,
    ackn_information character varying(100)
);


ALTER TABLE public.book_summary_history OWNER TO postgres;

--
-- Name: book_ticket_cpn; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_ticket_cpn (
    book_no integer NOT NULL,
    ticket_sequence_no smallint NOT NULL,
    coupon_sequence_no smallint NOT NULL,
    xo_indicator character(1),
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    flight_number character(7) NOT NULL,
    selling_class character(3) NOT NULL,
    board_date date NOT NULL,
    departure_time smallint NOT NULL,
    coupon_status character varying(3) NOT NULL,
    invol_ind character varying(3),
    uac_state character(1) DEFAULT 'N'::bpchar NOT NULL,
    cos_state character(1) DEFAULT 'N'::bpchar NOT NULL,
    fare_basis_code character(15) NOT NULL,
    valid_from_date date,
    valid_to_date date,
    baggage_alownce character(5),
    coupon_number smallint,
    coupon_disposition character(1) NOT NULL,
    sac_code character varying(20),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_ticket_cpn OWNER TO postgres;

--
-- Name: book_ticket; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_ticket (
    book_no integer NOT NULL,
    ticket_sequence_no smallint NOT NULL,
    tkt_document_no character(11),
    issued_by character varying(80),
    tour_code character(10),
    origin_dest character(11),
    intrnatnal_sale character(4),
    endrsmnt_rstrctns character varying(90),
    it_bt_fare numeric(15,5),
    it_bt_curr character(3),
    airline_data character(10),
    issued_in_exch character(13),
    fare_no smallint NOT NULL,
    pax_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    pax_name character(53) NOT NULL,
    conjunction_tckts character varying(35),
    conj_ticket_ind smallint NOT NULL,
    conj_ticket_sequence_no smallint NOT NULL,
    fare_amount numeric(15,5) NOT NULL,
    fare_curr character(3) NOT NULL,
    fare_text character(2),
    equiv_fare_pd numeric(15,5),
    equiv_fare_curr character(3),
    tax1_code character(15),
    tax1_amount numeric(15,5),
    tax1_currency character(3),
    tax1_nation_code character(2),
    tax1_text character(6),
    tax1_refund_flag character(1),
    tax1_exempt_flag character(1),
    tax2_code character(15),
    tax2_amount numeric(15,5),
    tax2_currency character(3),
    tax2_nation_code character(2),
    tax2_text character(6),
    tax2_refund_flag character(1),
    tax2_exempt_flag character(1),
    tax3_code character(15),
    tax3_amount numeric(15,5),
    tax3_currency character(3),
    tax3_nation_code character(2),
    tax3_text character(6),
    tax3_refund_flag character(1),
    tax3_exempt_flag character(1),
    total_amount numeric(15,5) NOT NULL,
    total_currency character(3) NOT NULL,
    total_text character(6),
    fare_construction character varying(255) NOT NULL,
    payment_form character varying(255),
    cc_approval_code character(6),
    cc_approval_type character varying(70),
    al_agent_no integer,
    stock_ctrl_no character(10),
    original_issue character varying(70),
    airline_code smallint,
    check_digit smallint,
    issue_date date,
    issue_branch character(12),
    ticket_type character(1),
    status_flag character(1) NOT NULL,
    ticket_disposition character(1) NOT NULL,
    agency_commission numeric(15,5),
    agency_curr_code character(3),
    scrutiny_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_ticket OWNER TO postgres;

--
-- Name: book_time_limits; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_time_limits (
    book_no integer NOT NULL,
    timelmt_sequence_no smallint NOT NULL,
    timelmt_type character(1) NOT NULL,
    limit_time timestamp WITH time zone,
    cancel_flag character(1) NOT NULL,
    queue_code character(5),
    dest_branch character(12) NOT NULL,
    remark_text character(240),
    all_pax_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.book_time_limits OWNER TO postgres;

--
-- Name: book_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE book_transaction (
    book_transaction_id integer NOT NULL,
    current_et_serial_no integer NOT NULL,
    book_no integer NOT NULL,
    begin_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    end_date_time timestamp WITH time zone,
    rollback_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    commit_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    ext_transaction_ref character varying(32),
    transaction_note character varying(255)
);


ALTER TABLE public.book_transaction OWNER TO postgres;

--
-- Name: book_transaction_book_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE book_transaction_book_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.book_transaction_book_transaction_id_seq OWNER TO postgres;

--
-- Name: book_transaction_book_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE book_transaction_book_transaction_id_seq OWNED BY book_transaction.book_transaction_id;


--
-- Name: booking_cleanup_book_ticket; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_cleanup_book_ticket (
    action_id integer NOT NULL,
    book_no integer NOT NULL,
    ticket_sequence_no smallint NOT NULL,
    tkt_document_no character(11),
    issued_by character varying(80),
    tour_code character(10),
    origin_dest character(11),
    intrnatnal_sale character(4),
    endrsmnt_rstrctns character varying(90),
    it_bt_fare numeric(15,5),
    it_bt_curr character(3),
    airline_data character(10),
    issued_in_exch character(13),
    fare_no smallint NOT NULL,
    pax_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    pax_name character(53) NOT NULL,
    conjunction_tckts character varying(35),
    conj_ticket_ind smallint NOT NULL,
    conj_ticket_sequence_no smallint NOT NULL,
    fare_amount numeric(15,5) NOT NULL,
    fare_curr character(3) NOT NULL,
    fare_text character(2),
    equiv_fare_pd numeric(15,5),
    equiv_fare_curr character(3),
    tax1_code character(15),
    tax1_amount numeric(15,5),
    tax1_currency character(3),
    tax1_nation_code character(2),
    tax1_text character(6),
    tax1_refund_flag character(1),
    tax1_exempt_flag character(1),
    tax2_code character(15),
    tax2_amount numeric(15,5),
    tax2_currency character(3),
    tax2_nation_code character(2),
    tax2_text character(6),
    tax2_refund_flag character(1),
    tax2_exempt_flag character(1),
    tax3_code character(15),
    tax3_amount numeric(15,5),
    tax3_currency character(3),
    tax3_nation_code character(2),
    tax3_text character(6),
    tax3_refund_flag character(1),
    tax3_exempt_flag character(1),
    total_amount numeric(15,5) NOT NULL,
    total_currency character(3) NOT NULL,
    total_text character(6),
    fare_construction character varying(255) NOT NULL,
    payment_form character varying(255),
    cc_approval_code character(6),
    cc_approval_type character varying(70),
    al_agent_no integer,
    stock_ctrl_no character(10),
    original_issue character varying(70),
    airline_code smallint,
    check_digit smallint,
    issue_date date,
    issue_branch character(12),
    ticket_type character(1),
    status_flag character(1) NOT NULL,
    ticket_disposition character(1) NOT NULL,
    agency_commission numeric(15,5),
    agency_curr_code character(3),
    scrutiny_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.booking_cleanup_book_ticket OWNER TO postgres;

--
-- Name: booking_cleanup_et; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_cleanup_et (
    action_id integer NOT NULL,
    et_serial_no integer NOT NULL,
    et_sequence_no smallint NOT NULL,
    key_code character(5) NOT NULL,
    book_no integer NOT NULL,
    company_code character(3) NOT NULL,
    process_type character(5) NOT NULL,
    tran_type character(1) NOT NULL,
    control_param character(25),
    validate_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    proc_date_time character(19),
    et_info_1 character varying(250),
    et_info_2 character varying(250),
    et_info_3 character varying(250),
    et_info_4 character varying(250),
    et_info_5 character varying(250),
    et_info_6 character varying(250),
    et_info_7 character varying(250),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.booking_cleanup_et OWNER TO postgres;

--
-- Name: booking_cleanup_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_cleanup_log (
    action_id integer NOT NULL,
    action_type character(1),
    book_no integer,
    locator character(6),
    action_reason character varying(100),
    create_time timestamp WITH time zone,
    create_user character(5)
);


ALTER TABLE public.booking_cleanup_log OWNER TO postgres;

--
-- Name: booking_cleanup_log_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE booking_cleanup_log_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.booking_cleanup_log_action_id_seq OWNER TO postgres;

--
-- Name: booking_cleanup_log_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE booking_cleanup_log_action_id_seq OWNED BY booking_cleanup_log.action_id;


--
-- Name: booking_cleanup_passenger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_cleanup_passenger (
    action_id integer NOT NULL,
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.booking_cleanup_passenger OWNER TO postgres;

--
-- Name: booking_cleanup_payment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_cleanup_payment (
    action_id integer NOT NULL,
    payment_no integer NOT NULL,
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
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.booking_cleanup_payment OWNER TO postgres;

--
-- Name: booking_summary; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary (
    booking_number integer NOT NULL,
    booking_date_time timestamp WITH time zone NOT NULL,
    booking_summary_type_rcd character(10),
    pax_name character varying(53),
    sid_no integer,
    voucher_number integer
);


ALTER TABLE public.booking_summary OWNER TO postgres;

--
-- Name: booking_summary_email_cc; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary_email_cc (
    booking_summary_email_cc_id bigint NOT NULL,
    email_address character varying(200) NOT NULL,
    user_code character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    create_user character(5) NOT NULL,
    inactivated_date_time timestamp WITH time zone,
    inactivated_user_code character(5),
    made_from_booking_summary_email_cc_id bigint
);


ALTER TABLE public.booking_summary_email_cc OWNER TO postgres;

--
-- Name: booking_summary_email_cc_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary_email_cc_mapping (
    booking_summary_email_cc_mapping_id bigint NOT NULL,
    booking_summary_email_cc_id bigint NOT NULL,
    booking_summary_type_rcd character(10) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    create_user character(5) NOT NULL,
    inactivated_date_time timestamp WITH time zone,
    inactivated_user_code character(5)
);


ALTER TABLE public.booking_summary_email_cc_mapping OWNER TO postgres;

--
-- Name: booking_summary_header; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary_header (
    column_name character varying(50) NOT NULL,
    column_caption character varying(100) NOT NULL
);


ALTER TABLE public.booking_summary_header OWNER TO postgres;

--
-- Name: booking_summary_temp; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary_temp (
    booking_number integer NOT NULL,
    booking_date_time timestamp WITH time zone NOT NULL,
    booking_summary_type_rcd character(10),
    pax_name character varying(53),
    sid_no integer,
    voucher_number integer
);


ALTER TABLE public.booking_summary_temp OWNER TO postgres;

--
-- Name: booking_summary_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE booking_summary_type_ref (
    booking_summary_type_rcd character(10) NOT NULL,
    description character(100) NOT NULL,
    user_code character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.booking_summary_type_ref OWNER TO postgres;

--
-- Name: branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE branch (
    branch_code character(12) NOT NULL,
    branch_name character varying(80),
    branch_type character(1),
    avl_display_digits smallint,
    no_of_days_forw smallint,
    no_of_days_back smallint,
    no_of_flights smallint,
    no_of_flts_back smallint,
    frequency_code character(7),
    oper_time_period1 character varying(100),
    oper_time_period2 character varying(100),
    oper_time_period3 character varying(100),
    address character varying(200),
    addr_city character(25),
    addr_state character(25),
    addr_zip character(15),
    addr_nation character(25),
    phone_no character varying(30),
    company_code character(3) NOT NULL,
    city_code character(5) NOT NULL,
    utr_recycle_days smallint,
    utr_recycle_mins smallint,
    lmtc_recycle_days smallint,
    lmtc_recycle_mins smallint,
    process_type character(5),
    numeric_code integer DEFAULT 0 NOT NULL,
    default_tty_addrs character(7),
    block_avail_time integer DEFAULT 0 NOT NULL,
    avail_display_mode character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.branch OWNER TO postgres;

--
-- Name: branch_stock_tckt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE branch_stock_tckt (
    branch_code character(12) NOT NULL,
    stock_number integer NOT NULL,
    stock_control_no character(10),
    book_no integer,
    ticket_status character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.branch_stock_tckt OWNER TO postgres;

--
-- Name: bsp_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE bsp_transaction (
    office_code integer NOT NULL,
    book_no integer NOT NULL,
    airline_code character(3) NOT NULL,
    tkt_document_no character(11) NOT NULL,
    ticket_type character(1) NOT NULL,
    transaction_code character(4) NOT NULL,
    full_exchange_info character varying(255),
    gross integer,
    total_discount integer,
    total_commission integer,
    total_tax integer,
    total_misc_charges integer,
    total_cash_payment integer,
    total_cc_payment integer,
    total_credit integer,
    total_ost integer,
    exchange_amount integer,
    total_ost_charge character varying(30),
    refunded_cpns character varying(4),
    total_refund_charge integer,
    issue_date date NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.bsp_transaction OWNER TO postgres;

--
-- Name: bulk_sms_zb; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE bulk_sms_zb (
    bulk_no integer NOT NULL,
    flight_number character varying(10),
    flight_date character varying(20),
    book_no character varying(10),
    msisdn character varying(13),
    userid character varying(5),
    xslt_template_id character varying(100),
    sent_date timestamp WITH time zone,
    status_code bigint,
    queued character(1),
    reply_ref_id bigint
);


ALTER TABLE public.bulk_sms_zb OWNER TO postgres;

--
-- Name: bulk_sms_zb_bulk_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bulk_sms_zb_bulk_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bulk_sms_zb_bulk_no_seq OWNER TO postgres;

--
-- Name: bulk_sms_zb_bulk_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE bulk_sms_zb_bulk_no_seq OWNED BY bulk_sms_zb.bulk_no;


--
-- Name: business_pax; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE business_pax (
    business_pax_id integer NOT NULL,
    description character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.business_pax OWNER TO postgres;

--
-- Name: business_pax_business_pax_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE business_pax_business_pax_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.business_pax_business_pax_id_seq OWNER TO postgres;

--
-- Name: business_pax_business_pax_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE business_pax_business_pax_id_seq OWNED BY business_pax.business_pax_id;


--
-- Name: business_pax_class; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE business_pax_class (
    business_pax_id integer NOT NULL,
    selling_class character varying(3) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.business_pax_class OWNER TO postgres;

--
-- Name: business_pax_fare; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE business_pax_fare (
    business_pax_id integer NOT NULL,
    fare_basis_code character varying(15) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.business_pax_fare OWNER TO postgres;

--
-- Name: cancel_fees; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE cancel_fees (
    company_code character(3) NOT NULL,
    xcl_code character(5) NOT NULL,
    pax_code character(5) NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    short_description character varying(30),
    description character varying(255),
    xcl_type character(1) NOT NULL,
    xcl_amount numeric(15,5) NOT NULL,
    xcl_currency character(3) NOT NULL,
    days_befr_depr smallint NOT NULL,
    applicable_flag character(5) NOT NULL,
    apply_for_flag character(1) NOT NULL,
    selling_class character(2) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    applies_to_branch_code character varying(15),
    applies_to_payment_type character varying(5),
    applies_to_payment_form character varying(5),
    tax_type character(1),
    tax_rate numeric(15,5),
    per_pax_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    fee_type character(1) DEFAULT 'B'::bpchar,
    fare_basis_code character varying(15),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.cancel_fees OWNER TO postgres;

--
-- Name: cash_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE cash_transaction (
    transaction_id integer NOT NULL,
    payment_no integer NOT NULL,
    action_code character(2) NOT NULL,
    terminal_id character(10) NOT NULL,
    orig_currcode character(3),
    orig_amount numeric(15,5),
    ext_sys_conf_no character varying(50),
    paid_currency character(3),
    paid_amount numeric(15,5),
    cancel_note character varying(255),
    reason_code character(7),
    process_code character(2),
    error_message character varying(255),
    create_time character(19) NOT NULL
);


ALTER TABLE public.cash_transaction OWNER TO postgres;

--
-- Name: cash_transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE cash_transaction_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cash_transaction_transaction_id_seq OWNER TO postgres;

--
-- Name: cash_transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE cash_transaction_transaction_id_seq OWNED BY cash_transaction.transaction_id;


--
-- Name: change_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE change_type_ref (
    change_type_code character(1) NOT NULL,
    description character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.change_type_ref OWNER TO postgres;

--
-- Name: changed_itinerary; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE changed_itinerary (
    book_no integer NOT NULL,
    route_no smallint NOT NULL,
    alt_itinerary_no smallint NOT NULL,
    itinerary_no smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.changed_itinerary OWNER TO postgres;

--
-- Name: char_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE char_mapping (
    ext_char character(1) NOT NULL,
    std_char character varying(3),
    description character varying(50)
);


ALTER TABLE public.char_mapping OWNER TO postgres;

--
-- Name: charging_stats; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE charging_stats (
    company_code character(3) NOT NULL,
    charge_code character(5) NOT NULL,
    charge_date date NOT NULL,
    charge_count smallint
);


ALTER TABLE public.charging_stats OWNER TO postgres;

--
-- Name: city; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE city (
    city_code character(5) NOT NULL,
    city_name character varying(60),
    state_code character(2) NOT NULL,
    flgt_serv_flag character(1) NOT NULL,
    generate_flag character(1) NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.city OWNER TO postgres;

--
-- Name: city_airport; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE city_airport (
    start_airport character(5) NOT NULL,
    end_airport character(5) NOT NULL,
    conn_time_mins smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.city_airport OWNER TO postgres;

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


--
-- Name: class_comb_route; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE class_comb_route (
    class_combine_id bigint NOT NULL,
    route_id bigint NOT NULL,
    active_flag character(1) NOT NULL,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.class_comb_route OWNER TO postgres;

--
-- Name: class_combinability; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE class_combinability (
    class_combine_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    class_code_1 character varying(15) NOT NULL,
    class_code_2 character varying(15) NOT NULL,
    allow_comb_flag character(1) NOT NULL,
    description character varying(200),
    active_flag character(1) NOT NULL,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.class_combinability OWNER TO postgres;

--
-- Name: client_contact_details; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_contact_details (
    client_prfl_no character(15) NOT NULL,
    contact_type character(1) NOT NULL,
    address character varying(200),
    city character varying(25),
    state character varying(25),
    zip character varying(15),
    nation character varying(25),
    phone_no character varying(30),
    mobile_no character varying(30),
    fax_no character varying(30),
    email_address character varying(150),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_contact_details OWNER TO postgres;

--
-- Name: client_credit_hist; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_credit_hist (
    client_prfl_no character(15) NOT NULL,
    crdt_sequence_no smallint NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    credit_amount numeric(15,5) NOT NULL,
    description character(80),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_credit_hist OWNER TO postgres;

--
-- Name: client_credits; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_credits (
    client_prfl_no character(15) NOT NULL,
    crdt_sequence_no smallint NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    credit_amount numeric(15,5) NOT NULL,
    org_credit_amount numeric(15,5),
    document_no character(51),
    document_date date,
    processing_date date,
    processing_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_credits OWNER TO postgres;

--
-- Name: client_documents; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_documents (
    client_prfl_no character(15) NOT NULL,
    docm_sequence_no smallint NOT NULL,
    document_catg character(3) NOT NULL,
    document_type character(2) NOT NULL,
    document_no character(25) NOT NULL,
    country_code character varying(2),
    gender character varying(2),
    docm_expry_date character varying(10),
    docm_issue_date date,
    last_used_date date NOT NULL,
    type_sequence_no smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_documents OWNER TO postgres;

--
-- Name: client_family; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_family (
    client_prfl_no character(15) NOT NULL,
    type_sequence_no smallint NOT NULL,
    family_type character(1) NOT NULL,
    family_name character varying(30),
    first_name character varying(30) NOT NULL,
    title character(5),
    initials character(3),
    birth_date date,
    anniversary_date date,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_family OWNER TO postgres;

--
-- Name: client_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_history (
    client_prfl_no character(15) NOT NULL,
    create_time character(19) NOT NULL,
    history_code character(3) NOT NULL,
    tran_type character(2) NOT NULL,
    item_sequence_no smallint NOT NULL,
    item_text character varying(255),
    duty_code character(5) NOT NULL,
    branch_code character(12) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL
);


ALTER TABLE public.client_history OWNER TO postgres;

--
-- Name: client_pax_code; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_pax_code (
    client_prfl_no character varying(15) NOT NULL,
    pax_code character varying(5) NOT NULL,
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_pax_code OWNER TO postgres;

--
-- Name: client_pos_defn; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_pos_defn (
    client_no smallint NOT NULL,
    pos_srno smallint NOT NULL,
    pos_table_no character(25) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_pos_defn OWNER TO postgres;

--
-- Name: client_preferences; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_preferences (
    client_prfl_no character(15) NOT NULL,
    attribute_sequence_no smallint NOT NULL,
    file_code character(4) NOT NULL,
    master_code character(5) NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_preferences OWNER TO postgres;

--
-- Name: client_profile; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_profile (
    client_prfl_no character(15) NOT NULL,
    client_name character(53) NOT NULL,
    pax_code character(5) DEFAULT 'ADULT'::bpchar NOT NULL,
    profile_type character(1) NOT NULL,
    company_prfl_no character(15),
    company_name character varying(30),
    client_title character(5),
    client_initial character(3),
    first_name character varying(30),
    branch_code character(12) NOT NULL,
    bussiness_title character varying(60),
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
    mail_address character varying(200),
    mail_city character(25),
    mail_state character(25),
    mail_zip character(15),
    mail_nation character(25),
    home_phone_no character varying(30),
    buss_phone_no character varying(30),
    contact_phone_no character varying(30),
    agent_phone_no character varying(30),
    client_fax_no character varying(30),
    carrier_codes character varying(40),
    hotel_codes character varying(75),
    car_rental_codes character varying(75),
    seat_types character varying(75),
    sport_hobbies character varying(75),
    holiday_dests character varying(75),
    holiday_types character varying(75),
    secretary_name character varying(38),
    trav_total_mile integer,
    trav_expenses numeric(15,5),
    cumm_start_dt date,
    language_codes character(20),
    birth_date date,
    anniversary_date date,
    file_expry_date date NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    email_address character varying(150),
    password_hash character varying(45) DEFAULT ''::character varying NOT NULL,
    alt_client_prfl_no character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_profile OWNER TO postgres;

--
-- Name: client_remarks; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_remarks (
    client_prfl_no character(15) NOT NULL,
    remark_sequence_no smallint NOT NULL,
    remark_type character(1) NOT NULL,
    remark_text character varying(240),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_remarks OWNER TO postgres;

--
-- Name: client_request; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_request (
    client_prfl_no character varying(15) NOT NULL,
    pax_code character varying(5) NOT NULL,
    rqst_code character varying(4) NOT NULL,
    request_text character varying(255),
    request_type_indicator character(1),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_request OWNER TO postgres;

--
-- Name: client_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_requests (
    client_prfl_no character(15) NOT NULL,
    rqst_sequence_no smallint NOT NULL,
    rqst_indicator character(1),
    rqst_code character(4),
    carrier_code character(3),
    action_code character(2),
    actn_number character(3),
    request_text character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_requests OWNER TO postgres;

--
-- Name: client_security; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_security (
    dest_id character(8) NOT NULL,
    user_code character(5) NOT NULL,
    phy_branch_code character(12) NOT NULL,
    log_branch_code character(12) NOT NULL,
    company_code character(3) NOT NULL,
    city_code character(5) NOT NULL,
    state_code character(2) NOT NULL,
    nation_code character(2) NOT NULL,
    process_code character(15),
    client_no integer NOT NULL,
    status character(1) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_security OWNER TO postgres;

--
-- Name: client_security_client_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE client_security_client_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_security_client_no_seq OWNER TO postgres;

--
-- Name: client_security_client_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE client_security_client_no_seq OWNED BY client_security.client_no;


--
-- Name: client_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_serial_nos (
    client_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.client_serial_nos OWNER TO postgres;

--
-- Name: client_serial_nos_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE client_serial_nos_client_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_serial_nos_client_id_seq OWNER TO postgres;

--
-- Name: client_serial_nos_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE client_serial_nos_client_id_seq OWNED BY client_serial_nos.client_id;


--
-- Name: client_travel; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE client_travel (
    client_prfl_no character(15) NOT NULL,
    travel_sequence_no smallint NOT NULL,
    locator character(6) DEFAULT ''::bpchar NOT NULL,
    book_no integer NOT NULL,
    flight_number character(7),
    board_date character(19),
    departure_airport character(5),
    arrival_airport character(5),
    departure_time character(19),
    arrival_time character(19),
    flight_path_code character(1),
    selling_class character(2),
    fare_basis_code character(15),
    fare_amount numeric(15,5),
    travel_credits numeric(15,5),
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.client_travel OWNER TO postgres;

--
-- Name: cls_exclusion_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE cls_exclusion_rule (
    rule_number integer NOT NULL,
    flight_number character(7) NOT NULL,
    departure_airport character(5),
    arrival_airport character(5),
    start_date date,
    end_date date,
    frequency_code character(7),
    config_table character(5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.cls_exclusion_rule OWNER TO postgres;

--
-- Name: comm_exception; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE comm_exception (
    agency_code character(8) NOT NULL,
    flight_path_code character(1) NOT NULL,
    company_code character(3) NOT NULL,
    valid_from_date date NOT NULL,
    commission_seq smallint NOT NULL,
    fare_basis_code character(15),
    departure_airport character(5),
    arrival_airport character(5),
    flight_number character(7),
    valid_to_date date NOT NULL,
    commission_meth character(1) NOT NULL,
    commission_amount numeric(15,5) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.comm_exception OWNER TO postgres;

--
-- Name: command_text; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE command_text (
    command_text_code character varying(5) NOT NULL,
    description character varying(250) NOT NULL,
    command_regexp character varying(250) NOT NULL,
    response_text character varying(250) NOT NULL,
    param_a_seqno integer NOT NULL,
    param_b_seqno integer NOT NULL,
    param_c_seqno integer NOT NULL,
    param_d_seqno integer NOT NULL,
    param_e_seqno integer NOT NULL,
    param_f_seqno integer NOT NULL,
    param_g_seqno integer NOT NULL,
    param_h_seqno integer NOT NULL
);


ALTER TABLE public.command_text OWNER TO postgres;

--
-- Name: commission_basic; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE commission_basic (
    comm_basic_code character(16) NOT NULL,
    flight_path_code character(1) NOT NULL,
    company_code character(3) NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    commission_meth character(1) NOT NULL,
    commission_amount numeric(15,5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone,
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone
);


ALTER TABLE public.commission_basic OWNER TO postgres;

--
-- Name: commission_volum; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE commission_volum (
    comm_volum_code character(16) NOT NULL,
    valid_from_date date NOT NULL,
    comm_range_from numeric(15,5) NOT NULL,
    valid_to_date date NOT NULL,
    comm_range_to numeric(15,5) NOT NULL,
    commission_meth character(1) NOT NULL,
    commission_amount numeric(15,5) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.commission_volum OWNER TO postgres;

--
-- Name: comp_ticket_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE comp_ticket_nos (
    ticket_type character(1) NOT NULL,
    ticket_no_from character(10) NOT NULL,
    ticket_no_to character(10) NOT NULL,
    next_ticket_no character(10) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.comp_ticket_nos OWNER TO postgres;

--
-- Name: company; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE company (
    company_code character(3) NOT NULL,
    company_name character varying(80),
    address character varying(200),
    addr_city character(25),
    addr_state character(25),
    addr_zip character(15),
    addr_nation character(25),
    phone_no character varying(30),
    city_code character(5) NOT NULL,
    numeric_code integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.company OWNER TO postgres;

--
-- Name: compartment_position_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE compartment_position_mapping (
    compartment_position integer NOT NULL,
    selling_class_code character(3) NOT NULL
);


ALTER TABLE public.compartment_position_mapping OWNER TO postgres;

--
-- Name: config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE config (
    item character(10),
    stringdata text,
    intdata integer,
    blobdata bytea,
    update_user character(5),
    update_group character(8),
    update_time character(9)
);


ALTER TABLE public.config OWNER TO postgres;

--
-- Name: connect_city; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE connect_city (
    city_pair integer NOT NULL,
    priority_number smallint NOT NULL,
    connect_cities character(17) NOT NULL,
    connect_status character(1) NOT NULL,
    min_connect_time character varying(255) DEFAULT ''::character varying NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.connect_city OWNER TO postgres;

--
-- Name: corporate_fare_basis_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE corporate_fare_basis_codes (
    corporate_type character(20) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.corporate_fare_basis_codes OWNER TO postgres;

--
-- Name: counter_sales_in_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE counter_sales_in_mesgs (
    serial_no integer NOT NULL,
    message_id integer DEFAULT 0,
    message_type smallint DEFAULT 0,
    failure_flag character(1) DEFAULT 'N'::bpchar,
    failure_reason character varying(100),
    message_body text,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.counter_sales_in_mesgs OWNER TO postgres;

--
-- Name: counter_sales_in_mesgs_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE counter_sales_in_mesgs_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.counter_sales_in_mesgs_serial_no_seq OWNER TO postgres;

--
-- Name: counter_sales_in_mesgs_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE counter_sales_in_mesgs_serial_no_seq OWNED BY counter_sales_in_mesgs.serial_no;


--
-- Name: counter_sales_mesg_types; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE counter_sales_mesg_types (
    message_type_id smallint NOT NULL,
    message_description character varying(50)
);


ALTER TABLE public.counter_sales_mesg_types OWNER TO postgres;

--
-- Name: counter_sales_out_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE counter_sales_out_mesgs (
    serial_no integer NOT NULL,
    message_id integer DEFAULT 0,
    message_type smallint DEFAULT 0,
    sent_flag character(1) DEFAULT 'Y'::bpchar,
    message_body text,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.counter_sales_out_mesgs OWNER TO postgres;

--
-- Name: counter_sales_out_mesgs_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE counter_sales_out_mesgs_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.counter_sales_out_mesgs_serial_no_seq OWNER TO postgres;

--
-- Name: counter_sales_out_mesgs_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE counter_sales_out_mesgs_serial_no_seq OWNED BY counter_sales_out_mesgs.serial_no;


--
-- Name: credit_card_fraud; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_card_fraud (
    credit_card_fraud_id bigint NOT NULL,
    old_credit_card_fraud_id bigint,
    last_name character(30),
    first_name character(30),
    origin_airport character(5),
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    destination_airport character(5),
    create_user character(5) NOT NULL,
    number_field character(50) NOT NULL,
    credit_card_fraud_level integer,
    credit_card_fraud_number_rcd character(5) NOT NULL,
    inactivated_user_code character(5),
    inactivated_date_time timestamp WITH time zone
);


ALTER TABLE public.credit_card_fraud OWNER TO postgres;

--
-- Name: credit_card_fraud_number_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_card_fraud_number_ref (
    credit_card_fraud_number_rcd character(5) NOT NULL,
    number_name character(18),
    active_flag integer,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    create_user character(5) NOT NULL
);


ALTER TABLE public.credit_card_fraud_number_ref OWNER TO postgres;

--
-- Name: credit_card_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_card_message (
    message_code character varying(20) NOT NULL,
    payment_form character varying(5) NOT NULL,
    message character varying(250),
    accept_approval character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.credit_card_message OWNER TO postgres;

--
-- Name: credit_card_tran_serial; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_card_tran_serial (
    cc_tran_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.credit_card_tran_serial OWNER TO postgres;

--
-- Name: credit_card_tran_serial_cc_tran_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE credit_card_tran_serial_cc_tran_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_card_tran_serial_cc_tran_no_seq OWNER TO postgres;

--
-- Name: credit_card_tran_serial_cc_tran_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE credit_card_tran_serial_cc_tran_no_seq OWNED BY credit_card_tran_serial.cc_tran_no;


--
-- Name: credit_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_requests (
    id integer NOT NULL,
    first_name character varying(53),
    last_name character varying(53),
    transaction_id character varying(10),
    ccnumber character varying(4),
    expiration_date character varying(4),
    amount integer,
    sale_type character varying(1),
    card_type character varying(1),
    transaction_type character varying(1),
    zipcode character varying(9),
    street_address character varying(20),
    ticket_count integer,
    request character varying(1024) NOT NULL,
    create_stamp timestamp WITH time zone DEFAULT now() NOT NULL,
    cvv2 character varying(5),
    currency_code character varying(3),
    ecommerce_indicator character varying(2)
);


ALTER TABLE public.credit_requests OWNER TO postgres;

--
-- Name: credit_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE credit_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_requests_id_seq OWNER TO postgres;

--
-- Name: credit_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE credit_requests_id_seq OWNED BY credit_requests.id;


--
-- Name: credit_settlement; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credit_settlement (
    id integer NOT NULL,
    record_type character(1) NOT NULL,
    batch_number character(8) NOT NULL,
    avs_code character(1),
    approval_code character(6),
    transaction_id character varying(10),
    updated_date timestamp WITH time zone NOT NULL,
    message character varying(255),
    answer character varying(255),
    cvvcode character varying(4)
);


ALTER TABLE public.credit_settlement OWNER TO postgres;

--
-- Name: credit_settlement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE credit_settlement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.credit_settlement_id_seq OWNER TO postgres;

--
-- Name: credit_settlement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE credit_settlement_id_seq OWNED BY credit_settlement.id;


--
-- Name: credt_card_branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credt_card_branch (
    branch_code character(12) NOT NULL,
    credt_card_id character(2) NOT NULL,
    auth_phone_no character varying(30) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.credt_card_branch OWNER TO postgres;

--
-- Name: credt_card_nation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE credt_card_nation (
    nation_code character(2) NOT NULL,
    credt_card_id character(2) NOT NULL,
    cc_type character(2) NOT NULL,
    auth_limit numeric(15,5),
    auto_address character(8),
    card_number_mask character(25),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.credt_card_nation OWNER TO postgres;

--
-- Name: crystal_reports_hierarchy; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE crystal_reports_hierarchy (
    report_code character varying(30) NOT NULL,
    report_menu_name character varying(30) NOT NULL,
    report_menu_type integer NOT NULL,
    report_hierarchy character varying(135) NOT NULL,
    report_description character varying(50),
    security_hook_name character varying(30),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.crystal_reports_hierarchy OWNER TO postgres;

--
-- Name: curr_convert; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE curr_convert (
    from_curr_code character(3) NOT NULL,
    to_curr_code character(3) NOT NULL,
    in_house_qual character(1) NOT NULL,
    qual_value numeric(9,5) NOT NULL,
    bank_rate numeric(9,5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.curr_convert OWNER TO postgres;

--
-- Name: currency_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE currency_codes (
    currency_code character(3) NOT NULL,
    description character varying(30),
    "precision" smallint NOT NULL,
    round_units smallint NOT NULL,
    nuc_rate numeric(9,5) NOT NULL,
    numeric_code integer,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.currency_codes OWNER TO postgres;

--
-- Name: db_purge_control; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE db_purge_control (
    tabid integer NOT NULL,
    tabname character varying(128) NOT NULL,
    category character varying(128) NOT NULL,
    priority integer NOT NULL,
    control_columns character varying(128) NOT NULL,
    active_flag character(1) NOT NULL,
    last_purged_date date NOT NULL,
    rows_deleted integer,
    start_date_time timestamp WITH time zone,
    end_date_time timestamp WITH time zone,
    create_date date NOT NULL,
    level integer,
    sub_column character varying(128),
    parent_id integer,
    t_rows_del integer
);


ALTER TABLE public.db_purge_control OWNER TO postgres;

--
-- Name: db_purge_temp; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE db_purge_temp (
    book_no integer NOT NULL,
    processed_flag character(1)
);


ALTER TABLE public.db_purge_temp OWNER TO postgres;

--
-- Name: db_purge_track; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE db_purge_track (
    book_no integer NOT NULL,
    create_date date NOT NULL,
    date_purged date,
    processed_flag character(1)
);


ALTER TABLE public.db_purge_track OWNER TO postgres;


--
-- Name: denied_cc_adjustments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE denied_cc_adjustments (
    ka_number integer NOT NULL,
    payment_no integer NOT NULL,
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
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.denied_cc_adjustments OWNER TO postgres;

--
-- Name: denied_cc_adjustments_ka_number_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE denied_cc_adjustments_ka_number_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.denied_cc_adjustments_ka_number_seq OWNER TO postgres;

--
-- Name: denied_cc_adjustments_ka_number_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE denied_cc_adjustments_ka_number_seq OWNED BY denied_cc_adjustments.ka_number;


--
-- Name: department; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE department (
    department_id integer NOT NULL,
    description character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.department OWNER TO postgres;

--
-- Name: dest; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE dest (
    dest_id character(8) NOT NULL,
    network_id character(15) NOT NULL,
    branch_code character(12) NOT NULL,
    dev_code character(3) NOT NULL,
    peripherls_dest_id character varying(45),
    status character(1) NOT NULL,
    cc_status character(1),
    resp_status character(1),
    receipt_status character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.dest OWNER TO postgres;

--
-- Name: dest_process; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE dest_process (
    dest_id character(8) NOT NULL,
    login_date_time character(19) NOT NULL,
    process_id character(15) NOT NULL
);


ALTER TABLE public.dest_process OWNER TO postgres;

--
-- Name: device; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE device (
    dev_code character(3) NOT NULL,
    description character varying(160),
    dev_type character(3) NOT NULL,
    device_time_out smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.device OWNER TO postgres;

--
-- Name: device_status_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE device_status_ref (
    device_status_rcd character varying(5) NOT NULL,
    description character varying(255),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.device_status_ref OWNER TO postgres;

--
-- Name: diners_club_tx; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE diners_club_tx (
    user_login character(100) NOT NULL,
    member_id integer,
    action_code integer NOT NULL,
    member_status integer,
    first_name character(100),
    surname character(100),
    mobile_number character(15),
    dob character(10),
    can_spend integer,
    can_earn integer,
    transaction_id integer,
    lifetime_points integer,
    points_balance integer,
    points_spent integer,
    points_refund integer,
    book_no integer,
    info_sent character(1),
    exchange_rate double precision,
    create_time timestamp WITH time zone,
    update_time timestamp WITH time zone
);


ALTER TABLE public.diners_club_tx OWNER TO postgres;

--
-- Name: document_category; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE document_category (
    document_type character(2) NOT NULL,
    document_catg character(3) NOT NULL,
    document_grp character(2) NOT NULL,
    payment_key character(1) NOT NULL,
    doc_strt_auth_level smallint NOT NULL,
    doc_end_auth_level smallint NOT NULL,
    type_description character varying(160),
    description character varying(160),
    crdt_expry_intvl smallint,
    fop_format character(1) NOT NULL,
    default_paid_flag character(1) DEFAULT 'N'::bpchar,
    single_payment_flag character(1) DEFAULT 'N'::bpchar,
    installments_enabled character(1) DEFAULT 'N'::bpchar,
    initial_deposit_type character(1),
    initial_deposit_amount numeric(15,5),
    number_of_installments integer,
    installment_period integer,
    installment_period_type character(1),
    reference_constant smallint,
    reference_id_type character(5) DEFAULT 'NONE'::bpchar,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.document_category OWNER TO postgres;

--
-- Name: document_category_save; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE document_category_save (
    document_type character(2) NOT NULL,
    document_catg character(3) NOT NULL,
    document_grp character(2) NOT NULL,
    payment_key character(1) NOT NULL,
    doc_strt_auth_level smallint NOT NULL,
    doc_end_auth_level smallint NOT NULL,
    type_description character varying(160),
    description character varying(160),
    crdt_expry_intvl smallint,
    fop_format character(1) NOT NULL,
    default_paid_flag character(1) DEFAULT 'N'::bpchar,
    single_payment_flag character(1) DEFAULT 'N'::bpchar,
    installments_enabled character(1) DEFAULT 'N'::bpchar,
    initial_deposit_type character(1),
    initial_deposit_amount numeric(15,5),
    number_of_installments integer,
    installment_period integer,
    installment_period_type character(1),
    reference_id_type character(5) DEFAULT 'NONE'::bpchar,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.document_category_save OWNER TO postgres;

--
-- Name: dup_maint_names; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE dup_maint_names (
    dupe_name character(53),
    dupe_book_no integer NOT NULL,
    dupe_origin character(5) NOT NULL,
    dupe_destination character(5) NOT NULL,
    dupe_int_cty1 character(5) NOT NULL,
    dupe_int_cty2 character(5) NOT NULL,
    dupe_int_cty3 character(5) NOT NULL,
    dupe_int_cty4 character(5) NOT NULL,
    dupe_int_cty5 character(5) NOT NULL,
    dupe_flt_nbr character(7) NOT NULL,
    dupe_flt_date date NOT NULL,
    dupe_pnr_no character(6) NOT NULL,
    dupe_branch character(12) NOT NULL,
    dupe_book_type character(1) NOT NULL,
    dupe_path_code character(1) NOT NULL
);


ALTER TABLE public.dup_maint_names OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE employee (
    employee_id bigint NOT NULL,
    employee_no character varying(10) NOT NULL,
    client_prfl_no character varying(15) NOT NULL,
    department_id integer,
    hire_date date,
    termination_date date,
    employment_status character(1),
    fulltime_flag character(1),
    return_to_work_date date,
    national_identity_no character varying(15),
    job_title character varying(255),
    remarks character varying(250),
    jump_seat_code character varying(20),
    suspension_date date,
    travel_start_date date,
    travel_end_date date,
    department_name character varying(100),
    buddy_pax_code character varying(5),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_buddy_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE employee_buddy_pass (
    employee_id bigint NOT NULL,
    buddy_pass_no character varying(30) NOT NULL,
    active_flag character(1),
    book_no integer,
    valid_from_date date NOT NULL,
    valid_until_date date NOT NULL,
    remarks character varying(255),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.employee_buddy_pass OWNER TO postgres;

--
-- Name: employee_family; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE employee_family (
    employee_id bigint NOT NULL,
    relative_client_prfl_no character varying(15) NOT NULL,
    relationship_type_id integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.employee_family OWNER TO postgres;

--
-- Name: employee_travel_benefit; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE employee_travel_benefit (
    employee_id bigint NOT NULL,
    dependant_travel_date date,
    buddy_pass_prefix character varying(5),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.employee_travel_benefit OWNER TO postgres;

--
-- Name: end_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE end_transaction (
    et_serial_no integer NOT NULL,
    et_sequence_no smallint NOT NULL,
    key_code character(5) NOT NULL,
    book_no integer NOT NULL,
    company_code character(3) NOT NULL,
    process_type character(5) NOT NULL,
    tran_type character(1) NOT NULL,
    control_param character(25),
    validate_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    proc_date_time character(19),
    et_info_1 character varying(250),
    et_info_2 character varying(250),
    et_info_3 character varying(250),
    et_info_4 character varying(250),
    et_info_5 character varying(250),
    et_info_6 character varying(250),
    et_info_7 character varying(250),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.end_transaction OWNER TO postgres;

--
-- Name: end_transaction_book; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE end_transaction_book (
    book_serial_no integer NOT NULL,
    book_no integer,
    processing_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    payment_no integer,
    et_serial_no integer DEFAULT 0 NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.end_transaction_book OWNER TO postgres;

--
-- Name: end_transaction_book_book_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE end_transaction_book_book_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.end_transaction_book_book_serial_no_seq OWNER TO postgres;

--
-- Name: end_transaction_book_book_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE end_transaction_book_book_serial_no_seq OWNED BY end_transaction_book.book_serial_no;


--
-- Name: equipment_change_processing_serial; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE equipment_change_processing_serial (
    equipment_change_processing_id integer NOT NULL
);


ALTER TABLE public.equipment_change_processing_serial OWNER TO postgres;

--
-- Name: equipment_change_processing_s_equipment_change_processing_i_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE equipment_change_processing_s_equipment_change_processing_i_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_change_processing_s_equipment_change_processing_i_seq OWNER TO postgres;

--
-- Name: equipment_change_processing_s_equipment_change_processing_i_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE equipment_change_processing_s_equipment_change_processing_i_seq OWNED BY equipment_change_processing_serial.equipment_change_processing_id;


--
-- Name: equipment_change_seat_reallocation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE equipment_change_seat_reallocation (
    equipment_change_seat_reallocation_id integer NOT NULL,
    old_seat_definition_id integer NOT NULL,
    new_seat_definition_id integer NOT NULL,
    active_flag character(1) NOT NULL,
    from_seat_map_id integer NOT NULL,
    to_seat_map_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT equipment_change_seat_reallocation_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.equipment_change_seat_reallocation OWNER TO postgres;

--
-- Name: equipment_change_seat_realloc_equipment_change_seat_realloc_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE equipment_change_seat_realloc_equipment_change_seat_realloc_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.equipment_change_seat_realloc_equipment_change_seat_realloc_seq OWNER TO postgres;

--
-- Name: equipment_change_seat_realloc_equipment_change_seat_realloc_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE equipment_change_seat_realloc_equipment_change_seat_realloc_seq OWNED BY equipment_change_seat_reallocation.equipment_change_seat_reallocation_id;


--
-- Name: error_code; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE error_code (
    src_code character(20) NOT NULL,
    src_err_code character(10) NOT NULL,
    src_err_msg character(300),
    mango_err_code character(10),
    mango_err_msg character(300),
    severity integer,
    language character(20) NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.error_code OWNER TO postgres;

--
-- Name: et_payments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE et_payments (
    payment_no integer NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.et_payments OWNER TO postgres;

--
-- Name: et_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE et_serial_nos (
    et_serial_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.et_serial_nos OWNER TO postgres;

--
-- Name: et_serial_nos_et_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE et_serial_nos_et_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.et_serial_nos_et_serial_no_seq OWNER TO postgres;

--
-- Name: et_serial_nos_et_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE et_serial_nos_et_serial_no_seq OWNED BY et_serial_nos.et_serial_no;


--
-- Name: et_valid_check; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE et_valid_check (
    company_code character(3) NOT NULL,
    process_type character(5) NOT NULL,
    book_type character(1) NOT NULL,
    book_category character(1) NOT NULL,
    field_name character(18) NOT NULL,
    edit_mask character varying(80),
    def_value character varying(80),
    validity_chk character(1) NOT NULL,
    iteration_chk smallint NOT NULL,
    dependencies smallint NOT NULL,
    process_codes smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.et_valid_check OWNER TO postgres;

--
-- Name: et_valid_usr_exit; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE et_valid_usr_exit (
    company_code character(3) NOT NULL,
    process_type character(5) NOT NULL,
    book_type character(1) NOT NULL,
    book_category character(1) NOT NULL,
    field_name character(18) NOT NULL,
    usr_exit_type character(1) NOT NULL,
    exit_sequence_no smallint NOT NULL,
    usr_exit_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.et_valid_usr_exit OWNER TO postgres;

--
-- Name: eticket_action; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_action (
    eticket_action_id integer NOT NULL,
    book_no integer,
    reserve_status character(5),
    flight_number character(7),
    flight_date date,
    depr_arport character(5),
    arrv_arport character(5),
    departure_time smallint,
    arrival_time smallint,
    tkt_action character(1),
    prcsd_flag character(1),
    physical_class character(2),
    selling_class character(2),
    status_flag character(1),
    coupon_count smallint,
    update_user character(5),
    update_time character(19)
);


ALTER TABLE public.eticket_action OWNER TO postgres;

--
-- Name: eticket_action_eticket_action_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_action_eticket_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_action_eticket_action_id_seq OWNER TO postgres;

--
-- Name: eticket_action_eticket_action_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_action_eticket_action_id_seq OWNED BY eticket_action.eticket_action_id;


--
-- Name: eticket_in_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_in_mesgs (
    serial_no integer NOT NULL,
    message_id bigint DEFAULT 0,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    book_no integer NOT NULL,
    failure_flag character(1) DEFAULT 'N'::bpchar,
    failure_reason character varying(50),
    message_body character varying(1024),
    xml character varying(4096) DEFAULT ''::character varying,
    edifact character varying(4096) DEFAULT ''::character varying,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.eticket_in_mesgs OWNER TO postgres;

--
-- Name: eticket_in_mesgs_old; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_in_mesgs_old (
    serial_no integer NOT NULL,
    message_id integer DEFAULT 0,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    book_no integer,
    failure_flag character(1) DEFAULT 'N'::bpchar,
    failure_reason character varying(50),
    message_body character varying(1024),
    xml character varying(4096) DEFAULT ''::character varying,
    edifact character varying(4096) DEFAULT ''::character varying,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.eticket_in_mesgs_old OWNER TO postgres;

--
-- Name: eticket_in_mesgs_old_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_in_mesgs_old_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_in_mesgs_old_serial_no_seq OWNER TO postgres;

--
-- Name: eticket_in_mesgs_old_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_in_mesgs_old_serial_no_seq OWNED BY eticket_in_mesgs_old.serial_no;


--
-- Name: eticket_in_mesgs_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_in_mesgs_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_in_mesgs_serial_no_seq OWNER TO postgres;

--
-- Name: eticket_in_mesgs_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_in_mesgs_serial_no_seq OWNED BY eticket_in_mesgs.serial_no;


--
-- Name: eticket_out_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_out_mesgs (
    serial_no integer NOT NULL,
    message_id bigint DEFAULT 0,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    book_no integer NOT NULL,
    status character varying(5),
    description character varying(50),
    message_body character varying(1024),
    create_time timestamp WITH time zone NOT NULL,
    edifact character varying(4096) DEFAULT ''::character varying,
    xml character varying(4096) DEFAULT ''::character varying
);


ALTER TABLE public.eticket_out_mesgs OWNER TO postgres;

--
-- Name: eticket_out_mesgs_old; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_out_mesgs_old (
    serial_no integer NOT NULL,
    message_id integer DEFAULT 0,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    book_no integer,
    status character varying(5),
    description character varying(50),
    message_body character varying(1024),
    create_time timestamp WITH time zone NOT NULL,
    edifact character varying(4096) DEFAULT ''::character varying,
    xml character varying(4096) DEFAULT ''::character varying
);


ALTER TABLE public.eticket_out_mesgs_old OWNER TO postgres;

--
-- Name: eticket_out_mesgs_old_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_out_mesgs_old_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_out_mesgs_old_serial_no_seq OWNER TO postgres;

--
-- Name: eticket_out_mesgs_old_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_out_mesgs_old_serial_no_seq OWNED BY eticket_out_mesgs_old.serial_no;


--
-- Name: eticket_out_mesgs_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_out_mesgs_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_out_mesgs_serial_no_seq OWNER TO postgres;

--
-- Name: eticket_out_mesgs_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_out_mesgs_serial_no_seq OWNED BY eticket_out_mesgs.serial_no;


--
-- Name: eticket_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE eticket_transaction (
    transaction_id integer NOT NULL,
    et_serial_no integer NOT NULL,
    book_no integer NOT NULL,
    tran_type character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    message_xml_req character varying(8192),
    message_edi_req character varying(8192),
    message_xml_res character varying(8192),
    message_edi_res character varying(4096),
    error_description character varying(1024),
    status character(1) DEFAULT 'N'::bpchar NOT NULL,
    upd_date_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.eticket_transaction OWNER TO postgres;

--
-- Name: eticket_transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE eticket_transaction_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.eticket_transaction_transaction_id_seq OWNER TO postgres;

--
-- Name: eticket_transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE eticket_transaction_transaction_id_seq OWNED BY eticket_transaction.transaction_id;


--
-- Name: euroline_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE euroline_transaction (
    transaction_id integer NOT NULL,
    locator character varying(10),
    approved character(1) DEFAULT 'N'::bpchar NOT NULL,
    request text,
    request_data text,
    reply text,
    rqst_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    rply_date_time timestamp WITH time zone,
    settled character(1) DEFAULT 'N'::bpchar NOT NULL,
    sett_request text,
    sett_request_data text,
    sett_reply text,
    sett_request_date_time timestamp WITH time zone,
    sett_reply_date_time timestamp WITH time zone,
    external_tran_id character varying(30),
    cc_approval_code character(6)
);


ALTER TABLE public.euroline_transaction OWNER TO postgres;

--
-- Name: euroline_transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE euroline_transaction_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.euroline_transaction_transaction_id_seq OWNER TO postgres;

--
-- Name: euroline_transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE euroline_transaction_transaction_id_seq OWNED BY euroline_transaction.transaction_id;


--
-- Name: fact_note; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fact_note (
    note_number smallint NOT NULL,
    authority_level smallint NOT NULL,
    fact_text character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.fact_note OWNER TO postgres;

--
-- Name: fare; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare (
    fare_id bigint NOT NULL,
    reference_flag character(1) NOT NULL,
    reference_fare_id bigint,
    original_fare_id bigint,
    fare_basis_code character(15) NOT NULL,
    fare_basis_code_desc character varying(255),
    value_can_split character(1),
    selling_class character(2) NOT NULL,
    booking_category character(1) NOT NULL,
    advance_purchase smallint,
    weekday_stay smallint,
    minimum_stay smallint,
    maximum_stay smallint,
    monday character(1),
    tuesday character(1),
    wednesday character(1),
    thursday character(1),
    friday character(1),
    saturday character(1),
    sunday character(1),
    refundable_flag character(1),
    oneway_return_flag character(1),
    combine_with_direction character(1),
    net_fare_flag character(1),
    atpco_export_flag character(1),
    activate_batch_id character(5),
    access_auth_level_low smallint,
    access_auth_level_high smallint,
    bypass_auth_level_low smallint,
    bypass_auth_level_high smallint,
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    footnote character(2),
    companion_fare character varying(15),
    companion_count integer,
    private_fare_flag character(1),
    tariff_code character varying(20),
    timelimit_days smallint,
    timelimit_time time WITH time zone,
    all_agency_flag character(1) DEFAULT 'Y'::bpchar NOT NULL,
    all_branch_flag character(1) DEFAULT 'Y'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare OWNER TO postgres;

--
-- Name: fare_agency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_agency (
    fare_id bigint NOT NULL,
    agency_code character varying(20) NOT NULL,
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_agency OWNER TO postgres;

--
-- Name: fare_batch_operation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_batch_operation (
    fare_batch_operation_id integer NOT NULL,
    batch_id character varying(5),
    operation_description character varying(255),
    user_code character varying(5) NOT NULL,
    user_comment character varying(255),
    system_name character varying(100),
    process_id integer,
    started_date_time timestamp WITH time zone,
    last_seen_date_time timestamp WITH time zone,
    last_operation_status_rcd character varying(5) NOT NULL,
    completed_date_time timestamp WITH time zone,
    can_be_cancelled_flag character(1) NOT NULL,
    cancel_flag character(1) NOT NULL,
    cancelled_by_user_code character varying(5),
    update_user character varying(5),
    update_group character varying(5),
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_batch_operation OWNER TO postgres;

--
-- Name: fare_batch_operation_fare_batch_operation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fare_batch_operation_fare_batch_operation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fare_batch_operation_fare_batch_operation_id_seq OWNER TO postgres;

--
-- Name: fare_batch_operation_fare_batch_operation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fare_batch_operation_fare_batch_operation_id_seq OWNED BY fare_batch_operation.fare_batch_operation_id;


--
-- Name: fare_batch_operation_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_batch_operation_history (
    fare_batch_operation_history_id integer NOT NULL,
    fare_batch_operation_id integer NOT NULL,
    event_date_time timestamp WITH time zone,
    op_status_rcd character varying(5) NOT NULL,
    can_be_cancelled_flag character(1) NOT NULL,
    cancel_flag character(1) NOT NULL,
    update_user character varying(5),
    update_group character varying(5),
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_batch_operation_history OWNER TO postgres;

--
-- Name: fare_batch_operation_history_fare_batch_operation_history_i_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fare_batch_operation_history_fare_batch_operation_history_i_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fare_batch_operation_history_fare_batch_operation_history_i_seq OWNER TO postgres;

--
-- Name: fare_batch_operation_history_fare_batch_operation_history_i_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fare_batch_operation_history_fare_batch_operation_history_i_seq OWNED BY fare_batch_operation_history.fare_batch_operation_history_id;


--
-- Name: fare_blackout; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_blackout (
    fare_id bigint NOT NULL,
    blackout_date date NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_blackout OWNER TO postgres;

--
-- Name: fare_branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_branch (
    fare_id bigint NOT NULL,
    branch_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_branch OWNER TO postgres;

--
-- Name: fare_basis_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_basis_codes (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_basis_codes OWNER TO postgres;

--
-- Name: fare_comb_route; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_comb_route (
    fare_combine_id bigint NOT NULL,
    route_id bigint NOT NULL,
    active_flag character(1) NOT NULL,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_comb_route OWNER TO postgres;

--
-- Name: fare_combinability; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_combinability (
    fare_combine_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    fare_pattern_1 character varying(15) NOT NULL,
    fare_pattern_2 character varying(15) NOT NULL,
    allow_comb_flag character(1) NOT NULL,
    description character varying(200),
    active_flag character(1) NOT NULL,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_combinability OWNER TO postgres;

--
-- Name: fare_combinations; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_combinations (
    fare_id bigint NOT NULL,
    fare_basis_code character(15),
    origin_airport character(5),
    dest_airport character(5),
    refundable_flag character(1),
    oneway_return_flag character(1),
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_combinations OWNER TO postgres;

--
-- Name: fare_companion; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_companion (
    fare_id bigint NOT NULL,
    pax_desc character(5) NOT NULL,
    pax_count smallint NOT NULL,
    companion_count smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_companion OWNER TO postgres;

--
-- Name: fare_date_period; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_date_period (
    fare_date_period_id bigint NOT NULL,
    fare_date_period_code character varying(2),
    description character varying(255),
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT fare_date_period_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.fare_date_period OWNER TO postgres;

--
-- Name: fare_date_period_dates; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_date_period_dates (
    fare_date_period_id bigint NOT NULL,
    seq_no integer NOT NULL,
    effective_from_date timestamp WITH time zone NOT NULL,
    effective_to_date timestamp WITH time zone NOT NULL,
    valid_from_date timestamp WITH time zone NOT NULL,
    valid_to_date timestamp WITH time zone NOT NULL,
    active_flag character(1) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT fare_date_period_dates_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.fare_date_period_dates OWNER TO postgres;

--
-- Name: fare_date_period_fare_date_period_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fare_date_period_fare_date_period_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fare_date_period_fare_date_period_id_seq OWNER TO postgres;

--
-- Name: fare_date_period_fare_date_period_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE fare_date_period_fare_date_period_id_seq OWNED BY fare_date_period.fare_date_period_id;


--
-- Name: fare_day_time; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_day_time (
    fare_id bigint NOT NULL,
    tod_sequence smallint NOT NULL,
    weekday smallint,
    start_time time WITH time zone,
    end_time time WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_day_time OWNER TO postgres;

--
-- Name: fare_designator; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_designator (
    fare_id bigint NOT NULL,
    designator_code character varying(255) NOT NULL,
    change_type character(1) NOT NULL,
    change_amount numeric(15,5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_designator OWNER TO postgres;

--
-- Name: fare_endorsements; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_endorsements (
    fare_id bigint NOT NULL,
    fare_text_type character(1) NOT NULL,
    endorsement_no integer DEFAULT 1 NOT NULL,
    fare_ticket_desc character varying(90),
    fare_description character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_endorsements OWNER TO postgres;

--
-- Name: fare_export; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_export (
    exp_date_time timestamp WITH time zone NOT NULL,
    exp_destination character(10) NOT NULL,
    exp_user_id character(5),
    exp_dest_id character(8)
);


ALTER TABLE public.fare_export OWNER TO postgres;

--
-- Name: fare_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_pass (
    fare_id bigint NOT NULL,
    pax_desc character(5) NOT NULL,
    change_type character(1),
    change_amount numeric(15,5),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_pass OWNER TO postgres;

--
-- Name: fare_route; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route (
    fare_route_id bigint NOT NULL,
    fare_id bigint NOT NULL,
    route_id integer NOT NULL,
    fare_amount numeric(15,5),
    currency_code character(3),
    valid_from_date date,
    valid_to_date date,
    effective_from_date timestamp WITH time zone,
    effective_to_date timestamp WITH time zone,
    active_flag character(1),
    inactive_date_time timestamp WITH time zone,
    original_fare_route_id bigint,
    activate_batch_id character(5),
    atpco_upload_date timestamp WITH time zone,
    atpco_custom_data character varying(255),
    fare_date_period_id bigint,
    seq_no integer,
    timelimit_days smallint,
    timelimit_time time WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route OWNER TO postgres;

--
-- Name: fare_route_agency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_agency (
    fare_route_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    agency_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_agency OWNER TO postgres;

--
-- Name: fare_route_branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_branch (
    fare_route_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    branch_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_branch OWNER TO postgres;

--
-- Name: fare_route_company; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_company (
    fare_route_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    all_agency_flag character(1),
    all_branch_flag character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_company OWNER TO postgres;

--
-- Name: fare_route_designator; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_designator (
    fare_route_id bigint NOT NULL,
    designator_code character varying(255) NOT NULL,
    change_type character(1) NOT NULL,
    change_amount numeric(15,5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_designator OWNER TO postgres;

--
-- Name: fare_route_flight; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_flight (
    fare_route_id bigint NOT NULL,
    flight_number character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_flight OWNER TO postgres;

--
-- Name: fare_route_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_route_pass (
    fare_route_id bigint NOT NULL,
    pax_desc character(5) NOT NULL,
    change_type character(1),
    change_amount numeric(15,5),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fare_route_pass OWNER TO postgres;

--
-- Name: fare_rule_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_rule_codes (
    company_code character(3) NOT NULL,
    fare_rule_no character(8) NOT NULL,
    rule_code_type character(4) NOT NULL,
    rule_code_value character(12) NOT NULL,
    description character varying(80),
    rule_type character(1) NOT NULL,
    rule_code_text character varying(255),
    tkt_description character varying(90),
    refund_flag character(1),
    flno_appl_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_rule_codes OWNER TO postgres;

--
-- Name: fare_segments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_segments (
    company_code character(3) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    city_pair integer NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    eff_from_date date,
    eff_to_date date,
    fare_amount numeric(15,5) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    export_timestamp timestamp WITH time zone,
    inactive_date timestamp WITH time zone,
    update_user character(8) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_segments OWNER TO postgres;

--
-- Name: fare_segm_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fare_segm_rule (
    company_code character(3) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    city_pair integer NOT NULL,
    valid_from_date date NOT NULL,
    fare_rule_no character(8) NOT NULL,
    valid_to_date date NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    export_timestamp timestamp WITH time zone,
    flight_number character(7),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.fare_segm_rule OWNER TO postgres;

--
-- Name: fee; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--


--
-- Name: book_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE fee_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE fees (
    fee_id integer DEFAULT nextval('fee_id_seq'::regclass) NOT NULL,
    company_code character(3),
    fee_type_rcd character(10) NOT NULL,
    fee_code character(5) NOT NULL,
    description character varying(250) NOT NULL,
    valid_from_date_time timestamp WITH time zone NOT NULL,
    valid_until_date_time timestamp WITH time zone NOT NULL,
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
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    inactivated_user_code character(5),
    inactivated_date_time timestamp WITH time zone,
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
-- Name: fee_branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fee_branches (
    fee_id bigint NOT NULL,
    branch_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fee_branches OWNER TO postgres;

--
-- Name: fee_class; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fee_classes (
    fee_id bigint NOT NULL,
    class_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fee_classes OWNER TO postgres;

--
-- Name: fee_fare; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fee_fares (
    fee_id bigint NOT NULL,
    fare_basis_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fee_fares OWNER TO postgres;

--
-- Name: fee_passenger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fee_passenger (
    fee_id bigint NOT NULL,
    pax_code character varying(20) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.fee_passenger OWNER TO postgres;

--
-- Name: fee_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE fee_type_ref (
    fee_type_rcd character(10) NOT NULL,
    description character varying(250) NOT NULL,
    active_flag integer NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    create_user character(5) NOT NULL
);


ALTER TABLE public.fee_type_ref OWNER TO postgres;

--
-- Name: field_control_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE field_control_type (
    field_control_type_rcd character varying(5) NOT NULL,
    field_control_type_name character varying(50) NOT NULL,
    data_type_code character varying(5) NOT NULL,
    source_table_name character varying(100),
    source_filter character varying(100),
    source_pk_field character varying(100),
    source_caption_field character varying(100),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.field_control_type OWNER TO postgres;

--
-- Name: financial_transaction_book; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE financial_transaction_book (
    serial_no integer NOT NULL,
    book_no integer NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    processing_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.financial_transaction_book OWNER TO postgres;

--
-- Name: financial_transaction_book_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE financial_transaction_book_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.financial_transaction_book_serial_no_seq OWNER TO postgres;

--
-- Name: financial_transaction_book_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE financial_transaction_book_serial_no_seq OWNED BY financial_transaction_book.serial_no;


--
-- Name: flgt_dt_availbty; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flgt_dt_availbty (
    live_test_availbty character(1) NOT NULL,
    flight_number character(7) NOT NULL,
    city_pair integer NOT NULL,
    schedule_period_no smallint NOT NULL,
    flight_date date NOT NULL,
    selling_class character(2) NOT NULL,
    dt_availb_seats smallint NOT NULL,
    prd_availb_seats smallint NOT NULL
);


ALTER TABLE public.flgt_dt_availbty OWNER TO postgres;

--
-- Name: flight_checkin; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_checkin (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    check_sequence_no smallint NOT NULL,
    pax_name character(53) NOT NULL,
    gender character(1),
    paddle_no smallint,
    check_code character(5),
    credit_amount numeric(15,5),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_checkin OWNER TO postgres;

--
-- Name: flight_date_leg; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_date_leg (
    flight_date_leg_id integer NOT NULL,
    flight_number character varying(7) NOT NULL,
    board_date date NOT NULL,
    flight_date date NOT NULL,
    departure_time time WITH time zone NOT NULL,
    departure_airport character varying(5) NOT NULL,
    arrival_airport character varying(5) NOT NULL,
    leg_number smallint NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_date_leg OWNER TO postgres;

--
-- Name: flight_date_leg_flight_date_leg_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE flight_date_leg_flight_date_leg_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flight_date_leg_flight_date_leg_id_seq OWNER TO postgres;

--
-- Name: flight_date_leg_flight_date_leg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE flight_date_leg_flight_date_leg_id_seq OWNED BY flight_date_leg.flight_date_leg_id;


--
-- Name: flight_event_ctrl; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_event_ctrl (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_intrvl_hrs smallint NOT NULL,
    adlr_intrvl_hrs smallint NOT NULL,
    adlf_intrvl_hrs smallint NOT NULL,
    fbi_intrvl_hrs smallint NOT NULL,
    fci_intrvl_hrs smallint NOT NULL,
    wii_intrvl_hrs smallint NOT NULL,
    wrp_intrvl_hrs smallint NOT NULL,
    wrp_value character(1) NOT NULL,
    pnl_incl_class character(1) NOT NULL,
    system_dests character varying(255),
    tty_priority character(2),
    tty_address1 character varying(144),
    tty_address2 character varying(144),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_event_ctrl OWNER TO postgres;

--
-- Name: flight_exceptions; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_exceptions (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    delay_code character(11),
    arrival_airport character(5) NOT NULL,
    std_gmt_time_str character(4) NOT NULL,
    etd_gmt_time_str character(4),
    atd_gmt_time_str character(4),
    sta_gmt_time_str character(4) NOT NULL,
    eta_gmt_time_str character(4),
    ata_gmt_time_str character(4),
    remarks_str character(80),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_exceptions OWNER TO postgres;

--
-- Name: flight_hierarchy; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_hierarchy (
    parent_flight_date_leg_id integer NOT NULL,
    child_flight_date_leg_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_hierarchy OWNER TO postgres;

--
-- Name: flight_information; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_information (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    seq_no integer NOT NULL,
    delay_code character(30),
    delay_description character varying(255),
    etd_time time WITH time zone,
    atd_time time WITH time zone,
    eta_time time WITH time zone,
    ata_time time WITH time zone,
    remarks text,
    supp_comment character varying(255),
    flight_landed_code character varying(20),
    off_ground_time smallint,
    on_ground_time smallint,
    arrival_fuel_on_board integer,
    departure_fuel_on_board integer,
    pilot_landed_flag integer DEFAULT 0,
    tail_number character varying(20),
    arrival_gate_number character varying(20),
    departure_gate_number character varying(20),
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_information OWNER TO postgres;

--
-- Name: flight_locked; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_locked (
    lock_id bigint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    description character varying(255) NOT NULL,
    invalidated_user character(5),
    invalidated_dest_id character(8),
    invalid_time timestamp WITH time zone,
    create_user character(5) NOT NULL,
    created_dest_id character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.flight_locked OWNER TO postgres;

--
-- Name: flight_perd_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_perd_cls (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    selling_class character(2) NOT NULL,
    parent_sell_cls character varying(240) NOT NULL,
    display_priority smallint NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_perd_cls OWNER TO postgres;

--
-- Name: flight_perd_dates; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_perd_dates (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    flight_date date NOT NULL
);


ALTER TABLE public.flight_perd_dates OWNER TO postgres;

--
-- Name: flight_perd_legs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_perd_legs (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time time WITH time zone,
    arrival_time time WITH time zone,
    date_change_ind smallint NOT NULL,
    config_table character(5) NOT NULL,
    flight_path_code character(1) NOT NULL,
    departure_terminal character(2) NOT NULL,
    arrival_terminal character(2) NOT NULL,
    leg_number smallint NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_perd_legs OWNER TO postgres;

--
-- Name: flight_perd_prnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_perd_prnt (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    selling_class character(2) NOT NULL,
    parent_sell_cls character(2) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_perd_prnt OWNER TO postgres;

--
-- Name: flight_perd_segm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_perd_segm (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    post_control_flag character(1) NOT NULL,
    aircraft_code character(3) NOT NULL,
    flight_closed_flag character(1) NOT NULL,
    flight_brdng_flag character(1) NOT NULL,
    segment_number character(22) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_perd_segm OWNER TO postgres;

--
-- Name: flight_periods; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_periods (
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    invt_end_date date NOT NULL,
    control_branch character(12) NOT NULL,
    invt_control_flag character(1) NOT NULL,
    wait_lst_ctrl_flag character(1) NOT NULL,
    via_cities character varying(135) NOT NULL,
    flgt_sched_status character(1) NOT NULL,
    open_end_flag character(1) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    gen_flag_invt character(1) NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_periods OWNER TO postgres;

--
-- Name: flight_reconcile; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_reconcile (
    dest_id character(8),
    flight_number character(7),
    flight_date date,
    city_pair integer,
    selling_class character(2),
    departure_airport character(5),
    arrival_airport character(5),
    segm_sngl_sold smallint,
    book_sngl_sold smallint,
    segm_group_sold smallint,
    book_group_sold smallint,
    segm_nrev_sold smallint,
    book_nrev_sold smallint,
    cor_sngl_sold smallint,
    cor_group_sold smallint,
    cor_nrev_sold smallint,
    update_user character(5),
    update_time character(19)
);


ALTER TABLE public.flight_reconcile OWNER TO postgres;

--
-- Name: flight_seat_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_seat_map (
    flight_date_leg_id integer NOT NULL,
    seat_map_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_seat_map OWNER TO postgres;

--
-- Name: flight_seat_reservation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_seat_reservation (
    flight_seat_reservation_id integer NOT NULL,
    flight_seat_reservation_group_id integer NOT NULL,
    flight_date_leg_id integer NOT NULL,
    seat_definition_id integer NOT NULL,
    reserve_reason_rcd character varying(5),
    book_no integer,
    blocked_flag character(1),
    temporary_reserve_flag character(1),
    release_date_time timestamp WITH time zone,
    active_flag character(1) NOT NULL,
    main_flight_seat_reservation_id integer,
    boarding_control_number_id integer,
    equipment_change_processing_id integer,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT flight_seat_reservation_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar]))),
    CONSTRAINT flight_seat_reservation_blocked_flag_check CHECK ((blocked_flag = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT flight_seat_reservation_temporary_reserve_flag_check CHECK ((temporary_reserve_flag = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);


ALTER TABLE public.flight_seat_reservation OWNER TO postgres;

--
-- Name: flight_seat_reservation_flight_seat_reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE flight_seat_reservation_flight_seat_reservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flight_seat_reservation_flight_seat_reservation_id_seq OWNER TO postgres;

--
-- Name: flight_seat_reservation_flight_seat_reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE flight_seat_reservation_flight_seat_reservation_id_seq OWNED BY flight_seat_reservation.flight_seat_reservation_id;


--
-- Name: flight_seat_reservation_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_seat_reservation_group (
    flight_seat_reservation_group_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_seat_reservation_group OWNER TO postgres;

--
-- Name: flight_seat_reservation_group_flight_seat_reservation_group_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE flight_seat_reservation_group_flight_seat_reservation_group_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flight_seat_reservation_group_flight_seat_reservation_group_seq OWNER TO postgres;

--
-- Name: flight_seat_reservation_group_flight_seat_reservation_group_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE flight_seat_reservation_group_flight_seat_reservation_group_seq OWNED BY flight_seat_reservation_group.flight_seat_reservation_group_id;


--
-- Name: flight_segment_dates; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_segment_dates (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    city_pair integer NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time time WITH time zone,
    arrival_time time WITH time zone,
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_segment_dates OWNER TO postgres;

--
-- Name: flight_segment_overlap; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_segment_overlap (
    flight_date_leg_id integer NOT NULL,
    overlap_flight_date_leg_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.flight_segment_overlap OWNER TO postgres;

--
-- Name: flight_shared_leg; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flight_shared_leg (
    dup_flight_number character(7) NOT NULL,
    dup_board_date date NOT NULL,
    dup_departure_airport character(5) NOT NULL,
    dup_arrival_airport character(5) NOT NULL,
    dup_flight_date date NOT NULL,
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    board_date date NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time smallint,
    arrival_time smallint,
    date_change_ind smallint,
    flight_path_code character(1),
    departure_terminal character(2),
    arrival_terminal character(2),
    config_table character(5),
    aircraft_code character(3),
    leg_number smallint,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.flight_shared_leg OWNER TO postgres;

--
-- Name: floating_definition; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE floating_definition (
    floating_def_id integer NOT NULL,
    class_code character(2) NOT NULL,
    departure_airport character(3) NOT NULL,
    arrival_airport character(3) NOT NULL,
    via_airport1 character(3),
    via_airport2 character(3),
    via_airport3 character(3),
    via_airport4 character(3),
    via_airport5 character(3),
    amount_currency character(3) NOT NULL,
    oneway_low_limit_amount numeric(15,5) NOT NULL,
    return_low_limit_amount numeric(15,5) NOT NULL,
    oneway_upgrade_amount numeric(15,5) NOT NULL,
    return_upgrade_amount numeric(15,5) NOT NULL,
    oneway_premium_amount numeric(15,5) NOT NULL,
    return_premium_amount numeric(15,5) NOT NULL,
    oneway_minimum_seats integer NOT NULL,
    return_minimum_seats integer NOT NULL,
    active_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_user character(5) NOT NULL,
    uptd_dest_id character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.floating_definition OWNER TO postgres;

--
-- Name: floating_definition_floating_def_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE floating_definition_floating_def_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.floating_definition_floating_def_id_seq OWNER TO postgres;

--
-- Name: floating_definition_floating_def_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE floating_definition_floating_def_id_seq OWNED BY floating_definition.floating_def_id;


--
-- Name: flt_check_bags; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_check_bags (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    bag_cnt smallint,
    bag_tag_no character(12),
    bag_weight real,
    arrival_airport character(5) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_check_bags OWNER TO postgres;

--
-- Name: flt_check_sequence_no; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_check_sequence_no (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    check_sequence_no smallint NOT NULL
);


ALTER TABLE public.flt_check_sequence_no OWNER TO postgres;

--
-- Name: flt_check_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_check_status (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    status_code character(8) NOT NULL,
    stat_date_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL
);


ALTER TABLE public.flt_check_status OWNER TO postgres;

--
-- Name: flt_config_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_config_rule (
    serial_number integer NOT NULL,
    exclusion_flag character(1) NOT NULL,
    flight_number character(7),
    departure_airport character(5),
    arrival_airport character(5),
    start_date date,
    end_date date,
    frequency_code character(7),
    config_table character(5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_config_rule OWNER TO postgres;

--
-- Name: flt_perd_seg_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_perd_seg_cls (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    ob_profile_no character(5) NOT NULL,
    segment_closed_flag character(1) NOT NULL,
    wl_closed_flag character(1) NOT NULL,
    wl_clear_inhibit_flag character(1) NOT NULL,
    wl_release_party_flag character(1) NOT NULL,
    meal_code character(7),
    beverage_code character(1),
    inflgt_serv_code character(17),
    segment_number character(22) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_perd_seg_cls OWNER TO postgres;

--
-- Name: flt_perd_seg_rstr; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_perd_seg_rstr (
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    city_pair integer NOT NULL,
    restrict_type character(1) NOT NULL,
    restrict_key character(25) NOT NULL,
    selling_class character varying(60),
    restrict_value smallint,
    rstr_perd_no smallint NOT NULL,
    gen_flag_rstr character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_perd_seg_rstr OWNER TO postgres;

--
-- Name: flt_seg_note_dt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_seg_note_dt (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    restrict_type character(1) NOT NULL,
    restrict_key character(5) NOT NULL,
    selling_class character varying(60),
    rstr_perd_no smallint NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_seg_note_dt OWNER TO postgres;

--
-- Name: flt_seg_pos_dt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE flt_seg_pos_dt (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    pos_table_no character(25) NOT NULL,
    rstr_perd_no smallint NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.flt_seg_pos_dt OWNER TO postgres;

--
-- Name: forced_fare; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE forced_fare (
    forced_fare_id integer NOT NULL,
    class_code character(2) NOT NULL,
    departure_date date NOT NULL,
    departure_airport character(3) NOT NULL,
    arrival_airport character(3) NOT NULL,
    via_airport1 character(3),
    via_airport2 character(3),
    via_airport3 character(3),
    via_airport4 character(3),
    via_airport5 character(3),
    flight_number1 character(7) NOT NULL,
    flight_number2 character(7),
    flight_number3 character(7),
    flight_number4 character(7),
    flight_number5 character(7),
    flight_number6 character(7),
    fare_basis_code character(16) NOT NULL,
    fare_amount numeric(15,5) NOT NULL,
    fare_currency character(3) NOT NULL,
    refundable_flag character(1) NOT NULL,
    return_flag character(1) NOT NULL,
    base_fare_basis_code character(16),
    base_class character(2),
    base_amount numeric(15,5),
    book_no integer,
    pax_code character(5) DEFAULT NULL::bpchar,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.forced_fare OWNER TO postgres;

--
-- Name: forced_fare_forced_fare_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE forced_fare_forced_fare_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.forced_fare_forced_fare_id_seq OWNER TO postgres;

--
-- Name: forced_fare_forced_fare_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE forced_fare_forced_fare_id_seq OWNED BY forced_fare.forced_fare_id;


--
-- Name: gmt_lc_con; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE gmt_lc_con (
    flight_number character(6) NOT NULL,
    gmt_flight_date date NOT NULL,
    rv_flight_date date NOT NULL,
    update_user character(6),
    update_group character(8),
    update_time character(19)
);


ALTER TABLE public.gmt_lc_con OWNER TO postgres;

--
-- Name: group_; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE group_ (
    group_code character(5) NOT NULL,
    group_type character(1) NOT NULL,
    duty_codes character varying(60),
    branch_codes character varying(130),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.group_ OWNER TO postgres;

--
-- Name: group_review; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE group_review (
    company_code character(3) NOT NULL,
    action_type character(12) NOT NULL,
    review_days smallint NOT NULL,
    tlt_interval smallint NOT NULL,
    auto_chck_flag character(1) NOT NULL,
    auto_chck_value smallint,
    disp_flag character(1) NOT NULL,
    rev_branch character(12),
    rev_queue_code character(5),
    seat_request_type character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.group_review OWNER TO postgres;

--
-- Name: group_security_function_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE group_security_function_mapping (
    group_security_function_mapping_id bigint NOT NULL,
    security_group_id bigint NOT NULL,
    function_id bigint NOT NULL,
    qualifier character varying(240),
    create_user character(5) NOT NULL,
    create_time date NOT NULL,
    create_group character(8) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8)
);


ALTER TABLE public.group_security_function_mapping OWNER TO postgres;

--
-- Name: grp_queue_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE grp_queue_codes (
    flight_number character(7) NOT NULL,
    dest_branch character(12) NOT NULL,
    xcl_queue_code character(5) NOT NULL,
    rqst_queue_code character(5) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.grp_queue_codes OWNER TO postgres;

--
-- Name: hist_book; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book (
    book_no integer NOT NULL,
    locator character(6),
    book_type character(2) NOT NULL,
    group_name character(53),
    no_of_seats smallint NOT NULL,
    book_category character(1) NOT NULL,
    group_wait_seats smallint,
    group_request_seats smallint,
    group_realtn_pcnt smallint,
    origin_branch_code character(12) NOT NULL,
    book_agency_code character(8),
    book_agency character(8),
    departure_airport character(5),
    departure_nation character(2),
    origin_address character(10),
    record_locator character varying(69),
    received_from character varying(60) NOT NULL,
    tour_code character(20),
    payment_amount numeric(15,5),
    processing_flag character(1) NOT NULL,
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
    et_serial_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book OWNER TO postgres;

--
-- Name: hist_book_fares; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book_fares (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(90),
    status_flag character(1) NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book_fares OWNER TO postgres;

--
-- Name: hist_book_fares_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book_fares_pass (
    book_no integer NOT NULL,
    pax_code character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(255),
    et_serial_no integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book_fares_pass OWNER TO postgres;

--
-- Name: hist_book_fares_paym; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book_fares_paym (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    payment_code character(5) NOT NULL,
    fare_calc_code character(15) NOT NULL,
    fare_paymt_amount numeric(15,5) NOT NULL,
    currency_code character(3) NOT NULL,
    tax_code character(5),
    nation_code character(5),
    refund_stat_flag character(1) NOT NULL,
    exempt_stat_flag character(1) NOT NULL,
    refundable_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    net_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    private_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    flight_number character(7),
    board_date date,
    flight_origin character(5),
    flight_destination character(5),
    source_ref_id bigint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book_fares_paym OWNER TO postgres;

--
-- Name: hist_booking_fare_segments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_booking_fare_segments (
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
    update_time timestamp WITH time zone,
    et_serial_no integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.hist_booking_fare_segments OWNER TO postgres;

--
-- Name: hist_book_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book_requests (
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book_requests OWNER TO postgres;

--
-- Name: hist_book_time_limits; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_book_time_limits (
    book_no integer NOT NULL,
    timelmt_sequence_no smallint NOT NULL,
    timelmt_type character(1) NOT NULL,
    limit_time_mins smallint NOT NULL,
    limit_date date NOT NULL,
    cancel_flag character(1) NOT NULL,
    queue_code character(5),
    dest_branch character(12) NOT NULL,
    remark_text character(240),
    all_pax_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_book_time_limits OWNER TO postgres;

--
-- Name: hist_coupon; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_coupon (
    ticket_no character varying(20) NOT NULL,
    coupon_sequence_no smallint NOT NULL,
    coupon_status character varying(3) NOT NULL,
    invol_ind character varying(3),
    sac_code character varying(20),
    uac_state character(1),
    cos_state character(1),
    hist_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.hist_coupon OWNER TO postgres;

--
-- Name: hist_currency_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_currency_codes (
    currency_code character(3) NOT NULL,
    valid_from_date_time timestamp WITH time zone NOT NULL,
    valid_to_date_time timestamp WITH time zone NOT NULL,
    description character varying(30),
    "precision" smallint NOT NULL,
    round_units smallint NOT NULL,
    nuc_rate numeric(9,5) NOT NULL,
    numeric_code integer,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_currency_codes OWNER TO postgres;

--
-- Name: hist_itinerary; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_itinerary (
    book_no integer NOT NULL,
    route_no smallint NOT NULL,
    alt_itinerary_no smallint NOT NULL,
    itinerary_no smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5),
    arrival_airport character(5),
    departure_time smallint,
    arrival_time smallint,
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_itinerary OWNER TO postgres;

--
-- Name: hist_passenger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_passenger (
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.hist_passenger OWNER TO postgres;

--
-- Name: hist_ticket; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hist_ticket (
    ticket_no character varying(20) NOT NULL,
    status_flag character(1) NOT NULL,
    pax_code character(5) NOT NULL,
    issued_in_exch character varying(13),
    total_amount numeric(15,5) DEFAULT 0 NOT NULL,
    conjunction_tckts character varying(20),
    conj_ticket_sequence_no smallint DEFAULT 0 NOT NULL,
    hist_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.hist_ticket OWNER TO postgres;

--
-- Name: hsbc_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE hsbc_transaction (
    hsbc_transaction_id integer NOT NULL,
    locator character varying(10),
    request text,
    request_data text,
    reply text,
    rqst_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    rply_date_time timestamp WITH time zone,
    settled character(1) DEFAULT 'N'::bpchar NOT NULL,
    reference_number character varying(20),
    error_description text,
    external_tran_id character varying(30)
);


ALTER TABLE public.hsbc_transaction OWNER TO postgres;

--
-- Name: hsbc_transaction_hsbc_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE hsbc_transaction_hsbc_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hsbc_transaction_hsbc_transaction_id_seq OWNER TO postgres;

--
-- Name: hsbc_transaction_hsbc_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE hsbc_transaction_hsbc_transaction_id_seq OWNED BY hsbc_transaction.hsbc_transaction_id;


--
-- Name: iline_req_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE iline_req_mesgs (
    message_id bigint NOT NULL,
    book_no integer DEFAULT 0 NOT NULL,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    requestor character(3) NOT NULL,
    edifact character varying(1024) DEFAULT NULL::character varying,
    xml character varying(1024) DEFAULT NULL::character varying,
    error_text character varying(1024) DEFAULT NULL::character varying,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.iline_req_mesgs OWNER TO postgres;

--
-- Name: iline_resp_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE iline_resp_mesgs (
    message_id bigint NOT NULL,
    book_no integer DEFAULT 0 NOT NULL,
    message_type character varying(15) DEFAULT 'unknown'::character varying,
    edifact character varying(1024) DEFAULT NULL::character varying,
    xml character varying(1024) DEFAULT NULL::character varying,
    error_text character varying(1024) DEFAULT NULL::character varying,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.iline_resp_mesgs OWNER TO postgres;

--
-- Name: inf11_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inf11_transaction (
    transaction_id integer NOT NULL,
    message_id character varying(24) NOT NULL,
    transaction_type character varying(10) NOT NULL,
    book_no integer NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    policy_number character varying(10) DEFAULT ''::character varying,
    failure_flag character(1) DEFAULT 'N'::bpchar,
    request_data character varying(16000),
    reply_data character varying(16000),
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    update_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.inf11_transaction OWNER TO postgres;

--
-- Name: inf11_transaction_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE inf11_transaction_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inf11_transaction_transaction_id_seq OWNER TO postgres;

--
-- Name: inf11_transaction_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE inf11_transaction_transaction_id_seq OWNED BY inf11_transaction.transaction_id;


--
-- Name: inventory_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventory_history (
    id integer NOT NULL,
    flight_number character varying(7),
    flight_date date,
    class_code character varying(2),
    city_pair integer,
    nett_sngl_change integer,
    segm_sngl_change integer,
    nett_sngl_change_wait integer,
    segm_sngl_change_wait integer,
    nett_group_change integer,
    segm_group_change integer,
    nett_group_change_wait integer,
    segm_group_change_wait integer,
    nett_nrev_change integer,
    segm_nrev_change integer,
    nett_nrev_change_wait integer,
    segm_nrev_change_wait integer,
    pid integer,
    user_code character varying(10),
    action_date_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.inventory_history OWNER TO postgres;

--
-- Name: inventory_history_detail; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventory_history_detail (
    inventory_history_detail_id bigint NOT NULL,
    inventory_history_update_id bigint NOT NULL,
    origin character(5) NOT NULL,
    destination character(5) NOT NULL,
    selling_class character(2) NOT NULL
);


ALTER TABLE public.inventory_history_detail OWNER TO postgres;

--
-- Name: inventory_history_detail_specific; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventory_history_detail_specific (
    inventory_history_detail_specific_id bigint NOT NULL,
    seat_capacity integer NOT NULL,
    seat_protect_level integer NOT NULL,
    limit_sales_level integer NOT NULL,
    before_flag integer NOT NULL,
    segment_closed character(1) NOT NULL,
    waitlist_closed character(1) NOT NULL,
    inventory_history_detail_id bigint NOT NULL
);


ALTER TABLE public.inventory_history_detail_specific OWNER TO postgres;

--
-- Name: inventory_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE inventory_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventory_history_id_seq OWNER TO postgres;

--
-- Name: inventory_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE inventory_history_id_seq OWNED BY inventory_history.id;


--
-- Name: inventory_history_update; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventory_history_update (
    inventory_history_update_id bigint NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    create_user character(5) NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL
);


ALTER TABLE public.inventory_history_update OWNER TO postgres;

--
-- Name: inventry_auto_rules; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventry_auto_rules (
    rule_id integer NOT NULL,
    selling_class character varying(3) NOT NULL,
    valid_from date NOT NULL,
    valid_to date NOT NULL,
    rule_type character(1) NOT NULL,
    rule_value integer NOT NULL,
    exclude_flag character(1),
    flight_number character varying(7),
    origin character varying(5),
    destination character varying(5),
    frequency character varying(7),
    future_to_scan integer,
    update_user character(5),
    update_time timestamp WITH time zone
);


ALTER TABLE public.inventry_auto_rules OWNER TO postgres;

--
-- Name: inventry_auto_rules_details; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventry_auto_rules_details (
    detail_id integer NOT NULL,
    rule_id integer NOT NULL,
    flight_number character varying(7),
    origin character varying(5),
    destination character varying(5),
    frequency character varying(7)
);


ALTER TABLE public.inventry_auto_rules_details OWNER TO postgres;

--
-- Name: inventry_auto_rules_details_detail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE inventry_auto_rules_details_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventry_auto_rules_details_detail_id_seq OWNER TO postgres;

--
-- Name: inventry_auto_rules_details_detail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE inventry_auto_rules_details_detail_id_seq OWNED BY inventry_auto_rules_details.detail_id;


--
-- Name: inventry_auto_rules_rule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE inventry_auto_rules_rule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventry_auto_rules_rule_id_seq OWNER TO postgres;

--
-- Name: inventry_auto_rules_rule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE inventry_auto_rules_rule_id_seq OWNED BY inventry_auto_rules.rule_id;


--
-- Name: inventry_realloc; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventry_realloc (
    create_time character(19) NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    segm_sngl_sold smallint NOT NULL,
    segm_sngl_wait smallint NOT NULL,
    segm_group_sold smallint NOT NULL,
    segm_group_wait smallint NOT NULL,
    segm_nrev_sold smallint NOT NULL,
    segm_nrev_wait smallint NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    perd_sequence_no smallint NOT NULL,
    action_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    remarks character varying(255),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.inventry_realloc OWNER TO postgres;

--
-- Name: inventry_segment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE inventry_segment (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
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
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.inventry_segment OWNER TO postgres;

--
-- Name: invoice_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE invoice_serial_nos (
    invoice_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.invoice_serial_nos OWNER TO postgres;

--
-- Name: invoice_serial_nos_invoice_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE invoice_serial_nos_invoice_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoice_serial_nos_invoice_no_seq OWNER TO postgres;

--
-- Name: invoice_serial_nos_invoice_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE invoice_serial_nos_invoice_no_seq OWNED BY invoice_serial_nos.invoice_no;


--
-- Name: invoices; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE invoices (
    invoice_no integer NOT NULL,
    invoice_date date NOT NULL,
    invoice_amount numeric(15,5) NOT NULL,
    invoice_to character(3) NOT NULL,
    invoice_to_code character(10) NOT NULL,
    invc_curr_code character(3) NOT NULL,
    status_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.invoices OWNER TO postgres;

--
-- Name: invt_status_chng; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE invt_status_chng (
    company_code character(3) NOT NULL,
    from_status_code character(2) NOT NULL,
    stat_condition character(1) NOT NULL,
    invt_control_flag character(1) NOT NULL,
    to_status_code character(2) NOT NULL,
    control_set_flag character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.invt_status_chng OWNER TO postgres;

--
-- Name: invt_update_ignore; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE invt_update_ignore (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    override_flag character(1) NOT NULL,
    schedule_period_no smallint NOT NULL
);


ALTER TABLE public.invt_update_ignore OWNER TO postgres;

--
-- Name: itineraries; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE itineraries (
    book_no integer NOT NULL,
    route_no smallint NOT NULL,
    alt_itinerary_no smallint NOT NULL,
    itinerary_no smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5),
    arrival_airport character(5),
    departure_time time WITH time zone,
    arrival_time time WITH time zone,
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.itineraries OWNER TO postgres;

--
-- Name: itinerary_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE itinerary_pass (
    book_no integer NOT NULL,
    contact_sequence_no smallint NOT NULL,
    transit_phone_no character(30) NOT NULL,
    transit_address character varying(200),
    transit_city character(25),
    transit_state character(25),
    transit_zip character(15),
    transit_nation character(25),
    all_pax_flag character(1) NOT NULL,
    all_itinerary_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.itinerary_pass OWNER TO postgres;


--
-- Name: k2_transaction; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE k2_transaction (
    k2_transaction_id integer NOT NULL,
    locator character varying(10),
    approved character(1) DEFAULT 'N'::bpchar NOT NULL,
    request text,
    request_data text,
    reply text,
    rqst_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    rply_date_time timestamp WITH time zone,
    settled character(1) DEFAULT 'N'::bpchar NOT NULL,
    sett_request text,
    sett_request_data text,
    sett_reply text,
    sett_request_date_time timestamp WITH time zone,
    sett_reply_date_time timestamp WITH time zone,
    reference_number character varying(20),
    approval_code character varying(7),
    avs_code character(1),
    avs_response character varying(20),
    error_description text,
    external_tran_id integer
);


ALTER TABLE public.k2_transaction OWNER TO postgres;

--
-- Name: k2_transaction_k2_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE k2_transaction_k2_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.k2_transaction_k2_transaction_id_seq OWNER TO postgres;

--
-- Name: k2_transaction_k2_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE k2_transaction_k2_transaction_id_seq OWNED BY k2_transaction.k2_transaction_id;


--
-- Name: language_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE language_ref (
    language_rcd character varying(20) NOT NULL,
    description character varying(240) NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.language_ref OWNER TO postgres;

--
-- Name: last_operation_status_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE last_operation_status_ref (
    last_operation_status_rcd character varying(5) NOT NULL,
    description character varying(255) NOT NULL,
    update_user character varying(5),
    update_group character varying(5),
    update_time timestamp WITH time zone
);


ALTER TABLE public.last_operation_status_ref OWNER TO postgres;


--
-- Name: log_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE log_serial_nos (
    log_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.log_serial_nos OWNER TO postgres;

--
-- Name: log_serial_nos_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE log_serial_nos_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.log_serial_nos_log_id_seq OWNER TO postgres;

--
-- Name: log_serial_nos_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE log_serial_nos_log_id_seq OWNED BY log_serial_nos.log_id;


--
-- Name: master_files; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE master_files (
    file_code character(4) NOT NULL,
    master_code character(5) NOT NULL,
    description character varying(160),
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.master_files OWNER TO postgres;

--
-- Name: mco_info; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE mco_info (
    mco_number character varying(20) NOT NULL,
    mco_type character varying(10) NOT NULL,
    mco_id integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.mco_info OWNER TO postgres;

--
-- Name: menu_item; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE menu_item (
    menu_item_id integer NOT NULL,
    parent_menu_item_id integer,
    menu_level smallint,
    menu_code character varying(100),
    parent_menu_code character varying(100),
    description character varying(255),
    caption character varying(255),
    popup_flag character(1),
    action_type_code character varying(5) NOT NULL,
    com_progid character varying(100),
    action_data character varying(255),
    shortcut_key character varying(5),
    seq_no smallint,
    active_flag character(1),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.menu_item OWNER TO postgres;

--
-- Name: misc_charge; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE misc_charge (
    misc_charge_code character(10) NOT NULL,
    description character(25) NOT NULL,
    currency_code character(5) NOT NULL,
    charge_amount numeric(15,5) NOT NULL,
    tax_application character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.misc_charge OWNER TO postgres;

--
-- Name: mvt_delay_code; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE mvt_delay_code (
    delay_code character varying(4) NOT NULL,
    delay_subcode character varying(4) NOT NULL,
    delay_type character varying(30),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.mvt_delay_code OWNER TO postgres;


--
-- Name: nation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE nation (
    nation_code character(2) NOT NULL,
    nation_name character varying(60),
    currency_code character(3) NOT NULL,
    visa_info character varying(255),
    inoculation_info character varying(255),
    driving_lic_info character varying(255),
    general_info character varying(200),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.nation OWNER TO postgres;

--
-- Name: ob_profiles; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ob_profiles (
    ob_profile_no character(5) NOT NULL,
    days_befr_depr smallint NOT NULL,
    next_days_befr smallint NOT NULL,
    overbooking_percnt smallint NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.ob_profiles OWNER TO postgres;

--
-- Name: office_mail; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE office_mail (
    message_id integer NOT NULL,
    msg_sequence_no smallint NOT NULL,
    create_time character(19) NOT NULL,
    message_type character(1) NOT NULL,
    message character varying(255)
);


ALTER TABLE public.office_mail OWNER TO postgres;

--
-- Name: oledb_tran_test; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE oledb_tran_test (
    row_no integer NOT NULL,
    context_id character varying(255) NOT NULL,
    activity_id character varying(255) NOT NULL,
    transaction_id character varying(255) NOT NULL,
    is_in_tran_flag smallint,
    custom_value character varying(255),
    abort_tran_flag smallint
);


ALTER TABLE public.oledb_tran_test OWNER TO postgres;

--
-- Name: origin_address_name; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE origin_address_name (
    origin_address character varying(20) NOT NULL,
    origin_address_name character varying(250) NOT NULL
);


ALTER TABLE public.origin_address_name OWNER TO postgres;

--
-- Name: origin_addrs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE origin_addrs (
    company_code character(3),
    message_code character(3),
    origin_address character(10) NOT NULL,
    update_user character(5) NOT NULL,
    gds_origin character(1) DEFAULT 'N'::bpchar NOT NULL,
    address_type character(1) DEFAULT 'I'::bpchar NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.origin_addrs OWNER TO postgres;

--
-- Name: origin_addrs_old; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE origin_addrs_old (
    company_code character(3),
    message_code character(3),
    origin_address character(10) NOT NULL,
    address_type character(1) DEFAULT 'I'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.origin_addrs_old OWNER TO postgres;

--
-- Name: osi_et_text; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE osi_et_text (
    osi_airport character(5) NOT NULL,
    osi_request_code character(4) NOT NULL,
    osi_request_text character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.osi_et_text OWNER TO postgres;

--
-- Name: paradox_chg; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE paradox_chg (
    create_time character(19) NOT NULL,
    prdx_table_name character(8) NOT NULL,
    keys character varying(60) NOT NULL,
    scrutiny_flag character(1),
    updt_flag character(1) NOT NULL,
    server_id character(15) NOT NULL,
    record1 character varying(255),
    record2 character varying(255),
    record3 character varying(255),
    record4 character varying(255),
    record5 character varying(230)
);


ALTER TABLE public.paradox_chg OWNER TO postgres;

--
-- Name: pax_contact; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pax_contact (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.pax_contact OWNER TO postgres;

--
-- Name: pass_desc_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pass_desc_codes (
    company_code character(3) NOT NULL,
    pax_code character(5) NOT NULL,
    description character varying(30),
    osi_indicator character(1) NOT NULL,
    rqst_code character(4),
    fqt_indicator character(1) NOT NULL,
    rcfm_canx_flag character(1) NOT NULL,
    book_category character(1),
    employee_no_required_flag character(1),
    buddy_pass_required_flag character(1),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pass_desc_codes OWNER TO postgres;

--
-- Name: pass_itin_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pass_itin_ref (
    prl_id integer NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    pax_seq smallint,
    pax_name character(53) NOT NULL,
    prl_flag character(1) NOT NULL,
    book_no integer,
    pax_no smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.pass_itin_ref OWNER TO postgres;

--
-- Name: pass_itin_ref_det; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pass_itin_ref_det (
    prl_id integer NOT NULL,
    item_seq smallint NOT NULL,
    item_type character(5),
    item_code character(5),
    item_text character varying(50),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.pass_itin_ref_det OWNER TO postgres;

--
-- Name: pax_remarks; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pax_remarks (
    book_no integer NOT NULL,
    remark_sequence_no smallint NOT NULL,
    remark_text character varying(240),
    all_pax_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pax_remarks OWNER TO postgres;

--
-- Name: passengers; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE passengers (
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    pax_name character(53) NOT NULL,
    birth_date date,
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.passengers OWNER TO postgres;

--
-- Name: pax_refund; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pax_refund (
    book_no integer NOT NULL,
    pax_name character(53),
    crdt_sequence_no smallint NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    credit_amount numeric(15,5) NOT NULL,
    document_no character(51),
    document_date date,
    processing_date date,
    processing_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pax_refund OWNER TO postgres;

--
-- Name: payment_amount_limits; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_amount_limits (
    payment_type character varying(5) NOT NULL,
    payment_form character varying(5) NOT NULL,
    currency_code character varying(3) NOT NULL,
    lower_amount numeric(15,5),
    upper_amount numeric(15,5),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.payment_amount_limits OWNER TO postgres;

--
-- Name: payment_backup; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_backup (
    payment_no integer NOT NULL,
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
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.payment_backup OWNER TO postgres;

--
-- Name: payment_channel_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_channel_config (
    payment_channel_config_id bigint NOT NULL,
    branch_code character(12),
    document_catg character(3),
    minutes_before_departure integer NOT NULL,
    deadline_in_minutes integer NOT NULL,
    deadline_is_instant_flag integer DEFAULT 0,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    inactivated_by_user_code character(5),
    inactivated_date_time timestamp WITH time zone,
    document_type character(2),
    deadline_in_workdays integer DEFAULT 0 NOT NULL,
    deadline_default_time integer DEFAULT 0 NOT NULL,
    monday character(1) DEFAULT 'Y'::bpchar,
    tuesday character(1) DEFAULT 'Y'::bpchar,
    wednesday character(1) DEFAULT 'Y'::bpchar,
    thursday character(1) DEFAULT 'Y'::bpchar,
    friday character(1) DEFAULT 'Y'::bpchar,
    saturday character(1) DEFAULT 'Y'::bpchar,
    sunday character(1) DEFAULT 'Y'::bpchar
);


ALTER TABLE public.payment_channel_config OWNER TO postgres;

--
-- Name: payment_et_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_et_ref (
    payment_no integer NOT NULL,
    et_serial_no integer NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.payment_et_ref OWNER TO postgres;

--
-- Name: payment_form_field; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_form_field (
    payment_form_field_id integer NOT NULL,
    control_name character varying(60) NOT NULL,
    display_name character varying(100) NOT NULL
);


ALTER TABLE public.payment_form_field OWNER TO postgres;

--
-- Name: payment_form_field_payment_form_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE payment_form_field_payment_form_field_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_form_field_payment_form_field_id_seq OWNER TO postgres;

--
-- Name: payment_form_field_payment_form_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE payment_form_field_payment_form_field_id_seq OWNED BY payment_form_field.payment_form_field_id;


--
-- Name: payment_form_field_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_form_field_status (
    payment_form_field_id integer NOT NULL,
    payment_type character varying(5) NOT NULL,
    payment_form character varying(5) NOT NULL,
    visible_flag character(1) DEFAULT 'Y'::bpchar NOT NULL,
    enabled_flag character(1) DEFAULT 'Y'::bpchar NOT NULL,
    locked_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    mandatory_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    default_value character varying(255)
);


ALTER TABLE public.payment_form_field_status OWNER TO postgres;

--
-- Name: payment_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE payment_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_no_seq OWNER TO postgres;

--
-- Name: payment_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payment_serial_nos (
    payment_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.payment_serial_nos OWNER TO postgres;

--
-- Name: payment_serial_nos_payment_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE payment_serial_nos_payment_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_serial_nos_payment_no_seq OWNER TO postgres;

--
-- Name: payment_serial_nos_payment_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE payment_serial_nos_payment_no_seq OWNED BY payment_serial_nos.payment_no;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payments (
    payment_no integer DEFAULT nextval('payment_no_seq'::regclass) NOT NULL,
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
    create_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: payments_reference; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payments_reference (
    payments_reference_id integer NOT NULL,
    payment_no integer NOT NULL,
    ref_payment_no integer NOT NULL,
    reference_type character(2) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.payments_reference OWNER TO postgres;

--
-- Name: payments_reference_payments_reference_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE payments_reference_payments_reference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_reference_payments_reference_id_seq OWNER TO postgres;

--
-- Name: payments_reference_payments_reference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE payments_reference_payments_reference_id_seq OWNED BY payments_reference.payments_reference_id;


--
-- Name: payments_uplift; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payments_uplift (
    file_nr character(9) NOT NULL,
    batch_nr character(9) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    batch_description character varying(50)
);


ALTER TABLE public.payments_uplift OWNER TO postgres;

--
-- Name: payments_uplift_detail; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE payments_uplift_detail (
    file_nr character(9) NOT NULL,
    batch_nr character(9) NOT NULL,
    create_user character(5) NOT NULL,
    payment_no smallint NOT NULL,
    payment_form character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    payment_mode character(1),
    payment_amount numeric(15,5) NOT NULL,
    book_amount numeric(15,5),
    payment_difference bigint,
    document_no character(25),
    book_no integer,
    pax_no smallint,
    posting_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    payment_no_ref integer,
    locator character(6),
    ins_upd_flag character(1),
    payment_no_diff_ref integer,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.payments_uplift_detail OWNER TO postgres;

-- *********************************************************************************************************************************


--
-- Name: pfs_counts; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pfs_counts (
    flight_number character(7) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    flight_date date NOT NULL,
    count1 integer,
    count2 integer,
    count3 integer,
    update_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.pfs_counts OWNER TO postgres;

--
-- Name: pnl_adl_book; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_book (
    pnl_adl_id integer NOT NULL,
    record_id integer NOT NULL,
    book_no integer NOT NULL,
    locator character(12) NOT NULL,
    party_ind character(8),
    reserve_status character(5),
    grp_name character(64),
    inbound character(255),
    outbound character(255),
    outbound2 character(255)
);


ALTER TABLE public.pnl_adl_book OWNER TO postgres;

--
-- Name: pnl_adl_iten; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_iten (
    pnl_adl_id integer NOT NULL,
    record_id integer NOT NULL,
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    selling_class character(2) NOT NULL,
    no_of_seats integer NOT NULL
);


ALTER TABLE public.pnl_adl_iten OWNER TO postgres;

--
-- Name: pnl_adl_pax; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_pax (
    pnl_adl_id integer NOT NULL,
    record_id integer NOT NULL,
    book_no integer NOT NULL,
    pax_id integer NOT NULL,
    pax_name character(64)
);


ALTER TABLE public.pnl_adl_pax OWNER TO postgres;

--
-- Name: pnl_adl_rem; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_rem (
    pnl_adl_id integer NOT NULL,
    record_id integer NOT NULL,
    book_no integer NOT NULL,
    pax_id integer NOT NULL,
    rem_id integer NOT NULL,
    remarks character(255) NOT NULL
);


ALTER TABLE public.pnl_adl_rem OWNER TO postgres;

--
-- Name: pnl_adl_rout; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_rout (
    routing_ind integer NOT NULL,
    departure_airport character(5) NOT NULL,
    tty_report_addrs character(7) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_adl_rout OWNER TO postgres;

--
-- Name: pnl_adl_store; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_store (
    sequence_no integer NOT NULL,
    pnl_adl_type character(1) NOT NULL,
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    routing_ind integer NOT NULL,
    message text,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    udpt_date_time character(19) NOT NULL
);


ALTER TABLE public.pnl_adl_store OWNER TO postgres;

--
-- Name: pnl_adl_tmp; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_tmp (
    flight_number character(7),
    flight_date date,
    flight_path character(60)
);


ALTER TABLE public.pnl_adl_tmp OWNER TO postgres;

--
-- Name: pnl_adl_trigger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_adl_trigger (
    pnl_adl_id integer NOT NULL,
    pnl_adl_type character(1) NOT NULL,
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_adl_rule_code character(5) NOT NULL,
    routing_ind integer,
    date_to_run date NOT NULL,
    time_to_run integer NOT NULL,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    udpt_date_time character(19) NOT NULL
);


ALTER TABLE public.pnl_adl_trigger OWNER TO postgres;

--
-- Name: pnl_flight; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_flight (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_type character(1) NOT NULL,
    system_dests character varying(255),
    tty_priority character(2),
    tty_address1 character varying(144),
    tty_address2 character varying(144),
    total_join_cnt smallint,
    total_transit_cnt smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_flight OWNER TO postgres;

--
-- Name: pnl_flt_seg_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_flt_seg_cls (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_type character(1) NOT NULL,
    arrival_airport character(5) NOT NULL,
    selling_class character(2) NOT NULL,
    total_join_cnt smallint,
    total_transit_cnt smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_flt_seg_cls OWNER TO postgres;

--
-- Name: pnl_pass_name; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_pass_name (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_type character(1) NOT NULL,
    pnl_pax_no smallint NOT NULL,
    arrival_airport character(5) NOT NULL,
    selling_class character(2) NOT NULL,
    pnl_code_type character(1) NOT NULL,
    pax_name character(53) NOT NULL,
    noof_passengers smallint,
    book_no integer NOT NULL,
    inbound_conn character(13),
    outbound_conn character(13),
    tkt_document_no character(13) NOT NULL,
    baggage_tag_nos character varying(70),
    seat_number character(4),
    document_no character(15),
    board_status character(2) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_pass_name OWNER TO postgres;

--
-- Name: pnl_pass_request; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_pass_request (
    flight_number character(7) NOT NULL,
    board_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    pnl_type character(1) NOT NULL,
    pnl_pax_no smallint NOT NULL,
    request_text character varying(75) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_pass_request OWNER TO postgres;

--
-- Name: pnl_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnl_rule (
    pnl_adl_rule_code character(5) NOT NULL,
    sort_indicator character(1) NOT NULL,
    flight_number character(7),
    start_date date,
    end_date date,
    start_time smallint,
    end_time smallint,
    frequency_code character(7),
    departure_airport character(5),
    pnl_gen_type character(1) NOT NULL,
    pnl_gen_time smallint NOT NULL,
    pnl_adl_route_ind smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnl_rule OWNER TO postgres;

--
-- Name: pnr_filter; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnr_filter (
    filter_id bigint NOT NULL,
    filter_name character varying(254),
    user_code character(5) NOT NULL,
    create_time date NOT NULL,
    invalid_date date,
    filter_is_private integer,
    include_booking integer,
    include_passenger integer,
    include_service integer,
    include_queue integer,
    include_flight integer,
    confirmed_bookings integer,
    passengers_not_reconfirmed integer,
    passengers_have_reconfirmed integer,
    passengers_with_ssr_osi integer,
    canceled_bookings integer,
    booking_on_waitlists integer,
    requested_bookings integer,
    group_bookings integer,
    passengers_with_ticket integer,
    passengers_without_ticket integer,
    pax_name character varying(254),
    flight_number character(7),
    flight_date_from date,
    flight_date_until date,
    departure character varying(10),
    arrival character varying(10),
    class character varying(10),
    ssr_osi character varying(254),
    queue character varying(254),
    flight_date_today integer,
    queue_company character varying(5),
    queue_city character varying(5),
    queue_branch character varying(5),
    filter_on_ssr_flag integer,
    service_filter_type character(1),
    max_hits integer,
    criteria integer
);


ALTER TABLE public.pnr_filter OWNER TO postgres;

--
-- Name: pnr_query; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnr_query (
    qry_user_code character(6) NOT NULL,
    qry_name character varying(30) NOT NULL,
    dest_branch character(12) NOT NULL,
    qry_description character varying(255),
    qry_type character(1) NOT NULL,
    read_strt_auth_level smallint NOT NULL,
    read_end_auth_level smallint NOT NULL,
    upd_strt_auth_level smallint NOT NULL,
    upd_end_auth_level smallint NOT NULL,
    qry_value_1 character varying(255),
    qry_value_2 character varying(255),
    qry_value_3 character varying(255),
    qry_value_4 character varying(255),
    qry_value_5 character varying(255),
    qry_value_6 character varying(255),
    qry_value_7 character varying(255),
    qry_value_8 character varying(255),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.pnr_query OWNER TO postgres;

--
-- Name: pnr_query_descr; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnr_query_descr (
    qry_user_code character(6) NOT NULL,
    qry_name character varying(30) NOT NULL,
    qry_sequence_no smallint NOT NULL,
    qry_description character varying(255),
    qry_txt_type character(1) NOT NULL
);


ALTER TABLE public.pnr_query_descr OWNER TO postgres;

--
-- Name: pnrnm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnrnm (
    name character(30) NOT NULL,
    book_no integer
);


ALTER TABLE public.pnrnm OWNER TO postgres;

--
-- Name: pnt_of_sale_defn; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnt_of_sale_defn (
    pos_table_no character(25) NOT NULL,
    pos_code_type character(4) NOT NULL,
    code_value character(12) NOT NULL,
    incl_excl_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnt_of_sale_defn OWNER TO postgres;

--
-- Name: pnt_of_sale_tabl; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pnt_of_sale_tabl (
    pos_table_no character(25) NOT NULL,
    group_other_flag character(1) NOT NULL,
    limit_sale_level smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pnt_of_sale_tabl OWNER TO postgres;

--
-- Name: pos_code_parties; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pos_code_parties (
    pos_code_type character(4) NOT NULL,
    pos_code_party character(2) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pos_code_parties OWNER TO postgres;

--
-- Name: post_departure; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_departure (
    post_departure_id bigint NOT NULL,
    book_no integer,
    post_departure_rcd character(10),
    from_class character(3),
    to_class character(3),
    flight_number character(7),
    flight_date date,
    origin character(5),
    destination character(5),
    user_code character(5),
    create_time date
);


ALTER TABLE public.post_departure OWNER TO postgres;

--
-- Name: post_departure_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_departure_ref (
    post_departure_rcd character(10),
    description character varying(250),
    user_code character(5),
    create_time date
);


ALTER TABLE public.post_departure_ref OWNER TO postgres;

--
-- Name: post_hist_book; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book (
    book_no integer NOT NULL,
    locator character(6),
    book_type character(2) NOT NULL,
    group_name character(53),
    no_of_seats smallint NOT NULL,
    book_category character(1) NOT NULL,
    group_wait_seats smallint,
    group_request_seats smallint,
    group_realtn_pcnt smallint,
    origin_branch_code character(12) NOT NULL,
    book_agency_code character(8),
    book_agency character(8),
    departure_airport character(5),
    departure_nation character(2),
    origin_address character(10),
    record_locator character varying(69),
    received_from character varying(60) NOT NULL,
    tour_code character(20),
    payment_amount numeric(15,5),
    processing_flag character(1) NOT NULL,
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
    et_serial_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book OWNER TO postgres;

--
-- Name: post_hist_book_fares; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book_fares (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(90),
    status_flag character(1) NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book_fares OWNER TO postgres;

--
-- Name: post_hist_book_fares_pass; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book_fares_pass (
    book_no integer NOT NULL,
    pax_code character(5) NOT NULL,
    currency_code character(3) NOT NULL,
    total_amount numeric(15,5),
    fare_construction character varying(255),
    endrsmnt_rstrctns character varying(255),
    et_serial_no integer DEFAULT 0 NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book_fares_pass OWNER TO postgres;

--
-- Name: post_hist_book_fares_paym; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book_fares_paym (
    book_no integer NOT NULL,
    fare_no smallint NOT NULL,
    pax_code character(5) NOT NULL,
    payment_code character(5) NOT NULL,
    fare_calc_code character(15) NOT NULL,
    fare_paymt_amount numeric(15,5) NOT NULL,
    currency_code character(3) NOT NULL,
    tax_code character(5),
    nation_code character(5),
    refund_stat_flag character(1) NOT NULL,
    exempt_stat_flag character(1) NOT NULL,
    refundable_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    net_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    private_fare_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    flight_number character(7),
    board_date date,
    flight_origin character(5),
    flight_destination character(5),
    source_ref_id bigint,
    post_hist_book_fares_paym_id integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book_fares_paym OWNER TO postgres;

--
-- Name: post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq OWNER TO postgres;

--
-- Name: post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq OWNED BY post_hist_book_fares_paym.post_hist_book_fares_paym_id;


--
-- Name: post_hist_booking_fare_segments; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_booking_fare_segments (
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
    et_serial_no integer DEFAULT 0 NOT NULL,
    post_hist_booking_fare_segments_id integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_booking_fare_segments OWNER TO postgres;

--
-- Name: post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq OWNER TO postgres;

--
-- Name: post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq OWNED BY post_hist_booking_fare_segments.post_hist_booking_fare_segments_id;


--
-- Name: post_hist_book_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book_requests (
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book_requests OWNER TO postgres;

--
-- Name: post_hist_book_time_limits; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_book_time_limits (
    book_no integer NOT NULL,
    timelmt_sequence_no smallint NOT NULL,
    timelmt_type character(1) NOT NULL,
    limit_time_mins smallint NOT NULL,
    limit_date date NOT NULL,
    cancel_flag character(1) NOT NULL,
    queue_code character(5),
    dest_branch character(12) NOT NULL,
    remark_text character(240),
    all_pax_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_book_time_limits OWNER TO postgres;

--
-- Name: post_hist_itinerary; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_itinerary (
    book_no integer NOT NULL,
    route_no smallint NOT NULL,
    alt_itinerary_no smallint NOT NULL,
    itinerary_no smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5),
    arrival_airport character(5),
    departure_time smallint,
    arrival_time smallint,
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_itinerary OWNER TO postgres;

--
-- Name: post_hist_passenger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE post_hist_passenger (
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
    et_serial_no integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.post_hist_passenger OWNER TO postgres;


--
-- Name: prl_serial; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE prl_serial (
    prl_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.prl_serial OWNER TO postgres;

--
-- Name: prl_serial_prl_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE prl_serial_prl_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prl_serial_prl_id_seq OWNER TO postgres;

--
-- Name: prl_serial_prl_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE prl_serial_prl_id_seq OWNED BY prl_serial.prl_id;


--
-- Name: process_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE process_status (
    client_no smallint NOT NULL,
    process_srno integer NOT NULL,
    process_code character(10) NOT NULL,
    process_status character(1) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.process_status OWNER TO postgres;

--
-- Name: process_status_process_srno_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE process_status_process_srno_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.process_status_process_srno_seq OWNER TO postgres;

--
-- Name: process_status_process_srno_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE process_status_process_srno_seq OWNED BY process_status.process_srno;


--
-- Name: processing_indicators; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE processing_indicators (
    recorded_date date NOT NULL,
    end_transaction_reject integer,
    unprocessed_gds_msg_in integer,
    unprocessed_gds_msg_out integer,
    unprocessed_web_msg integer,
    unprocessed_e_ticket integer,
    bookings_under_scrutiny integer,
    flight_reconcile_corrections integer,
    gui_errors integer,
    core_dumps integer,
    pros_inventory_not_found integer,
    unsent_e_mails integer,
    failed_pnr_adl_exports integer
);


ALTER TABLE public.processing_indicators OWNER TO postgres;

--
-- Name: pros_upload_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pros_upload_history (
    pros_date date NOT NULL,
    pros_time character(10) NOT NULL,
    inventory_items integer NOT NULL,
    inventory_items_failed integer NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.pros_upload_history OWNER TO postgres;

--
-- Name: prosv_aircraft_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE prosv_aircraft_config (
    prosv_aircraft_pk integer NOT NULL,
    prosv_aircraft_config_pk integer NOT NULL,
    compartment_position integer NOT NULL,
    physical_capacity integer NOT NULL
);


ALTER TABLE public.prosv_aircraft_config OWNER TO postgres;

--
-- Name: prosv_aircraft_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE prosv_aircraft_mapping (
    prosv_aircraft_pk integer NOT NULL,
    results_aircraft_config_pk character(5) NOT NULL
);


ALTER TABLE public.prosv_aircraft_mapping OWNER TO postgres;

--
-- Name: pta; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pta (
    pta_number integer NOT NULL,
    mco_number character(13),
    pta_source character(1) NOT NULL,
    issuing_office character(12),
    issued_at_city character(5),
    origin_address character(10) NOT NULL,
    issue_date date,
    review_date date,
    status character(1) NOT NULL,
    sponser_name character(53) NOT NULL,
    pax_name character(53) NOT NULL,
    group_name character(53),
    pax_address character varying(200),
    pax_city character(25),
    pax_state character(25),
    pax_zip character(15),
    pax_nation character(25),
    pax_phone_no character varying(30),
    sponsor_address character varying(200),
    sponsor_city character(25),
    sponsor_state character(25),
    sponsor_zip character(15),
    sponsor_nation character(25),
    sponsor_phone_no character varying(30),
    routing character(80) NOT NULL,
    fare_construction character varying(255),
    currency_code character(3) NOT NULL,
    fare_amount numeric(15,5) NOT NULL,
    total_amount numeric(15,5) NOT NULL,
    remark_text character varying(255),
    queue_code character(5),
    queue_branch_code character(12),
    book_no integer,
    ticket_nos character(70),
    crea_branch_code character(12) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pta OWNER TO postgres;

--
-- Name: pta_pta_number_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE pta_pta_number_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pta_pta_number_seq OWNER TO postgres;

--
-- Name: pta_pta_number_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE pta_pta_number_seq OWNED BY pta.pta_number;


--
-- Name: pta_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE pta_status (
    pta_number integer NOT NULL,
    old_status character(1) NOT NULL,
    new_status character(1) NOT NULL,
    status_remark character(80),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.pta_status OWNER TO postgres;

--
-- Name: que_grp_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE que_grp_serial_nos (
    queue_grp_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.que_grp_serial_nos OWNER TO postgres;

--
-- Name: que_grp_serial_nos_queue_grp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE que_grp_serial_nos_queue_grp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.que_grp_serial_nos_queue_grp_id_seq OWNER TO postgres;

--
-- Name: que_grp_serial_nos_queue_grp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE que_grp_serial_nos_queue_grp_id_seq OWNED BY que_grp_serial_nos.queue_grp_id;


--
-- Name: que_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE que_serial_nos (
    queue_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.que_serial_nos OWNER TO postgres;

--
-- Name: que_serial_nos_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE que_serial_nos_queue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.que_serial_nos_queue_id_seq OWNER TO postgres;

--
-- Name: que_serial_nos_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE que_serial_nos_queue_id_seq OWNED BY que_serial_nos.queue_id;


--
-- Name: queue_codes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE queue_codes (
    queue_code character(5) NOT NULL,
    short_description character varying(30),
    description character varying(60),
    text_format character varying(130),
    def_dest_branch character(12) NOT NULL,
    queue_catg character(3) NOT NULL,
    queue_type character(4) NOT NULL,
    read_strt_auth_level smallint NOT NULL,
    read_end_auth_level smallint NOT NULL,
    upd_strt_auth_level smallint NOT NULL,
    upd_end_auth_level smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.queue_codes OWNER TO postgres;

--
-- Name: queues; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE queues (
    queue_id integer NOT NULL,
    create_time character(19) NOT NULL,
    queue_code character(5) NOT NULL,
    prty_code character(1) NOT NULL,
    queue_grp_id integer NOT NULL,
    recycle_date_time character(19) NOT NULL,
    flight_number character(7),
    flight_date date,
    city_pair integer,
    selling_class character(2),
    book_no integer,
    pax_name character varying(77),
    no_of_seats smallint,
    book_category character(1),
    tty_message_id character varying(12),
    notify_code character(3),
    rqst_code character(4),
    agent_code character varying(10),
    locator character varying(13),
    flgt_numb_dupe character(7),
    flgt_date_dupe date,
    city_prno_dupe integer,
    book_no_dupe integer,
    pass_name_dupe character varying(77),
    queue_text character varying(240),
    dest_branch character(12) NOT NULL,
    processing_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.queues OWNER TO postgres;

--
-- Name: realloc_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE realloc_history (
    realloc_number integer NOT NULL,
    book_no integer,
    old_flight_no character(7) NOT NULL,
    old_flight_date date NOT NULL,
    old_departure_airport character(5) NOT NULL,
    old_arrival_airport character(5) NOT NULL,
    new1_flight_no character(7),
    new1_flight_date date,
    new1_departure_airport character(5),
    new1_arrival_airport character(5),
    new2_flight_no character(7),
    new2_flight_date date,
    new2_departure_airport character(5),
    new2_arrival_airport character(5),
    new3_flight_no character(7),
    new3_flight_date date,
    new3_departure_airport character(5),
    new3_arrival_airport character(5),
    new4_flight_no character(7),
    new4_flight_date date,
    new4_departure_airport character(5),
    new4_arrival_airport character(5),
    new5_flight_no character(7),
    new5_flight_date date,
    new5_departure_airport character(5),
    new5_arrival_airport character(5),
    old_selling_cls character(2),
    new1_selling_cls character(2),
    new2_selling_cls character(2),
    new3_selling_cls character(2),
    new4_selling_cls character(2),
    new5_selling_cls character(2),
    processing_flag character(1),
    reac_user_code character(5),
    reac_dest_id character(8),
    reac_date_time character(19)
);


ALTER TABLE public.realloc_history OWNER TO postgres;

--
-- Name: reallocation_request; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE reallocation_request (
    reallocation_request_id integer NOT NULL,
    request_description character varying(255),
    old_flight_count integer NOT NULL,
    new_flight_count integer NOT NULL,
    pax_retain_flag character(1) DEFAULT 'Y'::bpchar NOT NULL,
    waitlist_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    reallocate_to_cancel character(1) DEFAULT 'N'::bpchar NOT NULL,
    reallocate_to_other character(1) DEFAULT 'N'::bpchar NOT NULL,
    run_as_user_code character(5) NOT NULL,
    run_as_dest character(8) NOT NULL,
    run_as_branch character(12) NOT NULL,
    run_at_timestamp timestamp WITH time zone,
    started_at_timestamp timestamp WITH time zone,
    done_at_timestamp timestamp WITH time zone,
    call_output character varying(1024),
    bookings_bad_connection integer,
    bookings_to_process integer,
    items_to_process integer,
    items_processed integer,
    create_time timestamp WITH time zone NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    reallocate_bad_connections_flag character(1) DEFAULT 'N'::bpchar
);


ALTER TABLE public.reallocation_request OWNER TO postgres;

--
-- Name: reallocation_request_flights; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE reallocation_request_flights (
    reallocation_request_id integer NOT NULL,
    flight_sequence_id integer NOT NULL,
    flight_type character(1) NOT NULL,
    flight_number character(7) NOT NULL,
    city_pair integer,
    new_action_type character(1) DEFAULT 'G'::bpchar NOT NULL,
    new_days_offset integer DEFAULT 0 NOT NULL,
    old_schedule_period_no integer,
    old_perd_sequence_no integer,
    other_departure_airport character(3),
    other_arrival_airport character(3),
    other_departure_time smallint,
    other_arrival_time smallint,
    other_class_code character(2)
);


ALTER TABLE public.reallocation_request_flights OWNER TO postgres;

--
-- Name: reallocation_request_reallocation_request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE reallocation_request_reallocation_request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reallocation_request_reallocation_request_id_seq OWNER TO postgres;

--
-- Name: reallocation_request_reallocation_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE reallocation_request_reallocation_request_id_seq OWNED BY reallocation_request.reallocation_request_id;


--
-- Name: reconcile_reconciliation; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE reconcile_reconciliation (
    flight_number character(7),
    flight_date date,
    city_pair integer,
    selling_class character(2),
    from_status_code character(2),
    to_status_code character(2),
    because_inventory_is integer,
    create_time timestamp WITH time zone DEFAULT now()
);


ALTER TABLE public.reconcile_reconciliation OWNER TO postgres;

--
-- Name: relationship_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE relationship_type (
    relationship_type_id integer NOT NULL,
    description character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.relationship_type OWNER TO postgres;

--
-- Name: release_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE release_log (
    id integer NOT NULL,
    release_major character varying(10) NOT NULL,
    release_minor character varying(10) NOT NULL,
    loaded_date_time timestamp WITH time zone DEFAULT now() NOT NULL,
    release_notes character varying(1024),
    rollback_date_time timestamp WITH time zone
);


ALTER TABLE public.release_log OWNER TO postgres;

--
-- Name: release_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE release_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.release_log_id_seq OWNER TO postgres;

--
-- Name: release_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE release_log_id_seq OWNED BY release_log.id;


--
-- Name: rep_inventry_counts; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE rep_inventry_counts (
    dest_id character(8) NOT NULL,
    rep_type character(3) NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    cabin_code character(2) NOT NULL,
    selling_class character(2) NOT NULL,
    cabin_capacity smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    segm_available smallint NOT NULL,
    segm_booked smallint NOT NULL,
    segm_wlisted smallint NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    overbooking_percnt smallint NOT NULL,
    segment_closed_flag character(1) NOT NULL,
    wl_closed_flag character(1) NOT NULL,
    wl_clear_inhibit_flag character(1) NOT NULL,
    wl_release_party_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.rep_inventry_counts OWNER TO postgres;

--
-- Name: report_address; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE report_address (
    origin_carrier character(3) NOT NULL,
    tty_report_addr character(8) NOT NULL,
    tty_prior_nml character(2),
    tty_prior_spc character(2),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.report_address OWNER TO postgres;

--
-- Name: report_template_xslt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE report_template_xslt (
    report_template_id bigint NOT NULL,
    report_code character varying(30),
    description character varying(255),
    file_path character varying(255),
    seq_no smallint,
    allow_email character(1),
    allow_fax character(1),
    allow_print character(1),
    allow_mail character(1),
    allow_modify_email character(1),
    allow_sms character(1) DEFAULT 'N'::bpchar NOT NULL,
    print_page_header character varying(255) DEFAULT '&w&bPage &p of &P'::character varying NOT NULL,
    print_page_footer character varying(255) DEFAULT ''::character varying NOT NULL,
    print_margin_top numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_bottom numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_left numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_right numeric(5,2) DEFAULT 0.75 NOT NULL,
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.report_template_xslt OWNER TO postgres;

--
-- Name: reserve_reason_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE reserve_reason_ref (
    reserve_reason_rcd character varying(5) NOT NULL,
    description character varying(250) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.reserve_reason_ref OWNER TO postgres;

--
-- Name: response_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE response_data (
    tran_code smallint NOT NULL,
    tran_text character varying(255),
    resp_time_sec double precision NOT NULL,
    crea_user_id character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.response_data OWNER TO postgres;

--
-- Name: restrict_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE restrict_rule (
    table_number integer,
    flight_number character(7),
    departure_airport character(5),
    arrival_airport character(5),
    start_date date,
    end_date date,
    frequency_code character(7),
    traff_restrict character(1),
    exception_rec character(1),
    update_user character(5) DEFAULT 'RVRHA'::bpchar NOT NULL,
    update_group character(8) DEFAULT 'CONSOLE'::bpchar NOT NULL,
    update_time character(19) DEFAULT 'SYSDATETIME'::bpchar NOT NULL
);


ALTER TABLE public.restrict_rule OWNER TO postgres;

--
-- Name: route_surcharge; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE route_surcharge (
    route_surcharge_id bigint NOT NULL,
    surcharge_id bigint NOT NULL,
    route_id bigint NOT NULL,
    surcharge_amount numeric(15,5) NOT NULL,
    surcharge_currency character(3) NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    effective_from_date timestamp WITH time zone,
    effective_to_date timestamp WITH time zone,
    active_flag character(1) NOT NULL,
    inactive_date_time timestamp WITH time zone,
    company_code character(3) NOT NULL,
    pax_desc character(5),
    default_flag character(1),
    exclude_from_zero_fare character(1) DEFAULT 'N'::bpchar,
    exclude_from_non_revenue character(1) DEFAULT 'N'::bpchar,
    exclude_from_net_fare character(1) DEFAULT 'N'::bpchar,
    exclude_from_private_fare character(1) DEFAULT 'N'::bpchar,
    original_route_surcharge_id bigint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.route_surcharge OWNER TO postgres;

--
-- Name: route_surcharge_fare; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE route_surcharge_fare (
    route_surcharge_id bigint NOT NULL,
    fare_id bigint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.route_surcharge_fare OWNER TO postgres;

--
-- Name: routings; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE routings (
    route_id integer NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    route_airport_1 character(5),
    route_airport_2 character(5),
    route_airport_3 character(5),
    route_airport_4 character(5),
    route_airport_5 character(5),
    route_description character varying(255),
    atpco_route_no character(3),
    active_flag character(1) DEFAULT 'A'::bpchar,
    inactive_date_time timestamp WITH time zone,
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.routings OWNER TO postgres;

--
-- Name: routings_route_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE routings_route_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.routings_route_id_seq OWNER TO postgres;

--
-- Name: routings_route_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE routings_route_id_seq OWNED BY routings.route_id;


--
-- Name: rule_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE rule_type_ref (
    rule_type_code character(1) NOT NULL,
    description character varying(80),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.rule_type_ref OWNER TO postgres;

--
-- Name: saccode_messageid; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE saccode_messageid (
    sac_code character varying(20) NOT NULL,
    message_id bigint DEFAULT 0,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.saccode_messageid OWNER TO postgres;

--
-- Name: sales_report; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sales_report (
    branch_code character(12) NOT NULL,
    open_date_time timestamp WITH time zone NOT NULL,
    report_status character(1) NOT NULL,
    authorized_date date,
    scrutiny_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.sales_report OWNER TO postgres;


--
-- Name: schd_chng_action; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE schd_chng_action (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    segm_update_flag character(1) NOT NULL,
    seg_cls_update_flag character(1) NOT NULL,
    action_date date NOT NULL,
    action_type character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.schd_chng_action OWNER TO postgres;

--
-- Name: schd_chng_reject; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE schd_chng_reject (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    reject_type character(2) NOT NULL,
    book_no integer NOT NULL,
    action_type character(1) NOT NULL,
    schedule_period_no smallint NOT NULL,
    processing_flag character(1) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.schd_chng_reject OWNER TO postgres;

--
-- Name: schd_routing; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE schd_routing (
    company_code character(3) NOT NULL,
    receiving_carrier character(3) NOT NULL,
    flight_number character(7),
    start_date date,
    end_date date,
    frequency_code character(7),
    valid_start_date date,
    valid_end_date date,
    ssm_report_addr character(10) NOT NULL,
    ssm_mess_priority character(2) NOT NULL,
    ssm_active_flag character(1) NOT NULL,
    ssm_time_format character(1) NOT NULL,
    trans_ssm_del_days smallint NOT NULL,
    trans_ssm_del_hrs smallint NOT NULL,
    ssm_avs_hold character(1) NOT NULL,
    asm_report_addr character(10) NOT NULL,
    asm_mess_priority character(2) NOT NULL,
    asm_active_flag character(1) NOT NULL,
    asm_time_format character(1) NOT NULL,
    trans_asm_del_days smallint NOT NULL,
    trans_asm_del_hrs smallint NOT NULL,
    asm_avs_hold character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.schd_routing OWNER TO postgres;

--
-- Name: seat_attribute; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_attribute (
    seat_definition_id integer NOT NULL,
    seat_attribute_rcd character varying(5) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.seat_attribute OWNER TO postgres;

--
-- Name: seat_attribute_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_attribute_ref (
    seat_attribute_rcd character varying(5) NOT NULL,
    description character varying(250) NOT NULL,
    description_code character varying(5),
    active_flag character(1),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT seat_attribute_ref_active_flag_check CHECK ((active_flag = ANY (ARRAY['A'::bpchar, 'I'::bpchar])))
);


ALTER TABLE public.seat_attribute_ref OWNER TO postgres;

--
-- Name: seat_attribute_seat_definition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seat_attribute_seat_definition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seat_attribute_seat_definition_id_seq OWNER TO postgres;

--
-- Name: seat_attribute_seat_definition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE seat_attribute_seat_definition_id_seq OWNED BY seat_attribute.seat_definition_id;


--
-- Name: seat_definition; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_definition (
    seat_definition_id integer NOT NULL,
    row_number smallint NOT NULL,
    seat_code character varying(2) NOT NULL,
    seat_map_id integer,
    position_x integer,
    position_y integer,
    default_blocked_flag character(1),
    block_reserve_reason_rcd character varying(5),
    start_selling_time integer,
    stop_selling_time integer,
    next_seat_right_id integer,
    next_seat_left_id integer,
    assignment_priority_number integer,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT seat_definition_default_blocked_flag_check CHECK ((default_blocked_flag = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);


ALTER TABLE public.seat_definition OWNER TO postgres;

--
-- Name: seat_definition_seat_definition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seat_definition_seat_definition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seat_definition_seat_definition_id_seq OWNER TO postgres;

--
-- Name: seat_definition_seat_definition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE seat_definition_seat_definition_id_seq OWNED BY seat_definition.seat_definition_id;


--
-- Name: seat_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_map (
    seat_map_id integer NOT NULL,
    description character varying(250) NOT NULL,
    image_url_path character varying(250) NOT NULL,
    image_width integer NOT NULL,
    image_height integer NOT NULL,
    seat_width integer NOT NULL,
    seat_height integer NOT NULL,
    block_image character varying(250),
    vacant_image character varying(250),
    unavailable_image character varying(250),
    reserve_image character varying(250),
    vertical_layout_flag character(1),
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone,
    CONSTRAINT seat_map_vertical_layout_flag_check CHECK ((vertical_layout_flag = ANY (ARRAY['Y'::bpchar, 'N'::bpchar])))
);


ALTER TABLE public.seat_map OWNER TO postgres;

--
-- Name: seat_map_class; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_map_class (
    seat_map_id integer NOT NULL,
    selling_class character varying(2) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.seat_map_class OWNER TO postgres;

--
-- Name: seat_map_configuration; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_map_configuration (
    seat_map_id integer NOT NULL,
    config_table character varying(5) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.seat_map_configuration OWNER TO postgres;

--
-- Name: seat_map_seat_map_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seat_map_seat_map_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seat_map_seat_map_id_seq OWNER TO postgres;

--
-- Name: seat_map_seat_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE seat_map_seat_map_id_seq OWNED BY seat_map.seat_map_id;


--
-- Name: seat_reconfig_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_reconfig_history (
    seat_reconfig_history_id integer NOT NULL,
    flight_number character(7),
    board_date date,
    departure_airport character(7),
    arrival_airport character(7),
    book_no integer,
    pax_number integer,
    old_seat character varying(20),
    new_seat character varying(20),
    old_seat_map_id integer,
    new_seat_map_id integer,
    invalid_time timestamp WITH time zone,
    invalidated_user character(20),
    create_user character(20),
    create_time timestamp WITH time zone DEFAULT now()
);


ALTER TABLE public.seat_reconfig_history OWNER TO postgres;

--
-- Name: seat_reconfig_history_seat_reconfig_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seat_reconfig_history_seat_reconfig_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seat_reconfig_history_seat_reconfig_history_id_seq OWNER TO postgres;

--
-- Name: seat_reconfig_history_seat_reconfig_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE seat_reconfig_history_seat_reconfig_history_id_seq OWNED BY seat_reconfig_history.seat_reconfig_history_id;


--
-- Name: seat_reservation_setting; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE seat_reservation_setting (
    seat_reservation_setting_id integer NOT NULL,
    departure_airport character varying(5),
    arrival_airport character varying(5),
    flight_number character varying(10),
    start_date date,
    end_date date,
    start_selling_time time WITH time zone,
    stop_selling_time time WITH time zone,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.seat_reservation_setting OWNER TO postgres;

--
-- Name: seat_reservation_setting_seat_reservation_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE seat_reservation_setting_seat_reservation_setting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seat_reservation_setting_seat_reservation_setting_id_seq OWNER TO postgres;

--
-- Name: seat_reservation_setting_seat_reservation_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE seat_reservation_setting_seat_reservation_setting_id_seq OWNED BY seat_reservation_setting.seat_reservation_setting_id;


--
-- Name: sec_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sec_mapping (
    company_code character(3) NOT NULL,
    function_id integer NOT NULL,
    auth_sequence_no smallint NOT NULL,
    function_name character(80),
    condition_code character(2) NOT NULL,
    acss_strt_auth_level smallint NOT NULL,
    acss_end_auth_level smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.sec_mapping OWNER TO postgres;

--
-- Name: secu_func; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE secu_func (
    name character(100)
);


ALTER TABLE public.secu_func OWNER TO postgres;


--
-- Name: security_function; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_function (
    function_id bigint NOT NULL,
    security_function_rcd character varying(10) NOT NULL,
    function_code character varying(100) NOT NULL,
    function_name character varying(240) NOT NULL,
    create_user character(5) NOT NULL,
    create_time date NOT NULL,
    create_group character(8) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8)
);


ALTER TABLE public.security_function OWNER TO postgres;

--
-- Name: security_function_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_function_ref (
    security_function_rcd character varying(10) NOT NULL,
    name character varying(240) NOT NULL,
    create_user character(5) NOT NULL,
    create_time date NOT NULL,
    create_group character(8) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8)
);


ALTER TABLE public.security_function_ref OWNER TO postgres;

--
-- Name: security_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_group (
    security_group_id bigint NOT NULL,
    group_name character(240) NOT NULL,
    create_user character(5) NOT NULL,
    create_time date NOT NULL,
    create_group character(8) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8)
);


ALTER TABLE public.security_group OWNER TO postgres;

--
-- Name: security_group_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_group_history (
    security_group_id bigint NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time timestamp WITH time zone,
    inactivated_destination_id character(8),
    activated_date_time timestamp WITH time zone
);


ALTER TABLE public.security_group_history OWNER TO postgres;

--
-- Name: security_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_mapping (
    security_mapping_id bigint NOT NULL,
    security_mapping_rcd character(5) NOT NULL,
    security_group_id bigint,
    user_code character(5),
    read_flag integer,
    write_flag integer,
    update_flag integer,
    delete_flag integer,
    cancel_flag integer,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8),
    from_code character(10),
    to_code character(10),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.security_mapping OWNER TO postgres;

--
-- Name: security_mapping_dimension; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_mapping_dimension (
    security_mapping_dimension_id bigint NOT NULL,
    code_from character(5) NOT NULL,
    code_to character(5) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.security_mapping_dimension OWNER TO postgres;

--
-- Name: security_mapping_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE security_mapping_ref (
    security_mapping_rcd character(5) NOT NULL,
    name character(240) NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.security_mapping_ref OWNER TO postgres;

--
-- Name: segment_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE segment_status (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    status_type character(1) NOT NULL,
    segm_status_code character(2),
    leg_status_code character(2),
    first_post_flag character(1),
    tty_out_msg_id integer,
    recap_flag character(1),
    prev_avn_value smallint,
    new_avn_value smallint,
    tty_last_out_id integer,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.segment_status OWNER TO postgres;

--
-- Name: segment_status_update_history; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE segment_status_update_history (
    segment_status_update_history_id bigint NOT NULL,
    origin character(5),
    destination character(5),
    flight_number character(7),
    selling_class character(2),
    from_date date NOT NULL,
    until_date date NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.segment_status_update_history OWNER TO postgres;


--
-- Name: selling_class_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE selling_class_mapping (
    parent_code character(3),
    child_code character(3),
    first_child_flag integer,
    company_code character(3) NOT NULL
);


ALTER TABLE public.selling_class_mapping OWNER TO postgres;

--
-- Name: selling_conf; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE selling_conf (
    company_code character(3) NOT NULL,
    selling_class character(3) NOT NULL,
    cabin_code character(2) NOT NULL,
    parent_sell_cls character(3) NOT NULL,
    sell_cls_category character(2) NOT NULL,
    ffp_fact_mult numeric(5,2),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.selling_conf OWNER TO postgres;

--
-- Name: server_mast; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE server_mast (
    server_id character(15) NOT NULL,
    prdx_date_time character(19) NOT NULL,
    lan_type character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.server_mast OWNER TO postgres;

--
-- Name: service_requests; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE service_requests (
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
    update_time timestamp WITH time zone
);


ALTER TABLE public.service_requests OWNER TO postgres;

--
-- Name: slrv_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE slrv_serial_nos (
    sales_revenue_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.slrv_serial_nos OWNER TO postgres;

--
-- Name: slrv_serial_nos_sales_revenue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE slrv_serial_nos_sales_revenue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slrv_serial_nos_sales_revenue_id_seq OWNER TO postgres;

--
-- Name: slrv_serial_nos_sales_revenue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE slrv_serial_nos_sales_revenue_id_seq OWNED BY slrv_serial_nos.sales_revenue_id;


--
-- Name: sms_bulk; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sms_bulk (
    bulk_no integer NOT NULL,
    messagecount integer,
    reason text,
    request1 text,
    request2 text,
    request3 text,
    rqst_date_time timestamp WITH time zone,
    reply1 text,
    reply2 text,
    reply3 text,
    requestuser character(5),
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.sms_bulk OWNER TO postgres;

--
-- Name: sms_bulk_bulk_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sms_bulk_bulk_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sms_bulk_bulk_no_seq OWNER TO postgres;

--
-- Name: sms_bulk_bulk_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sms_bulk_bulk_no_seq OWNED BY sms_bulk.bulk_no;


--
-- Name: sms_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sms_mesgs (
    serial_no integer NOT NULL,
    book_no integer,
    request text,
    reply text,
    create_time timestamp WITH time zone NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.sms_mesgs OWNER TO postgres;

--
-- Name: sms_mesgs_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sms_mesgs_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sms_mesgs_serial_no_seq OWNER TO postgres;

--
-- Name: sms_mesgs_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sms_mesgs_serial_no_seq OWNED BY sms_mesgs.serial_no;


--
-- Name: special_service_request_inventory; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE special_service_request_inventory (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    book_no integer NOT NULL,
    rqst_code character(4) NOT NULL,
    usage_count integer NOT NULL,
    activated_user_code character(8),
    activated_dest_id character(8),
    activated_date_time character(19),
    inactivated_user_code character(8),
    inactivated_dest_id character(8),
    inactivated_date_time character(19),
    pax_name character varying(53) NOT NULL
);


ALTER TABLE public.special_service_request_inventory OWNER TO postgres;

--
-- Name: special_service_request_rules; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE special_service_request_rules (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    rqst_code character(4) NOT NULL,
    limit_number integer NOT NULL,
    default_price bigint NOT NULL,
    active_flag integer NOT NULL,
    flight_to_date date NOT NULL,
    currency_code character(3),
    ssr_type_rule character(1) DEFAULT 'N'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.special_service_request_rules OWNER TO postgres;

--
-- Name: ssd_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_config (
    name character varying(20),
    value character varying(128)
);


ALTER TABLE public.ssd_config OWNER TO postgres;

--
-- Name: ssd_t1; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t1 (
    col1 integer,
    col2 integer,
    col3 character(1),
    col4 integer,
    col5 integer,
    col6 integer,
    col7 character varying(128),
    col8 character varying(128),
    col9 smallint,
    col10 smallint,
    col11 smallint,
    col12 character varying(128)
);


ALTER TABLE public.ssd_t1 OWNER TO postgres;

--
-- Name: ssd_t2; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t2 (
    col1 integer,
    col2 integer,
    col3 smallint
);


ALTER TABLE public.ssd_t2 OWNER TO postgres;

--
-- Name: ssd_t3; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t3 (
    col1 integer NOT NULL,
    col2 character varying(128),
    col3 character varying(128),
    col4 character(1),
    col9 text,
    col8 character varying(128)
);


ALTER TABLE public.ssd_t3 OWNER TO postgres;

--
-- Name: ssd_t3_col1_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_t3_col1_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_t3_col1_seq OWNER TO postgres;

--
-- Name: ssd_t3_col1_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_t3_col1_seq OWNED BY ssd_t3.col1;


--
-- Name: ssd_t4; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t4 (
    col1 integer NOT NULL,
    col2 character varying(128) NOT NULL,
    col3 character varying(128),
    col4 character(1),
    col5 smallint
);


ALTER TABLE public.ssd_t4 OWNER TO postgres;

--
-- Name: ssd_t4_col1_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_t4_col1_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_t4_col1_seq OWNER TO postgres;

--
-- Name: ssd_t4_col1_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_t4_col1_seq OWNED BY ssd_t4.col1;


--
-- Name: ssd_t5; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t5 (
    col1 integer,
    col2 integer,
    col3 character varying(128),
    col4 character(1),
    col5 character(1),
    col6 text,
    col8 character varying(255),
    col7 smallint
);


ALTER TABLE public.ssd_t5 OWNER TO postgres;

--
-- Name: ssd_t6; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t6 (
    col1 integer NOT NULL,
    col2 integer,
    col3 character varying(128),
    col4 character varying(128),
    col5 character varying(128),
    col6 character varying(128),
    col7 character varying(128)
);


ALTER TABLE public.ssd_t6 OWNER TO postgres;

--
-- Name: ssd_t6_col1_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_t6_col1_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_t6_col1_seq OWNER TO postgres;

--
-- Name: ssd_t6_col1_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_t6_col1_seq OWNED BY ssd_t6.col1;


--
-- Name: ssd_t7; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_t7 (
    col1 integer NOT NULL,
    col2 integer,
    col3 integer,
    col4 character varying(128),
    col5 character varying(128),
    col6 character varying(128),
    col7 character varying(128),
    col8 character varying(128),
    col9 character varying(128)
);


ALTER TABLE public.ssd_t7 OWNER TO postgres;

--
-- Name: ssd_t7_col1_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_t7_col1_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_t7_col1_seq OWNER TO postgres;

--
-- Name: ssd_t7_col1_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_t7_col1_seq OWNED BY ssd_t7.col1;


--
-- Name: ssd_vcobjects; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_vcobjects (
    vc_objid integer NOT NULL,
    obj_name character varying(128),
    obj_owner character varying(128),
    obj_type character(1),
    database character varying(128),
    parm_list text,
    status integer,
    locked_by character varying(128),
    locked_when timestamp WITH time zone,
    last_revision_no integer,
    revision_count integer
);


ALTER TABLE public.ssd_vcobjects OWNER TO postgres;

--
-- Name: ssd_vcobjects_vc_objid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_vcobjects_vc_objid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_vcobjects_vc_objid_seq OWNER TO postgres;

--
-- Name: ssd_vcobjects_vc_objid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_vcobjects_vc_objid_seq OWNED BY ssd_vcobjects.vc_objid;


--
-- Name: ssd_vcversions; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssd_vcversions (
    rev_id integer NOT NULL,
    vc_objid integer,
    revision_no integer,
    project_ver_no character varying(20),
    revision_comment character varying(255),
    created_when timestamp WITH time zone,
    created_by character varying(128),
    by_operation character varying(10),
    line text
);


ALTER TABLE public.ssd_vcversions OWNER TO postgres;

--
-- Name: ssd_vcversions_rev_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ssd_vcversions_rev_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ssd_vcversions_rev_id_seq OWNER TO postgres;

--
-- Name: ssd_vcversions_rev_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ssd_vcversions_rev_id_seq OWNED BY ssd_vcversions.rev_id;


--
-- Name: ssm_tmp_acft_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_acft_config (
    config_table character(5) NOT NULL,
    company_code character(3) NOT NULL,
    selling_class character(2) NOT NULL,
    aircraft_code character(3) NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    gen_flag_invt character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time character(19) NOT NULL
);


ALTER TABLE public.ssm_tmp_acft_config OWNER TO postgres;

--
-- Name: ssm_tmp_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_cls (
    config_number character(5),
    hierarchy character(4)
);


ALTER TABLE public.ssm_tmp_cls OWNER TO postgres;

--
-- Name: ssm_tmp_date; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_date (
    flight_date integer
);


ALTER TABLE public.ssm_tmp_date OWNER TO postgres;

--
-- Name: ssm_tmp_hirarchy_avail_counts; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_hirarchy_avail_counts (
    selling_class character(2) NOT NULL,
    nett_availb_seats smallint NOT NULL
);


ALTER TABLE public.ssm_tmp_hirarchy_avail_counts OWNER TO postgres;

--
-- Name: ssm_tmp_old_flight_perd_legs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_old_flight_perd_legs (
    aircraft_code character(3) NOT NULL,
    selling_class character(2) NOT NULL,
    seat_capacity smallint NOT NULL,
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time smallint NOT NULL,
    arrival_time smallint NOT NULL,
    date_change_ind smallint NOT NULL,
    config_table character(5) NOT NULL,
    flight_path_code character(1) NOT NULL,
    departure_terminal character(2) NOT NULL,
    arrival_terminal character(2) NOT NULL,
    leg_number smallint NOT NULL,
    table_selector smallint NOT NULL,
    update_time character(19) NOT NULL
);


ALTER TABLE public.ssm_tmp_old_flight_perd_legs OWNER TO postgres;

--
-- Name: ssm_tmp_old_inventry_segment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_old_inventry_segment (
    aircraft_code character(3) NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
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
    table_selector smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time character(19) NOT NULL
);


ALTER TABLE public.ssm_tmp_old_inventry_segment OWNER TO postgres;

--
-- Name: ssm_tmp_parent_sell_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_parent_sell_cls (
    parent_sell_cls character(2)
);


ALTER TABLE public.ssm_tmp_parent_sell_cls OWNER TO postgres;

--
-- Name: ssm_tmp_wl_invt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ssm_tmp_wl_invt (
    flight_date date,
    city_pair integer,
    selling_class character(2),
    no_of_seats smallint,
    wl_seg_flag character(1)
);


ALTER TABLE public.ssm_tmp_wl_invt OWNER TO postgres;

--
-- Name: state; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE state (
    state_code character(2) NOT NULL,
    state_name character varying(60),
    nation_code character(2) NOT NULL,
    summer_start_date date NOT NULL,
    winter_start_date date NOT NULL,
    summer_diff_mins smallint NOT NULL,
    winter_diff_mins smallint NOT NULL,
    update_user character(16) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.state OWNER TO postgres;

--
-- Name: std_comment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE std_comment (
    comment_number smallint NOT NULL,
    comment_text character varying(255),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.std_comment OWNER TO postgres;

--
-- Name: sub_fare_seg_rule; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sub_fare_seg_rule (
    company_code character(3) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    city_pair integer NOT NULL,
    sub_fare_basis_code character(5) NOT NULL,
    fare_rule_no character(8) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    export_timestamp timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.sub_fare_seg_rule OWNER TO postgres;

--
-- Name: sub_fare_segm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE sub_fare_segm (
    company_code character(3) NOT NULL,
    fare_basis_code character(15) NOT NULL,
    city_pair integer NOT NULL,
    pax_code character(5) NOT NULL,
    sub_fare_basis_code character(5) NOT NULL,
    change_type character(1) NOT NULL,
    change_amount numeric(15,5) NOT NULL,
    active_flag character(1) DEFAULT 'A'::bpchar NOT NULL,
    export_timestamp timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.sub_fare_segm OWNER TO postgres;

--
-- Name: surcharge; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE surcharge (
    surcharge_id bigint NOT NULL,
    surcharge_code character(10) NOT NULL,
    description character varying(200),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.surcharge OWNER TO postgres;


--
-- Name: system_errors; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_errors (
    lang_code character(3) NOT NULL,
    error_code integer NOT NULL,
    message character(80) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_errors OWNER TO postgres;

--
-- Name: system_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_log (
    log_id integer NOT NULL,
    create_time character(19) NOT NULL,
    recycle_date_time character(19) NOT NULL,
    process_name character varying(25) NOT NULL,
    flight_number character(7),
    flight_date date,
    city_pair integer,
    selling_class character(2),
    book_no integer,
    pax_name character varying(77),
    no_of_seats smallint,
    book_category character(1),
    tty_message_id character varying(12),
    notify_code character(3),
    rqst_code character(4),
    agent_code character varying(10),
    log_text character varying(240),
    dest_branch character(12) NOT NULL,
    processing_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_log OWNER TO postgres;

--
-- Name: system_param; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_param (
    company_code character(3) NOT NULL,
    branch_code character(12),
    console_dest_id character(8) NOT NULL,
    local_crypt_key character(10),
    client_expiry_days smallint NOT NULL,
    last_ticket_end_no integer NOT NULL,
    book_time_limit smallint NOT NULL,
    book_days_limit smallint NOT NULL,
    avl_display_digits smallint NOT NULL,
    avl_forw_scan_days smallint NOT NULL,
    default_depr_time smallint NOT NULL,
    max_journey_hrs smallint NOT NULL,
    max_stopovr_hrs smallint NOT NULL,
    no_of_days_forw smallint NOT NULL,
    no_of_days_back smallint NOT NULL,
    no_of_flights smallint NOT NULL,
    no_of_flts_back smallint NOT NULL,
    max_no_of_stops smallint NOT NULL,
    max_no_of_conns smallint NOT NULL,
    aa_conn_mins smallint NOT NULL,
    tt_conn_mins smallint NOT NULL,
    st_conn_mins smallint NOT NULL,
    baggage_alownce character varying(105) NOT NULL,
    default_group_size smallint NOT NULL,
    wl_clear_inhibit_mins smallint NOT NULL,
    wl_close_percnt smallint NOT NULL,
    wait_lst_ctrl_flag character(1) NOT NULL,
    perd_range_mnths smallint NOT NULL,
    add_to_current_dt smallint NOT NULL,
    rec_locator_len smallint NOT NULL,
    passwd_expiry_days smallint NOT NULL,
    que_recycle_days smallint NOT NULL,
    que_recycle_mins smallint NOT NULL,
    flight_purge_days smallint NOT NULL,
    book_purge_days smallint NOT NULL,
    pnl_incl_class character(1),
    typb_msg_size smallint,
    flight_purge_hrs smallint NOT NULL,
    tti_ret_hrs smallint NOT NULL,
    tto_ret_hrs smallint NOT NULL,
    tti_purge_hrs smallint NOT NULL,
    tto_purge_hrs smallint NOT NULL,
    dupe_check_hrs smallint NOT NULL,
    group_check_hrs smallint NOT NULL,
    payment_reqd_hrs smallint NOT NULL,
    rcfm_check_hrs smallint NOT NULL,
    tlt_check_hrs smallint NOT NULL,
    rcfm_perd_hrs smallint NOT NULL,
    dupe_intntnl_days smallint NOT NULL,
    dupe_domstic_days smallint NOT NULL,
    crc_branch character(12) NOT NULL,
    tlt_canx_flag character(2) NOT NULL,
    grp_canx_flag character(2) NOT NULL,
    rcfm_canx_flag character(1) NOT NULL,
    dupe_range_days smallint NOT NULL,
    flt_rec_flt_rng smallint NOT NULL,
    flt_rec_dte_rng smallint NOT NULL,
    tmch_int_befr_mins smallint NOT NULL,
    tmch_int_aftr_mins smallint NOT NULL,
    tmch_dom_befr_mins smallint NOT NULL,
    tmch_dom_aftr_mins smallint NOT NULL,
    utr_recycle_days smallint NOT NULL,
    utr_recycle_mins smallint NOT NULL,
    lmtc_recycle_days smallint NOT NULL,
    lmtc_recycle_mins smallint NOT NULL,
    super_auth_level smallint NOT NULL,
    ctrl_auth_level smallint NOT NULL,
    tty_strt_auth_level smallint NOT NULL,
    tty_end_auth_level smallint NOT NULL,
    system_auth_level smallint NOT NULL,
    chkin_auth_level smallint,
    gate_auth_level smallint,
    mngr_auth_level smallint,
    stnsup_auth_level smallint,
    flifo_auth_level smallint,
    avn_trigger_level smallint NOT NULL,
    last_maint_date date NOT NULL,
    no_of_clients smallint NOT NULL,
    fetch_retries smallint NOT NULL,
    lock_wait_secs smallint NOT NULL,
    global_resp_status character(1) NOT NULL,
    process_type character(5) NOT NULL,
    local_time_zone character varying(50),
    queue_purge_days smallint,
    et_rej_actn_flag character(1),
    et_process_time interval hour to second,
    wl_default_cap smallint NOT NULL,
    q_cancel_flag character(1),
    routing_indicator character(1),
    appdir character(40),
    pta_action_queue character(5),
    pta_review_queue character(5),
    pta_review_period smallint,
    pta_retn_period smallint,
    pta_review_text character(80),
    rv_ticketing character(1) DEFAULT 'N'::bpchar NOT NULL,
    tat_retn_period smallint DEFAULT 5,
    optat_retn_period smallint DEFAULT 5,
    ab2_retn_period smallint DEFAULT 5,
    opab2_retn_period smallint DEFAULT 5,
    rqr_retry_hrs smallint,
    rqr_queue_cnt smallint,
    rqr_serv_hrs smallint,
    rqr_servque_cnt smallint,
    rlr_retry_hrs smallint,
    rlr_queue_cnt smallint,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_param OWNER TO postgres;

--
-- Name: system_setting; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_setting (
    system_setting_code character varying(20) NOT NULL,
    description character varying(250),
    system_setting_value character varying(250),
    system_setting_category_rcd character varying(5),
    company_code character varying(3),
    update_user character(16),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_setting OWNER TO postgres;

--
-- Name: system_setting_category_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_setting_category_ref (
    system_setting_category_rcd character varying(5) NOT NULL,
    description character varying(250) NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_setting_category_ref OWNER TO postgres;

--
-- Name: system_stock; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_stock (
    stock_number integer NOT NULL,
    stock_ctl_no_from character(10) NOT NULL,
    stock_ctl_no_to character(10) NOT NULL,
    ticket_type character(5) NOT NULL,
    stock_type character(1) NOT NULL,
    no_of_coupons smallint NOT NULL,
    stock_status character(1) NOT NULL,
    branch_code character(12),
    printer_dest_id character(8),
    printer_status character(1),
    next_ticket_no character(10) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_stock OWNER TO postgres;

--
-- Name: system_tables; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE system_tables (
    table_name character(18) NOT NULL,
    description character varying(160),
    prdx_table_name character(8),
    no_of_keys smallint NOT NULL,
    location_flag character(1) NOT NULL,
    updt_priority smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.system_tables OWNER TO postgres;

--
-- Name: tax_appl_code; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_appl_code (
    apply_code character(1) NOT NULL,
    apply_descr character varying(50),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_appl_code OWNER TO postgres;

--
-- Name: tax_category; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_category (
    tax_cat_id integer NOT NULL,
    company_code character(3) NOT NULL,
    tax_code character(5) NOT NULL,
    coverage_type character(1),
    short_description character varying(30),
    description character varying(255),
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    oneway_cap_amount numeric(15,5) NOT NULL,
    return_cap_amount numeric(15,5) NOT NULL,
    cap_currency character(3) NOT NULL,
    calc_seq smallint NOT NULL,
    compound_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    active_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    incl_in_availab character(1),
    apply_to_zero_fare character(3),
    oneway_cap_count integer,
    return_cap_count integer,
    apply_to_non_revenue character(1),
    apply_to_vias character(1) DEFAULT 'N'::bpchar NOT NULL,
    effective_from_date timestamp WITH time zone,
    effective_to_date timestamp WITH time zone,
    apply_to_net_fare character(1) DEFAULT 'Y'::bpchar NOT NULL,
    apply_to_private_fare character(1) DEFAULT 'Y'::bpchar NOT NULL,
    international_flag character(1) DEFAULT 'D'::bpchar NOT NULL,
    apply_for_origin_airport character(1) DEFAULT 'N'::bpchar NOT NULL,
    apply_for_book_origin character(1) DEFAULT 'N'::bpchar NOT NULL,
    apply_for_agency_location character(1) DEFAULT 'N'::bpchar NOT NULL,
    vat_percent numeric(6,3),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_category OWNER TO postgres;

--
-- Name: tax_category_tax_cat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tax_category_tax_cat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tax_category_tax_cat_id_seq OWNER TO postgres;

--
-- Name: tax_category_tax_cat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tax_category_tax_cat_id_seq OWNED BY tax_category.tax_cat_id;


--
-- Name: tax_coverage_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_coverage_type (
    coverage_type character(1) NOT NULL,
    coverage_descr character varying(50),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_coverage_type OWNER TO postgres;

--
-- Name: tax_detail; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_detail (
    tax_detail_id integer NOT NULL,
    tax_cat_id integer NOT NULL,
    default_flag character(1),
    pax_code character(5),
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    tax_type character(1) NOT NULL,
    tax_amount numeric(15,5) NOT NULL,
    tax_currency character(3),
    airport_code character varying(5),
    state_code character varying(5),
    nation_code character varying(5),
    calc_seq smallint NOT NULL,
    active_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL,
    tax_appliance character(1),
    effective_from_date timestamp WITH time zone,
    effective_to_date timestamp WITH time zone
);


ALTER TABLE public.tax_detail OWNER TO postgres;

--
-- Name: tax_detail_currency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_detail_currency (
    tax_detail_currency_id integer NOT NULL,
    tax_detail_id integer NOT NULL,
    tax_amount numeric(15,5) NOT NULL,
    tax_currency character(3) NOT NULL,
    active_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_detail_currency OWNER TO postgres;

--
-- Name: tax_detail_currency_tax_detail_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tax_detail_currency_tax_detail_currency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tax_detail_currency_tax_detail_currency_id_seq OWNER TO postgres;

--
-- Name: tax_detail_currency_tax_detail_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tax_detail_currency_tax_detail_currency_id_seq OWNED BY tax_detail_currency.tax_detail_currency_id;


--
-- Name: tax_detail_exclude; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_detail_exclude (
    tax_detail_exclude_id integer NOT NULL,
    tax_detail_id integer NOT NULL,
    airport_code character varying(5),
    state_code character varying(5),
    nation_code character varying(5),
    allow_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_detail_exclude OWNER TO postgres;

--
-- Name: tax_detail_exclude_tax_detail_exclude_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tax_detail_exclude_tax_detail_exclude_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tax_detail_exclude_tax_detail_exclude_id_seq OWNER TO postgres;

--
-- Name: tax_detail_exclude_tax_detail_exclude_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tax_detail_exclude_tax_detail_exclude_id_seq OWNED BY tax_detail_exclude.tax_detail_exclude_id;


--
-- Name: tax_detail_tax_detail_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tax_detail_tax_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tax_detail_tax_detail_id_seq OWNER TO postgres;

--
-- Name: tax_detail_tax_detail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tax_detail_tax_detail_id_seq OWNED BY tax_detail.tax_detail_id;


--
-- Name: tax_type_descr; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tax_type_descr (
    tax_type_code character(1) NOT NULL,
    tax_type_descr character varying(50),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.tax_type_descr OWNER TO postgres;

--
-- Name: taxes; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE taxes (
    company_code character(3) NOT NULL,
    tax_code character(5) NOT NULL,
    pax_code character(5) NOT NULL,
    valid_from_date date NOT NULL,
    valid_to_date date NOT NULL,
    short_description character varying(30),
    description character varying(255),
    tax_type character(1) NOT NULL,
    tax_amount numeric(15,5) NOT NULL,
    tax_currency character(3) NOT NULL,
    departure_airport character(5),
    state_code character(2),
    nation_code character(2),
    tax_category character(1) NOT NULL,
    tax_sequence smallint NOT NULL,
    misc_charge_code character(10),
    scrutiny_flag character(1) NOT NULL,
    tax_serial integer NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.taxes OWNER TO postgres;

--
-- Name: taxes_tax_serial_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE taxes_tax_serial_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taxes_tax_serial_seq OWNER TO postgres;

--
-- Name: taxes_tax_serial_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE taxes_tax_serial_seq OWNED BY taxes.tax_serial;


--
-- Name: ticket_layout; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ticket_layout (
    ticket_layout_code character(5) NOT NULL,
    ticket_format character(1) NOT NULL,
    uom_code character(3) NOT NULL,
    xyorigin_coord character(12) NOT NULL,
    xyendorse_start character(12) NOT NULL,
    xyendorse_end character(12) NOT NULL,
    xyorg_dest character(12) NOT NULL,
    xyairline_data character(12) NOT NULL,
    xytour_code character(12) NOT NULL,
    xyissue_exch_for character(12) NOT NULL,
    xypax_name character(12) NOT NULL,
    xyconjunction character(12) NOT NULL,
    xystopover character(12) NOT NULL,
    xyfrom_to character(12) NOT NULL,
    xycarrier character(12) NOT NULL,
    xyflight_number character(12) NOT NULL,
    xyselling_cls character(12) NOT NULL,
    xyflight_date character(12) NOT NULL,
    xyflight_time character(12) NOT NULL,
    xyreserve_status character(12) NOT NULL,
    xyfare_basis_code character(12) NOT NULL,
    xyvalid_before character(12) NOT NULL,
    xyvalid_after character(12) NOT NULL,
    xybagg_allow character(12) NOT NULL,
    xyline_space character(12) NOT NULL,
    xylast_line_space character(12) NOT NULL,
    xyfare_paid character(12) NOT NULL,
    xyequiv_farepd character(12) NOT NULL,
    xytax1 character(12) NOT NULL,
    xytax2 character(12) NOT NULL,
    xytax3 character(12) NOT NULL,
    xytotal character(12) NOT NULL,
    xyfare_calc_strt character(12) NOT NULL,
    xyfare_calc_end character(12) NOT NULL,
    xyticket_docmno character(12) NOT NULL,
    xyform_of_payment character(12) NOT NULL,
    xyorginal_issue character(12) NOT NULL,
    xyvalid_info_strt character(12) NOT NULL,
    xyvalid_info_end character(12) NOT NULL
);


ALTER TABLE public.ticket_layout OWNER TO postgres;


--
-- Name: temp_fare_route_agency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE temp_fare_route_agency (
    fare_route_id bigint NOT NULL,
    company_code character varying(3) NOT NULL,
    agency_code character varying(10) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.temp_fare_route_agency OWNER TO postgres;

--
-- Name: template_xslt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE template_xslt (
    report_code character varying(30) NOT NULL,
    report_version smallint DEFAULT 1 NOT NULL,
    function_id bigint NOT NULL,
    description character varying(255),
    language_rcd character varying(20) DEFAULT 'English'::character varying NOT NULL,
    xsl_template character varying(31500) NOT NULL,
    template_sequence_no smallint DEFAULT 0 NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL,
    inactivated_user_code character(5),
    inactivated_date_time timestamp WITH time zone,
    print_page_header character varying(255) DEFAULT '&w&bPage &p of &P'::character varying NOT NULL,
    print_page_footer character varying(255) DEFAULT ''::character varying NOT NULL,
    print_margin_top numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_bottom numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_left numeric(5,2) DEFAULT 0.75 NOT NULL,
    print_margin_right numeric(5,2) DEFAULT 0.75 NOT NULL
);


ALTER TABLE public.template_xslt OWNER TO postgres;

--
-- Name: template_xslt_components; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE template_xslt_components (
    function_id bigint NOT NULL,
    report_code character varying(60) NOT NULL,
    report_version smallint DEFAULT 1 NOT NULL,
    xsl_template character varying(31500) NOT NULL,
    template_sequence_no integer NOT NULL,
    inactivated_user_code character(5),
    inactivated_date_time timestamp WITH time zone,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.template_xslt_components OWNER TO postgres;

--
-- Name: template_xslt_components_template_sequence_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE template_xslt_components_template_sequence_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.template_xslt_components_template_sequence_no_seq OWNER TO postgres;

--
-- Name: template_xslt_components_template_sequence_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE template_xslt_components_template_sequence_no_seq OWNED BY template_xslt_components.template_sequence_no;


--
-- Name: terminal; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE terminal (
    airport_code character(5) NOT NULL,
    terminal_no character(2) NOT NULL,
    terminal_name character varying(60),
    dd_conn_mins smallint,
    di_conn_mins smallint,
    id_conn_mins smallint,
    ii_conn_mins smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.terminal OWNER TO postgres;

--
-- Name: test_inventry_segm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_inventry_segm (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
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
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_inventry_segm OWNER TO postgres;

--
-- Name: test_perd_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_perd_cls (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    selling_class character(2) NOT NULL,
    parent_sell_cls character varying(240) NOT NULL,
    display_priority smallint NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_perd_cls OWNER TO postgres;

--
-- Name: test_perd_legs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_perd_legs (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    departure_airport character(5) NOT NULL,
    arrival_airport character(5) NOT NULL,
    departure_time smallint NOT NULL,
    arrival_time smallint NOT NULL,
    date_change_ind smallint NOT NULL,
    config_table character(5) NOT NULL,
    flight_path_code character(1) NOT NULL,
    departure_terminal character(2) NOT NULL,
    arrival_terminal character(2) NOT NULL,
    leg_number smallint NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_perd_legs OWNER TO postgres;

--
-- Name: test_perd_prnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_perd_prnt (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    selling_class character(2) NOT NULL,
    parent_sell_cls character(2) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_perd_prnt OWNER TO postgres;

--
-- Name: test_perd_segm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_perd_segm (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    post_control_flag character(1) NOT NULL,
    aircraft_code character(3) NOT NULL,
    flight_closed_flag character(1) NOT NULL,
    flight_brdng_flag character(1) NOT NULL,
    segment_number character(22) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_perd_segm OWNER TO postgres;

--
-- Name: test_periods; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_periods (
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    invt_end_date date NOT NULL,
    control_branch character(12) NOT NULL,
    invt_control_flag character(1) NOT NULL,
    wait_lst_ctrl_flag character(1) NOT NULL,
    via_cities character varying(135) NOT NULL,
    flgt_sched_status character(1) NOT NULL,
    open_end_flag character(1) NOT NULL,
    scrutiny_flag character(1) NOT NULL,
    gen_flag_invt character(1) NOT NULL,
    authority_level smallint NOT NULL,
    chng_category character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.test_periods OWNER TO postgres;

--
-- Name: test_replication; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE test_replication (
    test_code integer,
    descr character(20)
);


ALTER TABLE public.test_replication OWNER TO postgres;

--
-- Name: text_test; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE text_test (
    serial_no integer NOT NULL,
    sample_text text
);


ALTER TABLE public.text_test OWNER TO postgres;

--
-- Name: text_test_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE text_test_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.text_test_serial_no_seq OWNER TO postgres;

--
-- Name: text_test_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE text_test_serial_no_seq OWNED BY text_test.serial_no;


--
-- Name: ticket_history_event; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ticket_history_event (
    hist_serial_no integer NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ticket_history_event OWNER TO postgres;

--
-- Name: ticket_history_event_hist_serial_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ticket_history_event_hist_serial_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ticket_history_event_hist_serial_no_seq OWNER TO postgres;

--
-- Name: ticket_history_event_hist_serial_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ticket_history_event_hist_serial_no_seq OWNED BY ticket_history_event.hist_serial_no;


--
-- Name: ticket_payment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ticket_payment (
    ticket_no character varying(20) NOT NULL,
    payment_no integer NOT NULL,
    et_serial_no integer DEFAULT 0 NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.ticket_payment OWNER TO postgres;

--
-- Name: ticket_segment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ticket_segment (
    ticket_no character varying(20) NOT NULL,
    segment_type character(3) NOT NULL,
    segment_level smallint DEFAULT 0 NOT NULL,
    segment_sequence_no smallint DEFAULT 0 NOT NULL,
    coupon_sequence_no smallint DEFAULT 0 NOT NULL,
    message_type smallint DEFAULT 0 NOT NULL,
    segment_text character varying(128) NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ticket_segment OWNER TO postgres;

--
-- Name: ticket_stock; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ticket_stock (
    printer_dest_id character(8) NOT NULL,
    printer_type character(5) NOT NULL,
    ticket_layout_code character(5) NOT NULL,
    validtn_code integer NOT NULL,
    validtn_location character varying(40),
    start_number integer,
    end_number integer,
    current_number integer,
    start_number2 integer,
    end_number2 integer,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.ticket_stock OWNER TO postgres;

--
-- Name: tmp_flt_check; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tmp_flt_check (
    dest_id character(8) NOT NULL,
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    flight_date date NOT NULL,
    date_type character(1) NOT NULL,
    processing_flag character(1) NOT NULL
);


ALTER TABLE public.tmp_flt_check OWNER TO postgres;

--
-- Name: tmp_flt_perd_segm; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tmp_flt_perd_segm (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    leg_number smallint NOT NULL
);


ALTER TABLE public.tmp_flt_perd_segm OWNER TO postgres;

--
-- Name: tmp_seg_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tmp_seg_status (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    status_type character(1) NOT NULL,
    segm_status_code character(2),
    leg_status_code character(2),
    first_post_flag character(1),
    tty_out_msg_id integer,
    recap_flag character(1),
    prev_avn_value smallint,
    new_avn_value smallint,
    tty_last_out_id integer,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tmp_seg_status OWNER TO postgres;

--
-- Name: tmp_ser; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tmp_ser (
    ser_no integer NOT NULL,
    create_user character(5) NOT NULL
);


ALTER TABLE public.tmp_ser OWNER TO postgres;

--
-- Name: tmp_ser_ser_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tmp_ser_ser_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tmp_ser_ser_no_seq OWNER TO postgres;

--
-- Name: tmp_ser_ser_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tmp_ser_ser_no_seq OWNED BY tmp_ser.ser_no;


--
-- Name: traff_restrict; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE traff_restrict (
    restrict_code character(1) NOT NULL,
    restrict_text character varying(60),
    avl_display_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.traff_restrict OWNER TO postgres;

--
-- Name: travel_agency; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE travel_agency (
    agency_code character(8) NOT NULL,
    tran_code character(1),
    iata_agency_code character(10),
    office_type character(2),
    entity_type character(1),
    trade_name character(25),
    trade_name_lbl character(3),
    legal_name character(50),
    agency_phone_no character(12),
    agency_address1 character varying(30),
    agency_address2 character varying(30),
    agency_city character(25),
    agency_state character(2),
    agency_zip character(10),
    agency_fax_no character(20),
    email_address character varying(80),
    ftp_address character varying(255),
    mail_name character(25),
    mail_address1 character varying(30),
    mail_address2 character varying(30),
    mail_city character(13),
    mail_state character(2),
    mail_zip character(9),
    application_date character(8),
    inclusion_date character(8),
    prev_agency_code character(8),
    hoa_agency_code character(8),
    host_agency_code character(8),
    mail_flag character(1),
    scrutiny_flag character(1) NOT NULL,
    payment_banned_flag character(1),
    accrediting_entity character(4),
    accreditation_type character(4),
    office_status character(2),
    nation_code character(2),
    time_limit smallint,
    mail_nation_code character(2),
    travel_agency_limit_type_rcd character(5) DEFAULT NULL::bpchar,
    invoice_schedule smallint,
    number_of_days_due smallint,
    agency_group_flag character(1),
    days_before_departure smallint,
    agency_credit_limit integer,
    external_agency_id character varying(255),
    invoice_payment_type character varying(2),
    invoice_payment_form character varying(3),
    invoice_fee bigint,
    markup character varying(15),
    corp_admin character varying(30),
    agency_mobile_no character varying(20),
    agency_vat_number character varying(30),
    agency_registration character varying(30),
    agency_bank_name character varying(30),
    agency_bank_branch character varying(30),
    agency_bank_account character varying(30),
    agency_passwd_expiry smallint,
    agency_branch_code character(12),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.travel_agency OWNER TO postgres;

--
-- Name: travel_agency_internet_special; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE travel_agency_internet_special (
    agency_code character(8) NOT NULL,
    agency_name character(25) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.travel_agency_internet_special OWNER TO postgres;

--
-- Name: travel_agency_limit_type_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE travel_agency_limit_type_ref (
    travel_agency_limit_type_rcd character(5) NOT NULL,
    name character varying(100) NOT NULL,
    active_flag integer NOT NULL,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.travel_agency_limit_type_ref OWNER TO postgres;

--
-- Name: tst_perd_seg_cls; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tst_perd_seg_cls (
    flight_number character(7) NOT NULL,
    schedule_period_no smallint NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    group_seat_level smallint NOT NULL,
    seat_protect_level smallint NOT NULL,
    limit_sale_level smallint NOT NULL,
    overbooking_level smallint NOT NULL,
    posting_level smallint NOT NULL,
    sale_notify_level smallint NOT NULL,
    cancel_notify_level smallint NOT NULL,
    seat_capacity smallint NOT NULL,
    ob_profile_no character(5) NOT NULL,
    segment_closed_flag character(1) NOT NULL,
    wl_closed_flag character(1) NOT NULL,
    wl_clear_inhibit_flag character(1) NOT NULL,
    wl_release_party_flag character(1) NOT NULL,
    meal_code character(7),
    beverage_code character(1),
    inflgt_serv_code character(17),
    segment_number character(22) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tst_perd_seg_cls OWNER TO postgres;

--
-- Name: tst_perd_seg_rstr; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tst_perd_seg_rstr (
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    city_pair integer NOT NULL,
    restrict_type character(1) NOT NULL,
    restrict_key character(25) NOT NULL,
    selling_class character varying(60),
    restrict_value smallint,
    rstr_perd_no smallint NOT NULL,
    gen_flag_rstr character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tst_perd_seg_rstr OWNER TO postgres;

--
-- Name: tty_avsstat_agrmnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_avsstat_agrmnt (
    company_code character(3) NOT NULL,
    receiving_carrier character(3) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    selling_class character(2) NOT NULL,
    agrmnt_code character(2) NOT NULL,
    apply_flag character(1) NOT NULL,
    agrmnt_status_flag character(1) NOT NULL,
    avn_trigger_level smallint NOT NULL,
    report_address character(10) NOT NULL,
    message_code character(4),
    avn_limit_control character(1),
    priority_code character(2),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_avsstat_agrmnt OWNER TO postgres;

--
-- Name: tty_depstat_agrmnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_depstat_agrmnt (
    company_code character(3) NOT NULL,
    receiving_carrier character(3) NOT NULL,
    departure_airport character(5) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    selling_class character(2) NOT NULL,
    agrmnt_code character(2) NOT NULL,
    agrmnt_status_flag character(1) NOT NULL,
    report_address character(10) NOT NULL,
    avn_trigger_level smallint,
    message_code character(4),
    avn_limit_control character(1),
    priority_code character(2),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_depstat_agrmnt OWNER TO postgres;

--
-- Name: tty_flight_agrmnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_flight_agrmnt (
    company_code character(3) NOT NULL,
    origin_carrier character(3) NOT NULL,
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    openend_flag character(1),
    frequency_code character(7) NOT NULL,
    selling_class character(2) NOT NULL,
    agrmnt_code character(2) NOT NULL,
    apply_flag character(1) NOT NULL,
    agrmnt_status_flag character(1) NOT NULL,
    seat_accept_level smallint NOT NULL,
    asr_flag character(1) NOT NULL,
    sell_deadline smallint,
    reporting_type character(1),
    predesignated_city character(5),
    function_designatr character(2),
    predesignate_comp character(3),
    multi_address_flag character(1),
    contact_flag character(1),
    timelimit_flag character(1),
    ticketnumber_flag character(1),
    pos_flag character(1),
    segments_flag character(1),
    ack_pnr character(1),
    grpf_flag character(1),
    rqr_retry_hrs smallint,
    rqr_queue_cnt smallint,
    rqr_serv_hrs smallint,
    rqr_servque_cnt smallint,
    rlr_retry_hrs smallint,
    rlr_queue_cnt smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_flight_agrmnt OWNER TO postgres;

--
-- Name: tty_fltstat_agrmnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_fltstat_agrmnt (
    company_code character(3) NOT NULL,
    receiving_carrier character(3) NOT NULL,
    flight_number character(7) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    frequency_code character(7) NOT NULL,
    selling_class character(2) NOT NULL,
    agrmnt_code character(2) NOT NULL,
    agrmnt_status_flag character(1) NOT NULL,
    report_address character(10) NOT NULL,
    avn_trigger_level smallint,
    message_code character(4),
    avn_limit_control character(1),
    priority_code character(2),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_fltstat_agrmnt OWNER TO postgres;

--
-- Name: tty_in_addrs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_in_addrs (
    tty_in_msg_id integer NOT NULL,
    origin_address character(10) NOT NULL,
    processing_flag character(1) NOT NULL,
    updt_usr_code character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_in_addrs OWNER TO postgres;

--
-- Name: tty_in_hash; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_in_hash (
    tty_in_msg_id integer NOT NULL,
    hash character varying(250) NOT NULL,
    hash_base character varying(250)
);


ALTER TABLE public.tty_in_hash OWNER TO postgres;

--
-- Name: tty_in_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_in_mesgs (
    tty_in_msg_id integer NOT NULL,
    msg_sequence_no smallint NOT NULL,
    message_code character(4) NOT NULL,
    priority_code character(2) NOT NULL,
    origin_address character(10) NOT NULL,
    book_no integer,
    message character varying(250),
    message_length smallint,
    company_code character(3) NOT NULL,
    processing_flag character(1) NOT NULL,
    ignore_until timestamp WITH time zone,
    create_time character(19) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_in_mesgs OWNER TO postgres;

--
-- Name: tty_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_map (
    company_code character(3) NOT NULL,
    city_code character(5) NOT NULL,
    tty_designator character(2) NOT NULL,
    addr_indicator character(1) NOT NULL,
    process_indicator character(1),
    server_name character(20),
    print_queue character(20),
    queue_code character(5),
    dest_branch character(12),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_map OWNER TO postgres;

--
-- Name: tty_out_addrs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_out_addrs (
    tty_out_msg_id integer NOT NULL,
    origin_address character(10) NOT NULL,
    processing_flag character(1) NOT NULL,
    priority_code character(2),
    transmit_date_time character(19),
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_out_addrs OWNER TO postgres;

--
-- Name: tty_out_mesgs; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_out_mesgs (
    tty_out_msg_id integer NOT NULL,
    msg_sequence_no smallint NOT NULL,
    create_time character(19) NOT NULL,
    message_code character(4) NOT NULL,
    origin_address character(10) NOT NULL,
    book_no integer,
    message character varying(250),
    message_length smallint,
    processing_flag character(1) NOT NULL,
    ignore_until timestamp WITH time zone,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_out_mesgs OWNER TO postgres;

--
-- Name: tty_passenger; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_passenger (
    book_no integer NOT NULL,
    pax_no smallint NOT NULL,
    fam_name_no smallint NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_passenger OWNER TO postgres;

--
-- Name: tty_sales_agrmnt; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE tty_sales_agrmnt (
    company_code character(3) NOT NULL,
    origin_carrier character(3) NOT NULL,
    selling_class character(2) NOT NULL,
    origin_selling_class character(2),
    start_date date NOT NULL,
    end_date date NOT NULL,
    openend_flag character(1),
    frequency_code character(7) NOT NULL,
    agrmnt_code character(2) NOT NULL,
    apply_flag character(1) NOT NULL,
    agrmnt_status_flag character(1) NOT NULL,
    seat_accept_level smallint NOT NULL,
    asr_flag character(1) NOT NULL,
    sell_deadline smallint,
    reporting_type character(1),
    predesignated_city character(5),
    function_designatr character(2),
    predesignate_comp character(3),
    multi_address_flag character(1),
    contact_flag character(1),
    timelimit_flag character(1),
    ticketnumber_flag character(1),
    pos_flag character(1),
    segments_flag character(1),
    ack_pnr character(1),
    grpf_flag character(1),
    rqr_retry_hrs smallint,
    rqr_queue_cnt smallint,
    rqr_serv_hrs smallint,
    rqr_servque_cnt smallint,
    rlr_retry_hrs smallint,
    rlr_queue_cnt smallint,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.tty_sales_agrmnt OWNER TO postgres;

--
-- Name: ttyi_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ttyi_serial_nos (
    tty_in_msg_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.ttyi_serial_nos OWNER TO postgres;

--
-- Name: ttyi_serial_nos_tty_in_msg_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ttyi_serial_nos_tty_in_msg_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ttyi_serial_nos_tty_in_msg_id_seq OWNER TO postgres;

--
-- Name: ttyi_serial_nos_tty_in_msg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ttyi_serial_nos_tty_in_msg_id_seq OWNED BY ttyi_serial_nos.tty_in_msg_id;


--
-- Name: ttyo_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE ttyo_serial_nos (
    tty_out_msg_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.ttyo_serial_nos OWNER TO postgres;

--
-- Name: ttyo_serial_nos_tty_out_msg_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE ttyo_serial_nos_tty_out_msg_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ttyo_serial_nos_tty_out_msg_id_seq OWNER TO postgres;

--
-- Name: ttyo_serial_nos_tty_out_msg_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE ttyo_serial_nos_tty_out_msg_id_seq OWNED BY ttyo_serial_nos.tty_out_msg_id;


--
-- Name: unit_of_meas; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE unit_of_meas (
    uom_code character(3) NOT NULL,
    description character varying(60),
    unit_type character(3) NOT NULL,
    factor numeric(5,2) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.unit_of_meas OWNER TO postgres;

--
-- Name: unusable_stock; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE unusable_stock (
    stock_number integer NOT NULL,
    ticket_number character(10) NOT NULL,
    ticket_status character(1) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.unusable_stock OWNER TO postgres;

--
-- Name: user_activity; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_activity (
    user_activity_id bigint NOT NULL,
    user_activity_rcd character(10) NOT NULL,
    user_code character(5) NOT NULL,
    logout_date_time timestamp WITH time zone,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.user_activity OWNER TO postgres;

--
-- Name: user_activity_ref; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_activity_ref (
    user_activity_rcd character(10) NOT NULL,
    description character varying(250) NOT NULL,
    user_code character(5) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.user_activity_ref OWNER TO postgres;

--
-- Name: user_group_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_group_mapping (
    user_group_mapping_id bigint NOT NULL,
    user_code character(5) NOT NULL,
    security_group_id bigint NOT NULL,
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8),
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time date NOT NULL
);


ALTER TABLE public.user_group_mapping OWNER TO postgres;

--
-- Name: user_gui_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_gui_config (
    update_user character(5) NOT NULL,
    function_code character(10) NOT NULL,
    profile_string1 character varying(255),
    profile_string2 character varying(255),
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.user_gui_config OWNER TO postgres;

--
-- Name: update_users; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_names (
    user_code character(5),
    user_name character varying(30),
    password character(8),
    passwd_expry_dt date,
    duty_codes character varying(60),
    branch_codes character varying(200),
    host_signin_ids character varying(38),
    home_phone_no character varying(30),
    buss_phone_no character varying(30),
    address character varying(200),
    addr_city character(25),
    addr_state character(25),
    addr_zip character(15),
    addr_nation character(25),
    emp_id character(12),
    job_title character varying(80),
    sup_user_code character(5),
    lang_code character(3),
    join_date date,
    expiry_date date,
    mail_id smallint,
    account_expired_flag integer DEFAULT 0,
    password_hash character varying(45),
    update_user character(5),
    update_group character(8),
    update_time character(19)
);


ALTER TABLE public.user_names OWNER TO postgres;

--
-- Name: user_security_function_mapping; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_security_function_mapping (
    user_security_function_mapping_id bigint NOT NULL,
    user_code character(5) NOT NULL,
    function_id bigint NOT NULL,
    qualifier character varying(240),
    inactivated_by_user character(5),
    inactivated_date_time date,
    inactivated_destination_id character(8),
    create_user character(5) NOT NULL,
    create_time date NOT NULL,
    create_group character(8) NOT NULL
);


ALTER TABLE public.user_security_function_mapping OWNER TO postgres;

--
-- Name: user_setting; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_setting (
    user_setting_code character varying(20) NOT NULL,
    description character varying(250),
    default_value character varying(250),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.user_setting OWNER TO postgres;

--
-- Name: user_setting_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE user_setting_user (
    user_code character(5) NOT NULL,
    user_setting_code character varying(20) NOT NULL,
    user_setting_value character varying(250),
    update_user character(5),
    update_group character(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.user_setting_user OWNER TO postgres;


--
-- Name: vips; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE vips (
    id integer NOT NULL,
    fname character varying(64) NOT NULL,
    lname character varying(64) NOT NULL,
    title character varying(8) NOT NULL,
    bdate timestamp WITH time zone NOT NULL,
    comment character varying(64),
    last_book_no integer DEFAULT 0,
    create_user character(5) NOT NULL,
    create_time timestamp WITH time zone DEFAULT now(),
    update_user character(5) NOT NULL,
    update_time timestamp WITH time zone DEFAULT now()
);


ALTER TABLE public.vips OWNER TO postgres;

--
-- Name: vips_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE vips_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vips_id_seq OWNER TO postgres;

--
-- Name: vips_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE vips_id_seq OWNED BY vips.id;


--
-- Name: voucher; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher (
    voucher_nr integer NOT NULL,
    voucher_reason character(3) NOT NULL,
    voucher_expiry date NOT NULL,
    voucher_status character(4) NOT NULL,
    book_no integer,
    applied_book_no integer,
    flight_no character varying(7),
    flight_date date,
    recipient_name character(53) NOT NULL,
    recipient_addr1 character varying(30),
    recipient_addr2 character varying(30),
    recipient_city character varying(25),
    recipient_state character(15),
    recipient_zip character(15),
    recipient_countr character varying(25),
    payer_name character(53),
    payer_addr1 character varying(30),
    payer_addr2 character varying(30),
    payer_city character varying(25),
    payer_state character(15),
    payer_zip character(15),
    payer_countr character varying(25),
    cnx_date date,
    payment_method character(2),
    voucher_amount numeric(15,5),
    voucher_curr_code character(3) NOT NULL,
    cc_number character(16),
    cc_expiry character(5),
    voucher_notes character varying(255),
    commision_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    percent_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    voucher_number character varying(12),
    record_locator character varying(60),
    applied_record_locator character varying(60),
    use_fee bigint,
    refundable_flag character(1),
    flight_origin character(3),
    flight_dest character(3),
    agency_code character(8),
    origin_voucher character varying(12),
    client_prfl_no character(15),
    business_pax_id integer,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.voucher OWNER TO postgres;

--
-- Name: voucher_payment; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher_payment (
    voucher_nr integer NOT NULL,
    payment_no integer NOT NULL,
    update_user character varying(5),
    update_group character varying(8),
    update_time timestamp WITH time zone
);


ALTER TABLE public.voucher_payment OWNER TO postgres;

--
-- Name: voucher_reason; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher_reason (
    reason_code character(3) NOT NULL,
    reason_descr character varying(50),
    require_book_no character(1) DEFAULT 'N'::bpchar NOT NULL,
    refundable character(1) DEFAULT 'N'::bpchar NOT NULL,
    require_payment character(1) DEFAULT 'N'::bpchar,
    discard_residual character(1) DEFAULT 'N'::bpchar,
    use_for_modify character(1) DEFAULT 'N'::bpchar,
    fee_on_use character(1) DEFAULT 'N'::bpchar,
    for_fare_only character(1) DEFAULT 'N'::bpchar,
    allow_percentage_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    for_manual_only character(1),
    allow_fixed_flag character(1),
    ref_xcl_only character(1),
    nonref_xcl_only character(1),
    modified_book_ref character(1),
    reprice_flown character(1),
    base_fare_disc character(1),
    fee_on_cancel character(1) DEFAULT 'N'::bpchar,
    name_match_required character(1) DEFAULT 'N'::bpchar,
    expiration_months integer DEFAULT 0,
    expiration_method character(1) DEFAULT 'B'::bpchar,
    for_tax_amount character(1) DEFAULT 'Y'::bpchar,
    for_fee_amount character(1) DEFAULT 'Y'::bpchar,
    for_surcharge_amount character(1) DEFAULT 'Y'::bpchar,
    per_pax_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    per_segment_flag character(1) DEFAULT 'N'::bpchar NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.voucher_reason OWNER TO postgres;

--
-- Name: voucher_reason_class; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher_reason_class (
    company_code character(3) NOT NULL,
    reason_code character(3) NOT NULL,
    class_code character(3) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.voucher_reason_class OWNER TO postgres;

--
-- Name: voucher_reason_fop; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher_reason_fop (
    reason_code character(3) NOT NULL,
    payment_type character(2) NOT NULL,
    payment_form character(3) NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.voucher_reason_fop OWNER TO postgres;

--
-- Name: voucher_serial; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE voucher_serial (
    voucher_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.voucher_serial OWNER TO postgres;

--
-- Name: voucher_serial_voucher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE voucher_serial_voucher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.voucher_serial_voucher_id_seq OWNER TO postgres;

--
-- Name: voucher_serial_voucher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE voucher_serial_voucher_id_seq OWNED BY voucher_serial.voucher_id;


--
-- Name: wait_list_release; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE wait_list_release (
    wait_list_id integer NOT NULL,
    create_time character(19) NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    city_pair integer NOT NULL,
    selling_class character(2) NOT NULL,
    segm_sngl_waitrel smallint NOT NULL,
    segm_group_waitrel smallint NOT NULL,
    segm_nrev_waitrel smallint NOT NULL,
    processing_flag character(1) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.wait_list_release OWNER TO postgres;

--
-- Name: wait_list_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE wait_list_status (
    client_no smallint NOT NULL,
    wl_srno smallint NOT NULL,
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    action_type character(2) NOT NULL,
    queue_party character(1) NOT NULL,
    duty_code_level character(5) NOT NULL,
    auto_process_flag character(1) NOT NULL,
    wait_list_status character(1) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.wait_list_status OWNER TO postgres;

--
-- Name: wait_lst_seg_rel; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE wait_lst_seg_rel (
    flight_number character(7) NOT NULL,
    flight_date date NOT NULL,
    wait_lst_id_start integer NOT NULL,
    wait_lst_id_end integer NOT NULL,
    wait_lst_ctrl_flag character(1) NOT NULL,
    processing_flag character(1) NOT NULL,
    create_time character(19) NOT NULL,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.wait_lst_seg_rel OWNER TO postgres;

--
-- Name: wait_serial_nos; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE wait_serial_nos (
    wait_list_id integer NOT NULL,
    create_user character(5) NOT NULL,
    create_group character(8) NOT NULL,
    create_time character(19) NOT NULL
);


ALTER TABLE public.wait_serial_nos OWNER TO postgres;

--
-- Name: wait_serial_nos_wait_list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE wait_serial_nos_wait_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wait_serial_nos_wait_list_id_seq OWNER TO postgres;

--
-- Name: wait_serial_nos_wait_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE wait_serial_nos_wait_list_id_seq OWNED BY wait_serial_nos.wait_list_id;


--
-- Name: waiver_reason; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE waiver_reason (
    reason_code character(3) NOT NULL,
    reason_descr character varying(50),
    inactive_user_code character(5),
    inactive_date_time timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone NOT NULL
);


ALTER TABLE public.waiver_reason OWNER TO postgres;

--
-- Name: watch_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE watch_list (
    entry_no integer NOT NULL,
    book_no integer NOT NULL,
    source_list character(1) NOT NULL,
    source_no integer NOT NULL,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    middle_name character varying(50),
    email_sent timestamp WITH time zone,
    update_user character(5) NOT NULL,
    update_group character(8) NOT NULL,
    update_time timestamp WITH time zone
);


ALTER TABLE public.watch_list OWNER TO postgres;

--
-- Name: watch_list_entry_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE watch_list_entry_no_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.watch_list_entry_no_seq OWNER TO postgres;

--
-- Name: watch_list_entry_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE watch_list_entry_no_seq OWNED BY watch_list.entry_no;


--
-- Name: agency_fare_modifier_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY agency_fare_modifier ALTER COLUMN agency_fare_modifier_id SET DEFAULT nextval('agency_fare_modifier_agency_fare_modifier_id_seq'::regclass);


--
-- Name: agency_route_fare_modifier_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY agency_route_fare_modifier ALTER COLUMN agency_route_fare_modifier_id SET DEFAULT nextval('agency_route_fare_modifier_agency_route_fare_modifier_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY aig_transaction ALTER COLUMN transaction_id SET DEFAULT nextval('aig_transaction_transaction_id_seq'::regclass);


--
-- Name: airport_device_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY airport_device ALTER COLUMN airport_device_id SET DEFAULT nextval('airport_device_airport_device_id_seq'::regclass);


--
-- Name: airport_device_queue_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY airport_device_queue ALTER COLUMN airport_device_queue_id SET DEFAULT nextval('airport_device_queue_airport_device_queue_id_seq'::regclass);


--
-- Name: airport_workstation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY airport_workstation ALTER COLUMN airport_workstation_id SET DEFAULT nextval('airport_workstation_airport_workstation_id_seq'::regclass);


--
-- Name: allotment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allotment_header ALTER COLUMN allotment_id SET DEFAULT nextval('allotment_header_allotment_id_seq'::regclass);


--
-- Name: action_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY asr_reconcile_history ALTER COLUMN action_id SET DEFAULT nextval('asr_reconcile_history_action_id_seq'::regclass);


--
-- Name: attribute_rule_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY attribute_rule ALTER COLUMN attribute_rule_id SET DEFAULT nextval('attribute_rule_attribute_rule_id_seq'::regclass);


--
-- Name: avs_history_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY avs_history ALTER COLUMN avs_history_id SET DEFAULT nextval('avs_history_avs_history_id_seq'::regclass);


--
-- Name: bbl_transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bbl_transaction ALTER COLUMN bbl_transaction_id SET DEFAULT nextval('bbl_transaction_bbl_transaction_id_seq'::regclass);


--
-- Name: boarding_control_number_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY boarding_control_number ALTER COLUMN boarding_control_number_id SET DEFAULT nextval('boarding_control_number_boarding_control_number_id_seq'::regclass);


--
-- Name: book_additional_data_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_additional_data ALTER COLUMN book_additional_data_id SET DEFAULT nextval('book_additional_data_book_additional_data_id_seq'::regclass);


--
-- Name: book_additional_data_field_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_additional_data_field ALTER COLUMN book_additional_data_field_id SET DEFAULT nextval('book_additional_data_field_book_additional_data_field_id_seq'::regclass);


--
-- Name: book_additional_data_field_value_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_additional_data_field_value ALTER COLUMN book_additional_data_field_value_id SET DEFAULT nextval('book_additional_data_field_va_book_additional_data_field_va_seq'::regclass);


--
-- Name: book_reinstate_log_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_reinstate_log ALTER COLUMN book_reinstate_log_no SET DEFAULT nextval('book_reinstate_log_book_reinstate_log_no_seq'::regclass);


--
-- Name: book_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_serial_nos ALTER COLUMN book_no SET DEFAULT nextval('book_serial_nos_book_no_seq'::regclass);


--
-- Name: book_transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book_transaction ALTER COLUMN book_transaction_id SET DEFAULT nextval('book_transaction_book_transaction_id_seq'::regclass);


--
-- Name: action_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY booking_cleanup_log ALTER COLUMN action_id SET DEFAULT nextval('booking_cleanup_log_action_id_seq'::regclass);


--
-- Name: bulk_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY bulk_sms_zb ALTER COLUMN bulk_no SET DEFAULT nextval('bulk_sms_zb_bulk_no_seq'::regclass);


--
-- Name: business_pax_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY business_pax ALTER COLUMN business_pax_id SET DEFAULT nextval('business_pax_business_pax_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cash_transaction ALTER COLUMN transaction_id SET DEFAULT nextval('cash_transaction_transaction_id_seq'::regclass);


--
-- Name: city_pair; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY city_pairs ALTER COLUMN city_pair SET DEFAULT nextval('city_pair_city_pair_seq'::regclass);


--
-- Name: client_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY client_security ALTER COLUMN client_no SET DEFAULT nextval('client_security_client_no_seq'::regclass);


--
-- Name: client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY client_serial_nos ALTER COLUMN client_id SET DEFAULT nextval('client_serial_nos_client_id_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY counter_sales_in_mesgs ALTER COLUMN serial_no SET DEFAULT nextval('counter_sales_in_mesgs_serial_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY counter_sales_out_mesgs ALTER COLUMN serial_no SET DEFAULT nextval('counter_sales_out_mesgs_serial_no_seq'::regclass);


--
-- Name: cc_tran_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY credit_card_tran_serial ALTER COLUMN cc_tran_no SET DEFAULT nextval('credit_card_tran_serial_cc_tran_no_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY credit_requests ALTER COLUMN id SET DEFAULT nextval('credit_requests_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY credit_settlement ALTER COLUMN id SET DEFAULT nextval('credit_settlement_id_seq'::regclass);

--
-- Name: ka_number; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY denied_cc_adjustments ALTER COLUMN ka_number SET DEFAULT nextval('denied_cc_adjustments_ka_number_seq'::regclass);


--
-- Name: book_serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY end_transaction_book ALTER COLUMN book_serial_no SET DEFAULT nextval('end_transaction_book_book_serial_no_seq'::regclass);


--
-- Name: equipment_change_processing_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY equipment_change_processing_serial ALTER COLUMN equipment_change_processing_id SET DEFAULT nextval('equipment_change_processing_s_equipment_change_processing_i_seq'::regclass);


--
-- Name: equipment_change_seat_reallocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY equipment_change_seat_reallocation ALTER COLUMN equipment_change_seat_reallocation_id SET DEFAULT nextval('equipment_change_seat_realloc_equipment_change_seat_realloc_seq'::regclass);


--
-- Name: et_serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY et_serial_nos ALTER COLUMN et_serial_no SET DEFAULT nextval('et_serial_nos_et_serial_no_seq'::regclass);


--
-- Name: eticket_action_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_action ALTER COLUMN eticket_action_id SET DEFAULT nextval('eticket_action_eticket_action_id_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_in_mesgs ALTER COLUMN serial_no SET DEFAULT nextval('eticket_in_mesgs_serial_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_in_mesgs_old ALTER COLUMN serial_no SET DEFAULT nextval('eticket_in_mesgs_old_serial_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_out_mesgs ALTER COLUMN serial_no SET DEFAULT nextval('eticket_out_mesgs_serial_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_out_mesgs_old ALTER COLUMN serial_no SET DEFAULT nextval('eticket_out_mesgs_old_serial_no_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY eticket_transaction ALTER COLUMN transaction_id SET DEFAULT nextval('eticket_transaction_transaction_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY euroline_transaction ALTER COLUMN transaction_id SET DEFAULT nextval('euroline_transaction_transaction_id_seq'::regclass);


--
-- Name: fare_batch_operation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fare_batch_operation ALTER COLUMN fare_batch_operation_id SET DEFAULT nextval('fare_batch_operation_fare_batch_operation_id_seq'::regclass);


--
-- Name: fare_batch_operation_history_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fare_batch_operation_history ALTER COLUMN fare_batch_operation_history_id SET DEFAULT nextval('fare_batch_operation_history_fare_batch_operation_history_i_seq'::regclass);


--
-- Name: fare_date_period_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY fare_date_period ALTER COLUMN fare_date_period_id SET DEFAULT nextval('fare_date_period_fare_date_period_id_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY financial_transaction_book ALTER COLUMN serial_no SET DEFAULT nextval('financial_transaction_book_serial_no_seq'::regclass);


--
-- Name: flight_date_leg_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY flight_date_leg ALTER COLUMN flight_date_leg_id SET DEFAULT nextval('flight_date_leg_flight_date_leg_id_seq'::regclass);


--
-- Name: flight_seat_reservation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY flight_seat_reservation ALTER COLUMN flight_seat_reservation_id SET DEFAULT nextval('flight_seat_reservation_flight_seat_reservation_id_seq'::regclass);


--
-- Name: flight_seat_reservation_group_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY flight_seat_reservation_group ALTER COLUMN flight_seat_reservation_group_id SET DEFAULT nextval('flight_seat_reservation_group_flight_seat_reservation_group_seq'::regclass);


--
-- Name: floating_def_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY floating_definition ALTER COLUMN floating_def_id SET DEFAULT nextval('floating_definition_floating_def_id_seq'::regclass);


--
-- Name: forced_fare_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY forced_fare ALTER COLUMN forced_fare_id SET DEFAULT nextval('forced_fare_forced_fare_id_seq'::regclass);


--
-- Name: hsbc_transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY hsbc_transaction ALTER COLUMN hsbc_transaction_id SET DEFAULT nextval('hsbc_transaction_hsbc_transaction_id_seq'::regclass);


--
-- Name: transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY inf11_transaction ALTER COLUMN transaction_id SET DEFAULT nextval('inf11_transaction_transaction_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY inventory_history ALTER COLUMN id SET DEFAULT nextval('inventory_history_id_seq'::regclass);


--
-- Name: rule_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY inventry_auto_rules ALTER COLUMN rule_id SET DEFAULT nextval('inventry_auto_rules_rule_id_seq'::regclass);


--
-- Name: detail_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY inventry_auto_rules_details ALTER COLUMN detail_id SET DEFAULT nextval('inventry_auto_rules_details_detail_id_seq'::regclass);


--
-- Name: invoice_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY invoice_serial_nos ALTER COLUMN invoice_no SET DEFAULT nextval('invoice_serial_nos_invoice_no_seq'::regclass);


--
-- Name: k2_transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY k2_transaction ALTER COLUMN k2_transaction_id SET DEFAULT nextval('k2_transaction_k2_transaction_id_seq'::regclass);


--
-- Name: log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY log_serial_nos ALTER COLUMN log_id SET DEFAULT nextval('log_serial_nos_log_id_seq'::regclass);


--
-- Name: payment_form_field_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY payment_form_field ALTER COLUMN payment_form_field_id SET DEFAULT nextval('payment_form_field_payment_form_field_id_seq'::regclass);


--
-- Name: payment_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY payment_serial_nos ALTER COLUMN payment_no SET DEFAULT nextval('payment_serial_nos_payment_no_seq'::regclass);


--
-- Name: payments_reference_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY payments_reference ALTER COLUMN payments_reference_id SET DEFAULT nextval('payments_reference_payments_reference_id_seq'::regclass);


--
-- Name: post_hist_book_fares_paym_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY post_hist_book_fares_paym ALTER COLUMN post_hist_book_fares_paym_id SET DEFAULT nextval('post_hist_book_fares_paym_post_hist_book_fares_paym_id_seq'::regclass);


--
-- Name: post_hist_booking_fare_segments_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY post_hist_booking_fare_segments ALTER COLUMN post_hist_booking_fare_segments_id SET DEFAULT nextval('post_hist_booking_fare_segments_post_hist_booking_fare_segments_id_seq'::regclass);


--
-- Name: prl_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY prl_serial ALTER COLUMN prl_id SET DEFAULT nextval('prl_serial_prl_id_seq'::regclass);


--
-- Name: process_srno; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY process_status ALTER COLUMN process_srno SET DEFAULT nextval('process_status_process_srno_seq'::regclass);


--
-- Name: pta_number; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY pta ALTER COLUMN pta_number SET DEFAULT nextval('pta_pta_number_seq'::regclass);


--
-- Name: queue_grp_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY que_grp_serial_nos ALTER COLUMN queue_grp_id SET DEFAULT nextval('que_grp_serial_nos_queue_grp_id_seq'::regclass);


--
-- Name: queue_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY que_serial_nos ALTER COLUMN queue_id SET DEFAULT nextval('que_serial_nos_queue_id_seq'::regclass);


--
-- Name: reallocation_request_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY reallocation_request ALTER COLUMN reallocation_request_id SET DEFAULT nextval('reallocation_request_reallocation_request_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY release_log ALTER COLUMN id SET DEFAULT nextval('release_log_id_seq'::regclass);


--
-- Name: route_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY routings ALTER COLUMN route_id SET DEFAULT nextval('routings_route_id_seq'::regclass);


--
-- Name: seat_definition_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY seat_attribute ALTER COLUMN seat_definition_id SET DEFAULT nextval('seat_attribute_seat_definition_id_seq'::regclass);


--
-- Name: seat_definition_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY seat_definition ALTER COLUMN seat_definition_id SET DEFAULT nextval('seat_definition_seat_definition_id_seq'::regclass);


--
-- Name: seat_map_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY seat_map ALTER COLUMN seat_map_id SET DEFAULT nextval('seat_map_seat_map_id_seq'::regclass);


--
-- Name: seat_reconfig_history_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY seat_reconfig_history ALTER COLUMN seat_reconfig_history_id SET DEFAULT nextval('seat_reconfig_history_seat_reconfig_history_id_seq'::regclass);


--
-- Name: seat_reservation_setting_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY seat_reservation_setting ALTER COLUMN seat_reservation_setting_id SET DEFAULT nextval('seat_reservation_setting_seat_reservation_setting_id_seq'::regclass);


--
-- Name: sales_revenue_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY slrv_serial_nos ALTER COLUMN sales_revenue_id SET DEFAULT nextval('slrv_serial_nos_sales_revenue_id_seq'::regclass);


--
-- Name: bulk_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sms_bulk ALTER COLUMN bulk_no SET DEFAULT nextval('sms_bulk_bulk_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sms_mesgs ALTER COLUMN serial_no SET DEFAULT nextval('sms_mesgs_serial_no_seq'::regclass);


--
-- Name: col1; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_t3 ALTER COLUMN col1 SET DEFAULT nextval('ssd_t3_col1_seq'::regclass);


--
-- Name: col1; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_t4 ALTER COLUMN col1 SET DEFAULT nextval('ssd_t4_col1_seq'::regclass);


--
-- Name: col1; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_t6 ALTER COLUMN col1 SET DEFAULT nextval('ssd_t6_col1_seq'::regclass);


--
-- Name: col1; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_t7 ALTER COLUMN col1 SET DEFAULT nextval('ssd_t7_col1_seq'::regclass);


--
-- Name: vc_objid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_vcobjects ALTER COLUMN vc_objid SET DEFAULT nextval('ssd_vcobjects_vc_objid_seq'::regclass);


--
-- Name: rev_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ssd_vcversions ALTER COLUMN rev_id SET DEFAULT nextval('ssd_vcversions_rev_id_seq'::regclass);


--
-- Name: tax_cat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tax_category ALTER COLUMN tax_cat_id SET DEFAULT nextval('tax_category_tax_cat_id_seq'::regclass);


--
-- Name: tax_detail_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tax_detail ALTER COLUMN tax_detail_id SET DEFAULT nextval('tax_detail_tax_detail_id_seq'::regclass);


--
-- Name: tax_detail_currency_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tax_detail_currency ALTER COLUMN tax_detail_currency_id SET DEFAULT nextval('tax_detail_currency_tax_detail_currency_id_seq'::regclass);


--
-- Name: tax_detail_exclude_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tax_detail_exclude ALTER COLUMN tax_detail_exclude_id SET DEFAULT nextval('tax_detail_exclude_tax_detail_exclude_id_seq'::regclass);


--
-- Name: tax_serial; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY taxes ALTER COLUMN tax_serial SET DEFAULT nextval('taxes_tax_serial_seq'::regclass);


--
-- Name: template_sequence_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY template_xslt_components ALTER COLUMN template_sequence_no SET DEFAULT nextval('template_xslt_components_template_sequence_no_seq'::regclass);


--
-- Name: serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY text_test ALTER COLUMN serial_no SET DEFAULT nextval('text_test_serial_no_seq'::regclass);


--
-- Name: hist_serial_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ticket_history_event ALTER COLUMN hist_serial_no SET DEFAULT nextval('ticket_history_event_hist_serial_no_seq'::regclass);


--
-- Name: ser_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tmp_ser ALTER COLUMN ser_no SET DEFAULT nextval('tmp_ser_ser_no_seq'::regclass);


--
-- Name: tty_in_msg_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ttyi_serial_nos ALTER COLUMN tty_in_msg_id SET DEFAULT nextval('ttyi_serial_nos_tty_in_msg_id_seq'::regclass);


--
-- Name: tty_out_msg_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY ttyo_serial_nos ALTER COLUMN tty_out_msg_id SET DEFAULT nextval('ttyo_serial_nos_tty_out_msg_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY vips ALTER COLUMN id SET DEFAULT nextval('vips_id_seq'::regclass);


--
-- Name: voucher_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY voucher_serial ALTER COLUMN voucher_id SET DEFAULT nextval('voucher_serial_voucher_id_seq'::regclass);


--
-- Name: wait_list_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY wait_serial_nos ALTER COLUMN wait_list_id SET DEFAULT nextval('wait_serial_nos_wait_list_id_seq'::regclass);


--
-- Name: entry_no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY watch_list ALTER COLUMN entry_no SET DEFAULT nextval('watch_list_entry_no_seq'::regclass);


--
-- Name: agency_book_agency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY agency_book_agency
    ADD CONSTRAINT agency_book_agency_pkey PRIMARY KEY (agency_code, auth_agency_code);


--
-- Name: agency_comm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY agency_comm
    ADD CONSTRAINT agency_comm_pkey PRIMARY KEY (agency_code, commission_type, commission_code);


--
-- Name: agency_hierarchy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY agency_hierarchy
    ADD CONSTRAINT agency_hierarchy_pkey PRIMARY KEY (agency_code);


--
-- Name: agency_office_status_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY agency_office_status_ref
    ADD CONSTRAINT agency_office_status_ref_pkey PRIMARY KEY (agency_office_status_rcd);


--
-- Name: agency_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY agency_user
    ADD CONSTRAINT agency_user_pkey PRIMARY KEY (agency_code, agent_code);


--
-- Name: aig_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY aig_transaction
    ADD CONSTRAINT aig_transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: airport_device_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_device
    ADD CONSTRAINT airport_device_pkey PRIMARY KEY (airport_device_id);


--
-- Name: airport_device_queue_entry_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_device_queue_entry_type_ref
    ADD CONSTRAINT airport_device_queue_entry_type_ref_pkey PRIMARY KEY (airport_device_queue_entry_type_rcd);


--
-- Name: airport_device_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_device_queue
    ADD CONSTRAINT airport_device_queue_pkey PRIMARY KEY (airport_device_queue_id);


--
-- Name: airport_device_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_device_type_ref
    ADD CONSTRAINT airport_device_type_ref_pkey PRIMARY KEY (airport_device_type_rcd);


--
-- Name: airport_workstation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_workstation
    ADD CONSTRAINT airport_workstation_pkey PRIMARY KEY (airport_workstation_id);


--
-- Name: airport_workstation_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY airport_workstation_type_ref
    ADD CONSTRAINT airport_workstation_type_ref_pkey PRIMARY KEY (airport_workstation_type_rcd);


--
-- Name: allotment_detail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY allotment_detail
    ADD CONSTRAINT allotment_detail_pkey PRIMARY KEY (allotment_id, flight_date);


--
-- Name: allotment_header_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY allotment_header
    ADD CONSTRAINT allotment_header_pkey PRIMARY KEY (allotment_id);


--
-- Name: asr_reconcile_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY asr_reconcile_history
    ADD CONSTRAINT asr_reconcile_history_pkey PRIMARY KEY (action_id);


--
-- Name: attribute_rule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY attribute_rule
    ADD CONSTRAINT attribute_rule_pkey PRIMARY KEY (attribute_rule_id);


--
-- Name: avs_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY avs_history
    ADD CONSTRAINT avs_history_pkey PRIMARY KEY (avs_history_id);


--
-- Name: bbl_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY bbl_transaction
    ADD CONSTRAINT bbl_transaction_pkey PRIMARY KEY (bbl_transaction_id);


--
-- Name: blocked_seat_update_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY blocked_seat_update_queue
    ADD CONSTRAINT blocked_seat_update_queue_pkey PRIMARY KEY (seat_map_id, change_date_time);


--
-- Name: boarding_control_number_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY boarding_control_number
    ADD CONSTRAINT boarding_control_number_pkey PRIMARY KEY (boarding_control_number_id);


--
-- Name: book_additional_data_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_additional_data_field
    ADD CONSTRAINT book_additional_data_field_pkey PRIMARY KEY (book_additional_data_field_id);


--
-- Name: book_additional_data_field_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_additional_data_field_value
    ADD CONSTRAINT book_additional_data_field_value_pkey PRIMARY KEY (book_additional_data_field_value_id);


--
-- Name: book_additional_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_additional_data
    ADD CONSTRAINT book_additional_data_pkey PRIMARY KEY (book_additional_data_id);


--
-- Name: book_commission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_commission
    ADD CONSTRAINT book_commission_pkey PRIMARY KEY (book_no, fare_no, pax_code);


--
-- Name: book_crs_index_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_cross_index
    ADD CONSTRAINT book_crs_index_pkey PRIMARY KEY (book_no);


--
-- Name: book_fares_pass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_fares_pass
    ADD CONSTRAINT book_fares_pass_pkey PRIMARY KEY (book_no, pax_code);


--
-- Name: book_fares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_fares
    ADD CONSTRAINT book_fares_pkey PRIMARY KEY (book_no, fare_no, pax_code);


--
-- Name: book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY bookings
    ADD CONSTRAINT bookings_pkey PRIMARY KEY (book_no);


--
-- Name: book_reinstate_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_reinstate_log
    ADD CONSTRAINT book_reinstate_log_pkey PRIMARY KEY (book_reinstate_log_no);


--
-- Name: book_requests_old_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_requests_old
    ADD CONSTRAINT book_requests_old_pkey PRIMARY KEY (book_no, rqst_sequence_no, item_no);


--
-- Name: book_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_requests
    ADD CONSTRAINT book_requests_pkey PRIMARY KEY (book_no, rqst_sequence_no, item_no);


--
-- Name: book_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY book_ticket
    ADD CONSTRAINT book_ticket_pkey PRIMARY KEY (book_no, ticket_sequence_no);


--
-- Name: bsp_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY bsp_transaction
    ADD CONSTRAINT bsp_transaction_pkey PRIMARY KEY (airline_code, tkt_document_no);


--
-- Name: business_pax_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY business_pax_class
    ADD CONSTRAINT business_pax_class_pkey PRIMARY KEY (business_pax_id, selling_class);


--
-- Name: business_pax_fare_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY business_pax_fare
    ADD CONSTRAINT business_pax_fare_pkey PRIMARY KEY (business_pax_id, fare_basis_code);


--
-- Name: business_pax_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY business_pax
    ADD CONSTRAINT business_pax_pkey PRIMARY KEY (business_pax_id);


--
-- Name: cash_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY cash_transaction
    ADD CONSTRAINT cash_transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: change_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY change_type_ref
    ADD CONSTRAINT change_type_ref_pkey PRIMARY KEY (change_type_code);


--
-- Name: char_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY char_mapping
    ADD CONSTRAINT char_mapping_pkey PRIMARY KEY (ext_char);


--
-- Name: client_contact_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY client_contact_details
    ADD CONSTRAINT client_contact_details_pkey PRIMARY KEY (client_prfl_no, contact_type);


--
-- Name: client_pax_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY client_pax_code
    ADD CONSTRAINT client_pax_code_pkey PRIMARY KEY (client_prfl_no, pax_code);


--
-- Name: client_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY client_preferences
    ADD CONSTRAINT client_preferences_pkey PRIMARY KEY (client_prfl_no, attribute_sequence_no);


--
-- Name: client_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY client_request
    ADD CONSTRAINT client_request_pkey PRIMARY KEY (client_prfl_no, pax_code, rqst_code);


--
-- Name: comm_exception_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY comm_exception
    ADD CONSTRAINT comm_exception_pkey PRIMARY KEY (agency_code, flight_path_code, company_code, valid_from_date, commission_seq);


--
-- Name: command_text_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY command_text
    ADD CONSTRAINT command_text_pkey PRIMARY KEY (command_text_code);


--
-- Name: commission_basic_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY commission_basic
    ADD CONSTRAINT commission_basic_pkey PRIMARY KEY (comm_basic_code, flight_path_code, company_code, valid_from_date);


--
-- Name: commission_volum_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY commission_volum
    ADD CONSTRAINT commission_volum_pkey PRIMARY KEY (comm_volum_code, valid_from_date, comm_range_from);


--
-- Name: counter_sales_in_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY counter_sales_in_mesgs
    ADD CONSTRAINT counter_sales_in_mesgs_pkey PRIMARY KEY (serial_no);


--
-- Name: counter_sales_mesg_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY counter_sales_mesg_types
    ADD CONSTRAINT counter_sales_mesg_types_pkey PRIMARY KEY (message_type_id);


--
-- Name: counter_sales_out_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY counter_sales_out_mesgs
    ADD CONSTRAINT counter_sales_out_mesgs_pkey PRIMARY KEY (serial_no);


--
-- Name: credit_card_fraud_number_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY credit_card_fraud_number_ref
    ADD CONSTRAINT credit_card_fraud_number_ref_pkey PRIMARY KEY (credit_card_fraud_number_rcd);


--
-- Name: credit_card_fraud_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY credit_card_fraud
    ADD CONSTRAINT credit_card_fraud_pkey PRIMARY KEY (credit_card_fraud_id);


--
-- Name: credit_card_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY credit_card_message
    ADD CONSTRAINT credit_card_message_pkey PRIMARY KEY (message_code, payment_form);


--
-- Name: credit_requests_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY credit_requests
    ADD CONSTRAINT credit_requests_transaction_id_key UNIQUE (transaction_id);


--
-- Name: credit_settlement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY credit_settlement
    ADD CONSTRAINT credit_settlement_pkey PRIMARY KEY (id);


--
-- Name: crystal_reports_hierarchy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY crystal_reports_hierarchy
    ADD CONSTRAINT crystal_reports_hierarchy_pkey PRIMARY KEY (report_code);


--
-- Name: db_purge_temp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY db_purge_temp
    ADD CONSTRAINT db_purge_temp_pkey PRIMARY KEY (book_no);


--
-- Name: db_purge_track_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY db_purge_track
    ADD CONSTRAINT db_purge_track_pkey PRIMARY KEY (book_no);


--
-- Name: denied_cc_adjustments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY denied_cc_adjustments
    ADD CONSTRAINT denied_cc_adjustments_pkey PRIMARY KEY (ka_number);


--
-- Name: department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY department
    ADD CONSTRAINT department_pkey PRIMARY KEY (department_id);


--
-- Name: device_status_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY device_status_ref
    ADD CONSTRAINT device_status_ref_pkey PRIMARY KEY (device_status_rcd);


--
-- Name: employee_buddy_pass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY employee_buddy_pass
    ADD CONSTRAINT employee_buddy_pass_pkey PRIMARY KEY (employee_id, buddy_pass_no);


--
-- Name: employee_family_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY employee_family
    ADD CONSTRAINT employee_family_pkey PRIMARY KEY (employee_id, relative_client_prfl_no);


--
-- Name: employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employee_id);


--
-- Name: employee_travel_benefit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY employee_travel_benefit
    ADD CONSTRAINT employee_travel_benefit_pkey PRIMARY KEY (employee_id);


--
-- Name: end_transaction_book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY end_transaction_book
    ADD CONSTRAINT end_transaction_book_pkey PRIMARY KEY (book_serial_no);


--
-- Name: equipment_change_processing_serial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY equipment_change_processing_serial
    ADD CONSTRAINT equipment_change_processing_serial_pkey PRIMARY KEY (equipment_change_processing_id);


--
-- Name: equipment_change_seat_reallocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY equipment_change_seat_reallocation
    ADD CONSTRAINT equipment_change_seat_reallocation_pkey PRIMARY KEY (equipment_change_seat_reallocation_id);


--
-- Name: et_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY et_payments
    ADD CONSTRAINT et_payments_pkey PRIMARY KEY (payment_no);


--
-- Name: eticket_in_mesgs_old_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY eticket_in_mesgs_old
    ADD CONSTRAINT eticket_in_mesgs_old_pkey PRIMARY KEY (serial_no);


--
-- Name: eticket_in_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY eticket_in_mesgs
    ADD CONSTRAINT eticket_in_mesgs_pkey PRIMARY KEY (serial_no);


--
-- Name: eticket_out_mesgs_old_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY eticket_out_mesgs_old
    ADD CONSTRAINT eticket_out_mesgs_old_pkey PRIMARY KEY (serial_no);


--
-- Name: eticket_out_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY eticket_out_mesgs
    ADD CONSTRAINT eticket_out_mesgs_pkey PRIMARY KEY (serial_no);


--
-- Name: eticket_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY eticket_transaction
    ADD CONSTRAINT eticket_transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: euroline_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY euroline_transaction
    ADD CONSTRAINT euroline_transaction_pkey PRIMARY KEY (transaction_id);


--
-- Name: fare_agency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_agency
    ADD CONSTRAINT fare_agency_pkey PRIMARY KEY (fare_id, agency_code);


--
-- Name: fare_batch_operation_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_batch_operation_history
    ADD CONSTRAINT fare_batch_operation_history_pkey PRIMARY KEY (fare_batch_operation_id, fare_batch_operation_history_id);


--
-- Name: fare_batch_operation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_batch_operation
    ADD CONSTRAINT fare_batch_operation_pkey PRIMARY KEY (fare_batch_operation_id);


--
-- Name: fare_blackout_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_blackout
    ADD CONSTRAINT fare_blackout_pkey PRIMARY KEY (fare_id, blackout_date);


--
-- Name: fare_branch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_branch
    ADD CONSTRAINT fare_branch_pkey PRIMARY KEY (fare_id, branch_code);


--
-- Name: fare_combinations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_combinations
    ADD CONSTRAINT fare_combinations_pkey PRIMARY KEY (fare_id);


--
-- Name: fare_companion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_companion
    ADD CONSTRAINT fare_companion_pkey PRIMARY KEY (fare_id, pax_desc);


--
-- Name: fare_date_period_dates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_date_period_dates
    ADD CONSTRAINT fare_date_period_dates_pkey PRIMARY KEY (fare_date_period_id, seq_no);


--
-- Name: fare_date_period_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_date_period
    ADD CONSTRAINT fare_date_period_pkey PRIMARY KEY (fare_date_period_id);


--
-- Name: fare_day_time_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_day_time
    ADD CONSTRAINT fare_day_time_pkey PRIMARY KEY (fare_id, tod_sequence);


--
-- Name: fare_endorsements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_endorsements
    ADD CONSTRAINT fare_endorsements_pkey PRIMARY KEY (fare_id, fare_text_type, endorsement_no);


--
-- Name: fare_export_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_export
    ADD CONSTRAINT fare_export_pkey PRIMARY KEY (exp_date_time, exp_destination);


--
-- Name: fare_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare
    ADD CONSTRAINT fare_pkey PRIMARY KEY (fare_id);


--
-- Name: fare_route_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fare_route
    ADD CONSTRAINT fare_route_pkey PRIMARY KEY (fare_route_id);


--
-- Name: fee_branch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee_branch
    ADD CONSTRAINT fee_branch_pkey PRIMARY KEY (fee_id, branch_code);


--
-- Name: fee_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee_class
    ADD CONSTRAINT fee_class_pkey PRIMARY KEY (fee_id, class_code);


--
-- Name: fee_fare_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee_fare
    ADD CONSTRAINT fee_fare_pkey PRIMARY KEY (fee_id, fare_basis_code);


--
-- Name: fee_pax_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee_passenger
    ADD CONSTRAINT fee_pax_pkey PRIMARY KEY (fee_id, pax_code);


--
-- Name: fee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee
    ADD CONSTRAINT fee_pkey PRIMARY KEY (fee_id);


--
-- Name: fee_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY fee_type_ref
    ADD CONSTRAINT fee_type_ref_pkey PRIMARY KEY (fee_type_rcd);


--
-- Name: field_control_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY field_control_type
    ADD CONSTRAINT field_control_type_pkey PRIMARY KEY (field_control_type_rcd);


--
-- Name: financial_transaction_book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY financial_transaction_book
    ADD CONSTRAINT financial_transaction_book_pkey PRIMARY KEY (serial_no);


--
-- Name: flight_date_leg_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_date_leg
    ADD CONSTRAINT flight_date_leg_pkey PRIMARY KEY (flight_date_leg_id);


--
-- Name: flight_hierarchy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_hierarchy
    ADD CONSTRAINT flight_hierarchy_pkey PRIMARY KEY (parent_flight_date_leg_id, child_flight_date_leg_id);


--
-- Name: flight_information_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_information
    ADD CONSTRAINT flight_information_pkey PRIMARY KEY (flight_number, board_date, departure_airport, arrival_airport, seq_no);


--
-- Name: flight_locked_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_locked
    ADD CONSTRAINT flight_locked_pkey PRIMARY KEY (lock_id);


--
-- Name: flight_seat_map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_seat_map
    ADD CONSTRAINT flight_seat_map_pkey PRIMARY KEY (flight_date_leg_id, seat_map_id);


--
-- Name: flight_seat_reservation_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_seat_reservation_group
    ADD CONSTRAINT flight_seat_reservation_group_pkey PRIMARY KEY (flight_seat_reservation_group_id);


--
-- Name: flight_seat_reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_seat_reservation
    ADD CONSTRAINT flight_seat_reservation_pkey PRIMARY KEY (flight_seat_reservation_id);


--
-- Name: flight_segment_overlap_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_segment_overlap
    ADD CONSTRAINT flight_segment_overlap_pkey PRIMARY KEY (flight_date_leg_id, overlap_flight_date_leg_id);


--
-- Name: flight_shared_leg_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY flight_shared_leg
    ADD CONSTRAINT flight_shared_leg_pkey PRIMARY KEY (dup_flight_number, dup_board_date, dup_departure_airport, dup_arrival_airport);


--
-- Name: floating_definition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY floating_definition
    ADD CONSTRAINT floating_definition_pkey PRIMARY KEY (floating_def_id);


--
-- Name: forced_fare_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY forced_fare
    ADD CONSTRAINT forced_fare_pkey PRIMARY KEY (forced_fare_id);


--
-- Name: group_security_function_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY group_security_function_mapping
    ADD CONSTRAINT group_security_function_mapping_pkey PRIMARY KEY (group_security_function_mapping_id);


--
-- Name: hist_coupon_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY hist_coupon
    ADD CONSTRAINT hist_coupon_pkey PRIMARY KEY (ticket_no, coupon_sequence_no, hist_serial_no, update_time);


--
-- Name: hist_currency_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY hist_currency_codes
    ADD CONSTRAINT hist_currency_codes_pkey PRIMARY KEY (currency_code, valid_from_date_time, valid_to_date_time);


--
-- Name: hist_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY hist_ticket
    ADD CONSTRAINT hist_ticket_pkey PRIMARY KEY (ticket_no, hist_serial_no, update_time);


--
-- Name: hsbc_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY hsbc_transaction
    ADD CONSTRAINT hsbc_transaction_pkey PRIMARY KEY (hsbc_transaction_id);


--
-- Name: iline_req_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY iline_req_mesgs
    ADD CONSTRAINT iline_req_mesgs_pkey PRIMARY KEY (message_id);


--
-- Name: iline_resp_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY iline_resp_mesgs
    ADD CONSTRAINT iline_resp_mesgs_pkey PRIMARY KEY (message_id);


--
-- Name: inventory_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY inventory_history
    ADD CONSTRAINT inventory_history_pkey PRIMARY KEY (id);


--
-- Name: inventry_auto_rules_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY inventry_auto_rules_details
    ADD CONSTRAINT inventry_auto_rules_details_pkey PRIMARY KEY (detail_id, rule_id);


--
-- Name: itinerary_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY itineraries
    ADD CONSTRAINT itineraries_pkey PRIMARY KEY (book_no, route_no, alt_itinerary_no, itinerary_no);


--
-- Name: k2_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY k2_transaction
    ADD CONSTRAINT k2_transaction_pkey PRIMARY KEY (k2_transaction_id);


--
-- Name: language_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY language_ref
    ADD CONSTRAINT language_ref_pkey PRIMARY KEY (language_rcd);


--
-- Name: last_operation_status_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY last_operation_status_ref
    ADD CONSTRAINT last_operation_status_ref_pkey PRIMARY KEY (last_operation_status_rcd);



--
-- Name: mco_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY mco_info
    ADD CONSTRAINT mco_info_pkey PRIMARY KEY (mco_number);


--
-- Name: menu_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY menu_item
    ADD CONSTRAINT menu_item_pkey PRIMARY KEY (menu_item_id);


--
-- Name: mvt_delay_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY mvt_delay_code
    ADD CONSTRAINT mvt_delay_code_pkey PRIMARY KEY (delay_code, delay_subcode);


--
-- Name: oledb_tran_test_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY oledb_tran_test
    ADD CONSTRAINT oledb_tran_test_pkey PRIMARY KEY (row_no, context_id);


--
-- Name: origin_address_name_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY origin_address_name
    ADD CONSTRAINT origin_address_name_pkey PRIMARY KEY (origin_address);


--
-- Name: osi_et_text_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY osi_et_text
    ADD CONSTRAINT osi_et_text_pkey PRIMARY KEY (osi_airport, osi_request_code);


--
-- Name: pax_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY pax_contact
    ADD CONSTRAINT pax_contact_pkey PRIMARY KEY (book_no, pax_no);


--
-- Name: pass_itin_ref_det_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY pass_itin_ref_det
    ADD CONSTRAINT pass_itin_ref_det_pkey PRIMARY KEY (prl_id, item_seq);


--
-- Name: pass_itin_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY pass_itin_ref
    ADD CONSTRAINT pass_itin_ref_pkey PRIMARY KEY (prl_id);


--
-- Name: pax_remarks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY pax_remarks
    ADD CONSTRAINT pax_remarks_pkey PRIMARY KEY (book_no, remark_sequence_no);


--
-- Name: pax_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY passengers
    ADD CONSTRAINT pax_pkey PRIMARY KEY (book_no, pax_no);


--
-- Name: payment_amount_limits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_amount_limits
    ADD CONSTRAINT payment_amount_limits_pkey PRIMARY KEY (payment_type, payment_form, currency_code);


--
-- Name: payment_backup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_backup
    ADD CONSTRAINT payment_backup_pkey PRIMARY KEY (payment_no);


--
-- Name: payment_channel_config_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_channel_config
    ADD CONSTRAINT payment_channel_config_pkey PRIMARY KEY (payment_channel_config_id);


--
-- Name: payment_et_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_et_ref
    ADD CONSTRAINT payment_et_ref_pkey PRIMARY KEY (payment_no);


--
-- Name: payment_form_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_form_field
    ADD CONSTRAINT payment_form_field_pkey PRIMARY KEY (payment_form_field_id);


--
-- Name: payment_form_field_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payment_form_field_status
    ADD CONSTRAINT payment_form_field_status_pkey PRIMARY KEY (payment_form_field_id, payment_type, payment_form);


--
-- Name: payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_no);


--
-- Name: payments_uplift_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY payments_uplift
    ADD CONSTRAINT payments_uplift_pkey PRIMARY KEY (file_nr, batch_nr, create_user);


--
-- Name: post_departure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY post_departure
    ADD CONSTRAINT post_departure_pkey PRIMARY KEY (post_departure_id);


--
-- Name: post_hist_book_fares_paym_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY post_hist_book_fares_paym
    ADD CONSTRAINT post_hist_book_fares_paym_pkey PRIMARY KEY (post_hist_book_fares_paym_id);


--
-- Name: post_hist_booking_fare_segments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY post_hist_booking_fare_segments
    ADD CONSTRAINT post_hist_booking_fare_segments_pkey PRIMARY KEY (post_hist_booking_fare_segments_id);


--
-- Name: prl_serial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY prl_serial
    ADD CONSTRAINT prl_serial_pkey PRIMARY KEY (prl_id);


--
-- Name: processing_indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY processing_indicators
    ADD CONSTRAINT processing_indicators_pkey PRIMARY KEY (recorded_date);


--
-- Name: queues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY queues
    ADD CONSTRAINT queues_pkey PRIMARY KEY (queue_id);


--
-- Name: relationship_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY relationship_type
    ADD CONSTRAINT relationship_type_pkey PRIMARY KEY (relationship_type_id);


--
-- Name: report_template_xslt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY report_template_xslt
    ADD CONSTRAINT report_template_xslt_pkey PRIMARY KEY (report_template_id);


--
-- Name: reserve_reason_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY reserve_reason_ref
    ADD CONSTRAINT reserve_reason_ref_pkey PRIMARY KEY (reserve_reason_rcd);


--
-- Name: route_surcharge_fare_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY route_surcharge_fare
    ADD CONSTRAINT route_surcharge_fare_pkey PRIMARY KEY (route_surcharge_id, fare_id);


--
-- Name: routings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY routings
    ADD CONSTRAINT routings_pkey PRIMARY KEY (route_id);


--
-- Name: rule_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY rule_type_ref
    ADD CONSTRAINT rule_type_ref_pkey PRIMARY KEY (rule_type_code);


--
-- Name: saccode_messageid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY saccode_messageid
    ADD CONSTRAINT saccode_messageid_pkey PRIMARY KEY (sac_code, create_time);


--
-- Name: seat_attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_attribute
    ADD CONSTRAINT seat_attribute_pkey PRIMARY KEY (seat_definition_id, seat_attribute_rcd);


--
-- Name: seat_attribute_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_attribute_ref
    ADD CONSTRAINT seat_attribute_ref_pkey PRIMARY KEY (seat_attribute_rcd);


--
-- Name: seat_definition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_definition
    ADD CONSTRAINT seat_definition_pkey PRIMARY KEY (seat_definition_id);


--
-- Name: seat_map_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_map_class
    ADD CONSTRAINT seat_map_class_pkey PRIMARY KEY (seat_map_id, selling_class);


--
-- Name: seat_map_configuration_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_map_configuration
    ADD CONSTRAINT seat_map_configuration_pkey PRIMARY KEY (seat_map_id, config_table);


--
-- Name: seat_map_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_map
    ADD CONSTRAINT seat_map_pkey PRIMARY KEY (seat_map_id);


--
-- Name: seat_reconfig_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_reconfig_history
    ADD CONSTRAINT seat_reconfig_history_pkey PRIMARY KEY (seat_reconfig_history_id);


--
-- Name: seat_reservation_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY seat_reservation_setting
    ADD CONSTRAINT seat_reservation_setting_pkey PRIMARY KEY (seat_reservation_setting_id);


--
-- Name: security_function_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY security_function
    ADD CONSTRAINT security_function_pkey PRIMARY KEY (function_id);


--
-- Name: security_function_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY security_function_ref
    ADD CONSTRAINT security_function_ref_pkey PRIMARY KEY (security_function_rcd);


--
-- Name: security_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY security_group
    ADD CONSTRAINT security_group_pkey PRIMARY KEY (security_group_id);


--
-- Name: security_mapping_dimension_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY security_mapping_dimension
    ADD CONSTRAINT security_mapping_dimension_pkey PRIMARY KEY (security_mapping_dimension_id);


--
-- Name: security_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY security_mapping
    ADD CONSTRAINT security_mapping_pkey PRIMARY KEY (security_mapping_id);


--
-- Name: sms_bulk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY sms_bulk
    ADD CONSTRAINT sms_bulk_pkey PRIMARY KEY (bulk_no);


--
-- Name: sms_mesgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY sms_mesgs
    ADD CONSTRAINT sms_mesgs_pkey PRIMARY KEY (serial_no);


--
-- Name: special_service_request_inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY special_service_request_inventory
    ADD CONSTRAINT special_service_request_inventory_pkey PRIMARY KEY (flight_number, flight_date, city_pair, book_no, rqst_code, pax_name);


--
-- Name: special_service_request_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY special_service_request_rules
    ADD CONSTRAINT special_service_request_rules_pkey PRIMARY KEY (flight_number, flight_date, city_pair, rqst_code, flight_to_date);


--
-- Name: ssd_t3_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ssd_t3
    ADD CONSTRAINT ssd_t3_pkey PRIMARY KEY (col1);


--
-- Name: ssd_t4_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ssd_t4
    ADD CONSTRAINT ssd_t4_pkey PRIMARY KEY (col1, col2);


--
-- Name: ssm_tmp_old_inventry_segment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ssm_tmp_old_inventry_segment
    ADD CONSTRAINT ssm_tmp_old_inventry_segment_pkey PRIMARY KEY (flight_number, flight_date, city_pair, selling_class);


--
-- Name: system_setting_category_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY system_setting_category_ref
    ADD CONSTRAINT system_setting_category_ref_pkey PRIMARY KEY (system_setting_category_rcd);


--
-- Name: system_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY system_setting
    ADD CONSTRAINT system_setting_pkey PRIMARY KEY (system_setting_code);


--
-- Name: tax_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY tax_category
    ADD CONSTRAINT tax_category_pkey PRIMARY KEY (tax_cat_id);


--
-- Name: tax_detail_currency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY tax_detail_currency
    ADD CONSTRAINT tax_detail_currency_pkey PRIMARY KEY (tax_detail_currency_id);


--
-- Name: tax_detail_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY tax_detail
    ADD CONSTRAINT tax_detail_pkey PRIMARY KEY (tax_detail_id);


--
-- Name: temp_fare_route_agency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY temp_fare_route_agency
    ADD CONSTRAINT temp_fare_route_agency_pkey PRIMARY KEY (fare_route_id, company_code, agency_code);


--
-- Name: template_xslt_components_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY template_xslt_components
    ADD CONSTRAINT template_xslt_components_pkey PRIMARY KEY (function_id, report_code, report_version, template_sequence_no);


--
-- Name: template_xslt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY template_xslt
    ADD CONSTRAINT template_xslt_pkey PRIMARY KEY (function_id, report_code, report_version, template_sequence_no);


--
-- Name: ticket_history_event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ticket_history_event
    ADD CONSTRAINT ticket_history_event_pkey PRIMARY KEY (hist_serial_no);


--
-- Name: ticket_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ticket_payment
    ADD CONSTRAINT ticket_payment_pkey PRIMARY KEY (ticket_no, payment_no);


--
-- Name: ticket_segment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY ticket_segment
    ADD CONSTRAINT ticket_segment_pkey PRIMARY KEY (ticket_no, segment_type, segment_level, segment_sequence_no, coupon_sequence_no);


--
-- Name: travel_agency_internet_special_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY travel_agency_internet_special
    ADD CONSTRAINT travel_agency_internet_special_pkey PRIMARY KEY (agency_code);


--
-- Name: travel_agency_limit_type_ref_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY travel_agency_limit_type_ref
    ADD CONSTRAINT travel_agency_limit_type_ref_pkey PRIMARY KEY (travel_agency_limit_type_rcd);


--
-- Name: travel_agency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY travel_agency
    ADD CONSTRAINT travel_agency_pkey PRIMARY KEY (agency_code);


--
-- Name: user_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY user_activity
    ADD CONSTRAINT user_activity_pkey PRIMARY KEY (user_activity_id);


--
-- Name: user_group_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY user_group_mapping
    ADD CONSTRAINT user_group_mapping_pkey PRIMARY KEY (user_group_mapping_id);


--
-- Name: user_security_function_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY user_security_function_mapping
    ADD CONSTRAINT user_security_function_mapping_pkey PRIMARY KEY (user_security_function_mapping_id);


--
-- Name: user_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY user_setting
    ADD CONSTRAINT user_setting_pkey PRIMARY KEY (user_setting_code);


--
-- Name: user_setting_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY user_setting_user
    ADD CONSTRAINT user_setting_user_pkey PRIMARY KEY (user_code, user_setting_code);


--
-- Name: voucher_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher_payment
    ADD CONSTRAINT voucher_payment_pkey PRIMARY KEY (voucher_nr, payment_no);


--
-- Name: voucher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher
    ADD CONSTRAINT voucher_pkey PRIMARY KEY (voucher_nr);


--
-- Name: voucher_reason_class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher_reason_class
    ADD CONSTRAINT voucher_reason_class_pkey PRIMARY KEY (reason_code, class_code);


--
-- Name: voucher_reason_fop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher_reason_fop
    ADD CONSTRAINT voucher_reason_fop_pkey PRIMARY KEY (reason_code, payment_type, payment_form);


--
-- Name: voucher_reason_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher_reason
    ADD CONSTRAINT voucher_reason_pkey PRIMARY KEY (reason_code);


--
-- Name: voucher_serial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY voucher_serial
    ADD CONSTRAINT voucher_serial_pkey PRIMARY KEY (voucher_id);


--
-- Name: waiver_reason_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY waiver_reason
    ADD CONSTRAINT waiver_reason_pkey PRIMARY KEY (reason_code);


--
-- Name: watch_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY watch_list
    ADD CONSTRAINT watch_list_pkey PRIMARY KEY (entry_no);


--
-- Name: flight_segment_dates_fndda; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE UNIQUE INDEX flight_segment_dates_fndda ON flight_segment_dates USING btree (flight_number, flight_date, departure_airport, arrival_airport);


--
-- Name: ind_temp_wl_invt; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE INDEX ind_temp_wl_invt ON ssm_tmp_wl_invt USING btree (flight_date, city_pair, selling_class);


--
-- Name: ind_tmp_date; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE INDEX ind_tmp_date ON ssm_tmp_date USING btree (flight_date);


--
-- Name: u_hac; Type: INDEX; Schema: public; Owner: postgres; Tablespace:
--

CREATE INDEX u_hac ON ssm_tmp_hirarchy_avail_counts USING btree (selling_class);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

