



pcd = 'paycalcdata'; /* SAVING CALCULATOR DATA */

pd = 'paydata'; /* SAVING CALCULATOR DATA FOR AM SCHEDULE */

numDays = 60;  /* DAYS UNTIL COOKIE EXPIRES (EG. 183 DAYS = 6 MONTHS) */



//------------------------------------



/* FOR FRENCH USERS WHO WILL INPUT A COMMA AS A DECIMAL PLACE, THIS FUNCITON CONVERTS THE COMMA TO A DECIMAL */

function changeToDecimal(a){

// input value to be changed; output lastnum, which is the same number in English format for calculations.

if (a.value!= null) {

	var firstnum = a.value;

	}

	else {

	var firstnum = a;

	firstnum += "";

	}



var u = firstnum.indexOf(",");

if (u > 0){

	var beginnum = firstnum.substring(0, u);

	var endnum = firstnum.substring((u+1),firstnum.length);

	var lastnum = (beginnum + "." + endnum);

	}

	else{

	var lastnum = firstnum;

	}

return lastnum;

}



/* FOR FRENCH USERS THAT WANT A DECIMAL CHANGED TO A COMMA FOR OUTPUT */

function changeToComma(a){

// input value to be changed; output lastnum, which is the same number in French format for display.

if (a.value!= null) {

	var firstnum = a.value;

	}

	else {

	var firstnum = a;

	firstnum += "";

	}



var u = firstnum.indexOf(".");

if (u > 0){

	var beginnum = firstnum.substring(0, u);

	var endnum = firstnum.substring((u+1),firstnum.length);

	var lastnum = (beginnum + "," + endnum);

	}

	else{

	var lastnum = firstnum;

	}

return lastnum;

}





/* FUNCTION THAT ADDS COMMAS TO THE CURRENCY VALUE (i.e. $1000000.00 -> $1 000 000,00) */



function addCommas(currencyValue){

	currencyValue = "" + currencyValue;

	var dollars = 0;

	var cents = "";

	if ( currencyValue.indexOf(",") != -1 ) {

		return currencyValue;

	} else if ( currencyValue.indexOf(".") != -1 ){

		dollars = currencyValue.substring(0,currencyValue.indexOf("."));

		cents = currencyValue.substring(currencyValue.indexOf("."),currencyValue.length);

	} else if ( currencyValue > 0 ){

		dollars = currencyValue;

	} else {

		return currencyValue;

	}

	var returnValue = "";

	for (var i=1;i<=dollars.length;i++){

		if (i % 3 == 1 && i != 1){

			returnValue = " " + returnValue;// uses space instead of a comma for thousands separator.

		}

		returnValue = dollars.charAt(dollars.length - i) + returnValue;

	}

	returnValue += cents;

	returnValue = changeToComma(returnValue);//call French formatting function

	return returnValue;

}





//------------------------------------



/*THE FOLLOWING TWO FUNCTIONS CHECK THAT ALL NUMERIC VALUES ARE REAL NUMBER AND REMOVE DOUBLE DECIMALS */

function check(a)

{

var pest = 0;

var b = "";

for(i=0;i<=a.length;i++){

   var u = a.charAt(i);

   if((u>="0"&&u<="9")||u=="."||u==","){

     	if(u=="."){

      		var pest = pest+1;

      		if(pest==2){

      			break;

      		}

      	}

		var b = b + u;

	}

}

return b;

}



//------------------------------------



function doSum(a){

a.value = check(a.value);

}



//------------------------------------



/* TESTS VERSIONS FOR WHICH WILL SUPPORT POP UP WINDOWS */

function versTest()

{

var one = '';

var two = '';

if ((navigator.appName.substring(0,8)=="Netscape" && (navigator.appVersion.substring(0,3) == "3.0" ||  navigator.appVersion.substring(0,3) =="4.0"))){

	var one='true';

}

if((navigator.appName.substring(0,9) == "Microsoft" && navigator.appVersion.substring(0,3) == "3.0" && navigator.appVersion.indexOf("Macintosh")>=0)){

	var two='true';

}

if(one=='true' || two=='true' || (navigator.appName.substring(0,9) == "Microsoft" && navigator.appVersion.indexOf("MSIE 3.0")>=0 && navigator.appVersion.indexOf("Windows 3.1")>=0)){

	return true;

}

else{

	return false;

}

}



