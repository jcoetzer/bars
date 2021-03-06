
-- delete from city_pairs;
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('CPT', 'JNB', 'A', 1500, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('JNB', 'CPT', 'A', 1500, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('JNB', 'DUR', 'A', 600 , '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('DUR', 'JNB', 'A', 600 , '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('CPT', 'DUR', 'A', 1250, '20kg', 1, '', 'SAM', 'BARS', NOW());
-- insert into city_pairs(departure_airport,arrival_airport,pair_indicator,distance,baggage_alownce,pair_rule_no,remarks,update_user,update_group,update_time)
--  values('DUR', 'CPT', 'A', 1250, '20kg', 1, '', 'SAM', 'BARS', NOW());

delete from airport;

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

delete from city;

insert into city select city_code, city_name, 'ZA', 'A', 'N', 'SAM', 'BARS', NOW() from airport;
