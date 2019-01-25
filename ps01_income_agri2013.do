cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"


//Consumption of output price per kilogram
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC5A.dta"
sort cropID a5aq6c a5aq6b
collapse (median) a5aq6d, by( cropID a5aq6b)
rename a5aq6d median_kgconvertor01
replace median_kgconvertor01 = 1 if a5aq6b == 1
rename a5aq6b untcd
merge m:1 cropID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\cropid_itmcd.dta", keepusing(itmcd)
keep if _merge==3
drop _merge
sort itmcd untcd
quietly by itmcd untcd:  gen dup = cond(_N==1,0,_n)
keep if dup==0
save "food_tokg_convertor.dta", replace

clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC15B.dta"
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1.dta", keepusing(regurb)		//Merge variable region from GSEC1
drop _merge
merge m:1 itmcd untcd using "food_tokg_convertor.dta"
keep if _merge==3
drop _merge

sort cropID itmcd untcd regurb
collapse (median) h15bq12 , by(cropID itmcd regurb)
rename h15bq12 m_price_2013_kg
label var m_price_2013_kg "Median market price per kilogram, by region, 2013"
save "Median_foodprices_kg_2013.dta", replace

/////////////////////////
///Agricultural profit///
/////////////////////////

////////////
//1. Costs//
////////////
//1.1: Rent paid for rights to use
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC2B.dta"
destring HHID, replace
*format HHID %16.0f
sort HHID
rename a2bq9 rent_paid_year_2013
collapse (sum) rent_paid_year_2013 , by(HHID)		// Sum up within household of both
label var rent_paid_year_2013 "Annual household rent paid, 2013"
save "rent_paid_year_2013.dta", replace

//1.2: Input cost (a3aq8 a3aq18 a3aq27) and labour cost
	//1st Season
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC3A.dta"
destring HHID, replace
format HHID %16.0f
sort HHID
rename a3aq8 org_fertilizers_s1 
rename a3aq18 chem_fertilizers_s1
rename a3aq27 pesticides_s1 
rename a3aq36 labourcost_s1
collapse (sum) org_fertilizers_s1 chem_fertilizers_s1 pesticides_s1 labourcost_s1 , by(HHID)
save "inputcost_s1_2013.dta", replace

		//S1 Seeds
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC4A.dta"
destring HHID, replace
*format HHID %16.0f
sort HHID
rename a4aq15 seeds_s1
collapse (sum) seeds_s1, by(HHID)
save "inputcost_seeds_s1_2013.dta", replace

	//2nd Season
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC3B.dta"
sort HHID
destring HHID, replace
format HHID %16.0f
rename a3bq8 org_fertilizers_s2 
rename a3bq18 chem_fertilizers_s2
rename a3bq27 pesticides_s2 
rename a3bq36 labourcost_s2
collapse (sum) org_fertilizers_s2 chem_fertilizers_s2 pesticides_s2 labourcost_s2 , by(HHID)
save "inputcost_s2_2013.dta", replace

		//S2 Seeds
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC4B.dta"
destring HHID, replace
format HHID %16.0f
sort HHID
rename a4bq15 seeds_s2
collapse (sum) seeds_s2, by(HHID)
save "inputcost_seeds_s2_2013.dta", replace

///////////////
//Farm Output//
///////////////

	//Gen a file of kg convertor
	clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC5A.dta"
destring HHID, replace
format HHID %16.0f
sort cropID a5aq6b
collapse (median) a5aq6d, by(cropID a5aq6b)
rename a5aq6d median_kgconvertor02
*rename a5aq6b a5aq7b
rename a5aq6b a5aq7c
save "median_kgconvertor02.dta", replace
rename a5aq7c a5bq7c
save "median_kgconvertor02_s2.dta", replace

	//1st Season
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC5A.dta"
destring HHID, replace
format HHID %16.0f
		// For total output