//------------------------------------



/* TESTS IF VERSION IS MSIE 3.0 FOR MAC */

function msTest()

{

if(navigator.appName.substring(0,9) == "Microsoft" && (navigator.appVersion.substring(0,3) == "3.0" && navigator.appVersion.indexOf("Macintosh")>=0)){

	return true;

}

else{

	return false;

}

}



//------------------------------------





function nineTest()

{

if(navigator.appName.substring(0,9) == "Microsoft" && (navigator.appVersion.substring(0,3)=="3.0" || navigator.appVersion.indexOf("MSIE 3.0")>=0) && (navigator.appVersion.indexOf("Macintosh")==-1 || navigator.appVersion.indexOf("Windows 3.1")== -1)){

	return true;

}

else{

	return false;

}

}



//------------------------------------



/* OPENS POP UP WINDOW TO DISPLAY VALIDATION MESSAGES IN NETSCAPE 3.0 AND 4.0 */

function fixpro(n,q)

{

if(versTest() == true||nineTest()==true){

	if(msTest()==true){

		var winNam='';

	}

	else{

		var slash = location.href.lastIndexOf("/")+1;

		var filNam = location.href.substring(0,slash);

		var winNam = filNam+'empty.html';

	}

	fix = window.open(winNam,'FIX','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=300,height=100');

	if(navigator.appName.substring(0,8) == "Netscape"){

		fix.focus();

	}

	fix.document.write('<html><head><title>Calculators</title>');

	fix.document.write('</head><body bgcolor=ffffff><form name="fixer">');

	fix.document.write('<font size=2 face="Arial, Helvetica" color=306798>'+n+'</font><p><font size=2 FACE="Arial, Helvetica">'+q+'<p>');

	fix.document.write('<center><input type=button value=OK onClick=self.close()>');

	fix.document.write('</center></form></body></html>');

	fix.document.close();

}

else{

	alert(n+'\n'+q)

}

}



//------------------------------------



/* FUNCTION CONFIRMS THAT THE VALUE ENTERED INTO A FIELD FALLS WITHIN THE PRE-DETERMINED MINIMUM AND MAXIMUM VALUES, AND DISPLAYS AN ERROR MESSAGE WITH THE ALLOWABLE NUMERIC RANGE FOR THE FIELD DATA IN A POP UP VALIDATION WINDOW */

function checkNumber(input, min, max, msg)

{

var str = input.value;

for (var i = 0; i < str.length; i++) {

	var ch = str.substring(i, i + 1)

	if ((ch < "0" || "9" < ch) && ch != '.' && ch != ',') {

    	alert(msg);

    	return false;

	}

}

if(input.value!=""){

	var num = 0 + str

    if (num < min || max < num) {

    	var sendn = msg+":";

   		var sendq = "Vous avez entrer " + input.value + ". Veuillez inscrire un nombre entre " + min + " et " + max + ".";

  		fixpro(sendn,sendq);

		return false;

	}

	input.value = str;

	return true;

}

}



//------------------------------------



/* CALLS UPON THE FUNCTIONS TO DETERMINE IF THE NUMBERS ENTERED ARE VALID AND TO CALCULATE THE RESULTS OF THE ENTERED DATA FOR EXAMPLE - MORTGAGE PAYMENT, GDS AND TDS RATIOS, AND LOAN TO VALUE. THIS FUNCTION IS EXECUTED EVERYTIME A VALUE IS CHANGED IN A FIELD */

function computeField(input,min,max,msage)

{

doSum(input);

return (checkNumber(input,min,max,msage));

}



//------------------------------------



function validAm(input,min,max,msg)

{

doSum(input);

var py = document.prpaycalc;

if(input.name == "NAMORTY"){

	py.NAMORTM.value = 0;

}

if(input.name == "NAMORTM" && py.NAMORTY.value==40){

	fixpro('Question 3: Initial Amortization Period:','The entered amortization period cannot exceed 40 years.');

	input.value = 0;

}

if(input.value > max || input.value < min){

	checkNumber(input,min,max,msg);

	if(input.name == "NAMORTM"){

		input.value = 0;

	}

}

}



