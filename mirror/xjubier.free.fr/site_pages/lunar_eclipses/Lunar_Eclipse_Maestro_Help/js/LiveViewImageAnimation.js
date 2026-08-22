<!--
var gFirstImage = true;

function animate( )
{
  setInterval("loadImage()", 5000);	// Every 5 seconds
}

function loadImage( )
{
  if (gFirstImage == true)
    document.getElementById("liveview").src = "../gfx/LiveViewDlg.png";
  else
    document.getElementById("liveview").src = "../gfx/LiveViewDlgZoom.png";
  gFirstImage = !gFirstImage;
}
//-->