sort cropID a5aq7c
by cropID a5aq7c : egen median_kgconvertor01 = median(a5aq6d)	
gen output_kg = a5aq6a*median_kgconvertor01

		// For sale output: Note that we need to separate this convertor from the previous since the selling product might be in different unit
sort cropID a5aq7c
merge m:1 cropID a5aq7c using "median_kgconvertor02.dta"
drop if _merge==2
drop _merge
gen saleoutput_kg = a5aq7a*median_kgconvertor02

//Convert all home used quantities into kg
rename a5aq12 gift
rename a5aq13 consume
rename a5aq14a food_prod
rename a5aq14b animal
rename a5aq15 forseed
rename a5aq21 stored
foreach var of varlist gift consume food_prod animal forseed stored {
gen `var'_kg = `var'*median_kgconvertor01
}
rename a5aq16 percentloss
gen loss = percentloss*output_kg/100
egen output02_kg = rowtotal(saleoutput_kg gift_kg consume_kg food_prod_kg animal_kg forseed_kg stored_kg)
count if output_kg==output02_kg + loss
count if output_kg>output02_kg + loss	// Possible during the process
count if output_kg<output02_kg + loss	// Should not be possible
//After checking, we go with output02_kg

//Output median farm-gate price per kg
gen farm_price_kg_2013 = a5aq8/saleoutput_kg
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1BOYAO.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
sort cropID regurb
drop if _merge==2
drop _merge
by cropID regurb: egen median_f_cropprice_2013 = median(farm_price_kg_2013)		// farm gate price
//Merge with consumption price
merge m:1 cropID regurb using "Median_foodprices_kg_2013.dta", keepusing(m_price_2013_kg)		//Merge variable region from GSEC1
drop if _merge==2
drop _merge

//Calculate value of output
	// Sale and stored outputs with farm prices
	gen value_sale_s1=saleoutput_kg*farm_price_kg_2013
	replace value_sale_s1= a5aq8 if saleoutput_kg ==. & a5aq8<.
	gen value_stored_s1=stored*farm_price_kg_2013
	replace value_stored_s1= a5aq8 *stored/ a5aq7a if value_stored_s1 ==. & stored<.
	// Gift, household consumed, food product, animal fed, and seed outputs with consumption
	gen value_gift_s1=gift*median_f_cropprice_2013
	replace value_gift_s1 = gift*farm_price_kg_2013 if value_gift==. & median_f_cropprice_2013 ==.	//replace with farm price if consumption price is not available
	
	gen value_consume_s1=consume*median_f_cropprice_2013
	replace value_consume_s1 = consume*farm_price_kg_2013 if value_consume==. & median_f_cropprice_2013 ==.
	
	gen value_food_prod_s1=food_prod*median_f_cropprice_2013
	replace value_food_prod_s1= food_prod*farm_price_kg_2013 if value_food_prod==. & median_f_cropprice_2013 ==.
	
	gen value_animal_s1=animal*median_f_cropprice_2013
	replace value_animal_s1 = animal*farm_price_kg_2013 if value_animal==. & median_f_cropprice_2013 ==.
	
	gen value_seed_s1=forseed*median_f_cropprice_2013
	replace value_seed_s1 = forseed*farm_price_kg_2013 if value_seed==. & median_f_cropprice_2013 ==.

	egen tt_output_s1 = rowtotal(value_sale_s1 value_stored_s1 value_gift_s1 value_consume_s1 value_food_prod_s1 value_animal_s1 value_seed_s1)
collapse (sum) tt_output_s1 value_sale_s1 value_stored_s1 value_gift_s1 value_consume_s1 value_food_prod_s1 value_animal_s1 value_seed_s1, by(HHID)
save "hh_outputvalue_s1_2013.dta", replace

	//////////////	
	//2nd Season//
	//////////////
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC5B.dta"
destring HHID, replace
format HHID %16.0f
		// For total output
sort cropID a5bq6c
by cropID a5bq6c : egen median_kgconvertor01 = median(a5bq6d)	
gen output_kg = a5bq6a*median_kgconvertor01

		// For sale output: Note that we need to separate this convertor from the previous since the selling product might be in different unit
