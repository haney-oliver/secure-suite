function logURLBeforeNavigation(details) {
    console.log("Navigating to: " + details.url);
    var data = {
        url: details.url,
        session_key: "5a380ec6-4152-407b-915c-f970ece38672",
        user_key: "41356fc0-2d1c-4292-8c55-21f1c2589321",
    }


    createAndOrAnalyzeUrl(data)
        .then((resp) => {
            console.log(resp.ok)
        }).catch((resp) => {
            console.log("Error:")
            console.log(resp)
        })

}

browser.webNavigation.onBeforeNavigate.addListener(logURLBeforeNavigation);

async function createAndOrAnalyzeUrl(request) {
    const response = await fetch("http://localhost:5000/api/CreateOrAnalyzeUrl", {
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


function logURLBeforeNavigation(details) {
    console.log("Navigating to: " + details.url);
    var data = {
        url: details.url,
        session_key: "578fa0ca-bee8-4d68-88c3-d222ddeeb3df",
        user_key: "41356fc0-2d1c-4292-8c55-21f1c2589321",
    }


    createAndOrAnalyzeUrl(data)
        .then((resp) => {
            console.log(resp.ok)
        }).catch((resp) => {
            console.log("Error:")
            console.log(resp)
        })

}

browser.webNavigation.onBeforeNavigate.addListener(logURLBeforeNavigation);

async function createAndOrAnalyzeUrl(request) {
    const response = await fetch("http://localhost:5000/api/CreateOrAnalyzeUrl", {
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



