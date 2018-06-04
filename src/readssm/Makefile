
INCS = -g -I.. -I../../../src -I/usr/local/include/gef
WFLAG = -Wall -Wno-unused-but-set-variable
DFLAG = -O0 -D_DEBUG -DNOTUX -D_PROCSSM

CFLAGS = -I/usr/include/postgresql $(INCS) $(WFLAG)
SRC_PATH=../../../src

CWARN = -Wall

CCC = /usr/bin/g++
ESQL = ecpg -C INFORMIX


PGFLAGS = -I/usr/include/postgresql -I/usr/include
PLFLAGS = -lecpg -lecpg_compat -lpq

CFLAGS = -g $(CWARN) -O


YACCDEBUG = --debug --verbose

all: ssmread ssmwrite

install: ssmread ssmwrite

clean :
	rm -f $(WOBJS) $(ROBJS) $(COBJS)
	rm -f core.* readssm.output
	rm -f readssm_lex.c readssm.tab.c readssm.tab.h readssm.c
	rm -f ssmwrite ssmread
	rm -rf html/

docs: Doxyfile
	doxygen Doxyfile

install: ssmread ssmwrite
	rm -f /opt/bars/bin/core.*
	cp ssmread ssmwrite /opt/bars/bin/

POBJS = procssm_yacc.o readssm_lex.o ProcSsmFile.o SsmData.o CheckFlightDb.o QueueError.o \
	FlightData.o update_shared_leg.o fp_legs_from_assm.o config_rule.o \
	split_opr_period.o freq_date_gen.o flt_chg_from_assm.o waitlist_place50_asm.o del_flight_period.o \
	ssm_flgt_inventry_gen.o flt_perds_gen.o flgt_ssim_notify.o flgt_inventry_avl.o \
	time_chng_notif45e_for_assm.o SsmUtils.o \
	SsmFlightPerdLegs.o SsmDb.o proc_tim.o proc_new.o ssm_extendSchedule.o fp_from_ssm.o proc_rpl.o \
	update_inventry_segment.o \
	fp_seg_cls_gen.o realloc_gen.o flt_per_seg_rstr.o invt_update50.o check_wrel_realoc.o serial_nos.o \
	flgt_schedule_ctg.o ssm_flgt_schedule_upd_asm.o generate_skd.o fp_segm_cmp.o \
	ssm_avs_notify50.o proc_cnl.o proc_eqt.o  proc_cnl_db.o \
	clear_time_chng45e_asm.o auto_restrict.o avs_notify50.o date_fns.o extend_segment_status.o \
	flgt_restrict_gen.o invt_return50.o upd_flight_period.o SsmFrequencies.o \
	SsmFlightData.o ReadSsmConfig.o ParseSsmFile.o DbDate.o GetDate.o DbConnect.o ReadTmpDate.o \
	frqcon.o gmt_diff_mns.o DbFlightPerdLegs.o freq_nxdt_gen.o SsmDate.o SsmDateIfx.o SsmDateIfxCpp.o \
	extend_inventry_segment.o flt_chg_from_assm_all.o DbFlightSegmDate.o populate_flt_asr.o \
	fp_prnt_gen.o getdatechange.o getsegmentrestrict.o getsegmentclass.o generate_adm.o \
	gen_prnt_sell_cls.o validateStartDateInFuture.o AirportTerminal.o GetFlightData.o \
	add_shared_leg.o writeFlifo.o ReadOldInventrySegments.o FpSegClsEntry.o restart_serial.o \
	fp_seg_cls_cmp.o flgt_inventry_gen.o book_rqst_realloc.o ssm_flgt_inventry_mod.o \
	flight_change_asr.o flgt_inventry_rlc.o DbFlightDateLeg.o QueueMessage.o SegmentData.o \
	ConfigData.o LegData.o ssm_fp_seg_cls_gen.o
	#ListFlightTables.o