//------------------------------------



function amortLink(whatyear)

{

if(navigator.appVersion.substring(0,3) == 2.0 &&  navigator.appName.substring(0,8)=="Netscape" && (navigator.appVersion.indexOf("Macintosh")>=0||navigator.appVersion.indexOf("PowerPC")>=0)){

	if(validResults()==true && computeResults(2,whatyear)==true){

		setTimeout("document.amlump.submit()",100);

	}

}

else{

	if(validResults()==true && computeResults(2,whatyear)==true){

		document.amlump.submit();

	}

}

}



//------------------------------------



function amortonLink()

{

if(validResults==true && validLumps('valid')==true && computeResults(2,0)==true){

	document.amlump.submit();return false;

}

else{

	return false;

}

}



//------------------------------------



function roundReg(n)

{

if(n > 0){

	pennies = n*100;

	pennies = Math.round(pennies);

	strPennies = "" + pennies;

	len = strPennies.length;

	if (len<3 ) {

		var times=3-len;

		for (i=0;i<times; i++) {

			strPennies=0+strPennies;

		}

	}

	len = strPennies.length;

	return strPennies.substring(0, len - 2) + "." + strPennies.substring(len -2, len);

}

else

	return 0;

}



//------------------------------------



function validResults()

{

var py = document.prpaycalc;

if((py.MORTAMT.value == null|| py.MORTAMT.value.length == 0)|| (py.MORTAMT.value <20000|| py.MORTAMT.value > 10000000) ){

	fixpro('Question 1: (Montant de l\'hypoth�que)','Veuillez inscrire un nombre entre 20 000 et 10 000 000.');return false;

}



if((py.MISE.value == null|| py.MISE.value.length == 0)|| (py.MISE.value <1|| py.MISE.value > 10000000) ){

	fixpro('Question 1: (Montant de la mise de fonds)','Veuillez inscrire un nombre entre 1 et 10 000 000.');return false;

}



if((py.RATE.value == null || py.RATE.value.length == 0)||(py.RATE.value < 1 || py.RATE.value > 30)){

	fixpro('Question 2: (Taux d\'int�r�t)','Veuillez inscrire un nombre entre 1,0 et 30,0.');return false;

}



if((py.NAMORTY.value == null || py.NAMORTY.value.length == 0)|| (py.NAMORTY.value < 0 || py.NAMORTY.value > 40)){

fixpro('Question 3: (P�riode d\'amortissement - ans)','Veuillez inscrire un nombre entre 0 et 40.');return false;}



if((py.NAMORTM.value == null || py.NAMORTM.value.length == 0)|| (py.NAMORTM.value < 0 || py.NAMORTM.value > 11)){

fixpro('Question 3: (P�riode d\'amortissement - mois)','Veuillez inscrir un nombre entre 0 et 11.');return false;}



if(py.NAMORTM.value < 6 && py.NAMORTY.value < 1){

fixpro('Question 3: (P�riode d\'amortissement)','Veuillez inscrir un p�riode d\'amortissement au moins 6 mois.');return false;}



if(py.NAMORTM.value==""){

	py.NAMORTM.value = "0"

}



if((py.MAINPAY.value == null|| py.MAINPAY.value.length == 0) || (py.MAINPAY.value<0 || py.MAINPAY.value > 10000000)){

	fixpro('Question 4: (Montant de l\'hypoth�que)','Veuillez inscrir un nombre entre 10000 et 1000000.');return false;

}

/*

if(py.PFREQ.selectedIndex == 0){

	fixpro('Question 5: Payment Frequency','You have not answered this question, click on the PLEASE CHOOSE button to select your option.');return false;

}*/



return true;

}



//------------------------------------



/* CALCULATES VALUES TO BE ENTERED INTO THE TEXT BOXES AT THE BOTTOM OF THE PAGE WHEN THE USER CLICKS ON COMPUTE OR COMPUTE AMORTIZATION */

function computeResults(n,whatyear)

