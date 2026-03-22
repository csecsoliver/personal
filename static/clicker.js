const shopItems = [
  {
    name: "Cat",
    description: "Cats click for you, earning *us* money.",
    cost: 10,
    startingCost: 10,
  },
  {
    name: "Upgrade",
    description: "Upgrades the earning power of your clicks.",
    cost: 50,
    startingCost: 50,
  },
];

const boughtItems = [];
let localCoins = 0;
class Cat {
  constructor() {
    this.name = "Cat"
    setInterval(() => {
      click()
    }, 1000);
  }
}
class Upgrade {
  constructor() {
    this.name = "Upgrade"
  }
}

async function click() {
  let multiplier = 1;
  for (const i in boughtItems.filter((x) => x instanceof Upgrade)) {
    multiplier += Math.ceil((parseInt(i) + 1) / 2);
  }
  for (let i = 0; i < multiplier - 1; i++) {
    fetch("/click", { method: "POST" });
    localCoins++;
  }

  document.getElementById("counter").innerHTML = await (await fetch("/click", { method: "POST" })).text();
  localCoins++;
  document.getElementById("local-counter").innerHTML = localCoins;


}


function createShopItems() {
  const shopContainer = document.getElementById("game-shop");
  document.querySelectorAll(".shop-item").forEach(element => {
    element.remove();
  });
  for (const i of shopItems) {
    const shopItem = document.createElement("div");
    shopItem.className = "shop-item";
    shopItem.innerHTML = `
<div>
  <h3>${i.name}</h3>
  <p>${i.description}</p>
  <button onclick="buyItem(${i.name})">Buy: ${i.cost}</button>
</div>
`;
    shopItem.addEventListener("click", () => { buyItem(i.name) });
    shopContainer.appendChild(shopItem);
    console.log("ads")
  }
  document.getElementById("clicker-button").addEventListener("click", click);
  for (const i of shopItems) {
    document.getElementById("bought-items").innerHTML += `
      ${boughtItems.filter((x) => i.name == x.name).length}x ${i.name}<br>
    `
  }

}

function buyItem(name) {
  let item = shopItems.find((v) => v.name == name);

  if (!item) {
    return
  }
  if (localCoins >= item.cost) {
    localCoins -= item.cost;
  } else {
    alert("Insufficient funds!");
    return;
  }
  switch (name) {
    case "Cat":
      boughtItems.push(new Cat());
      shopItems.find(x => x.name == name).cost *= 3;
      break;
    case "Upgrade":
      boughtItems.push(new Upgrade());
      shopItems.find(x => x.name == name).cost *= 2;
      break;
    default:
      break;
  }
  createShopItems();
  document.getElementById("bought-items").innerHTML = "";
  for (const i of shopItems) {
    document.getElementById("bought-items").innerHTML += `
${boughtItems.filter((x) => i.name == x.name).length}x ${i.name}<br>
`
  }
  console.log(boughtItems);
  document.getElementById("local-counter").innerHTML = localCoins;

}

createShopItems();

