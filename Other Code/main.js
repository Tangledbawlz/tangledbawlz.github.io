phase = document.querySelector('#phase');
phase.addEventListener('change', () => {
    let cipher = document.querySelector('#ciphers').value;

    if(cipher == "Vigenere Cipher")
    {
        vigenereCipher();
    }

    else if(cipher == "Cesear Cipher"){
        cesarCipher();
    }

    else if(cipher == "Password Cipher")
    {
        passwordCipher();
    }
    else
    {
        alert("No Cipher given, Input Password or leave!");
    }
});

function cesarCipher()
{
    pass = document.querySelector('#pass').value;
    let shifted = "";
    number = parseInt(phase.value)
    if(number < 0)
    {
        number = 34 - number;
    }

    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    for(let i = 0; i < pass.length; i++)
    {
        char = pass[i];
        if(letters.includes(char)){
            shifted += letters[(letters.indexOf(pass[i].toLowerCase()) + number) % 34] ;
        }
        else
        {
            shifted += letters[(letters.indexOf(pass[i]) + number) % 34] ;
        }        

    }
    console.log(shifted);
    document.querySelector("#Encrypted").textContent = shifted;

}

function passwordCipher()
{

}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }


function vigenereCipher()
{
    let passwordArr = [];
    let randIndex = getRandomInt(100);
    let results;
    
    let result = fetch("https://raw.githubusercontent.com/WillieStevenson/top-100-passwords/master/password-list.txt") // fetch text file
    .then((response) => {
        if (response.ok) {
            return response.text();
          } else {
            console.log("error:", response);
          }
    })
    .then((data) => {
        results = data;
        // console.log("first: ", results);
    });
    
    while(results == undefined)
    {
        //do nothing
    }
    

    console.log(results);
    
    return 0;


}
