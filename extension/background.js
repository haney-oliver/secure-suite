function logURLBeforeNavigation(details) {
    console.log("Navigating to: " + details.url);
    var data = {
        url: details.url
    }
    checkUrl(data)
        .then((response) => {
            console.log("Then: ")
            console.log(response)

            var postUrlData = {
                url: {
                    urlTokens: response.tokens[0],
                    urlSequence: response.sequence,
                    urlMalicious: !response.urlGood
                },
                userId: "6012f892-96b7-4675-a9fe-f9a849372600"
            }

            createUrl(postUrlData)
                .then((resp) => {
                    console.log(resp.ok)
                }).catch((resp) => {
                    console.log("Error:")
                    console.log(resp)
                })

            if (response.status == 200) {
                if (response.urlGood == false) {
                    browser.tabs.query({
                        active: true
                    }).then((tabs) => {
                        console.log("Tab object: ")
                        console.log(tabs[0])
                        browser.tabs.sendMessage(
                            tabs[0].id,
                            { "urlGood": false }
                        ).then(response => {
                            console.log("Message from the content script: ")
                            console.log(response.response)
                        }).catch(error => console.log(error))
                        return {redirectUrl: 'http://localhost:3000/'}; 
                    }).catch(error => {
                        console.log("Error:")
                        console.log(error)
                    })
                }
            }
        })
        .catch((error) => {
            console.log("Error:")
            console.log(error)
        });
}

browser.webNavigation.onBeforeNavigate.addListener(logURLBeforeNavigation);

async function checkUrl(request) {
    const response = await fetch("http://localhost:5000/api/AnalyzeUrl", {
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

async function createUrl(request) {
    const response = await fetch("http://localhost:8080/api/CreateUrl", {
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