COBJS = checkssm_yacc.o readssm_lex.o checkssm_file.o check__CheckFlightDb.o \
	check__SsmData.o check__SsmFlightData.o check__SsmDb.o check__SsmUtils.o \
	check__CheckFlightTables.o check__FlightData.o check__list_flight_tables.o
ROBJS = readssm_yacc.o readssm_lex.o ReadSsmFile.o
WOBJS = WriteSsm.o WriteSsmFile.o SsmUtils.o SsmDate.o

checkssm :  ssm_userlog.h Makefile $(COBJS)
	g++ $(WFLAG) -o checkssm $(COBJS) -lfl $(PLFLAGS)

procssm : Makefile $(POBJS)
	g++ $(WFLAG) -o procssm $(POBJS) -lfl $(PLFLAGS)

ssmwrite : gitrev.h Makefile $(WOBJS)
	g++ $(WFLAG) -o ssmwrite $(WOBJS)

ssmread : gitrev.h readssm.tab.c Makefile $(ROBJS)
	g++ $(WFLAG) -o ssmread $(ROBJS) -lfl

add_shared_leg.o : ssm_userlog.h Makefile add_shared_leg.ec add_shared_leg.h
	$(ESQL) $(PGFLAGS) -c add_shared_leg.ec -o add_shared_leg.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c add_shared_leg.c

AirportTerminal.o : ssm_userlog.h Makefile AirportTerminal.ec AirportTerminal.h
	$(ESQL) $(PGFLAGS) -c AirportTerminal.ec -o AirportTerminal.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c AirportTerminal.c

auto_restrict.o : ssm_userlog.h Makefile auto_restrict.ec auto_restrict.h
	$(ESQL) $(PGFLAGS) -c auto_restrict.ec -o auto_restrict.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c auto_restrict.c

avs_notify50.o : ssm_userlog.h Makefile avs_notify50.ec avs_notify50.h
	$(ESQL) $(PGFLAGS) -c avs_notify50.ec -o avs_notify50.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c avs_notify50.c

book_rqst_realloc.o : ssm_userlog.h Makefile book_rqst_realloc.ec book_rqst_realloc.h
	$(ESQL) $(PGFLAGS) -c book_rqst_realloc.ec -o book_rqst_realloc.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c book_rqst_realloc.c

check__CheckFlightDb.o : ssm_userlog.h Makefile CheckFlightDb.ec CheckFlightDb.h
	$(ESQL) $(PGFLAGS) -c CheckFlightDb.ec -o check__CheckFlightDb.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c check__CheckFlightDb.c

check__FlightData.o : ssm_userlog.h Makefile FlightData.cpp FlightData.h
	g++ $(WFLAG) $(INCS) -c -o check__FlightData.o FlightData.cpp

check__CheckFlightTables.o : ssm_userlog.h Makefile CheckFlightTables.ec CheckFlightTables.h
	$(ESQL) $(PGFLAGS) -c CheckFlightTables.ec -o check__CheckFlightTables.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c check__CheckFlightTables.c

check__list_flight_tables.o : ssm_userlog.h Makefile list_flight_tables.ec list_flight_tables.h
	$(ESQL) $(PGFLAGS) -c list_flight_tables.ec -o check__list_flight_tables.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c check__list_flight_tables.c

check__SsmData.o : ssm_userlog.h Makefile SsmData.cpp SsmData.h
	g++ $(INCS) -c -o check__SsmData.o SsmData.cpp

check__SsmFlightData.o : ssm_userlog.h Makefile SsmFlightData.cpp SsmFlightData.h
	g++ $(WFLAG) $(INCS) -c -o check__SsmFlightData.o SsmFlightData.cpp

check__SsmDb.o : ssm_userlog.h Makefile SsmDb.ec SsmDb.h
	$(ESQL) $(PGFLAGS) -c SsmDb.ec -o check__SsmDb.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c check__SsmDb.c

check__SsmUtils.o : ssm_userlog.h Makefile SsmUtils.cpp SsmUtils.h
	g++ $(WFLAG) $(INCS) -c -o check__SsmUtils.o SsmUtils.cpp

