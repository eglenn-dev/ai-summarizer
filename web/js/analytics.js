function runAnalytics() {
    const script = document.createElement('script');
    script.async = true;
    script.defer = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=G-3V6XPZH1V3';

    document.head.appendChild(script);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());

    gtag('config', 'G-3V6XPZH1V3');
}

runAnalytics();