let next = document.getElementById("next");
      let back = document.getElementById("back");
      var myTable = {% autoescape off %}{{data}}{% endautoescape %};
      next.addEventListener("click", function(){
         let ChonNgay = document.getElementById("lbChonNgay");
         ChonNgay.innerHTML= myTable;
      });
