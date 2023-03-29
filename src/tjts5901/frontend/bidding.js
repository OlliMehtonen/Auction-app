
"use strict"


//Create empty data structures
//

let currencyTable = {}
let categoryTable = {}
let user = {}
let auction = {}

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
        auction = getAuctionData()
        addAuctionData(auction)



        
        //ADD AUCTION FORM EVENT LISTENER INITIALIZATION
        aaFormEventListenersInitializers()

        






})


//
//GET USER DATA AND AUCTION DATA AND POPULTE LISTS WITH THE AUCTION INFORMATION
//

//User and auction data related functions

const getUserData = ()=>{
        //replace these with calls to backend
        let user = {'username': 'John Doe', 'uid': '32423hj2j3n2j3rj2n'}
        let myActiveAuctions = [{'id':'sad34f8', 'name': 'guernsey cow', 'cat': 'Animals', 'initPrice': 5, 'topBid': 67, 'desc': 'pure-bred Guernsey cow', 'expires':'2023-05-12T23:50:21.817Z'  }, {'name': 'guernsey cow2', 'id':'9sa8udjd3' ,'cat': 'Animals', 'subcat': 'Other domestic animals', 'initPrice': 5, 'topBid': -1, 'desc': 'pure-bred Guernsey cow', 'expires':'2023-05-10T23:50:21.817Z'  }]

        let myExpiredAuctions = [{'id':'sadf8', 'name': '1970s cookbook', 'cat': 'Animals', 'initPrice': 6, 'topBid': 10, 'desc': 'a real classic', 'expires':'2020-05-12T23:50:21.817Z'  }, {'name': 'siamese dogs', 'id':'9lsk8udjd3' ,'cat': 'Animals', 'subcat': 'Other domestic animals', 'initPrice': 100, 'topBid': -1, 'desc': 'regular dog with two heads', 'expires':'2022-05-10T23:50:21.817Z'  }]
        return {'user':user, 'active': myActiveAuctions, 'expired': myExpiredAuctions}
}


//Get auctions from database
//NOT PROPERLY IMPLEMENTED YET
//TODO: CALL BACKEND
const getAuctiondata = ()=>{

        return {'id':'sadf8', 'name': 'First edition of Pokemon cookbook', 'cat': 'Animals', 'initPrice': 6, 'topBid': 10, 'desc': 'a real classic', 'expires':'2023-03-02T23:50:21.817Z'  }
}



//MAIN FUNCTIONS TO ADD AUCTIONS
//

//Populate page with data from auction
const addOwnAuctions = ({'active': acAuc, 'expired': exAuc}) => {
        //Add active auctions to correct place
        let myActUl = document.getElementById('myactive')
        
        let relevantKeysActive =  {'name': textDiv, 'cat': textDiv, 'subcat': textDiv, "topBid": bidsDiv, 'expires': timeRemainingDiv, 'id': removeAucButton }

        let activeElemList = acAuc.map((e)=>aucToLi(relevantKeysActive, e ))
        myActUl.append(...activeElemList)

        //Add expired auctions to correct place
        let myExpUl = document.getElementById('myexpired')
        let relevantKeysExpired = {'name': textDiv, 'cat': textDiv, 'subcat':textDiv, 'topBid': finalPrice, 'expires': textDiv, 'initPrice': textDiv  }
        let expiredElemList = exAuc.map((e)=>aucToLi(relevantKeysExpired, e ))
        myExpUl.append(...expiredElemList)


}


// Add on going auctions to their own tab
const addAuctions = (aucs) =>{

        //Add active auctions to correct place
        let allActUl = document.getElementById('allAucs')
        
        let relevantKeysActive =  {'name': textDiv, 'cat': textDiv, 'subcat': textDiv, "topBid": bidsDiv, 'expires': timeRemainingDiv}

        let activeElemList = aucs.map((e)=>aucToLi(relevantKeysActive, e ))
        allActUl.append(...activeElemList)


}