checkssm_file.o : ssm_userlog.h Makefile checkssm_file.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o checkssm_file.o checkssm_file.cpp

checkssm_yacc.o : ssm_userlog.h Makefile readssm.tab.c
	gcc -D_CHECKSSM $(INCS) -c -o checkssm_yacc.o readssm.tab.c

CheckFlightDb.o : ssm_userlog.h Makefile CheckFlightDb.ec CheckFlightDb.h
	$(ESQL) $(PGFLAGS) -c CheckFlightDb.ec -o CheckFlightDb.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c CheckFlightDb.c

CheckFlightTables.o : ssm_userlog.h Makefile CheckFlightTables.ec CheckFlightTables.h
	$(ESQL) $(PGFLAGS) -c CheckFlightTables.ec -o CheckFlightTables.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c CheckFlightTables.c

check_wrel_realoc.o : ssm_userlog.h Makefile check_wrel_realoc.ec check_wrel_realoc.h
	$(ESQL) $(PGFLAGS) -c check_wrel_realoc.ec -o check_wrel_realoc.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c check_wrel_realoc.c

clear_time_chng45e_asm.o : ssm_userlog.h Makefile clear_time_chng45e_asm.ec clear_time_chng45e_asm.h
	$(ESQL) $(PGFLAGS) -c clear_time_chng45e_asm.ec -o clear_time_chng45e_asm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c clear_time_chng45e_asm.c

ConfigData.o : ssm_userlog.h Makefile ConfigData.cpp ConfigData.hpp
	g++ $(INCS) -c -o ConfigData.o ConfigData.cpp

config_rule.o : ssm_userlog.h Makefile config_rule.ec config_rule.h
	$(ESQL) $(PGFLAGS) -c config_rule.ec -o config_rule.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c config_rule.c

date_fns.o : ssm_userlog.h Makefile date_fns.ec date_fns.h
	$(ESQL) $(PGFLAGS) -c date_fns.ec -o date_fns.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c date_fns.c

DbConnect.o : ssm_userlog.h Makefile DbConnect.ec DbConnect.h
	$(ESQL) $(PGFLAGS) -c DbConnect.ec -o DbConnect.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c DbConnect.c

DbDate.o : ssm_userlog.h Makefile DbDate.ec DbDate.h
	$(ESQL) $(PGFLAGS) -c DbDate.ec -o DbDate.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c DbDate.c

DbFlightDateLeg.o : ssm_userlog.h Makefile DbFlightDateLeg.ec DbFlightDateLeg.h
	$(ESQL) $(PGFLAGS) -c DbFlightDateLeg.ec -o DbFlightDateLeg.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c DbFlightDateLeg.c

DbFlightPerdLegs.o : ssm_userlog.h Makefile DbFlightPerdLegs.ec DbFlightPerdLegs.h
	$(ESQL) $(PGFLAGS) -c DbFlightPerdLegs.ec -o DbFlightPerdLegs.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c DbFlightPerdLegs.c

DbFlightSegmDate.o : ssm_userlog.h Makefile DbFlightSegmDate.ec DbFlightSegmDate.h
	$(ESQL) $(PGFLAGS) -c DbFlightSegmDate.ec -o DbFlightSegmDate.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c DbFlightSegmDate.c

del_flight_period.o : ssm_userlog.h Makefile del_flight_period.ec del_flight_period.h
	$(ESQL) $(PGFLAGS) -c del_flight_period.ec -o del_flight_period.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c del_flight_period.c

extend_inventry_segment.o : ssm_userlog.h Makefile extend_inventry_segment.ec extend_inventry_segment.h
	$(ESQL) $(PGFLAGS) -c extend_inventry_segment.ec -o extend_inventry_segment.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c extend_inventry_segment.c