{

var py = document.prpaycalc;



//MORTGAGE SCENARIO INFORMATION

var mortgage = (changeToDecimal(py.MORTAMT.value)*1.0);

var intRate = (changeToDecimal(py.RATE.value)*1.0)/100;

var amortMon = (py.NAMORTM.value*1.0)+(py.NAMORTY.value*1.0*12);

var paymentx = changeToDecimal(py.MAINPAY.value.replace(/['$'|' ']/g, ''))*1.0;

var payment=paymentx;

var payFreq = py.PFREQ.selectedIndex*1.0;

var accel = py.ACCSEL.selectedIndex*1.0;

var numPay1 = calcNumPay(payFreq,1);

var numPay2 = calcNumPay(payFreq,2);

var compFreq = 2;

var intFact = calcIntFact(intRate,compFreq,numPay1);

var compFact = calcCompFact(amortMon,intFact,numPay2);



//CALCULATE REVISED AMORTIZATION FOR COMPARISON

var baseRevAm = calcAmort(mortgage,payment,intFact);

var baseRevAmMonths = Math.round((baseRevAm/numPay2)*12);



//CALCULATE TOTAL INTEREST FOR REGULAR MORTGAGE

var regIntBal = calcBal(mortgage,intFact,payment,baseRevAm);

var regularInterest = (payment*baseRevAm)-(mortgage-regIntBal);



//LUMP SUM PAYMENT DECLARATION

var lumpAmt = py.LUMPAMT.value*1.0;

var lumpTime = py.LUMPYRS.value*1.0;



//MORTGAGE PAYMENT INCREASE DECLARATION

var incpayAmt = py.INCPAY.value*1.0;

var incpayType = py.INCTYPE.selectedIndex*1.0;

var incpayTime = py.INCYEARS.value*1.0;



//SOLVE FOR REVISED AMORTIZATION & INTEREST SAVED;



var principalBal = mortgage;

var prepayInterest = 0;

var annualCount = 1;

var aYear = 0;

var lastInterest=0;

for(payAdd = 1; principalBal>0&&payAdd<=baseRevAm; payAdd ++){

	//SET FLAG IF THIS PAYMENT IS AN ANNIVERSARY

	if(payAdd/Math.floor(numPay1)==annualCount){

		var aYear = 1;}



	//INCREASE MORTGAGE PAYMENT IF REQUESTED

	if(aYear==1&&incpayTime>=annualCount){

		var payment = (incpayType==0) ? roundReg((1.0+(incpayAmt/100))*payment)*1.0 : payment+incpayAmt*1.0; }



	//INTEREST AND PRINCIPAL PAYMENT

	var interestPayment = roundReg(principalBal * intFact)*1.0;

  	var principalPayment =  roundReg(payment - interestPayment)*1.0;

  	var checkBal = (principalPayment > principalBal) ? principalBal : principalPayment;

  	var principalBal =  roundReg(principalBal-checkBal)*1.0;





  	//LUMPSUM PAYMENT IF REQUESTED

  	if(aYear==1&&lumpTime>=annualCount){

  		var checkLump = (lumpAmt > principalBal) ? principalBal : lumpAmt;

  		var principalBal = roundReg(principalBal - checkLump)*1.0;}



	var prepayInterest =  roundReg(prepayInterest+interestPayment)*1.0;

	var realPayment = roundReg(interestPayment+checkBal)*1.0;

	if(principalBal==0){var newPayAdd = payAdd;}

	//RESETS THE ANNIVERSARY

	if(aYear==1){

		var annualCount = annualCount+1;

		var aYear = 0;}

}





//REVISED AMORTIZATION PERIOD & INTEREST SAVINGS DONE

if(principalBal!=0){var newPayAdd = baseRevAm;}

if(realPayment<(payment/2)){var newPayAdd = newPayAdd-1;}



var revAmortMon = Math.round((newPayAdd/numPay2)*12);



var newYrs = Math.floor(revAmortMon/12);

var newMos = revAmortMon % 12;

var savedInterest = roundReg(regularInterest - prepayInterest);



//RETURN RESULTS

py.AMNEWY.value = newYrs;

py.AMNEWM.value = newMos;



if (((py.LUMPAMT.value * py.LUMPYRS.value)>0) || ((py.INCPAY.value * py.INCYEARS.value)>0)){

	py.AMINTSAVE.value = addCommas(savedInterest);

}else{

	py.AMINTSAVE.value = 0;

}

if(n==2){

quickCook(mortgage,paymentx,intFact,numPay2,baseRevAm,intRate,accel,lumpAmt,lumpTime,incpayAmt,incpayType,incpayTime,whatyear);

}



return true;

}



