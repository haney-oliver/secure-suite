# Senior Research Notes and Outline

## Overview
Open source security suite. Password manager, malicious url detection, and malicious network traffic detection. Eventually encrypted email and file storage.  For enterprise options, full secrets manager with role authorization patterns for secrets controls. I understand that I probably won’t get all of this done so I request my advisor’s opinion on the prioritization of things. 

## Password Manager
A password manager. Have a prototype server already created. I have developed some useful patterns in Java web application development using the [Dropwizard framework](http://www.dropwizard.io/en/stable/)over the past year or so. The current patterns provide for the flexibility to prototype and develop freely using the same codebase distributed across any number of environments, making it fast and easy to implement new modifications and updates. The idea is to have an open source password manager, and eventually develop an application, using flutter if possible, as well as a chrome extension for intuitive and on demand access. 

Not sure if monetization is an option, but my initial idea is to have a full blown enterprise role based secrets manager with encrypted file upload and categories for different stored types (credit cards, bank credentials, etc.).  Maybe encrypted file storage without role administration could be used in a community version to some extent. I understand the kinds of questions this raises, because if I were to adopt the current standards of today—like moving towards centralization of computing and storage, essentially utilizing cloud computing—this would result in a great cost paid to whichever cloud hosting provider I choose. My answer to this is to make the non-enterprise portions of the codebase to be open source and easily distributable. I like the idea of at least somewhat encouraging the decentralization of computing, and enabling the user to own their own data. Now I don’t know if there should be a choice and I should offer some sort of cloud based solution because I understand that increases the ease of use on the user side, but again, cost. 

There are free solutions that I have explored in the past, such as Heroku, but those free solutions certainly won’t hold up to any sort of demand if I am optimistic about the usefulness of this product. On the enterprise side of things I feel like this decision is a non issue, my logic being: given that there is any business at all it will be easier to generate initial cash flow to support cloud based hosting, at least in the beginning.  I really have no idea what I am talking about here though. 


## Malicious URL Detection and Classification
Simple logistic regression binary classification. Already have a prototype completed and found a dataset. I am not quite satisfied with my knowledge to in any way conclude which approach would be best for such classification, and again request the advice of my advisor. 

## Other Modules
As stated above, I am not going to go into too much detail about these loftier ideas as I am unsure that I am up to the challenge given the time constraints, but we will see if I can maybe accomplish one of these other goals:
- encrypted instant messaging
- machine learning  malicious network traffic detection (useful for open source distribution)
- encrypted email
- vpn

## Thinking About Marketing
I would very much like to use and promote the message of privacy and discourage the intrusion and damage caused by any malicious hacker, whether they be a self-motivated or state-motivated agent. 

