/////////////////////
////LABOUR SUPPLY////
/////////////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "indi_laboursupply_year_2013_b.dta"
egen indi_wage_year_2013 = rowtotal (year_wage_main year_wage_sec year_wage_us01)
keep HHID HHID PID indi_laboursupply_year_2013 indi_wage_year_2013 worker
label var indi_laboursupply_year_2013 "Individual labour supply (hours), 2013 "
label var indi_wage_year_2013 "Individual wage earned, 2010 "
save "indi_laboursupply_year_2013.dta", replace
