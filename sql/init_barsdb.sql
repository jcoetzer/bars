insert into system_setting values('ASMSSMOBP','SSM profile','SSM','SSM','ZZ','SAM','BARS',NOW());

insert into currency_codes values('ZAR','South African Rand',10,100,13.0,NULL,'SAM','BARS',NOW());
insert into taxes(departure_airport,company_code,tax_code,short_description,tax_type,tax_amount,tax_currency,pax_code,valid_from_date,valid_to_date,tax_category,tax_sequence,scrutiny_flag,update_user,update_group,update_time) values ('JNB','ZZ','ZA','Passenger Service Charge','=',72.0,'ZAR','ADULT','2018-06-01','2019-12-31','T',138,'N','SAM','BARS',NOW());
insert into taxes(departure_airport,company_code,tax_code,short_description,tax_type,tax_amount,tax_currency,pax_code,valid_from_date,valid_to_date,tax_category,tax_sequence,scrutiny_flag,update_user,update_group,update_time) values ('JNB','ZZ','UM','Passenger Security Charge','=',19.0,'ZAR','ADULT','2018-06-01','2019-12-31','T',136,'N','SAM','BARS',NOW());
insert into taxes(departure_airport,company_code,tax_code,short_description,tax_type,tax_amount,tax_currency,pax_code,valid_from_date,valid_to_date,tax_category,tax_sequence,scrutiny_flag,update_user,update_group,update_time) values ('JNB','ZZ','ZV','Value Added Tax','%',15.0,'ZAR','ADULT','2018-06-01','2019-12-31','T',5,'N','SAM','BARS',NOW());
insert into taxes(departure_airport,company_code,tax_code,short_description,tax_type,tax_amount,tax_currency,pax_code,valid_from_date,valid_to_date,tax_category,tax_sequence,scrutiny_flag,update_user,update_group,update_time) values ('JNB','ZZ','EV','Civil Aviation Authority Tax','=',18.72,'ZAR','ADULT','2018-06-01','2019-12-31','T',5,'N','SAM','BARS',NOW());

-- insert into master_files values ('ACFT', '738', 'Boeing 737-800', 'SAM', 'BARS');
-- insert into master_files values ('ACFT', '733', 'Boeing 737-300', 'SAM', 'BARS');
-- insert into master_files values ('ACFT', '320', 'Airbus A320', 'SAM', 'BARS');
--
-- insert into aircraft_config values ('738','ZZ','Y','738',0,0,0,0,0,0,0,186,'N','N','SSM','BARS',NOW());
-- insert into aircraft_config values ('738','ZZ','C','738',0,0,0,0,0,0,0,2,'N','N','SSM','BARS',NOW());
-- insert into aircraft_config values ('733','ZZ','Y','733',0,0,0,0,0,0,0,2,'N','N','SSM','BARS',NOW());

insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'Y', 'Y', 'Y', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'Z', 'Y', 'Y', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'A', 'Y', 'Z', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'U', 'Y', 'A', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'S', 'Y', 'U', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'B', 'Y', 'S', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'M', 'Y', 'B', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'P', 'Y', 'M', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'D', 'Y', 'P', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'I', 'Y', 'D', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'T', 'Y', 'I', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'H', 'Y', 'T', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'Q', 'Y', 'H', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'V', 'Y', 'Q', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'W', 'Y', 'V', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'L', 'Y', 'W', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'X', 'Y', 'L', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'R', 'Y', 'X', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'N', 'Y', 'R', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'G', 'Y', 'N', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'E', 'Y', 'G', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'F', 'Y', 'E', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'K', 'Y', 'F', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'J', 'Y', 'K', 'Y', 1.05, 'SAM', 'BARS', NOW());
insert into selling_conf (company_code, selling_class, cabin_code, parent_sell_cls, sell_cls_category, ffp_fact_mult, update_user, update_group, update_time)
 values('ZZ', 'O', 'Y', 'J', 'Y', 1.05, 'SAM', 'BARS', NOW());


