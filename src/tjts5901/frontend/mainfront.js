"use strict"


//Create empty data structures
//

let currencyTable = {}
let categoryTable = {}
let user = {}
let auctions = []
let myAuctions = []

//Read the default currency.
localStorage.setItem("currencyChosen", document.getElementById('defaultcurrency').textContent.trim())

//Initialize page
window.addEventListener("load", async () => {



        //Fetch Currency information and add data to forms
        initCurrencies()


        //Fetch categories, parse and add data to forms
        initCats()

        //Add region options to forms
        initRegions()
        
        //Get user data and list current and former auctions
        user = getUserData()


        //Get data and add current active auctions
        auctions = await getOwnAuctions()
        auctions['othersAuctions'] = await getAuctions()
        console.log("Auctions", auctions)
        addAuctions(auctions['othersAuctions'])
        addOwnAuctions(auctions)



        
        //ADD AUCTION FORM EVENT LISTENER INITIALIZATION
        aaFormEventListenersInitializers()

        






})


//
//GET USER DATA AND AUCTION DATA AND POPULTE LISTS WITH THE AUCTION INFORMATION
//

//User and auction data related functions

const getUserData = ()=>{

        //Get username
        let username = document.getElementById('usernametag').textContent


        let user = {'username': username}
        return user
}


//Get auctions from database
// Return object with key,value pairs:
//   'othersAuctions' : array of not own auctions
//   'myAc' : arr of own active auctions
//   'myExp': arr of own expired auc
const getAuctions = async ()=>{

        const options = {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('13jwtstore')}`,
            }
        }
        let response = await fetch(window.location.origin.concat('/auction_item'), options)
        console.log(response)
        let text = await response.text()
        let items  = await JSON.parse(JSON.parse(text))
        console.log(items)

        
        //Helper to filter own auctions
        let isMine = (e) =>{
                return e['owned_by'] === user['username']}

        let others = items.filter( (e) =>  !isMine(e))
        console.log("muut vain ", others) 
        //Helper to filter expired auctions

        return others 
}


//Get users own auctions

const getOwnAuctions = async ()=>{

        const options = {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('13jwtstore')}`,
            }
        }
        let response = await fetch(window.location.origin.concat('/auction_item/my'), options)
        console.log(response)
        let text = await response.text()
        let items  = await JSON.parse(JSON.parse(text))
        console.log(items)

        
        //Helper to filter expired auctions
        let isActive = (e) =>{
                return e['is_expired'] !== true
        }

        let [myExp, myActive] = items.reduce( ([e, a], elem) =>  isActive(elem) ? [e, [...a, elem]] : [[...e, elem], a] , [[], []])
        return { 'myAc': myActive, 'myExp': myExp } 
}

//Time in milliseconds to expDate
//startTime given in GMT +0 timestamp
//Subtracts the effect of local timezone
const timeLeft = (startTime, length = 86400000) =>{
        let expTime = startTime + length
        let now = new Date(Date.now())
        return expTime - now - now.getTimezoneOffset()*60000





}



//MAIN FUNCTIONS TO ADD AUCTIONS
//

//Add users auction active and expired to the correct ul -tags
const addOwnAuctions = ({'myAc': acAuc, 'myExp': exAuc}) => {
        //Add active auctions to correct place
        let myActUl = document.getElementById('myaclist')
        
        myActUl.replaceChildren()
        let relevantKeysActive =  {'name': textDiv, 'category': textDiv, 'subcategory': textDiv, "highest_bid_price": bidsDiv, 'created_at': timeRemainingDiv, '_id': removeAucButton }

        let activeElemList = acAuc.map((e)=>aucToLi(relevantKeysActive, e ))
        myActUl.append(...activeElemList)

        //Add expired auctions to correct place
        let myExpUl = document.getElementById('myexplist')
        myExpUl.replaceChildren()
        let relevantKeysExpired = {'name': textDiv, 'category': textDiv, 'subcategory':textDiv, 'highest_bid_price': finalPrice, 'created_at': textDiv, 'starting_price': moneyDiv  }
        let expiredElemList = exAuc.map((e)=>aucToLi(relevantKeysExpired, e ))
        myExpUl.append(...expiredElemList)


}


// Add on going auctions to their own tab
const addAuctions = (aucs) =>{

        //Add active auctions to correct place
        //Find right elem and remove children first.
        let allActUl = document.getElementById('allAucs')
        allActUl.replaceChildren()
        
        let relevantKeysActive =  {'name': textDiv, 'category': textDiv, 'subcategory': textDiv, "starting_price": moneyDiv, "highest_bid_price": bidsDiv, 'created_at': timeRemainingDiv } //, 'expires': timeRemainingDiv}

        let activeElemList = [...aucs].map((e)=>aucToLi(relevantKeysActive, e ))
        allActUl.append(...activeElemList)


}



