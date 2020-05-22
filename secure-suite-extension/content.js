

browser.runtime.onMessage.addListener(request => {
    console.log("UrlGood from content " + request.urlGood)
    alert("Secure Suite has flagged this url. Proceed with caution...")
    return Promise.resolve({ response: true });
});