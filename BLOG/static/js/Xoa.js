// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
let btns = document.querySelectorAll(".delete");
for(let i = 0; i < btns.length; i ++)
    {
      btns[i].addEventListener("click", function(){
        if(confirm("Bạn có muốn xóa khong?")==true){
           let tr = this.closest("tr");
           tr.remove;

        }
      })
    }