extend_segment_status.o : ssm_userlog.h Makefile extend_segment_status.ec extend_segment_status.h
	$(ESQL) $(PGFLAGS) -c extend_segment_status.ec -o extend_segment_status.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c extend_segment_status.c

flgt_inventry_avl.o : ssm_userlog.h Makefile flgt_inventry_avl.ec flgt_inventry_avl.h
	$(ESQL) $(PGFLAGS) -c flgt_inventry_avl.ec -o flgt_inventry_avl.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_inventry_avl.c

flgt_inventry_gen.o : ssm_userlog.h Makefile flgt_inventry_gen.ec flgt_inventry_gen.h
	$(ESQL) $(PGFLAGS) -c flgt_inventry_gen.ec -o flgt_inventry_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_inventry_gen.c

flgt_inventry_rlc.o : ssm_userlog.h Makefile flgt_inventry_rlc.ec flgt_inventry_rlc.h
	$(ESQL) $(PGFLAGS) -c flgt_inventry_rlc.ec -o flgt_inventry_rlc.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_inventry_rlc.c

flgt_restrict_gen.o : ssm_userlog.h Makefile flgt_restrict_gen.ec flgt_restrict_gen.h
	$(ESQL) $(PGFLAGS) -c flgt_restrict_gen.ec -o flgt_restrict_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_restrict_gen.c

flgt_schedule_ctg.o : ssm_userlog.h Makefile flgt_schedule_ctg.ec flgt_schedule_ctg.h
	$(ESQL) $(PGFLAGS) -c flgt_schedule_ctg.ec -o flgt_schedule_ctg.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_schedule_ctg.c

flgt_ssim_notify.o : ssm_userlog.h Makefile flgt_ssim_notify.ec flgt_ssim_notify.h
	$(ESQL) $(PGFLAGS) -c flgt_ssim_notify.ec -o flgt_ssim_notify.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flgt_ssim_notify.c

FlightData.o : ssm_userlog.h Makefile FlightData.cpp FlightData.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o FlightData.o FlightData.cpp

flight_change_asr.o : ssm_userlog.h Makefile flight_change_asr.ec flight_change_asr.h
	$(ESQL) $(PGFLAGS) -c flight_change_asr.ec -o flight_change_asr.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flight_change_asr.c

flt_chg_from_assm.o : ssm_userlog.h Makefile flt_chg_from_assm.ec flt_chg_from_assm.h
	$(ESQL) $(PGFLAGS) -c flt_chg_from_assm.ec -o flt_chg_from_assm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flt_chg_from_assm.c

flt_chg_from_assm_all.o : ssm_userlog.h Makefile flt_chg_from_assm_all.ec flt_chg_from_assm.h
	$(ESQL) $(PGFLAGS) -c flt_chg_from_assm_all.ec -o flt_chg_from_assm_all.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flt_chg_from_assm_all.c

flt_per_seg_rstr.o : ssm_userlog.h Makefile flt_per_seg_rstr.ec flt_per_seg_rstr.h
	$(ESQL) $(PGFLAGS) -c flt_per_seg_rstr.ec -o flt_per_seg_rstr.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flt_per_seg_rstr.c

flt_perds_gen.o : ssm_userlog.h Makefile flt_perds_gen.ec flt_perds_gen.h
	$(ESQL) $(PGFLAGS) -c flt_perds_gen.ec -o flt_perds_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c flt_perds_gen.c

FpSegClsEntry.o : ssm_userlog.h Makefile FpSegClsEntry.cpp FpSegClsEntry.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o FpSegClsEntry.o FpSegClsEntry.cpp

fp_from_ssm.o : ssm_userlog.h Makefile fp_from_ssm.ec fp_from_ssm.h
	$(ESQL) $(PGFLAGS) -c fp_from_ssm.ec -o fp_from_ssm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_from_ssm.c

fp_legs_from_assm.o : ssm_userlog.h Makefile fp_legs_from_assm.ec fp_legs_from_assm.h
	$(ESQL) $(PGFLAGS) -c fp_legs_from_assm.ec -o fp_legs_from_assm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_legs_from_assm.c