sort cropID a5bq7c
merge m:1 cropID a5bq7c using "median_kgconvertor02_s2.dta"
drop if _merge==2
drop _merge
gen saleoutput_kg = a5bq7a*median_kgconvertor02

//Convert all home used quantities into kg
rename a5bq12 gift
rename a5bq13 consume
rename a5bq14a food_prod
rename a5bq14b animal
rename a5bq15 forseed
rename a5bq21 stored
foreach var of varlist gift consume food_prod animal forseed stored {
gen `var'_kg = `var'*median_kgconvertor01
}
rename a5bq16 percentloss
gen loss = percentloss*output_kg/100
egen output02_kg = rowtotal(saleoutput_kg gift_kg consume_kg food_prod_kg animal_kg forseed_kg stored_kg)
count if output_kg==output02_kg + loss
count if output_kg>output02_kg + loss	// Possible during the process
count if output_kg<output02_kg + loss	// Should not be possible
//After checking, we go with output02_kg

//Output median farm-gate price per kg
gen farm_price_kg_2013 = a5bq8/saleoutput_kg
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1BOYAO.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
sort cropID regurb
drop if _merge==2
drop _merge
by cropID regurb: egen median_f_cropprice_2013 = median(farm_price_kg_2013)		// farm gate price
//Merge with consumption price
merge m:1 cropID regurb using "Median_foodprices_kg_2013.dta", keepusing(m_price_2013_kg)		//Merge variable region from GSEC1
drop if _merge==2
drop _merge

//Calculate value of output
	// Sale and stored outputs with farm prices
	gen value_sale_s2=saleoutput_kg*farm_price_kg_2013
	replace value_sale_s2= a5bq8 if saleoutput_kg ==. & a5bq8<.
	gen value_stored_s2=stored*farm_price_kg_2013
	replace value_stored_s2= a5bq8 *stored/ a5bq7a if value_stored_s2 ==. & stored<.
	// Gift, household consumed, food product, animal fed, and seed outputs with consumption
	gen value_gift_s2=gift*median_f_cropprice_2013
	replace value_gift_s2 = gift*farm_price_kg_2013 if value_gift==. & median_f_cropprice_2013 ==.	//replace with farm price if consumption price is not available
	
	gen value_consume_s2=consume*median_f_cropprice_2013
	replace value_consume_s2 = consume*farm_price_kg_2013 if value_consume==. & median_f_cropprice_2013 ==.
	
	gen value_food_prod_s2=food_prod*median_f_cropprice_2013
	replace value_food_prod_s2= food_prod*farm_price_kg_2013 if value_food_prod==. & median_f_cropprice_2013 ==.
	
	gen value_animal_s2=animal*median_f_cropprice_2013
	replace value_animal_s2 = animal*farm_price_kg_2013 if value_animal==. & median_f_cropprice_2013 ==.
	
	gen value_seed_s2=forseed*median_f_cropprice_2013
	replace value_seed_s2 = forseed*farm_price_kg_2013 if value_seed==. & median_f_cropprice_2013 ==.

	egen tt_output_s2 = rowtotal(value_sale_s2 value_stored_s2 value_gift_s2 value_consume_s2 value_food_prod_s2 value_animal_s2 value_seed_s2)
collapse (sum) tt_output_s2 value_sale_s2 value_stored_s2 value_gift_s2 value_consume_s2 value_food_prod_s2 value_animal_s2 value_seed_s2, by(HHID)
save "hh_outputvalue_s2_2013.dta", replace

/////////////
//LIVESTOCK//
/////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
		//Livestock 6A
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC6A.dta"
destring HHID, replace
format HHID %16.0f
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1Boyao.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
drop if _merge==2
drop _merge
gen tt_livestock_2013 = a6aq7+a6aq8+a6aq9-a6aq10--a6aq11-a6aq12+a6aq13a -a6aq14a-a6aq15
	//Gen median price