//Helper function to transform auction data objects to li elements
// addThese is object with keys equal to ones used from item and the corresponding
// value is function used to produced desired div element to listing li element
// Below one can find some functions already used to produce div-elements.
const aucToLi = (addThese, item) => {
        
        let li = document.createElement('li')
        li.addEventListener('click', (e)=>{
                console.log(item)

                window.location.href="/auction/".concat(item['_id'])
        })

        //  
        for (let [key, call] of Object.entries(addThese)){
                let itemDiv = call(item[key])
                li.appendChild(itemDiv)
        }

        //let itemCatDiv =  document.createElement('div')
        //itemCatDiv.textContent = `${item['cat']}`
        //li.appendChild(itemCatDiv)


        return li


}

// Helper functions to produce relevant div elements in listing

const textDiv = (text)=>{
        
                let itemDiv = document.createElement('div')
                itemDiv.textContent = text
                return itemDiv

}

const moneyDiv = (value) =>{
        return textDiv(valueInLocCurrency(value))
}

const bidsDiv = (value) =>{
        return (value <= 0 ? textDiv('No bids yet') : moneyDiv(value) )
        
}

const finalPrice = (value) =>{
        return (value <= 0 ? textDiv('No bids') : moneyDiv(value))
}

const timeRemainingDiv = (timeString) =>{
        let startTime = Date.parse(timeString)
        let itemDiv = document.createElement('div')
        const updateTime = ()=>{
                //let now = new Date(Date.now())

                //let d = expTime - now - now.getTimezoneOffset()*60000
                let d = timeLeft(startTime)
                if (d < 0){
                        clearInterval(timeUpdater)
                        //Should be changed to automatic moving to expired auctions array.
                        itemDiv.textContent = "Expired"
                } else {

                        let s = Math.floor((d % (60000))/1000)
                        let m =  Math.floor((d % (3600000))/60000)
                        let h =  Math.floor((d % (24*3600000))/3600000)
                        itemDiv.textContent =  `${h} h ${m} m ${s} s remaining`
                }
        }


        let timeUpdater = setInterval(updateTime, 1000)
        return itemDiv
}


const removeAucButton = (aucId)=>{
        let div = document.createElement('div')
        let button = document.createElement('button')
        button.textContent = "Cancel Auction"
        
        div.addEventListener('click', async (e)=>{
                e.preventDefault()
                e.stopPropagation()
                console.log("poistetaan", aucId)

                let removeReq = {
                        method: 'DELETE',
                        headers: {
                                'Content-Type': 'application/json',
                                "Authorization": `Bearer ${localStorage.getItem('13jwtstore')}`
                        }
                }
                let url = "/auction_item/".concat(aucId)
                let response = await fetch(url, removeReq)
                console.log(response)


        })
        div.appendChild(button)
        return div

}

//Currency related functions
//

const initCurrencies = async  () => {
        currencyTable = await getExchangeRates() 


        //Add currency options
        //First nonseelctable option


        let op =document.createElement('option')
        op.setAttribute('value', '')
        op.textContent = "Choose currency"
        op.setAttribute('disabled', "")
        op.setAttribute('hidden', "")
        
        //get parent tag
        let currSel = document.getElementById("aafCurr")
        addOptions(currSel, Object.values(currencyTable), 'cur', 'code', op, localStorage.getItem('currencyChosen') )

        
        //Update currency texts
        updateCurrencyText(localStorage.getItem('currencyChosen'))

        //Event listener for change of currency 
        currSel.addEventListener('change', ()=>{
                let val = currSel.value
                localStorage.setItem('currencyChosen', val)

                addAuctions(auctions['othersAuctions'])
                addOwnAuctions(auctions)
                updateCurrencyText(val)





        })
        



}


//Get exchange rates from ECB parse them to jsobject with currency codes as keys.
//each value is a object with following keys:
//  -code: 3 letter currency code (same as key)
//  -cur: name of currency
//  -rate: cur/EUR exchange rate
const getExchangeRates = async () => {
        
        //Check if rates are saved in local storage
        let curObj = localStorage.getItem('currencies')
        if (curObj === null){
                
                let rateReq = await fetch("https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D..EUR.SP00.A?startPeriod=2023-01-01&lastNObservations=1&format=jsondata")
                console.log("rates")
                let data = await rateReq.json()
                console.log(data)
                let rates = Object.values(data.dataSets[0].series)
                let currencyNames = data.structure.dimensions.series[1].values
                curObj = {'EUR': {'cur': 'European Euro', 'code': 'EUR',  'rate':1}}
                for (let i in rates){
                        curObj[currencyNames[i]['id']] = {'code':currencyNames[i]['id'], 'cur': currencyNames[i]['name'], 'rate':rates[i]['observations'][0][0]}
                }
                //Put currencies to localStorage to use them on item page too
                localStorage.setItem('currencies', JSON.stringify(curObj))
                console.log(curObj)
                console.log("dollari", curObj)
        } else {
                console.log("PARSING")
                curObj = JSON.parse(curObj)
        }
        return curObj //{'USD': {'cur': "USD", "rate": 1.23}, "Monopoly money": {'cur': 'Monopoly money', 'rate': 2}} 
}