fp_prnt_gen.o : ssm_userlog.h Makefile fp_prnt_gen.ec fp_prnt_gen.h
	$(ESQL) $(PGFLAGS) -c fp_prnt_gen.ec -o fp_prnt_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_prnt_gen.c

fp_seg_cls_cmp.o : ssm_userlog.h Makefile fp_seg_cls_cmp.ec fp_seg_cls_cmp.h
	$(ESQL) $(PGFLAGS) -c fp_seg_cls_cmp.ec -o fp_seg_cls_cmp.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_seg_cls_cmp.c

fp_seg_cls_gen.o : ssm_userlog.h Makefile fp_seg_cls_gen.ec fp_seg_cls_gen.h
	$(ESQL) $(PGFLAGS) -c fp_seg_cls_gen.ec -o fp_seg_cls_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_seg_cls_gen.c

fp_segm_cmp.o : ssm_userlog.h Makefile fp_segm_cmp.ec fp_segm_cmp.h
	$(ESQL) $(PGFLAGS) -c fp_segm_cmp.ec -o fp_segm_cmp.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c fp_segm_cmp.c

freq_date_gen.o : ssm_userlog.h Makefile freq_date_gen.ec freq_date_gen.h
	$(ESQL) $(PGFLAGS) -c freq_date_gen.ec -o freq_date_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c freq_date_gen.c

freq_nxdt_gen.o : ssm_userlog.h Makefile freq_nxdt_gen.ec freq_nxdt_gen.h
	$(ESQL) $(PGFLAGS) -c freq_nxdt_gen.ec -o freq_nxdt_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c freq_nxdt_gen.c

frqcon.o : ssm_userlog.h Makefile frqcon.ec frqcon.h
	$(ESQL) $(PGFLAGS) -c frqcon.ec -o frqcon.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c frqcon.c

generate_adm.o : ssm_userlog.h Makefile generate_adm.ec generate_adm.h
	$(ESQL) $(PGFLAGS) -c generate_adm.ec -o generate_adm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c generate_adm.c

generate_skd.o : ssm_userlog.h Makefile generate_skd.ec generate_skd.h
	$(ESQL) $(PGFLAGS) -c generate_skd.ec -o generate_skd.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c generate_skd.c

gen_prnt_sell_cls.o : ssm_userlog.h Makefile gen_prnt_sell_cls.ec gen_prnt_sell_cls.h
	$(ESQL) $(PGFLAGS) -c gen_prnt_sell_cls.ec -o gen_prnt_sell_cls.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c gen_prnt_sell_cls.c

getdatechange.o : ssm_userlog.h Makefile getdatechange.ec getdatechange.h
	$(ESQL) $(PGFLAGS) -c getdatechange.ec -o getdatechange.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c getdatechange.c

GetFlightData.o : ssm_userlog.h Makefile GetFlightData.ec GetFlightData.h
	$(ESQL) $(PGFLAGS) -c GetFlightData.ec -o GetFlightData.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c GetFlightData.c

getsegmentclass.o : ssm_userlog.h Makefile getsegmentclass.ec getsegmentclass.h
	$(ESQL) $(PGFLAGS) -c getsegmentclass.ec -o getsegmentclass.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c getsegmentclass.c

getsegmentrestrict.o : ssm_userlog.h Makefile getsegmentrestrict.ec getsegmentrestrict.h
	$(ESQL) $(PGFLAGS) -c getsegmentrestrict.ec -o getsegmentrestrict.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c getsegmentrestrict.c

GetDate.o : ssm_userlog.h Makefile GetDate.cpp GetDate.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o GetDate.o GetDate.cpp

gmt_diff_mns.o : ssm_userlog.h Makefile gmt_diff_mns.ec gmt_diff_mns.h
	$(ESQL) $(PGFLAGS) -c gmt_diff_mns.ec -o gmt_diff_mns.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c gmt_diff_mns.c