sort LiveStockID regurb
gen buy = a6aq13b
gen sell = a6aq14b
by LiveStockID regurb: egen buy_price_2013 = median(buy)	
by LiveStockID regurb: egen sell_price_2013 = median(sell)
gen wealth_livestock_2013 = sell_price_2013*tt_livestock_2013	// Total wealth from livestock is evaluated from price sold
gen livestock_cost_2013 = a6aq13a*buy_price_2013
gen livestock_revenue_2013 = a6aq14a*sell_price_2013
collapse (sum) wealth_livestock_2013 livestock_cost_2013 livestock_revenue_2013, by(HHID)
save "hh_income_livestock_2013.dta", replace

		//Small Livestock 6B last 12 month
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC6B.dta"
destring HHID, replace
format HHID %16.0f
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1BOYAO.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
drop if _merge==2
drop _merge
gen tt_livestock_2013 = a6bq7+a6bq8+a6bq9-a6bq10-a6bq11-a6bq12 + a6bq13a-a6bq14a-a6bq15
	//Gen median price
sort ALiveStock_Small_ID regurb
gen buy = a6bq13b
gen sell = a6bq14b
by ALiveStock_Small_ID regurb: egen buy_price_2013 = median(buy)	
by ALiveStock_Small_ID regurb: egen sell_price_2013 = median(sell)
gen s_wealth_livestock_2013 = sell_price_2013*tt_livestock_2013	// Total wealth from livestock is evaluated from price sold
gen s_livestock_cost_2013 = a6bq13a*buy_price_2013
gen s_livestock_revenue_2013 = a6bq14a*sell_price_2013
collapse (sum) s_wealth_livestock_2013 s_livestock_cost_2013 s_livestock_revenue_2013, by(HHID)
replace s_livestock_cost_2013 = s_livestock_cost_2013		//convert to annual
replace s_livestock_revenue_2013 = s_livestock_revenue_2013		//convert to annual
save "hh_income_livestocksmall_2013.dta", replace

//Poultry
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC6C.dta"
destring HHID, replace
format HHID %16.0f
merge m:1 HHID using "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\GSEC1BOYAO.dta"	///
, keepusing(regurb)		//Merge variable region from GSEC1
drop if _merge==2
drop _merge
gen tt_livestock_2013 = a6cq7+a6cq8+a6cq9-a6cq10-a6cq11-a6cq12+a6cq13a - a6cq14a-a6cq15
	//Gen median price
sort APCode regurb
gen buy = a6cq13b
gen sell = a6cq14b
by APCode regurb: egen buy_price_2013 = median(buy)	
by APCode regurb: egen sell_price_2013 = median(sell)
gen p_wealth_livestock_2013 = sell_price_2013*tt_livestock_2013	// Total wealth from livestock is evaluated from price sold
gen p_livestock_cost_2013 = a6cq13a*buy_price_2013
gen p_livestock_revenue_2013 = a6cq14a*sell_price_2013
collapse (sum) p_wealth_livestock_2013 p_livestock_cost_2013 p_livestock_revenue_2013, by(HHID)
replace p_livestock_cost_2013 = p_livestock_cost_2013*4		//convert to annual
replace p_livestock_revenue_2013 = p_livestock_revenue_2013*4		//convert to annual
save "hh_income_livestockpoultry_2013.dta", replace

//livestock input
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC7.dta"
destring HHID, replace
format HHID %16.0f
collapse (sum) a7bq2e, by(HHID)
rename a7bq2e inputcost_livestock_2013
save "inputcost_livestock_2013.dta", replace