//------------------------------------



function calcPay(mortgage,intfact,compfact){

return roundReg((mortgage*intfact*compfact)/(compfact-1))*1.0;

}



//------------------------------------



function calcIntFact(intrate,compfreq,numpay1){

return Math.pow((1+intrate/compfreq),(compfreq/numpay1))-1;

}



//------------------------------------



function calcCompFact(amort,intfact,numpay2){

var amortPays = Math.floor((amort/12)*numpay2);

return Math.pow((1+intfact),amortPays);

}



//------------------------------------

function calcBal(mortgage,intfact,payment,whatPay){

return roundReg((mortgage*(Math.pow((1.0 + intfact),(whatPay)))) -  ((payment * ((Math.pow((1.0 + intfact),(whatPay))) - 1.0))/intfact))*1.0;

}



//------------------------------------

function calcAccelPay(payment,numpay1){

return roundReg((payment*13)/Math.floor(numpay1))*1.0;

}



//------------------------------------



/*RETURNS CALCULATED AMORTIZATION PERIOD*/

function calcAmort(mortgage,payment,intfact)

{

return Math.round(Math.log(payment/(payment-mortgage*intfact))/Math.log(1+intfact));

}



//------------------------------------



function calcReverseAccel(payment,numpay1){

return roundReg(((payment*Math.floor(numpay1))/13))*1.0;

}



//------------------------------------



function calcMtgAmount(intfact,payment,whatPay){

return roundReg(payment*((Math.pow((1.0 + intfact),(whatPay)))-1)/(intfact*(Math.pow((1.0 + intfact),(whatPay)))));

}



//------------------------------------



/*RETURNS CALCULATED INTEREST RATE*/

function calcRate(mortgage,amortMon,numPay1,numPay2,payment)

{

if (amortMon!=0) {

var lowgs = 0;

var highgs = 99;

var solvePay=0;

var lastRate = 49.5;

var gsRate = (highgs+lowgs)/2;

var chkDif = 10;

var chkPay=10;

for(gsRate;((chkDif>=0.001)||(chkPay>=0.01)&&gsRate>=0.0001);gsRate=(highgs+lowgs)/2){

var intFact = calcIntFact((gsRate/100),2,numPay1);

var compFact = calcCompFact(amortMon,intFact,numPay2);

var solvePay = calcPay(mortgage,intFact,compFact)*1.0;

if(solvePay<payment){

	var lowgs=gsRate;

	var chkPay = roundReg(payment - solvePay)*1.0;}

else{

	var highgs=gsRate;

	var chkPay = roundReg(solvePay- payment)*1.0;}



newRate = (highgs+lowgs)/2;

if(gsRate>newRate){

	var chkDif = gsRate-newRate;}

else{

	var chkDif = newRate-gsRate;}

if(chkDif<0.001||chkPay<0.01){

break;}

}

return gsRate;

}





else {

return 0;

}

}



//-----------------------------------------------



function calcNumPay(freq,n){

if(n==1){

	var numD = 365;

}

if(n==2){

	var numD = 365.25;

}

if(freq==0){

	return 12;

}

if(freq==1){

	return 24;

}

if(freq==2){

	return (numD/14);

}

if(freq==3){

	return (numD/7);

}

}



//------------------------------------





/* SAVES COOKIE CONTAINING DATA TO BE USED IN AMORTIZATION SCHEDULE */

function quickCook(mortgage,payment,intFact,numPay2,baseRevAm,intRate,accel,lumpAmt,lumpTime,incpayAmt,incpayType,incpayTime,whatyear)

