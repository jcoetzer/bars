INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('MANUAL','TDB','BIKE','Tandem Bike','2018-01-01 00:00','2020-12-31 23:59',300.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('MANUAL','BIK','BIKE','Bike','2018-01-01 00:00','2020-12-31 23:59',180.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('MANUAL','XBO','XBAG','Excess Baggage','2018-01-01 00:00','2020-12-31 23:59',100.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('SSR','SEA','SEAT','Seat Request','2018-01-01 00:00','2020-12-31 23:59',50.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('SSR','ALO','AILO','Travel Insurance Leisure','2018-01-01 00:00','2020-12-31 23:59',20.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('SSR','ACO','AICO','Travel Insurance Corporate','2018-01-01 00:00','2020-12-31 23:59',20.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('SSR','UNC','UNCF','Unicef Donation','2018-01-01 00:00','2020-12-31 23:59',10.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('NCHANGE','NMO','','Name change','2018-01-01 00:00','2020-12-31 23:59',200.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('ICHANGE','ICO','','Itinerary change','2018-01-01 00:00','2020-12-31 23:59',250.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

INSERT into fees(fee_type_rcd,fee_code,ssr_code,description,valid_from_date_time,valid_until_date_time,fee_amount,fee_currency,fee_percent_flag,tax_percent_flag,use_days_before_departure_flag,create_user,create_time,active_flag,international_domestic_indicator,per_segment_flag)
VALUES('SSR','SPE','SPEQ','Sport equipment','2018-01-01 00:00','2020-12-31 23:59',200.0,'ZAR',0,0,0,'FOO',NOW(),1,'D',1);

UPDATE fees SET payment_form=fee_code;
