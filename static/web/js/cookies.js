ifCookiesAccepted();

function acceptCookies() {
    // Get the current date and add 7 days to it for the expiration date
    const currentDate = new Date();
    const expiresDate = new Date(currentDate.getTime() + 7 * 24 * 60 * 60 * 1000);

    // Call the setCookie function with the desired values
    setCookie('acceptPolicy', 'accpet', expiresDate);
	
	addFacebookPixel();
	addTagManager();
    //addGoogleTag();
    addAnalyticsTracking();
    closeCookiesPopup();

}
function closeCookiesPopup() {
    if (areCookiesAccepted()) {
        // If cookies have been accepted, update the element's style
        const element = document.getElementById('privacy-policies-message');
        if (element) {
            element.style.transform = 'translateY(200%)';
        }
    }

}
function getCookie(name) {
    // Split the document.cookie string into individual cookies
    const cookiesArray = document.cookie.split('; ');

    // Loop through the cookies to find the one with the specified name
    for (const cookie of cookiesArray) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue); // Decode the value to handle special characters
        }
    }

    // Return null if the cookie with the specified name is not found
    return null;
}
function setCookie(name, value, expires) {
    // Calculate the expiration date in UTC format
    const expirationDate = new Date(Date.now() + expires * 24 * 60 * 60 * 1000).toUTCString();

    // Set the cookie with the provided parameters
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expirationDate}; path=/`;

    // Update the local storage variable to indicate that cookies are accepted
    localStorage.setItem('accept-cookies', 'true');
    closeCookiesPopup();
}
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}
function areCookiesAccepted() {
    return localStorage.getItem('accept-cookies') === 'true';
}

function removeDisplayedElement() {
    const displayedElement = document.querySelector('.displayed');
    if (displayedElement) {
        displayedElement.remove();
    }
}
function addDisplayedElement() {

    // If cookies have been accepted, update the element's style
    const element = document.getElementById('privacy-policies-message');
    if (element) {
        element.style.display = 'block';
    }
}
function ifCookiesAccepted(){
    const myCookieValue = getCookie('acceptPolicy');
    if (myCookieValue) {
        // If cookies have been accepted, remove class displayed (popup)
        removeDisplayedElement();
		addFacebookPixel();
		addTagManager();
        addGoogleTag();
        addAnalyticsTracking();
    }
    else {
        addDisplayedElement();
        localStorage.setItem('accept-cookies', 'false');

    }

}
function addAnalyticsTracking(){


    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
        (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
        m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
        ga('create', 'UA-93134370-48', 'auto');
        ga('send', 'pageview');
}
function addFacebookPixel(){

    adroll_adv_id = "TSILNXG4EFET3LZFK6IDYE"; 
    adroll_pix_id = "X7LOROAHYFHN3B6IIB4UES"; 
    adroll_version = "2.0"; 
    (function(w, d, e, o, a) { 
        w.__adroll_loaded = true; 
        w.adroll = w.adroll || []; 
        w.adroll.f = [ 'setProperties', 'identify', 'track' ]; 
        var roundtripUrl = "https://s.adroll.com/j/" + adroll_adv_id + "/roundtrip.js"; 
        for (a = 0; a < w.adroll.f.length; a++) { 
            w.adroll[w.adroll.f[a]] = w.adroll[w.adroll.f[a]] || (function(n) { 
                return function() { 
                    w.adroll.push([ n, arguments ]) } })(w.adroll.f[a]) } 
                    e = d.createElement('script'); 
                    o = d.getElementsByTagName('script')[0]; 
                    e.async = 1; e.src = roundtripUrl; o.parentNode.insertBefore(e, o); })(window, document); 
                    adroll.track("pageView");
    adroll_adv_id = "TSILNXG4EFET3LZFK6IDYE";
    adroll_pix_id = "X7LOROAHYFHN3B6IIB4UES";
    adroll_version = "2.0";

    (function(w, d, e, o, a) {
        w.__adroll_loaded = true;
        w.adroll = w.adroll || [];
        w.adroll.f = [ 'setProperties', 'identify', 'track' ];
        var roundtripUrl = "https://s.adroll.com/j/" + adroll_adv_id
                + "/roundtrip.js";
        for (a = 0; a < w.adroll.f.length; a++) {
            w.adroll[w.adroll.f[a]] = w.adroll[w.adroll.f[a]] || (function(n) {
                return function() {
                    w.adroll.push([ n, arguments ])
                }
            })(w.adroll.f[a])
        }

        e = d.createElement('script');
        o = d.getElementsByTagName('script')[0];
        e.async = 1;
        e.src = roundtripUrl;
        o.parentNode.insertBefore(e, o);
    })(window, document);
    adroll.track("pageView");

(function(w,i,d,g,e,t){w["WidgetTrackerObject"]=g;(w[g]=w[g]||function() {
    (w[g].q=w[g].q||[]).push(arguments);}),(w[g].ds=1*new Date());(e="script"), (t=d.createElement(e)),(e=d.getElementsByTagName(e)[0]);
    t.async=1;t.src=i; e.parentNode.insertBefore(t,e);}) (window,"https://widgetbe.com/agent",document,"widgetTracker"); 
    window.widgetTracker("create", "WT-KSMAOKTW"); window.widgetTracker("send", "pageview"); 

!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window,document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
 fbq('init', '1494417464404515'); 
fbq('track', 'PageView');
}
function addGoogleTag(){
    window.dataLayer = window.dataLayer || []; 
	function gtag(){
		dataLayer.push(arguments);
   	} 
	gtag('js', new Date()); 
	gtag('config', 'G-1S4QZ0P8DT'); 
}
function addTagManager(){
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5VZG49W');
}