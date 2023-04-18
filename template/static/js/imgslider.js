var images = document.getElementsByTagName('img');
for (var i = 0; i < images.length; i++) {
  images[i].className += ' q1';
  images[i].onclick = function() {
    change_img(this);
  };

}
function change_img(img) {
  var q = img.className.match(/q(\d+)/)[1];
  var next_q = q == 4 ? 1 : parseInt(q) + 1;
  img.className = img.className.replace(/q\d+/, 'q' + next_q);
}