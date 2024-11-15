dict_en = {
  'en':'fr',
  'properties':'proprietes',
  'propertie':'propriete',
  'properties-for-sale':'proprietes-a-vendre',
  'properties-for-rent':'proprietes-a-louer',
  'real-estate-broker':'courtier-immobilier',
  'buying':'acheter',
  'selling':'vendre',
  'contact-realestate-broker':'contact-courtier-immobilier',
  'privacy-policy':'politique-confidentialite',
}

dict_fr = {
  'fr':'en',
  'proprietes':'properties',
  'propriete':'propertie',
  'proprietes-a-vendre':'properties-for-sale',
  'proprietes-a-louer':'properties-for-rent',
  'courtier-immobilier':'real-estate-broker',
  'acheter':'buying',
  'vendre':'selling',
  'contact-courtier-immobilier':'contact-realestate-broker',
  'politique-confidentialite':'privacy-policy',
}


function changeParameterInURL(search, param) {
  var dict = (search === 'fr') ? dict_fr : dict_en;
  
  var currentUrl = window.location.href;
  var newUrl = currentUrl;

  for (var key in dict) {
    if (dict.hasOwnProperty(key)) {
      var value_search = '/' + key + '/';
      var value_replace = '/' + dict[key] + '/';
      newUrl = newUrl.split(value_search).join(value_replace);
    }
  }

  if (newUrl !== currentUrl) {
    window.location.href = newUrl;
  } else {
    window.location.href = newUrl + param+'/';
  }
}

