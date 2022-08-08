/*

.__   __.   ______   .___________. __    __   __  .__   __.   _______    .___________.  ______           _______. _______  _______     __    __   _______ .______       _______    
|  \ |  |  /  __  \  |           ||  |  |  | |  | |  \ |  |  /  _____|   |           | /  __  \         /       ||   ____||   ____|   |  |  |  | |   ____||   _  \     |   ____|   
|   \|  | |  |  |  | `---|  |----`|  |__|  | |  | |   \|  | |  |  __     `---|  |----`|  |  |  |       |   (----`|  |__   |  |__      |  |__|  | |  |__   |  |_)  |    |  |__      
|  . `  | |  |  |  |     |  |     |   __   | |  | |  . `  | |  | |_ |        |  |     |  |  |  |        \   \    |   __|  |   __|     |   __   | |   __|  |      /     |   __|     
|  |\   | |  `--'  |     |  |     |  |  |  | |  | |  |\   | |  |__| |        |  |     |  `--'  |    .----)   |   |  |____ |  |____    |  |  |  | |  |____ |  |\  \----.|  |____ __ 
|__| \__|  \______/      |__|     |__|  |__| |__| |__| \__|  \______|        |__|      \______/     |_______/    |_______||_______|   |__|  |__| |_______|| _| `._____||_______(_ )
                                                                                                                                                                                |/ 
.___  ___.   ______   ____    ____  _______         ___       __        ______   .__   __.   _______                                                                               
|   \/   |  /  __  \  \   \  /   / |   ____|       /   \     |  |      /  __  \  |  \ |  |  /  _____|                                                                              
|  \  /  | |  |  |  |  \   \/   /  |  |__         /  ^  \    |  |     |  |  |  | |   \|  | |  |  __                                                                                
|  |\/|  | |  |  |  |   \      /   |   __|       /  /_\  \   |  |     |  |  |  | |  . `  | |  | |_ |                                                                               
|  |  |  | |  `--'  |    \    /    |  |____     /  _____  \  |  `----.|  `--'  | |  |\   | |  |__| |                                                                               
|__|  |__|  \______/      \__/     |_______|   /__/     \__\ |_______| \______/  |__| \__|  \______|                                                                               
                                                                                                                                                                                   

*/

const lang = document.body.parentElement.getAttribute("lang");

const errorMsgs = {};

if (lang == "en") {
	errorMsgs.invalidName = "The name fields cannot contain /, - or _.";
	errorMsgs.firstName = "Please enter a first name.";
	errorMsgs.familyName = "Please enter a family name.";
	errorMsgs.size = "Please select a size.";
	errorMsgs.colour = "Please select a colour.";
	errorMsgs.order = "You cannot have an empty order.";
	errorMsgs.email = "Please enter an email address.";
} else {
	errorMsgs.invalidName = "Les champs de nom ne peuvent pas contenir /, - or _.";
	errorMsgs.firstName = "Veuillez entrer un prénom.";
	errorMsgs.familyName = "Veuillez entrer un nom.";
	errorMsgs.size = "Veuillez sélectionner une taille.";
	errorMsgs.colour = "Veuillez sélectionner une couleur.";
	errorMsgs.order = "Vous ne pouvez pas avoir une commande vide.";
	errorMsgs.email = "Veuillez entrer une adresse e-mail.";
}

