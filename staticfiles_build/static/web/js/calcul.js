function addCommas(nStr)

{

	nStr += '';

	x = nStr.split('.');

	x1 = x[0];

	x2 = x.length > 1 ? ',' + x[1] : '';

	var rgx = /(\d+)(\d{3})/;

	while (rgx.test(x1)) {

		x1 = x1.replace(rgx, '$1' + ' ' + '$2');

	}

	return x1 + x2;

}





/*

0$ - 50 000$ =

0,5% de la somme qui se situe dans cette tranche.



50 000$ - 250 000$ =

1,0% de la somme qui se situe dans cette tranche.



250 000$ et plus =

1,5% de la somme qui se situe dans cette tranche.

*/

function calculerTaxeDeBienvenue(lang){


 var radioButtons = document.getElementsByName("radio");

      for (var x = 0; x < radioButtons.length; x ++) {

        if (radioButtons[x].checked) {

          areataxmutation = radioButtons[x].id;

        }

      }

	  if(taxmutationamount.value == ""){alert("L'information suivante est manquante:\n\n- Veuillez indiquer la valeur de la propriété.\n")

			  return;

		  }



	  if(areataxmutation == "region"){

	

		var montant = "";



		montant = document.getElementById("taxmutationamount").value.replace(/[' '|'$']/g, '');

		montant = montant.replace(' ', '');

		montant = montant.replace(/\s/gi,"");

		/*alert(montant);*/

		montant = montant.replace(',', '', 'g');

		montant = montant.replace('.', '', 'g');

		var resultat = 0;

		

		

		montant = parseInt(montant);

		

		level4 = montant - 500000;

		if(level4>0) {

			resultat += (level4*2/100);

			montant -= level4;

		}

	

		level3 = montant - 250000;

		if(level3>0 && level3<250001) {

			resultat += (level3*1.5/100);

			montant -= level3;

		}

		

		level2 = montant - 50000;

		if(level2>0) {

			resultat += (level2*1.0/100);

			montant -= level2;

		}

		

		level1 = montant;

		if(level1>0) {

			resultat += (level1*0.5/100);

			montant -= level1;

		}



	  }else{

			var montant = "";

		

		montant = document.getElementById("taxmutationamount").value;

		

		montant = montant.replace(' ', '');

		montant = montant.replace(/\s/gi,"");

		montant = montant.replace(',', '', 'g');

		montant = montant.replace('.', '', 'g');

		var resultat = 0;

		

		montant = parseInt(montant);

	

		level3 = montant - 250000;

		if(level3>0) {

			resultat += (level3*1.5/100);

			montant -= level3;

		}

		

		level2 = montant - 50000;

		if(level2>0) {

			resultat += (level2*1.0/100);

			montant -= level2;

		}

		

		level1 = montant;

		if(level1>0) {

			resultat += (level1*0.5/100);

			montant -= level1;

		}



	  }

	if(lang=='fr'){

		resultat=addCommas(resultat)+ ' $';

	}

	else {

		resultat='$ '+ addCommas(resultat);

	}

	document.getElementById("taxmutation_result").innerHTML = resultat;

	

}