{

if (whatyear == -1 ){

	var timeKindA = 0;

}else{

	whatyear = 0;

	var timeKindA = 1;

}



var pdData = " " ;

var pdData = pdData + '`' + mortgage + '`'  + payment + '`' + intFact + '`' + numPay2 + '`' + baseRevAm + '`'  + 0 + '`'  + 0 + '`'  + 3 + '`'  + timeKindA + '`'  +intRate + '`' + accel + '`' + whatyear + '`' +lumpAmt+ '`' +lumpTime+ '`' +incpayAmt+ '`' +incpayType+ '`' +incpayTime;

document.cookie = pd +"=" + escape(pdData) +";path=/" ;

}





//------------------------------------



function prepayCook(startLump,startLumpT,timeLump,incrLump,incrLumpT)

{

var preyears = document.prpaycalc.LUMPYRS.value*1.0;

preyears = changeToDecimal(preyears);

var expire = new Date ();

expire.setTime (expire.getTime() + (numDays * 24 * 3600000));/* 2 MONTHS */

var ppData = " ";

var ppData = ppData + '`' + startLump + '`' + startLumpT + '`' + timeLump + '`' + incrLump + '`' + incrLumpT;

document.cookie = ppd +"=" + escape(ppData) +"; expires=" + expire.toGMTString()+"; path=/" ;

}



//------------------------------------



/* OPENS WINDOW USED TO DISPLAY HELP MESSAGES WHEN THE USER CLICKS ON A HELP BUTTON. THE HELP MESSAGE DISPLAYED IS DETERMINED IN THE ARRAY WHICH IS REFERENCED ACCORDING TO THE HELP BUTTON WHICH WAS CLICKED */

function winopen(name)

{

var linkit = "help/"+name;

if(versTest() == true||nineTest()==true){

	qc=window.open(linkit,'helpscreen','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=250,height=180');

	if(navigator.appName.substring(0,8) == "Netscape"){

		qc.focus();

	}

}

else{

	location.href=linkit;

}

}



//------------------------------------



function controlCompute(n,x)

{

if(navigator.appVersion.substring(0,3) == 2.0 &&  navigator.appName.substring(0,8)=="Netscape" && navigator.appVersion.indexOf("Macintosh")>=0){

	if(validResults()==true){

		setTimeout("computeResults(n,0)",200);

		if(x==1){

			saveWin();

		}

	}

}

else{

	if(validResults()==true){

		computeResults(n,0);

		if(x==1){

			saveWin();

		}

	}

}

}



//------------------------------------



function saveWin()

{



if(versTest() == true||nineTest()==true){

	sw=window.open('prepay_save.html','savings','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=250,height=180');

	if(navigator.appName.substring(0,8) == "Netscape"){

		sw.focus();

	}

}

else{

	location.href='privilege.html';

}

}





//------------------------------------



function controlMortgage(n)

{

if(navigator.appVersion.substring(0,3) == 2.0 &&  navigator.appName.substring(0,8)=="Netscape" && navigator.appVersion.indexOf("Macintosh")>=0){

	if(validResults()==true){

		setTimeout("calcMortgage(3)",200);

		if(n==1){

			controlCompute(1,0);

		}

	}

}

else{

	if(validResults()==true){

		calcMortgage(3);

		if(n==1){

			controlCompute(1,0);

		}

	}

}

}



//------------------------------------



function validLumps(field)

{

doSum(field);

return true;

}



//------------------------------------



//FUNCTION CALCULATES MISSING ELEMENT IN MORTGAGE SCENARIO



