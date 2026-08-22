<!--
var gFirstImage = true;

function animate( )
{
  setInterval("loadImage()", 5000);	// Every 5 seconds
}

function loadImage( )
{
  if (gFirstImage == true)
    document.getElementById("eclipsediagram").src = "../gfx/MoonEarthUmbraPenumbra_Diagram1.png";
  else
    document.getElementById("eclipsediagram").src = "../gfx/MoonEarthUmbraPenumbra_Diagram2.png";
  gFirstImage = !gFirstImage;
}
//-->