////////////////////////
///COMBINE DATASHEETS///
////////////////////////
clear all
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC2.dta"
keep HHID PID h2q3 h2q4 h2q8 h2q9a h2q9b h2q9c h2q10 
merge 1:1 HHID PID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC4.dta", keepusing(h4q5 h4q7)
drop _merge
*destring HHID, replace
format HHID %16.0f
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta", keepusing(region regurb urban month year)
drop _merge

*bysort HHID: egen hhsize = count(HHID) gives me type mismatch error i will take it into account later
rename h2q3 sex
rename h2q4 hhstatus
rename h2q8 age
rename h2q9a br_day
rename h2q9b br_mon
rename h2q9c br_yr
rename h2q10 marital
rename h4q5 school_status
rename h4q7 education

///Now we have individual dataset
/////////////
////MERGE////
/////////////
merge m:1 HHID using "hh_consumption_year_2013.dta"
drop _merge
merge m:1 HHID using "hh_nonagri_income_2013.dta"
drop _merge
merge m:1 HHID using "wealth.dta"
drop _merge
merge m:1 HHID PID using "indi_laboursupply_year_2013.dta"
drop _merge
save "hh_income_nonagri2013,dta",replace

////Now merge the Agri_profit
clear
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\hh_income_nonagri2013.dta"
merge m:1 HHID using "agri_profit_2013.dta"
drop _merge
egen hh_ttincome_2013 = rowtotal(otherincome_2013 hh_nonagri_income_2013 agri_profit_2013)
label var hh_ttincome_2013 "Household total income, 2013"

//////////////
///TRIMMING///
//////////////
//Trim out top and bottom 2 percent in comsumption, income, and wealth

rename h2q3 sex
rename h2q4 hhstatus
rename h2q8 age
rename h2q9a br_day
rename h2q9b br_mon
rename h2q9c br_yr
rename h2q10 marital
rename h4q5 school_status
rename h4q7 education 
save "uganda_2013_main.dta", replace
////*
*xtile inc_pc = hh_ttincome_2013 if hhstatus==1, nquantiles(100) 
*xtile con_pc = hh_consumption_year_2013 if hhstatus==1, nquantiles(100) 
*xtile weal_pc = hh_wealth_2013 if hhstatus==1, nquantiles(100) 
*gen byte hhtrim = 1 if  hhstatus==1
*replace  hhtrim = 0 if inc_pc>98 & hhstatus==1 | con_pc>98 & hhstatus==1 | weal_pc>98 & hhstatus==1
*replace  hhtrim = 0 if inc_pc<3 & hhstatus==1 | con_pc<3 & hhstatus==1 | weal_pc<3 & hhstatus==1
*bysort HHID: egen trim = total(hhtrim)
*drop inc_pc-hhtrim


clear all
cd "G:\My Drive\Phd\An IDEA\02_21 Development\dev ps\development ps01"
use "uganda_2010_main.dta"
gen dollar = 2360.8374 
gen annual_consumption_pc_2010 = hh_consumption_year_2010/hhsize
gen annual_income_pc_2010 = hh_ttincome_2010/hhsize
label var annual_consumption_pc_2010 "Household consumption per capita, 2010"
label var annual_income_pc_2010 "Household income per capita, 2010"
label var land_value_2010 "Land value including agricultural lands, 2010"

global list01 hh_consumption_year_2010 annual_consumption_pc_2010 hh_nondurable_year_2010	///
hh_durable_year_2010 hh_ttincome_2010 annual_income_pc_2010 agri_profit_2010 	///
hh_labourincome_year_2010 hh_nonagri_income_2010 hh_wealth_2010 land_value_2010

global list02 hh_consumption_year_2010 hh_ttincome_2010 hh_wealth_2010

foreach var of varlist $list01  {
replace `var'=`var'/dollar
}
///1.1///
estpost sum $list01 if hhstatus==1 & trim==1 & urban==0
est store a
estpost sum $list01 if hhstatus==1 & trim==1 & urban==1
est store b
 esttab a b using "q1_1.tex" , replace label  ///
cells("mean(pattern(1 1) fmt(0)) sd(pattern(1 1) fmt(0)) count(pattern(1 1) fmt(0))") ///
 mtitles("Rural" "Urban") title("Summary CIW Uganda, current USD, 2010"\label{CIW}) ///
addnote("Note: Current USD is 2360.8374 UGX on 31/10/2010.")
