delete from master_files where file_code = 'ACFT';

insert into master_files values ('ACFT', '738', 'Boeing 737-800', 'SAM', 'BARS');
insert into master_files values ('ACFT', '733', 'Boeing 737-300', 'SAM', 'BARS');
insert into master_files values ('ACFT', '320', 'Airbus A320', 'SAM', 'BARS');

delete from aircraft_config;

insert into aircraft_config values ('738','ZZ','Y','738',0,0,0,0,0,0,0,186,'N','N','SSM','BARS',NOW());
insert into aircraft_config values ('738','ZZ','C','738',0,0,0,0,0,0,0,2,'N','N','SSM','BARS',NOW());
insert into aircraft_config values ('733','ZZ','Y','733',0,0,0,0,0,0,0,2,'N','N','SSM','BARS',NOW());