function calcMortgage(calcField,lang){

var py = document.prpaycalc;



//make sure that the other 3 fields are filled in



document.getElementById('erreur_montant_versement').style.display='none';



if(py.MORTAMT.value == null || py.MORTAMT.value.length == 0 && calcField != 0){

	alert ("Vous devez repondre a Question 1 pour calculer ce montant.");

} else if (py.RATE.value.length == 0 && calcField != 1){

	alert ("Vous devez repondre a Question 2 pour calculer ce montant.");

} else if (py.NAMORTY.value.length == 0 && py.NAMORTM.value.length == 0 && calcField != 2){

	alert ("Vous devez repondre a Question 3 pour calculer ce montant.");

} else if (py.MAINPAY.value.length == 0 && calcField != 3){

	document.getElementById('erreur_montant_versement').style.display='block';

} else {







//DECLARE VARIABLES FOR KNOWN INFO

if(calcField!=0){var mortgage = changeToDecimal(py.MORTAMT.value)*1.0;}

if(calcField!=1){var intRate = (changeToDecimal(py.RATE.value)*1.0)/100;}

if(calcField!=2){var amortMon =(py.NAMORTM.value*1.0)+(py.NAMORTY.value*1.0*12);}

if(calcField!=3){var payment = changeToDecimal(py.MAINPAY.value.replace(/['$'|' ']/g, ''))*1.0;}



var accel = py.ACCSEL.selectedIndex*1.0;

var payFreq = py.PFREQ.selectedIndex*1.0;

var compFreq = 2;

var numPay1 = calcNumPay(payFreq,1);

var numPay2 = calcNumPay(payFreq,2);



//SOLVE FOR MORTGAGE AMOUNT

if(calcField==0){

	if(accel==1){

		var regPayment = calcReverseAccel(payment,numPay1);

		var mortgage = calcMtgAmount(calcIntFact(intRate,compFreq,12),regPayment,amortMon);

	}

	if(accel==0){

		var initialAmPays = Math.floor((amortMon/12)*numPay2);

		var intFact = calcIntFact(intRate,compFreq,numPay1);

		var misefond = (py.MISE.value);  //  Mise de fonds dans formulaire

		// var mortgage = calcMtgAmount(intFact,payment,initialAmPays); vieille ligne

		var mortgage = Number(misefond)+Number(calcMtgAmount(intFact,payment,initialAmPays));

		

	}

	

	py.MORTAMT.value=addCommas(roundReg(mortgage));

	if(lang=='En'){

		document.getElementById("venue_resultat").innerHTML = '$ '+addCommas(roundReg(mortgage));//ajouter virgule

	}

	else {

		document.getElementById("venue_resultat").innerHTML = addCommas(roundReg(mortgage))+' $';//ajouter virgule

	}

	py.MISE.value=addCommas(roundReg(misefond)); //ajouter virgule

	//py.MAINPAY.value=payment;  //ajouter virgule

}



//SOLVE FOR INTEREST RATE

if(calcField==1){

	if(accel==1){

		var regPayment = calcReverseAccel(payment,numPay1);

		var intRate = calcRate(mortgage,amortMon,numPay1,numPay2,regPayment);}

	if(accel==0){

		var intRate = calcRate(mortgage,amortMon,numPay1,numPay2,payment);

	}

//	py.RATE.value=intRate;

	py.RATE.value=addCommas((Math.round(intRate*1000)/1000));

}



//SOLVE FOR AMORTIZATION PERIOD



if(calcField==2){

	if(accel==1){

		var regPayment = calcReverseAccel(payment,numPay1);

		var amortMon2 = calcAmort(mortgage,regPayment,calcIntFact(intRate,compFreq,12));

		var initAmortMon = Math.round((amortMon2/12)*12);

	}

	if(accel==0){

		var intFact = calcIntFact(intRate,compFreq,numPay1);

		var amortMon2 = calcAmort(mortgage,payment,intFact);

		var initAmortMon = Math.round((amortMon2/numPay2)*12);

	}

	py.NAMORTM.value = initAmortMon % 12;

	py.NAMORTY.value = Math.floor(initAmortMon/12);

}



//SOLVE FOR MORTGAGE PAYMENT

if(calcField==3){

	if(accel==1){

		var monIntFact = calcIntFact(intRate,compFreq,12);

		var monCompFact = calcCompFact(amortMon,monIntFact,12);

		var monPayment = calcPay(mortgage,monIntFact,monCompFact);

		var payment = calcAccelPay(monPayment,numPay1);}

	if(accel==0){

		var intFact = calcIntFact(intRate,compFreq,numPay1);

		var compFact = calcCompFact(amortMon,intFact,numPay2);

		var payment = calcPay(mortgage,intFact,compFact);

	}

	py.MAINPAY.value=addCommas(roundReg(payment));

}

}

}