invt_return50.o : ssm_userlog.h Makefile invt_return50.ec invt_return50.h
	$(ESQL) $(PGFLAGS) -c invt_return50.ec -o invt_return50.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c invt_return50.c

invt_update50.o : ssm_userlog.h Makefile invt_update50.ec invt_update50.h
	$(ESQL) $(PGFLAGS) -c invt_update50.ec -o invt_update50.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c invt_update50.c

LegData.o : ssm_userlog.h Makefile LegData.cpp LegData.hpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o LegData.o LegData.cpp

ListFlightTables.o : ssm_userlog.h Makefile ListFlightTables.ec ListFlightTables.h
	$(ESQL) $(PGFLAGS) -c ListFlightTables.ec -o ListFlightTables.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ListFlightTables.c

populate_flt_asr.o : ssm_userlog.h Makefile populate_flt_asr.ec populate_flt_asr.h
	$(ESQL) $(PGFLAGS) -c populate_flt_asr.ec -o populate_flt_asr.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c populate_flt_asr.c

proc_cnl.o : ssm_userlog.h Makefile proc_cnl.ec proc_cnl.h
	$(ESQL) $(PGFLAGS) -c proc_cnl.ec -o proc_cnl.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_cnl.c

proc_cnl_db.o : ssm_userlog.h Makefile proc_cnl_db.ec proc_cnl_db.h
	$(ESQL) $(PGFLAGS) -c proc_cnl_db.ec -o proc_cnl_db.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_cnl_db.c

proc_eqt.o : ssm_userlog.h Makefile proc_eqt.ec proc_eqt.h
	$(ESQL) $(PGFLAGS) -c proc_eqt.ec -o proc_eqt.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_eqt.c

proc_new.o : ssm_userlog.h Makefile proc_new.ec proc_new.h
	$(ESQL) $(PGFLAGS) -c proc_new.ec -o proc_new.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_new.c

proc_rpl.o : ssm_userlog.h Makefile proc_rpl.ec proc_rpl.h
	$(ESQL) $(PGFLAGS) -c proc_rpl.ec -o proc_rpl.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_rpl.c

proc_tim.o : ssm_userlog.h Makefile proc_tim.ec proc_tim.h
	$(ESQL) $(PGFLAGS) -c proc_tim.ec -o proc_tim.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c proc_tim.c

ProcSsmFile.o : ssm_userlog.h Makefile ProcSsmFile.cpp ReadSsmFile.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o ProcSsmFile.o ProcSsmFile.cpp

procssm_yacc.o : ssm_userlog.h Makefile readssm.tab.c
	gcc $(DFLAG) $(INCS) -c -o procssm_yacc.o readssm.tab.c

QueueError.o : ssm_userlog.h Makefile QueueError.ec QueueError.h
	$(ESQL) $(PGFLAGS) -c QueueError.ec -o QueueError.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c QueueError.c

QueueMessage.o : ssm_userlog.h Makefile QueueMessage.ec QueueMessage.h
	$(ESQL) $(PGFLAGS) -c QueueMessage.ec -o QueueMessage.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c QueueMessage.c

ReadOldInventrySegments.o : ssm_userlog.h Makefile ReadOldInventrySegments.ec ReadOldInventrySegments.h
	$(ESQL) $(PGFLAGS) -c ReadOldInventrySegments.ec -o ReadOldInventrySegments.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ReadOldInventrySegments.c

ReadSsmConfig.o : ssm_userlog.h Makefile ReadSsmConfig.cpp ReadSsmConfig.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o ReadSsmConfig.o ReadSsmConfig.cpp

ReadSsmFile.o : ssm_userlog.h Makefile ReadSsmFile.cpp ReadSsmFile.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o ReadSsmFile.o ReadSsmFile.cpp

readssm_lex.o : ssm_userlog.h Makefile readssm_lex.c
	gcc $(INCS) -c -o readssm_lex.o readssm_lex.c

