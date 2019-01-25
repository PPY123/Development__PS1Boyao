cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"

//Median price data 2013: Foods
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15B.dta"
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta" // all matched
//, keepusing(regurb)	
sort itmcd untcd regurb
by itmcd untcd regurb: egen m_price_2013 =  median(h15bq12)  // market price
by itmcd untcd regurb: egen f_price_2013 = median(h15bq13)		// farm gate price
collapse (median) m_price_2013 f_price_2013 , by( itmcd untcd regurb)
label var m_price_2013 "Median market price, by region, 2013"
label var f_price_2013 "Median farm-gate price, by region, 2013"
save "Median_foodprices_2013.dta", replace

//Median price data 2013: Non durable
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15C.dta"
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta"	//
///, keepusing(regurb)
drop if _merge==2
sort itmcd h15cq3 regurb
collapse (median) h15cq10 , by( itmcd h15cq3 regurb)
rename h15cq10 nd_price_2013
label var nd_price_2013 "Median market price, by region, 2013"
save "Median_nondurableprices_2013.dta", replace


//////////////////////////////////////////////////
////Food consumption per household Section 15B////
//////////////////////////////////////////////////
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15B.dta"
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
drop _merge
// Merge median price of each product and size
merge m:1 itmcd untcd regurb using "Median_foodprices_2013.dta"	///
, keepusing(m_price_2013 f_price_2013)	//Merge variables of market and farm prices
egen tt_con_q = rowtotal(h15bq4 h15bq6 h15bq8 h15bq10)
gen tt_con01 = tt_con_q*m_price_2013
// Not all item has market price and farm gate price, for example foods buying outside home,
// so I replace these empty entries with consumption value when quatity is not available
replace tt_con01 = h15bq15 if m_price_2013 == . & tt_con01 == .		// Now we have total consumption value with median market price

// Then, to recheck, we generate total consumption value from the questionaire
// We sum up quantities instead of using total value, h15bq15, because there are 60 observation that both variables are not equal and it seems that this generated one is more consistent
egen tt_con02 = rowtotal(h15bq5 h15bq7 h15bq9 h15bq11)	// Sum up quantities

collapse (sum) tt_con02 tt_con01 , by(HHID)		// Sum up within household consumption of both
rename tt_con01 hh_food_con01_week_2013
label var hh_food_con01_week_2013 "Weekly household comsuption (2013, median market price)"
rename tt_con02 hh_food_con02_week_2013
label var hh_food_con02_week_2013 "Weekly household comsuption (2013, market price)"
save "hh_food_con_week_2013.dta", replace

//////////////////////////////////////////
/// Non durable consumption Section 15C///
//////////////////////////////////////////
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15C.dta"
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
drop _merge		// There are 4 households that don't report any item in this data sheet. I will keep tham here with zero entry.
merge m:1 itmcd h15cq3 regurb using "Median_nondurableprices_2013.dta" // //Merge median market prices of non durable goods
egen tt_nondurable01_q = rowtotal(h15cq4 h15cq6 h15cq8)	// Gen total quantity of each item
gen tt_nondurable01 = tt_nondurable01_q * nd_price_2013	// Gen value using median mkt price
// Rent, imputed rent, water, and electricity bill are recorded only in value. Then we replace missing with these values.
replace tt_nondurable01 = h15cq5 if tt_nondurable01==. & nd_price_2013 ==.
replace tt_nondurable01 = h15cq7 if tt_nondurable01==. & nd_price_2013 ==.
replace tt_nondurable01 = h15cq9 if tt_nondurable01==. & nd_price_2013 ==.

//Gen tt_nondurable02 using value from the data sheet to recheck
egen tt_nondurable02 = rowtotal(h15cq5 h15cq7 h15cq9)

collapse (sum) tt_nondurable01 tt_nondurable02 , by(HHID)		// Sum up within household of both
rename tt_nondurable01 hh_nondurable01_month_2013
label var hh_nondurable01_month_2013 "Monthly household non-durable consumption (2013, median market price)"
rename tt_nondurable02 hh_nondurable02_month_2013
label var hh_nondurable02_month_2013 "Monthly household non-durable consumption (2013, market price)"
save "hh_nondurable_month_2013.dta", replace


//////////////////////////////////////
/// Durable consumption Section 15D///
//////////////////////////////////////
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15D.dta"
//Gen tt_nondurable02 using value from the data sheet to recheck
egen tt_durable02 = rowtotal(h15dq3 h15dq4 h15dq5)
collapse (sum) tt_durable , by(HHID)		// Sum up within household of both
rename tt_durable hh_durable_year_2013
label var hh_durable_year_2013 "Annual household durable consumption (2010, market price)"
save "hh_durable_year_2013.dta", replace

///////////////////////
///MERGE CONSUMPTION///
///////////////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "hh_food_con_week_2013.dta"
gen hh_food_con_year_2013 = hh_food_con01_week_2013*52
keep HHID hh_food_con_year_2013
merge 1:1 HHID using "hh_nondurable_month_2013.dta", keepusing (hh_nondurable01_month_2013)
drop _merge
gen hh_nondurable_year_2013 = hh_nondurable01_month_2013*12
drop hh_nondurable01_month_2013
merge 1:1 HHID using "hh_durable_year_2013.dta"
drop _merge
egen hh_consumption_year_2013 = rowtotal(hh_food_con_year_2013 hh_nondurable_year_2013 hh_durable_year_2013)
label var hh_food_con_year_2013 "Household food consumption, 2013"
label var hh_nondurable_year_2013 "Household non-durable consumption, 2013"
label var hh_durable_year_2013 "Household durable consumption, 2013"
label var hh_consumption_year_2013 "Household total consumption, 2013"
save "hh_consumption_year_2013.dta", replace
