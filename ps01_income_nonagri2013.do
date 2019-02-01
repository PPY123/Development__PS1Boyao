cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"

/////////////////////
//ENTERPRISE PROFIT//
/////////////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC12.dta"
rename hhid HHID
destring HHID, replace
**format HHID %16.0f
gen enter_profit_2013 = 12*(h12q13-h12q15-h12q16-h12q17)
rename h12q13 enter_rev
rename h12q15 enter_laborcost
rename h12q16 enter_materialcost
rename h12q17 enter_energycost
collapse (sum) enter_profit_2013 enter_rev enter_laborcost enter_materialcost enter_energycost, by(HHID)
save "enter_profit_2013.dta", replace

///////////////////
///LABOUR INCOME///
///////////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC8_1.dta"
destring HHID, replace
**format HHID %16.0f
*gen byte wage_earner=(h8q22==1) if h8q15==.	//Indictor of wage earner: only 12% of total workers

	//main job hours
	egen weekly_hr_main = rowtotal(h8q36a h8q36b h8q36c h8q36d h8q36e h8q36f h8q36g)
	rename h8q30b week_permonth
	rename h8q30 month_peryear
	egen day_perweek = rownonmiss(h8q36a h8q36b h8q36c h8q36d h8q36e h8q36f h8q36g)
	gen year_hr_main = weekly_hr_main * month_peryear * week_permonth

	//main job pay
	egen wageearn =rowtotal(h8q31a h8q31b)
	gen year_wage_main = wageearn*year_hr_main if h8q31c==1
	replace year_wage_main = wageearn*day_perweek*week_permonth*month_peryear if h8q31c==2
	replace year_wage_main = wageearn*week_permonth*month_peryear if h8q31c==3
	replace year_wage_main = wageearn*month_peryear if h8q31c==4
	replace year_wage_main = wageearn if h8q31c==5

	//second job hours
	rename h8q43 hour_perweek_sec 
	rename h8q44b week_permonth_sec 
	rename h8q44 month_peryear_sec 
	gen year_hr_sec = hour_perweek_sec*week_permonth_sec*month_peryear_sec
	//Second job pay: we don't have info of working days per week so we construct this only for those who get daily wage by using proxy that people work 8 hours a day
	gen day_perweek_sec = 0 if hour_perweek_sec==0 & h8q45c == 2
	replace day_perweek_sec =1 if hour_perweek_sec>0 & hour_perweek_sec<=8 & h8q45c == 2
	replace day_perweek_sec =2 if hour_perweek_sec>8 & hour_perweek_sec<=16 & h8q45c == 2
	replace day_perweek_sec =3 if hour_perweek_sec>16 & hour_perweek_sec<=24 & h8q45c == 2
	replace day_perweek_sec =4 if hour_perweek_sec>24 & hour_perweek_sec<=32 & h8q45c == 2
	replace day_perweek_sec =5 if hour_perweek_sec>32 & hour_perweek_sec<=40 & h8q45c == 2
	egen wageearn_sec =rowtotal(h8q45a h8q45b)
	gen year_wage_sec = wageearn_sec*year_hr_sec if h8q45c==1
	replace year_wage_sec = wageearn_sec*day_perweek_sec*week_permonth_sec*month_peryear_sec if h8q45c==2
	replace year_wage_sec = wageearn_sec*week_permonth_sec*month_peryear_sec if h8q45c==3
	replace year_wage_sec = wageearn_sec*month_peryear_sec if h8q45c==4
	replace year_wage_sec = wageearn_sec if h8q45c==5
	
		//usual01 job hours
	rename h8q52_2 hour_perweek_us01 
	rename h8q52_1 week_permonth_us01 
	replace week_permonth_us01 = 4 if week_permonth_us01==12
	rename h8q52 month_peryear_us01 
	gen year_hr_us01 = hour_perweek_us01*week_permonth_us01*month_peryear_us01
	//Second job pay: we don't have info of working days per week so we construct this only for those who get daily wage by using proxy that people work 8 hours a day
	// In this case, some workers work more than 7 days a week, we can think of those extra days as wage for working over time
	gen day_perweek_us01 = 0 if hour_perweek_us01==0 & h8q53c == 2
	replace day_perweek_us01 =1 if hour_perweek_us01>0 & hour_perweek_us01<=8 & h8q53c == 2
	replace day_perweek_us01 =2 if hour_perweek_us01>8 & hour_perweek_us01<=16 & h8q53c == 2
	replace day_perweek_us01 =3 if hour_perweek_us01>16 & hour_perweek_us01<=24 & h8q53c == 2
	replace day_perweek_us01 =4 if hour_perweek_us01>24 & hour_perweek_us01<=32 & h8q53c == 2
	replace day_perweek_us01 =5 if hour_perweek_us01>32 & hour_perweek_us01<=40 & h8q53c == 2
	replace day_perweek_us01 =6 if hour_perweek_us01>40 & hour_perweek_us01<=48 & h8q53c == 2
	replace day_perweek_us01 =7 if hour_perweek_us01>48 & hour_perweek_us01<=54 & h8q53c == 2
	replace day_perweek_us01 =8 if hour_perweek_us01>54 & hour_perweek_us01<=62 & h8q53c == 2
	replace day_perweek_us01 =9 if hour_perweek_us01>62 & hour_perweek_us01<=70 & h8q53c == 2
	replace day_perweek_us01 =10 if hour_perweek_us01>70 & hour_perweek_us01<=78 & h8q53c == 2
	egen wageearn_us01 =rowtotal(h8q53a h8q53b)
	gen year_wage_us01 = wageearn_us01*year_hr_us01 if h8q53c==1
	replace year_wage_us01 = wageearn_us01*day_perweek_us01*week_permonth_us01*month_peryear_us01 if h8q53c==2
	replace year_wage_us01 = wageearn_us01*week_permonth_us01*month_peryear_us01 if h8q53c==3
	replace year_wage_us01 = wageearn_us01*month_peryear_us01 if h8q53c==4
	replace year_wage_us01 = wageearn_us01 if h8q53c==5
	
		//usual02 job hours
	rename h8q57_2 hour_perweek_us02 
	replace hour_perweek_us02 = 48 if hour_perweek_us02==5000	//Fixing error report
	rename h8q57_1 week_permonth_us02
	replace week_permonth_us02=4 if week_permonth_us02==19600	//Fixing error report
	replace week_permonth_us02=4 if week_permonth_us02==4000	//Fixing error report
	replace week_permonth_us02=4 if week_permonth_us02==12	//Fixing error report
	replace week_permonth_us02=4 if week_permonth_us02==9	//Fixing error report
	replace week_permonth_us02=4 if week_permonth_us02==6	//Fixing error report
	rename h8q57 month_peryear_us02 
	gen year_hr_us02 = hour_perweek_us02*week_permonth_us02*month_peryear_us02
	//Second job pay: we don't have info of working days per week so we construct this only for those who get daily wage by using proxy that people work 8 hours a day
	// In this case, some workers work more than 7 days a week, we can think of those extra days as wage for working over time
	gen day_perweek_us02 = 0 if hour_perweek_us02==0 & h8q58c == 2
	replace day_perweek_us02 =1 if hour_perweek_us02>0 & hour_perweek_us02<=8 & h8q58c == 2
	replace day_perweek_us02 =2 if hour_perweek_us02>8 & hour_perweek_us02<=16 & h8q58c == 2
	replace day_perweek_us02 =3 if hour_perweek_us02>16 & hour_perweek_us02<=24 & h8q58c == 2
	replace day_perweek_us02 =4 if hour_perweek_us02>24 & hour_perweek_us02<=32 & h8q58c == 2
	replace day_perweek_us02 =5 if hour_perweek_us02>32 & hour_perweek_us02<=40 & h8q58c == 2
	replace day_perweek_us02 =6 if hour_perweek_us02>40 & hour_perweek_us02<=48 & h8q58c == 2
	replace day_perweek_us02 =7 if hour_perweek_us02>48 & hour_perweek_us02<=54 & h8q58c == 2
	replace day_perweek_us02 =8 if hour_perweek_us02>54 & hour_perweek_us02<=62 & h8q58c == 2
	replace day_perweek_us02 =9 if hour_perweek_us02>62 & hour_perweek_us02<=70 & h8q58c == 2
	replace day_perweek_us02 =10 if hour_perweek_us02>70 & hour_perweek_us02<=78 & h8q58c == 2
	egen wageearn_us02 =rowtotal(h8q58a h8q58b)
	gen year_wage_us02 = wageearn_us02*year_hr_us02 if h8q58c==1
	replace year_wage_us02 = wageearn_us02*day_perweek_us02*week_permonth_us02*month_peryear_us02 if h8q58c==2
	replace year_wage_us02 = wageearn_us02*week_permonth_us02*month_peryear_us02 if h8q58c==3
	replace year_wage_us02 = wageearn_us02*month_peryear_us02 if h8q58c==4
	replace year_wage_us02 = wageearn_us02 if h8q58c==5