readssm_lex.c : Makefile readssm.l
	flex -o readssm_lex.c readssm.l

readssm_yacc.o : ssm_userlog.h Makefile readssm.tab.c
	gcc $(INCS) -c -o readssm_yacc.o readssm.tab.c

readssm.tab.c : Makefile readssm.y
	bison $(YACCDEBUG) -d readssm.y

ReadTmpDate.o : ssm_userlog.h Makefile ReadTmpDate.ec ReadTmpDate.h
	$(ESQL) $(PGFLAGS) -c ReadTmpDate.ec -o ReadTmpDate.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ReadTmpDate.c

realloc_gen.o : ssm_userlog.h Makefile realloc_gen.ec realloc_gen.h
	$(ESQL) $(PGFLAGS) -c realloc_gen.ec -o realloc_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c realloc_gen.c

restart_serial.o : ssm_userlog.h Makefile restart_serial.ec restart_serial.h
	$(ESQL) $(PGFLAGS) -c restart_serial.ec -o restart_serial.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c restart_serial.c

serial_nos.o : ssm_userlog.h Makefile serial_nos.ec serial_nos.h
	$(ESQL) $(PGFLAGS) -c serial_nos.ec -o serial_nos.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c serial_nos.c

split_opr_period.o : ssm_userlog.h Makefile split_opr_period.ec split_opr_period.h
	$(ESQL) $(PGFLAGS) -c split_opr_period.ec -o split_opr_period.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c split_opr_period.c

SegmentData.o : ssm_userlog.h Makefile SegmentData.cpp SegmentData.h
	g++ $(DFLAG) $(INCS) -c -o SegmentData.o SegmentData.cpp

SsmData.o : ssm_userlog.h Makefile SsmData.cpp SsmData.h
	g++ $(DFLAG) $(INCS) -c -o SsmData.o SsmData.cpp

SsmDate.o : ssm_userlog.h Makefile SsmDate.cpp SsmDate.hpp
	g++ $(DFLAG) $(INCS) -c -o SsmDate.o SsmDate.cpp

SsmDateIfx.o : ssm_userlog.h Makefile SsmDateIfx.ec SsmDateIfx.h
	$(ESQL) $(PGFLAGS) -c SsmDateIfx.ec -o SsmDateIfx.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c SsmDateIfx.c

SsmDateIfxCpp.o : ssm_userlog.h Makefile SsmDateIfx.cpp SsmDateIfx.hpp
	g++ $(DFLAG) $(INCS) -c -o SsmDateIfxCpp.o SsmDateIfx.cpp

SsmDb.o : ssm_userlog.h Makefile SsmDb.ec SsmDb.h
	$(ESQL) $(PGFLAGS) -c SsmDb.ec -o SsmDb.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c SsmDb.c

SsmFlightData.o : ssm_userlog.h Makefile SsmFlightData.cpp SsmFlightData.hpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o SsmFlightData.o SsmFlightData.cpp

ssm_avs_notify50.o : ssm_userlog.h Makefile ssm_avs_notify50.ec ssm_avs_notify50.h
	$(ESQL) $(PGFLAGS) -c ssm_avs_notify50.ec -o ssm_avs_notify50.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_avs_notify50.c

ssm_extendSchedule.o : ssm_userlog.h Makefile ssm_extendSchedule.ec ssm_extendSchedule.h
	$(ESQL) $(PGFLAGS) -c ssm_extendSchedule.ec -o ssm_extendSchedule.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_extendSchedule.c

ssm_flgt_schedule_upd_asm.o : ssm_userlog.h Makefile ssm_flgt_schedule_upd_asm.ec ssm_flgt_schedule_upd_asm.h
	$(ESQL) $(PGFLAGS) -c ssm_flgt_schedule_upd_asm.ec -o ssm_flgt_schedule_upd_asm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_flgt_schedule_upd_asm.c