const getOrders = (ignoreErrors = false) => {
	const orderContainers = Array.from(document.getElementsByClassName("order-container"));

	var error = null;

	const orders = orderContainers.map(cont => {
		const info = {
			firstname: cont.querySelector(".name-form").querySelector(".first-name").value,
			lastname: cont.querySelector(".name-form").querySelector(".family-name").value,
			year: cont.querySelector(".name-form").querySelector(".year").value
		};

		if (/.*[-_/].*/.test(info.firstname)) {
			if (!error) error = {error: errorMsgs.invalidName, data: cont.querySelector(".name-form").querySelector(".first-name")};
		}
		if (info.firstname.length == 0) {
			if (!error) error = {error: errorMsgs.firstName, data: cont.querySelector(".name-form").querySelector(".first-name")};
		}
		if (/.*[-_/].*/.test(info.lastname)) {
			if (!error) error = {error: errorMsgs.invalidName, data: cont.querySelector(".name-form").querySelector(".family-name")};
		}
		if (info.lastname.length == 0) {
			if (!error) error = {error: errorMsgs.familyName, data: cont.querySelector(".name-form").querySelector(".family-name")};
		}

		const items = {
			hoodie: [],
			sweater: [],
			totebag: 0
		};

		if (cont.querySelector(".hoodie-selector.expandable-header").classList.contains("selected")) {
			items.hoodie = Array.from(cont.querySelectorAll(".hoodie-selector.expandable-content .hoodie-form")).map(item => {
				if (item.querySelector(".size-select .selected").classList.contains("invalid-default")) {
					if (!error) error = {error: errorMsgs.size, data: item.querySelector(".size-select")};
				}
				if (item.querySelector(".colour-select .selected").classList.contains("invalid-default")) {
					if (!error) error = {error: errorMsgs.colour, data: item.querySelector(".colour-select")};
				}
				return ({size: item.querySelector(".size-select .selected").innerHTML.toLowerCase(), colour: item.querySelector(".colour-select .selected").innerHTML.toLowerCase()})
			});
		}

		if (cont.querySelector(".sweater-selector.expandable-header").classList.contains("selected")) {
			items.sweater = Array.from(cont.querySelectorAll(".sweater-selector.expandable-content .sweater-form")).map(item => {
				if (item.querySelector(".size-select .selected").classList.contains("invalid-default")) {
					if (!error) error = {error: errorMsgs.size, data: item.querySelector(".size-select")};
				}
				if (item.querySelector(".colour-select .selected").classList.contains("invalid-default")) {
					if (!error) error = {error: errorMsgs.colour, data: item.querySelector(".colour-select")};
				}
				return ({size: item.querySelector(".size-select .selected").innerHTML.toLowerCase(), colour: item.querySelector(".colour-select .selected").innerHTML.toLowerCase()})
			});
		}

		if (cont.querySelector(".totebag-selector.expandable-header").classList.contains("selected")) {
			items.totebag = parseInt(cont.querySelector(".totebag-selector.expandable-content .counter-text").innerHTML);
		}

		if (items.hoodie.length == 0 && items.sweater.length == 0 && items.totebag == 0) {
			if (!error) error = {error: errorMsgs.order, data: cont};
		}

		return {...info, cart: items};
	});

	if (!ignoreErrors && error) {
		return error;
	}
	return {error: null, data: orders};
};

const getTotalPrice = orders => {
	const hoodies = orders.reduce((acc, order) => acc + order.cart.hoodie.length, 0);
	const sweaters = orders.reduce((acc, order) => acc + order.cart.sweater.length, 0);
	const totebags = orders.reduce((acc, order) => acc + order.cart.totebag, 0);

	const combos = Math.min(hoodies, sweaters, totebags);

	return {noDiscount: hoodies * 25 + sweaters * 20 + totebags * 7.5, actual: combos * 50 + (hoodies - combos) * 25 + (sweaters - combos) * 20 + (totebags - combos) * 7.5};
};

const showError = (msg, then) => {
	alert(msg);
	then();
};

const highlight = elem => {
	elem.scrollIntoView({behavior: "smooth", block: "nearest", inline: "nearest"});

	elem.classList.add("error-highlight");
	setTimeout(() => elem.classList.remove("error-highlight"), 1000);
};

const order = () => {
	const orders = getOrders();

	if (orders.error) {
		showError(orders.error, () => highlight(orders.data));
		return;
	}

	const email = document.getElementById("invoice-email").value;
	if (email.length == 0) {
		showError(errorMsgs.email, () => highlight(document.getElementById("invoice-email")));
		return;
	}

	const everything = {
		email: email,
		orders: orders.data
	};

	const req = new XMLHttpRequest();

	req.open("POST", "/"); 
	req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	req.onload = function() {
		const dataReply = JSON.parse(this.responseText);

		document.getElementById("order-id").innerHTML = dataReply["order_id"];
		document.getElementById("order-price").innerHTML = dataReply["price"] + " €";

		document.querySelector(".order-confirmation-wrapper").style.display = "initial";
		setTimeout(() => document.querySelector(".order-confirmation-wrapper").classList.add("appear"), 1);
	};

	req.send(JSON.stringify(everything));
};

const update = () => {
	const orders = getOrders(true);

	if (orders.error) {
		return;
	}

	const totalPrice = getTotalPrice(orders.data);

	document.getElementById("total-no-discount").innerHTML = totalPrice.noDiscount.toFixed(2) + " €";
	document.getElementById("discount").innerHTML = (-(totalPrice.noDiscount - totalPrice.actual)).toFixed(2) + " €";
	document.getElementById("total-price").innerHTML = totalPrice.actual.toFixed(2) + " €";
};

const getElementDepth = elem => {
	var l = 0;
	for (; elem.parentElement != document.body; elem = elem.parentElement, l++);
	return l;
};