//Helper function to transform auction data objects to li elements
// addThese is object with keys equal to ones used from item and the corresponding
// value is function used to produced desired div element to listing li element
// Below one can find some functions already used to produce div-elements.
const aucToLi = (addThese, item) => {
        
        let li = document.createElement('li')
        li.addEventListener('click', (e)=>{

                window.location.href="https://www.hs.fi"
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

const bidsDiv = (value) =>{
        return (value < 0 ? textDiv('No bids yet') : textDiv(value))
        
}

const finalPrice = (value) =>{
        return (value < 0 ? textDiv('No bids') : textDiv(value))
}

const timeRemainingDiv = (timeString) =>{
        let expirationTime = Date.parse(timeString)
        let timeRemaining = expirationTime-Date.now()

        let itemDiv = document.createElement('div')
        itemDiv.textContent = timeRemaining
        const updateTime = ()=>{
                let d = expirationTime - Date.now()
                if (d<0){
                        clearInterval(timeUpdater)
                        //Should be changed to automatic moving to expired auctions array.
                        itemDiv.textContent = "Expired"
                }
                let s = Math.floor((d % (60000))/1000)
                let m =  Math.floor((d % (3600000))/60000)
                let h =  Math.floor((d % (24*3600000))/3600000)
                //console.log("h", h, "m", m, "s", s)
                itemDiv.textContent =  `${h} h ${m} m ${s} s remaining`
        }


        let timeUpdater = setInterval(updateTime, 1000)
        return itemDiv
}


const removeAucButton = (aucId)=>{
        let div = document.createElement('div')
        let button = document.createElement('button')
        button.textContent = "Cancel Auction"
        
        div.addEventListener('click', (e)=>{
                e.preventDefault()
                console.log("poistetaan", aucId)
                e.stopPropagation()

        })
        div.appendChild(button)
        return div

}

//Currency related functions
//

const initCurrencies =  () => {
        currencyTable = getExchangeRates() //TODO: make async when connection added

        //Add currency options
        //First nonseelctable option


        let op =document.createElement('option')
        op.setAttribute('value', '')
        op.textContent = "Choose currency"
        op.setAttribute('disabled', "")
        op.setAttribute('selected', "")
        op.setAttribute('hidden', "")
        
        //get parent tag
        let currSel = document.getElementById("aafCurr")
console.log(Object.values(currencyTable))
        addOptions(currSel, Object.values(currencyTable), 'cur', 'cur', op )



}


//TODO: Get exchangerates from the bank
const getExchangeRates = () => {
        console.error("METHOD getExchangeRates NOT IMPLEMENTED")
        return {'USD': {'cur': "USD", "rate": 1.23}, "Monopoly money": {'cur': 'Monopoly money', 'rate': 2}} 
}


//Category related functions

//TODO: Get category, subcategory object

const getCategories = () => {
        console.error("METHOD getCategories not implemented yet.")
        return {"Animals":{'cat': 'Animals',  'subcats':[{'name ':"Wild animals"}, {'name': "Dogs"},{'name': "Cats"}, {'name': "Other domestic animals" }]}, "Electronics":{'cat': "Electronics", 'subcats': [{'name': "Phones"},{'name': "Laptops"},{'name': "Desktop"},{'name': "Game consoles"}, {'name': "TVs" },{'name': "Electric toothbrushes"}]} }
}


const initCats = ()=>{

        categoryTable = getCategories() //TODO: make async when connection added

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
        console.log(translateThis)
        for (let [orig_key, new_key] of Object.entries(dictionary)){
                console.log(orig_key, new_key)
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
const addOptions = (parent, list, textTag, valueTag, headerOption = null  ) => {
        if (Array.isArray(headerOption)  ){
                parent.append(...headerOption)


        } else if (headerOption !== null){
                parent.appendChild(headerOption)

        }
        console.log(list)
        for (let ob of list){
                console.log(ob)
                let op = document.createElement("option")
                op.setAttribute('value', ob[valueTag])
                op.textContent=ob[textTag]
                parent.appendChild(op)
        }

}


//Add event listener for form submit button click and category and currency change 
const aaFormEventListenersInitializers = ()=>{

        //Submit button click
        const aadButton = document.getElementById("aadButton")
        aadButton.addEventListener('click', async (e) => {
                e.preventDefault()
                console.log("Button clicked. TODO: rest...")
                let form = e.target.form
                let isValid =  form.reportValidity()
                console.log(form)
                        //JUST TESTING DELETE LATER
                        //FIXME 
                        let a =await fetch('/auction_item')
                                .then((r) =>r.json())
                                .then((a)=> console.log(a))

                        //U TO HERE
                if (isValid){
                        console.log("SUBMIT TO BACKEND")
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

                        console.log("DATA:", dataWithRightKeys)

                        // Send auction data to backend.
                        let newAucReq = {
                                method: 'POST',
                                headers: {
                                        'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(dataWithRightKeys)
                        }
                        console.log("läh", newAucReq)
                        let url = "/auction_item"
                        //FIXME
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
