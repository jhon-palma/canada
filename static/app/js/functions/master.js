function checkForModalParameter() {
    const urlParams = new URLSearchParams(window.location.search);
    const popupValue = urlParams.get('popup');

    switch (popupValue) {
        case 'newsletter':
        case 'infolettre':
          selector = "#index > footer > div.wrap.wrap_contact > div.finfo.fcontact_col2 > a"
          break;
        case 'free_evaluation':
        case 'évaluation_gratuite':
          selector = "#index > section.banner > div > a"
          break;
        case 'buying':
        case 'acheter':
          selector = '#index > section.profilhome.wwuhome.ww_buyint.profilhome2 > div > div.txt > div.__diplex > a.bouton.btn-wwu.boutonnre4.pointer'
          break;
        case 'selling':
        case 'vendre':
          selector = '#index > section.profilhome.wwuhome.ww_buyint2.profilhome2 > div > div.txt > div.__diplex > a.bouton.btn-wwu.boutonnre4.pointer'
          break;
    } 

    if (popupValue) {
        document.querySelector(selector).click();
    }
}



