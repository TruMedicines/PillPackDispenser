var ac = {
  init : function () {

    // Get the current time - hour, min, seconds
    ac.chr = document.getElementById("chr");
    ac.cmin = document.getElementById("cmin");
    ac.csec = document.getElementById("csec");

    // The time picker - Hr, Min, Sec
    ac.thr = ac.createSel(23);
    document.getElementById("tpick-h").appendChild(ac.thr);
    ac.thm = ac.createSel(59);
    document.getElementById("tpick-m").appendChild(ac.thm);
    ac.ths = ac.createSel(59);
    document.getElementById("tpick-s").appendChild(ac.ths);

    // The time picker - Set, reset
    ac.tset = document.getElementById("tset");
    ac.tset.addEventListener("click", ac.set);
    ac.treset = document.getElementById("treset");
    ac.treset.addEventListener("click", ac.reset);

    // The alarm sound
    ac.sound = document.getElementById("alarm-sound");

    // Start the clock
    ac.alarm = null;
    setInterval(ac.tick, 1000);
  },



  tick : function () {
  // ac.tick() : update the current time

    // Current time
    var now = new Date();
    var hr = ac.padzero(now.getHours());
    var min = ac.padzero(now.getMinutes());
    var sec = ac.padzero(now.getSeconds());

    // Update current clock
    ac.chr.innerHTML = hr;
    ac.cmin.innerHTML = min;
    ac.csec.innerHTML = sec;

    // Check and sound alarm
    if (ac.alarm != null) {
      now = hr + min + sec;
      if (now == ac.alarm) {
        if (ac.sound.paused) {
          ac.sound.play();
        }
      }
    }
  },

  set : function () {
  // ac.set() : set the alarm

    ac.alarm = ac.thr.value + ac.thm.value + ac.ths.value;
    ac.thr.disabled = true;
    ac.thm.disabled = true;
    ac.ths.disabled = true;
    ac.tset.disabled = true;
    ac.treset.disabled = false;
  },

  reset : function () {
  // ac.reset() : reset the alarm

    if (!ac.sound.paused) {
      ac.sound.pause();
    }
    ac.alarm = null;
    ac.thr.disabled = false;
    ac.thm.disabled = false;
    ac.ths.disabled = false;
    ac.tset.disabled = false;
    ac.treset.disabled = true;
  }
};


// INIT - RUN ALARM CLOCK
window.addEventListener("load", ac.init);

var c = 0;

function pop(){
    if(c == 0){
        document.getElementById("box").style.display = "block";
        c = 1;
    }
    else{
        document.getElementById("box").style.display = "none";
        c = 0;
    }

}
