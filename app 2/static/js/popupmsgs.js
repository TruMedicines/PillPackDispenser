var snooze = true;
var stime = '1:31:30 AM';

function digit() {
    var tPills = '{{pillBtn}}';
    var yesAlarm = (tPills == 'True');
    var ctime = null;
    var audio = document.getElementById('alarm-sound');
    audio.loop = true;

    var date = new Date(),
        hour = date.getHours(),
        minute = checkTime(date.getMinutes()),
        ss = checkTime(date.getSeconds());

    function checkTime(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }


    if (hour > 12) {
        hour = hour - 12;
        if (hour == 12) {
            ctime = hour + ":" + minute + ":" + ss + " AM";
        }
        else {
            ctime = hour + ":" + minute + ":" + ss + " PM";
        }
    }
    else {
        if (hour == 0) {
            hour = checkTime(hour);
        }
        ctime = hour + ":" + minute + ":" + ss + " AM";
    }
    document.getElementById("tt").innerHTML = ctime;

    if (ctime == stime) {
        if (!yesAlarm) {
            document.querySelector(".bg-modal").style.display = 'flex';
            snooze = false;
            audio.pause();
        }
    }

    if (ctime == stime) {
        if (!yesAlarm) {
            audio.play();
        }
    }

    document.querySelector(".snooze").addEventListener("click",
        function () {
            snooze = true;
            document.querySelector(".bg-modal").style.display = 'none';
            audio.pause();

            if (snooze) {
                var fiveMinsSnooze = new Date();
                fiveMinsSnooze.setMinutes(fiveMinsSnooze.getMinutes() + 1);
                var stimehr = fiveMinsSnooze.getHours();
                var stimemin = checkTime(fiveMinsSnooze.getMinutes());
                var stimesec = checkTime(fiveMinsSnooze.getSeconds());
                if (stimehr > 12) {
                    stimehr = stimehr - 12;
                    if (stimehr == 12) {
                        stimehr = checkTime(stimehr);
                        stime = stimehr + ":" + stimemin + ":" + stimesec + " AM";
                    }
                    else {
                        stimehr = checkTime(stimehr);
                        stime = stimehr + ":" + stimemin + ":" + stimesec + " PM";
                    }
                }
                else {
                    stime = stimehr + ":" + stimemin + ":" + stimesec + " AM";
                }
                snooze = false;
            }
            
        })

    var time = setTimeout(digit, 1000);
}
window.addEventListener("load", digit());
/*
        if (stimehr > 12) {
            stimehr = stimehr - 12;
            if (stimehr == 12) {
                stimehr = checkTime(stimehr);
                stime = stimehr + ":" + checkTime(stime.getMinutes()) + ":" + checkTime(stime.getSeconds()) + " AM";
                document.getElementById("scheduledtime").innerHTML = stimehr;
            }
            else {
                stimehr = checkTime(stimehr);
                stime = stimehr + ":" + checkTime(stime.getMinutes()) + ":" + checkTime(stime.getSeconds()) + " PM";
                document.getElementById("scheduledtime").innerHTML = stimehr;
            }
        }
        else {
            stime = stimehr + ":" + checkTime(stime.getMinutes()) + ":" + checkTime(stime.getSeconds()) + " AM";
            document.getElementById("scheduledtime").innerHTML = stimehr;
        }
*/