ssm_flgt_inventry_gen.o : ssm_userlog.h Makefile ssm_flgt_inventry_gen.ec ssm_flgt_inventry_gen.h
	$(ESQL) $(PGFLAGS) -c ssm_flgt_inventry_gen.ec -o ssm_flgt_inventry_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_flgt_inventry_gen.c

ssm_flgt_inventry_mod.o : ssm_userlog.h Makefile ssm_flgt_inventry_mod.ec ssm_flgt_inventry_mod.h
	$(ESQL) $(PGFLAGS) -c ssm_flgt_inventry_mod.ec -o ssm_flgt_inventry_mod.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_flgt_inventry_mod.c

ssm_fp_seg_cls_gen.o : ssm_userlog.h Makefile ssm_fp_seg_cls_gen.ec ssm_fp_seg_cls_gen.h
	$(ESQL) $(PGFLAGS) -c ssm_fp_seg_cls_gen.ec -o ssm_fp_seg_cls_gen.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c ssm_fp_seg_cls_gen.c

SsmUtils.o : ssm_userlog.h Makefile SsmUtils.cpp SsmUtils.h
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o SsmUtils.o SsmUtils.cpp

SsmFlightPerdLegs.o : ssm_userlog.h Makefile SsmFlightPerdLegs.ec SsmFlightPerdLegs.h
	$(ESQL) $(PGFLAGS) -c SsmFlightPerdLegs.ec -o SsmFlightPerdLegs.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c SsmFlightPerdLegs.c

SsmFrequencies.o : ssm_userlog.h Makefile SsmFrequencies.ec SsmFrequencies.h
	$(ESQL) $(PGFLAGS) -c SsmFrequencies.ec -o SsmFrequencies.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c SsmFrequencies.c

time_chng_notif45e_for_assm.o : ssm_userlog.h Makefile time_chng_notif45e_for_assm.ec time_chng_notif45e_for_assm.h
	$(ESQL) $(PGFLAGS) -c time_chng_notif45e_for_assm.ec -o time_chng_notif45e_for_assm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c time_chng_notif45e_for_assm.c

update_inventry_segment.o : ssm_userlog.h Makefile update_inventry_segment.ec update_inventry_segment.h
	$(ESQL) $(PGFLAGS) -c update_inventry_segment.ec -o update_inventry_segment.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c update_inventry_segment.c

upd_flight_period.o : ssm_userlog.h Makefile upd_flight_period.ec upd_flight_period.h
	$(ESQL) $(PGFLAGS) -c upd_flight_period.ec -o upd_flight_period.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c upd_flight_period.c

update_shared_leg.o : ssm_userlog.h Makefile update_shared_leg.ec update_shared_leg.h
	$(ESQL) $(PGFLAGS) -c update_shared_leg.ec -o update_shared_leg.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c update_shared_leg.c

validateStartDateInFuture.o : ssm_userlog.h Makefile validateStartDateInFuture.ec validateStartDateInFuture.h
	$(ESQL) $(PGFLAGS) -c validateStartDateInFuture.ec -o validateStartDateInFuture.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c validateStartDateInFuture.c

waitlist_place50_asm.o : ssm_userlog.h Makefile waitlist_place50_asm.ec waitlist_place50_asm.h
	$(ESQL) $(PGFLAGS) -c waitlist_place50_asm.ec -o waitlist_place50_asm.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c waitlist_place50_asm.c

writeFlifo.o : ssm_userlog.h Makefile writeFlifo.ec writeFlifo.h
	$(ESQL) $(PGFLAGS) -c writeFlifo.ec -o writeFlifo.c
	$(CC) $(CFLAGS) $(PGFLAGS) -Wno-unused-result -c writeFlifo.c

WriteSsm.o : Makefile WriteSsm.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o WriteSsm.o WriteSsm.cpp

WriteSsmFile.o : Makefile WriteSsmFile.cpp
	g++ $(DFLAG) $(WFLAG) $(INCS) -c -o WriteSsmFile.o WriteSsmFile.cpp
