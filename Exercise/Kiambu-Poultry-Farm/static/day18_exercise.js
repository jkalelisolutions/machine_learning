API_BASE_URL = "http://localhost:5000/api"

async function  get_eggs(shed) {
    const output = document.getElementById("output");
    
    const btn = document.getElementById("get-eggs-button");

    btn.disabled = true;
    btn.textContent = "Fetching...";
    output.textContent = "";

    const response = await fetch(`${API_BASE_URL}/eggs/${shed}`);
    const data = await response.json();
    output.textContent = response.ok
        ? `Shed: ${shed}\nEgg count: ${data.count}\nUpdated: ${data.date}`
        : data.error;
    
    btn.disabled=false;
    btn.textContent="Get Egg Count";
    

    return data;
}

async function add_eggs(){
  const shed = document.getElementById("shed").value;
    const count = document.getElementById("count").value;
    const output = document.getElementById("output");
    const response = await fetch(`${API_BASE_URL}/eggs`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({shed, count: Number(count)})
    });
    const data = await response.json();
    output.textContent = response.ok?`Egg count updated for ${shed}`: "Error updating egg count";
    return data;
}