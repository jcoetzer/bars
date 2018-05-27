# -P JNB 1xx
# -P DUR 3xx
# -P CPT 2xx

/opt/bars/bin/ssmwrite --new -A 738 -F ZZ123 -G AA9123 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P JNB -Q CPT -T ZSFOO -X 0900 -Y 1105 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ223 -G AA9223 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q JNB -P CPT -T ZSFOO -X 1200 -Y 1405 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ124 -G AA9124 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P JNB -Q CPT -T ZSFOO -X 1500 -Y 1705 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ224 -G AA9224 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q JNB -P CPT -T ZSFOO -X 1800 -Y 2005 | /opt/bars/bin/ProcSsm.py -V -

/opt/bars/bin/ssmwrite --new -A 738 -F ZZ133 -G AA9133 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P JNB -Q DUR -T ZSFOO -X 0900 -Y 1030 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ333 -G AA9333 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q JNB -P DUR -T ZSFOO -X 1200 -Y 1330 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ134 -G AA9134 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P JNB -Q DUR -T ZSFOO -X 1500 -Y 1630 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ334 -G AA9334 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q JNB -P DUR -T ZSFOO -X 1800 -Y 1930 | /opt/bars/bin/ProcSsm.py -V -

/opt/bars/bin/ssmwrite --new -A 738 -F ZZ243 -G AA9143 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P CPT -Q DUR -T ZSFOO -X 0900 -Y 1100 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ343 -G AA9343 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q CPT -P DUR -T ZSFOO -X 1200 -Y 1400 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ244 -G AA9144 -D 01JUN2018 -E 31JUL2018 -K 1234567 -P CPT -Q DUR -T ZSFOO -X 1500 -Y 1700 | /opt/bars/bin/ProcSsm.py -V -
/opt/bars/bin/ssmwrite --new -A 738 -F ZZ344 -G AA9344 -D 01JUN2018 -E 31JUL2018 -K 1234567 -Q CPT -P DUR -T ZSFOO -X 1800 -Y 2000 | /opt/bars/bin/ProcSsm.py -V -