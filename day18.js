async function Summarize() {
    const text = document.getElementById("input").value;
    const response = await fetch("https://localhost:5000/summarize",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({text})
        }
    );
    const data = await response.json();
    document.getElementById("output").textContent=data.summary;
    
}

async function summarize() {
    const btn= document.getElementById("submit-btn");
    const output= document.getElementById("output");

    //show loading state
    btn.disabled= true;
    btn.textContent= "Summarizing..."
    output.textContent= "";

    try{
        const response = await fetch ("/summarize", {/*...*/});
        if (!response.ok) throw new Error ("server error");
        const data = await response.json();
        output.textContent = data.summary;
    } catch(err){
        output.textContent= "Something went wrong. Try again.";
    }finally{
        btn.disabled= false;
        btn.textContent="Summarize"
    }
    
}