//livestock outputs
//meat
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC8A.dta"
destring HHID, replace
format HHID %16.0f
//There are only 30 items that have been slaguthed and sold in the datasheet. We don't use median price method but just the reported value
rename a8aq5 livestockproduct__income_2013
collapse (sum) livestockproduct__income_2013, by(HHID)
save "livestockproduct_income_meat_2013.dta", replace
//milk
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC8B.dta"
destring HHID, replace
format HHID %16.0f
//There are only 30 items that have been slaguthed and sold in the datasheet. We don't use median price method but just the reported value
rename a8bq9 livestockproduct_milk_2013
collapse (sum) livestockproduct_milk_2013, by(HHID)
save "livestockproduct_income_milk_2013.dta", replace
//egg 3 months
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC8C.dta"
destring HHID, replace
format HHID %16.0f
//There are only 30 items that have been slaguthed and sold in the datasheet. We don't use median price method but just the reported value
gen livestockproduct_egg_2013 = a8cq5*4
collapse (sum) livestockproduct_egg_2013, by(HHID)
save "livestockproduct_income_egg_2013.dta", replace

	
/////////other livestock cost
	//extension services
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC9.dta"
destring HHID, replace
format HHID %16.0f
rename a9q9 ext_serv_cost_2013
collapse (sum) ext_serv_cost_2013, by(HHID)
save "ext_serv_cost_2013.dta", replace
	//Machinery
clear all
use "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao\AGSEC10.dta"
destring HHID, replace
format HHID %16.0f
rename a10q8 machine_cost_2013
collapse (sum) machine_cost_2013, by(HHID)
save "machine_cost_2013.dta", replace

///////////////////////////////////
/////////MERGE: Finally!!!/////////
///////////////////////////////////
cd "C:\Users\boyao\Desktop\UAB\Development\PS1Boyao"
///AGRI INCOME///
clear all
use "hh_outputvalue_s1_2013.dta"
merge 1:1 HHID using "hh_outputvalue_s1_2013.dta"
drop _merge
merge 1:1 HHID using "hh_outputvalue_s2_2013.dta"
drop _merge
merge 1:1 HHID using "hh_income_livestock_2013.dta"
drop _merge
merge 1:1 HHID using "hh_income_livestocksmall_2013.dta"
drop _merge
merge 1:1 HHID using "hh_income_livestockpoultry_2013.dta"
drop _merge
merge 1:1 HHID using "livestockproduct_income_meat_2013.dta"
drop _merge
merge 1:1 HHID using "livestockproduct_income_milk_2013.dta"
drop _merge
merge 1:1 HHID using "livestockproduct_income_egg_2013.dta"
drop _merge

//Cost
merge 1:1 HHID using "rent_paid_year_2013.dta"
drop _merge
merge 1:1 HHID using "inputcost_s1_2013.dta"
drop _merge
merge 1:1 HHID using "inputcost_seeds_s1_2013.dta"
drop _merge
merge 1:1 HHID using "inputcost_s2_2013.dta"
drop _merge
merge 1:1 HHID using "inputcost_seeds_s2_2013.dta"
drop _merge
merge 1:1 HHID using "inputcost_livestock_2013.dta"
drop _merge
merge 1:1 HHID using "ext_serv_cost_2013.dta"
drop _merge
merge 1:1 HHID using "machine_cost_2013.dta"
drop _merge

egen agri_income_2013 =  rowtotal(tt_output_s1 tt_output_s2 livestock_revenue_2013 s_livestock_revenue_2013 p_livestock_revenue_2013 ///
inputcost_livestock_2013)

egen agri_cost_2013 =  rowtotal(rent_paid_year_2013 org_fertilizers_s1 chem_fertilizers_s1 pesticides_s1 labourcost_s1 seeds_s1	///
org_fertilizers_s2 chem_fertilizers_s2 pesticides_s2 labourcost_s2 seeds_s2 livestock_cost_2013 ///
inputcost_livestock_2013 ext_serv_cost_2013 machine_cost_2013)

gen agri_profit_2013 = agri_income_2013 - agri_cost_2013
keep agri_income_2013 agri_cost_2013 agri_profit_2013 HHID
label var agri_income_2013 "Household agricultural revenue, 2013"
label var agri_cost_2013 "Household agricultural cost, 2013"
label var agri_profit_2013 "Household agricultural profit, 2013"
save "agri_profit_2013.dta", replace