const handleHeaderExpansion = elem => {
	elem.classList.toggle("selected");

	if (elem.classList.contains("selected")) {
		if (!elem.classList.contains("no-expand")) elem.nextElementSibling.style.height = elem.nextElementSibling.scrollHeight + "px";

		elem.children[1].innerHTML = "&check;";
	} else {
		if (!elem.classList.contains("no-expand")) elem.nextElementSibling.style.height = "0px";

		elem.children[1].innerHTML = "";
	}

	update();
};

Array.from(document.getElementsByClassName("expandable-header")).forEach(elem => elem.setAttribute("onclick", "handleHeaderExpansion(this)"));

const handleOptionSelector = elem => {
	const currentIndex = Array.prototype.findIndex.call(elem.children, elem => elem.classList.contains("selected"));
	const newIndex = (currentIndex - 1 + 1) % (elem.children.length - 1) + 1;

	elem.children[currentIndex].classList.remove("selected");
	elem.children[newIndex].classList.add("selected");

	elem.children[0].style.marginTop = -newIndex * elem.children[0].scrollHeight + "px";

	update();
};

Array.from(document.getElementsByClassName("option-selector")).forEach(elem => {
	const currentIndex = Array.prototype.findIndex.call(elem.children, elem => elem.classList.contains("selected"));

	elem.children[0].style.marginTop = -currentIndex * elem.children[0].scrollHeight + "px";

	elem.setAttribute("onclick", "handleOptionSelector(this)");
});

const handleCounterUpdate = (elem, change) => {
	const counterElem = elem.previousElementSibling || elem.nextElementSibling;

	counterElem.innerHTML = Math.max(parseInt(counterElem.innerHTML) + change, 1);

	update();
};

Array.from(document.getElementsByClassName("counter-text")).forEach(counter => {
	counter.previousElementSibling.setAttribute("onclick", "handleCounterUpdate(this, -1)");
	counter.nextElementSibling.setAttribute("onclick", "handleCounterUpdate(this, 1)");
});

/*

The code below must be last because it creates reference clones from elements on the
page. All event handlers and attributes must therefore be attached beforehand.

*/

const getElementsWithDuplicationId = (cont, id) => Array.prototype.filter.call(cont.children, elem => elem.getAttribute("duplication-id") == id);

const duplicatables = new Map();

const handlePlusButton = button => {
	const id = button.getAttribute("duplication-id");

	const newElem = duplicatables.get(id).cloneNode(true);

	button.parentElement.insertBefore(newElem, button);

	if (getElementsWithDuplicationId(button.parentElement, id).length - 2 == 2) {
		button.classList.add("combined");
	}

	if (button.parentElement.parentElement.previousElementSibling?.classList.contains("selected")) {
		button.parentElement.parentElement.style.height = button.parentElement.scrollHeight + 15 + "px";
	}

	update();
};

const handleDeleteButton = button => {
	const id = button.getAttribute("duplication-id");

	const elems = getElementsWithDuplicationId(button.parentElement, id);

	button.parentElement.removeChild(elems[elems.length - 3]);

	if (elems.length - 2 == 2) {
		button.previousElementSibling.classList.remove("combined");
	}

	if (button.parentElement.parentElement.previousElementSibling?.classList.contains("selected")) {
		button.parentElement.parentElement.style.height = button.parentElement.scrollHeight + 15 + "px";
	}

	update();
};

Array.from(document.getElementsByClassName("allow-multiple")).sort((a, b) => getElementDepth(b) - getElementDepth(a)).forEach(elem => {
	const id = elem.getAttribute("duplication-id");

	const plusButton = document.createElement("div");
	if (lang == "en") {
		plusButton.innerHTML = "Add another " + elem.getAttribute("duplication-item").toLowerCase();
	} else {
		const name = elem.getAttribute("duplication-item").toLowerCase();
		if (name.split(" ")[0].charAt(name.split(" ")[0].length - 1) == "e") { // French moment
			plusButton.innerHTML = "Ajouter une autre " + name;
		} else {
			plusButton.innerHTML = "Ajouter un autre " + name;
		}
	}
	plusButton.classList.add("plus-button");
	plusButton.setAttribute("onclick", "handlePlusButton(this)");
	plusButton.setAttribute("duplication-id", id);
	elem.parentElement.insertBefore(plusButton, elem.nextElementSibling);

	const deleteButton = document.createElement("div");
	deleteButton.innerHTML = lang == "en"? "Remove previous" : "Supprimer le précédent";
	deleteButton.classList.add("delete-button");
	deleteButton.setAttribute("onclick", "handleDeleteButton(this)");
	deleteButton.setAttribute("duplication-id", id);
	elem.parentElement.insertBefore(deleteButton, plusButton.nextElementSibling);

	duplicatables.set(id, elem.cloneNode(true));
});