//Convert param value (integer or number) to string of form 'VAL CUR' where VAL is value in currently chosen currency and CUR is the abbreviation of the currency
//If currency not found everything is given in euros
const valueInLocCurrency = (value) => {
        let rate = 1
        let cur = "EUR"
        let h = currencyTable[localStorage.getItem('currencyChosen')]
        if (!["EUR", null].includes(h)){
                rate = h.rate 
                cur = h.code
        }
        return `${value*rate} ${cur}`
}

const updateCurrencyText = (cur) =>{
        let tagList = document.getElementsByClassName('curtag')

        for ( let t of tagList){
                t.textContent = cur
        }

}

//Category related functions


const getCategories = () => {
        console.log("METHOD getCategories just returns a list.")
        return {"Animals":{'cat': 'Animals',  'subcats':[{'name ':"Wild animals"}, {'name': "Dogs"},{'name': "Cats"}, {'name': "Other domestic animals" }]}, "Electronics":{'cat': "Electronics", 'subcats': [{'name': "Phones"},{'name': "Laptops"},{'name': "Desktop"},{'name': "Game consoles"}, {'name': "TVs" },{'name': "Electric toothbrushes"}]} }
}


const initCats = ()=>{

        categoryTable = getCategories() 

        //Add category options
        //First nonselectable option


        let op =document.createElement('option')
        op.setAttribute('value', '')
        op.textContent = "Choose main category"
        op.setAttribute('disabled', "")
        op.setAttribute('selected', "")
        op.setAttribute('hidden', "")
        
        //get parent tag
        let catSel = document.getElementById("aafCat")
        addOptions(catSel, Object.values(categoryTable), 'cat', 'cat', op )


}

const initRegions = ()=>{
        let regions = [{'r': 'Everywhere'}, {'r': 'Europe'}, {'r': 'Asia'}, {'r': 'Africa'}, {'r': 'North America'}, {'r': 'South America'}]
        let regSel = document.getElementById('aafContinents')
        addOptions(regSel, regions, 'r', 'r')


}

const addSubCats = (cat) =>{
               
        
        let op =document.createElement('option')
        op.setAttribute('value', '')
        op.textContent = "Choose subcategory (optional)"
        op.setAttribute('disabled', "")
        op.setAttribute('selected', "")
        op.setAttribute('hidden', "")

        let subCatSel = document.getElementById("aafSubCat")
        subCatSel.replaceChildren()
        addOptions(subCatSel, categoryTable[cat]['subcats'], 'name', "name", op)
}


//Change keys of an object according to the dictionary object argument
const keyTranslate = (dictionary, translateThis) =>{
        let ans = {}
        for (let [orig_key, new_key] of Object.entries(dictionary)){
                ans[new_key]=translateThis.get(orig_key)
        }
        return ans


}


//Reusable function to add options to select fields
//parent = parent node
//list = list of objects that are made to options
//textTag :string = object key for option field textContent
//valueTag :string = object key for option field value field
//headerOption :option tag = option tag used as first option for giving input which is not automatically generated 
const addOptions = (parent, list, textTag, valueTag, headerOption = null, defaultValue = null  ) => {
        if (Array.isArray(headerOption)  ){
                parent.append(...headerOption)


        } else if (headerOption !== null){
                parent.appendChild(headerOption)

        }
        for (let ob of list){
                let op = document.createElement("option")
                op.setAttribute('value', ob[valueTag])
                //if (ob[valueTag] === defaultValue ){
                        //op.setAttribute('selected', 'selected')
                //}
                op.textContent=ob[textTag]
                parent.appendChild(op)
        }
        parent.value = defaultValue

}


//Add event listener for form submit button click and category and currency change 
const aaFormEventListenersInitializers = ()=>{

        //Submit button click
        const aadButton = document.getElementById("aadButton")
        aadButton.addEventListener('click', async (e) => {
                e.preventDefault()
                let form = e.target.form
                let isValid =  form.reportValidity()
                if (isValid){
                        const data = new FormData(form)
                        const newKeys = {
                                'aafName': 'name',
                                'aafCat': 'category',
                                'aafSubCat': 'subcategory',
                                'aafStartPrice': 'starting_price',
                                'aafDesc': 'description'//,
                               // 'aafContinents': 'area'

                        }
                        let dataWithRightKeys = keyTranslate( newKeys, data)
                        //Change currency to EUR
                        let rate = currencyTable[localStorage.getItem('currencyChosen')]['rate']
                        let priceInCur = parseInt(dataWithRightKeys['starting_price'])

                        dataWithRightKeys['starting_price'] = priceInCur / rate


                        // Send auction data to backend.
                        let newAucReq = {
                                method: 'POST',
                                headers: {
                                        'Content-Type': 'application/json',
                                        "Authorization": `Bearer ${localStorage.getItem('13jwtstore')}`
                                },
                                body: JSON.stringify(dataWithRightKeys)
                        }
                        let url = "/auction_item"
                        let response = await fetch(url, newAucReq)
                        console.log(response)
                }

        })

        //Category select change
        const aadCatSelect = document.getElementById("aafCat")
        aadCatSelect.addEventListener('change', () => {

                addSubCats(aadCatSelect.value, true)
        })
};


