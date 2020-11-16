var user_key;
var session_key;



function logURLBeforeNavigation(details) {
    console.log("Navigating to: " + details.url);
    var data = {
        url: details.url,
        session_key: session_key,
        user_key: user_key,
    }
    createAndOrAnalyzeUrl(data)
        .catch((resp) => {
            console.log("Error:")
            console.log(resp)
        })

}

browser.webNavigation.onHistoryStateUpdated.addListener(logURLBeforeNavigation);

browser.runtime.onMessage.addListener(function(request, sender) {
    data = request.options.message;
    user_key = data.user.user_key;
    session_key = data.session_key;  
})


async function createAndOrAnalyzeUrl(request) {
    const response = await fetch("http://192.168.1.165:5000/api/CreateOrAnalyzeUrl", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        body: JSON.stringify(request)
    });
    return response.json();
}




