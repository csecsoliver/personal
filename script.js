const counterEl = document.getElementById("counter")
const messageEl = document.getElementById("message")
const boardEl = document.getElementById("board")
counterEl.innerText = parseInt(localStorage.getItem("counter"))
document.getElementById("submit_message").addEventListener("click", async () => {
  counterEl.innerText = parseInt(localStorage.getItem("counter")) + 1
  localStorage.setItem("counter", parseInt(counterEl.innerText))
  const response = await fetch("/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ "msg": messageEl.value }),
  })
  boardEl.innerHTML = await response.text()
  messageEl.value = ""
})