//Collapse
sort HHID PID
gen byte worker = 1 if h8q4==1 | h8q6==1 | h8q8==1 | h8q10==1 | h8q12==1 
replace worker =0 if worker==.
collapse (sum) year_* worker, by(HHID PID)
egen indi_laboursupply_year_2013 = rowtotal(year_hr*)
save "indi_laboursupply_year_2013_b.dta", replace		//Individual labour supply

collapse (sum) year_* indi_laboursupply_year_2013, by(HHID)
rename indi_laboursupply_year_2013 hh_laboursupply_year_2013
egen hh_labourincome_year_2013 = rowtotal(year_wage*)
save "hh_labourincome_year_2013.dta", replace

//////////////////
///OTHER INCOME///
//////////////////
//We use only GSEC11B, not with GSEC11A becasue it is redundant.
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC11A.dta"
destring HHID, replace
*format HHID %16.0f
egen otherincome_2013 = rowtotal(h11q5 h11q6)
collapse (sum) otherincome_2013, by(HHID)
save "otherincome_2013.dta", replace

/////merge/////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "enter_profit_2013.dta"
merge 1:1 HHID using "hh_labourincome_year_2013.dta"
drop _merge
merge 1:1 HHID using "otherincome_2013.dta"
drop _merge

keep HHID enter_profit_2013 hh_laboursupply_year_2013 hh_labourincome_year_2013 otherincome_2013
egen hh_nonagri_income_2013 = rowtotal (enter_profit_2013 hh_labourincome_year_2013 otherincome_2013)
label var enter_profit_2013 "Household income from business, 2013"
label var hh_laboursupply_year_2013 "Household labour supply (hours), 2013"
label var hh_labourincome_year_2013 "Household labour income, 2013"
label var otherincome_2013 "Household other income, 2013"
label var hh_nonagri_income_2013 "Household non-agricultural income, 2013"
save "hh_nonagri_income_2013.dta",replace