insert into airport values('AAM', 'FAMD', 'Mala Mala Airport','Mala Mala', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ADY', 'FAAL', 'Alldays Airport', 'Alldays', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('AFD', 'FAPA', 'Port Alfred Airport', 'Port Alfred', 'ZA','UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('BFN', 'FABL', 'Bloemfontein Airport ', 'Bloemfontein', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('CDO', 'FACD', 'Cradock Airport', 'Cradock', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('CPT', 'FACT', 'Cape Town International Airport', 'Cape Town', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('DUK', 'FADK', 'Dukuduku Airport', 'Mtubatuba', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('DUR', 'FALE', 'King Shaka International Airport', 'Durban', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ELL', 'FAER', 'Ellisras Airport', 'Ellisras', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ELS', 'FAEL', 'East London Airport', 'East London', 'ZA','UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('FCB', 'FAFB', 'Ficksburg Airport', 'Ficksburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('GCJ', 'FAGC', 'Grand Central Airport', 'Johannesburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('HDS', 'FAHS', 'Air Force Base Hoedspruit','Hoedspruit', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('HLA', 'FALA', 'Lanseria International Airport', 'Johannesburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('JNB', 'FAOR', 'O. R. Tambo International Airport', 'Johannesburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('JOH', 'FAPJ', 'Port St. Johns Airport', 'Port St. Johns', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('KIM', 'FAKM', 'Kimberley Airport','Kimberley', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('KLZ', 'FAKZ', 'Kleinzee Airport', 'Kleinzee', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('LAY', 'FALY', 'Ladysmith Airport','Ladysmith', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('KMH', 'FAKU', 'Johan Pienaar Airport', 'Kuruman', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('KOF', 'FAKP', 'Komatipoort Airport', 'Komatipoort', 'ZA','UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('MBD', 'FAMM', 'Mahikeng Airport', 'Mmabatho', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('MEZ', 'FAMS', 'Messina Airport', 'Messina', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('MGH', 'FAMG', 'Margate Airport', 'Margate', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('NCS', 'FANC', 'Newcastle Airport', 'Newcastle', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('NLP', 'FANS', 'Nelspruit Airport', 'Nelspruit', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('OUH', 'FAOH', 'Oudtshoorn Airport', 'Oudtshoorn', 'ZA','UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('OVG', 'FAOB', 'Air Force Base Overberg', 'Bredasdorp', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PBZ', 'FAPG', 'Plettenberg Bay Airport','Plettenberg Bay', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PCF', 'FAPS', 'Potchefstroom Airport', 'Potchefstroom', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PHW', 'FAPH', 'Hendrik Van Eck Airport', 'Phalaborwa', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PLZ', 'FAPE', 'Port Elizabeth Airport', 'Port Elizabeth', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PRK', 'FAPK', 'Prieska Airport', 'Prieska', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PRY', 'FAWB', 'Wonderboom Airport', 'Pretoria', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('PTG', 'FAPP', 'Polokwane International Airport', 'Polokwane', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('QRA', 'FAGM', 'Rand Airport', 'Johannesburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('RCB', 'FARB', 'Richards Bay Airport', 'Richards Bay', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ROD', 'FARS', 'Robertson Airfield', 'Robertson', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('RVO', 'FARI', 'Reivilo Airport', 'Reivilo', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('SBU', 'FASB', 'Springbok Airport', 'Springbok', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('SDB', 'FALW', 'Air Force Base Langebaanweg', 'Saldanha Bay', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('SBU', 'FASB', 'Springbok Airport', 'Springbok', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('SIS', 'FASS', 'Sishen Airport', 'Dingleton', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('SZK', 'FASZ', 'Skukuza Airport', 'Skukuza', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('TCU', 'FATN', 'Thaba Nchu Airport', 'Thaba Nchu', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('THY', 'FATH', 'P.R. Mphephu Airport', 'Thohoyandou', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ULD', 'FAUL', 'Ulundi Airport', 'Ulundi', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('VRE', 'FAVR', 'Vredendal Airport', 'Vredendal', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('VRU', 'FAVB', 'Vryburg Airport', 'Vryburg', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('WEL', 'FAWM', 'Welkom Airport', 'Welkom', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('WKF', 'FAWK', 'Air Force Base Waterkloof', 'Pretoria', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());
insert into airport values('ZEC', 'FASC', 'Secunda Airport', 'Secunda', 'ZA', 'UTC+02:00', 'SAM', 'BARS', NOW());

insert into city select city_code, city_name, 'ZA', 'A', 'N', 'SAM', 'BARS', NOW() from airport;

-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('CPT', 'JNB', 'A', 1500, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('JNB', 'CPT', 'A', 1500, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('JNB', 'DUR', 'A', 600 , '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('DUR', 'JNB', 'A', 600 , '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('CPT', 'DUR', 'A', 1250, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pair(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('DUR', 'CPT', 'A', 1250, '20kg', 1, '', 'SAM', 'BARS', NOW());

-- insert into fare_segm values('ZZ','XZZOW',1,'2018-01-01','2018-12-31','2017-12-01',NULL,3000.0,'BASR','SSM',NOW());
-- insert into fare_segm values('ZZ','XZZOW',2,'2018-01-01','2018-12-31','2017-12-01',NULL,3000.0,'BASR','SSM',NOW());
-- insert into fare_segm values('ZZ','XZZOW',3,'2018-01-01','2018-12-31','2017-12-01',NULL,1200.0,'BASR','SSM',NOW());
-- insert into fare_segm values('ZZ','XZZOW',4,'2018-01-01','2018-12-31','2017-12-01',NULL,3000.0,'BASR','SSM',NOW());
-- insert into fare_segm values('ZZ','XZZOW',5,'2018-01-01','2018-12-31','2017-12-01',NULL,2500.0,'BASR','SSM',NOW());
-- insert into fare_segm values('ZZ','XZZOW',6,'2018-01-01','2018-12-31','2017-12-01',NULL,3000.0,'BASR','SSM',NOW());
--
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','Y','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','Z','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','A','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','U','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','S','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','B','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','M','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','P','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','D','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','I','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','T','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','H','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','Q','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','V','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','W','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','L','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','X','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','R','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','N','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','G','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','E','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','F','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','K','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','J','ZZOW','R','BARS','SSM',NOW());
-- insert into fare_codes(company_code,fare_code,short_description,description,selling_class,fare_category,onw_return_ind,update_user,update_group,update_time) values('ZZ','XZZOW','Fare','Fare stuff','O','ZZOW','R','BARS','SSM',NOW());
-- update fare_codes set acss_strt_auth_level=100;
-- update fare_codes set acss_end_auth_level=100;

insert into service_requests values('ZZ','CKIN',
'Passenger checkin details',
'CKIN',NULL,'S','Y','Y','Y','Y','Y','Y','Y','Y','TARFU','SRVRQ','SRVRQ','SRVRQ','SRVRQ','N','A','Y','A',NULL,NULL,1,NULL,NULL,NULL,'SSM','BARS',NOW());
