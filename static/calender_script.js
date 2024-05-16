let activeCell = null;

function showCalender() {    
    document.getElementById('calender-modal').style.display = 'block'; 
    showArrows(); // Show arrows when the calender is shown
}

function hideCalender() {
    document.getElementById('calender-modal').style.display = 'none';  
    hideArrows();  
}

// toggled month: dynaimcially adjusted by user
// realMonth: static value 
function generatecalender(toggledMonth, days, realMonth) {
    document.getElementById('month-header').textContent = toggledMonth;
 
    var calenderBody = document.getElementById('calender-body'); calenderBody.innerHTML = '';

    // get time today
    var today = new Date();
    var realDay = today.getDate();
    
    var startDay = 1;  var daysInMonth = [...Array(days).keys()].map(x => x + 1);
    var rowIndex = 0; var cellIndex = 0; var row = calenderBody.insertRow(rowIndex);

    // generate days
    var cnt = 1 
    for (var i = 0; i < daysInMonth.length; i++) { 
    var dayOfWeek = new Date(today.getFullYear(), today.getMonth(), daysInMonth[i]).getDay();

    // fillers 
    if (cellIndex === 0 && dayOfWeek !== 1) { 
        var fillersNeeded = dayOfWeek === 0 ? 4 : dayOfWeek - 1;
        for (var j = 0; j < fillersNeeded; j++) {
        var fillerCell = row.insertCell(cellIndex);
        fillerCell.textContent = '';  
        cellIndex++;
        }
        cnt--;
    }

    // only weekdays 
    
    if (dayOfWeek !== 6 && dayOfWeek !== 0) {
        if (cellIndex === 5) {  
        rowIndex++;  
        row = calenderBody.insertRow(rowIndex);  
        cellIndex = 0;  
        }

        var cell = row.insertCell(cellIndex);
        cell.textContent = daysInMonth[i];
        var schoolDay = (cnt) % 4 + 1; 
        var subscript = document.createElement('sub');
        subscript.textContent = 'Day ' + schoolDay;
        subscript.className = 'school-day';
        cell.appendChild(subscript);

        // today = green
        if (daysInMonth[i] === realDay && toggledMonth == realMonth) {
        cell.classList.add('current-day');
        }

        // Highlight next two weeks in blue
        var futureDate = new Date(today);
        futureDate.setDate(futureDate.getDate() + 14); // Get date 14 days ahead
        if (daysInMonth[i] > realDay && daysInMonth[i] <= futureDate.getDate() && toggledMonth == realMonth) {
        cell.classList.add('future-day');
        }

        cell.addEventListener('click', function (event) {
        if (activeCell) {
            activeCell.classList.remove('active');
        }
        activeCell = event.target;
        activeCell.classList.add('active');
        document.getElementById('input-overlay').classList.add('active');
        });

        cellIndex++;
        cnt++; 
    }
    }
}

// wil remove when we get gib sheet 
function setSchoolDay() { 
    var selectedDay = document.getElementById('school-day').value; 
    if (!isNaN(selectedDay) && selectedDay >= 1 && selectedDay <= 4 && activeCell) {
    var schoolDayElement = findSchoolDayElement(activeCell);
    if (schoolDayElement !== null) {
        schoolDayElement.textContent = 'Day ' + selectedDay;
        updatecalender();
    } else {
        console.error("School day element not found in active cell:", activeCell);
    }
    activeCell = null;
    var inputOverlay = document.getElementById('input-overlay');
    if (inputOverlay !== null) {
        inputOverlay.classList.remove('active');
    } 
    }
}

function findSchoolDayElement(element) {
    while (element !== null) {
    if (element.classList.contains('active')) {
        var schoolDayElement = element.querySelector('.school-day');
        if (schoolDayElement !== null) {
        return schoolDayElement;
        }
    }
    element = element.parentElement;
    }
    return null;
}

// calibration, will remove when gib sheet 
function updatecalender() { 
    // Get all cells with the class 'school-day'
    var schoolDayCells = document.querySelectorAll('.school-day');
    var patternStartIndex = -1; // Initialize the pattern start index to -1
    var x;
    // Find the point where the pattern breaks
    for (var i = 0; i < schoolDayCells.length; i++) {
    var currentCell = schoolDayCells[i];
    var currentDay = parseInt(currentCell.textContent.split(' ')[1]); // Extract the day number

    // Check if the current day breaks the pattern

    if (currentDay !== ((i % 4) + 1)) {
        patternStartIndex = i;
        x = currentDay
        break; // Exit loop as soon as we find the point where the pattern breaks
    }
    }

    // Adjust all cells based on the detected pattern break

    // console.log(patternStartIndex)
    if (patternStartIndex !== -1) {
    for (var j = 0; j < schoolDayCells.length; j++) { 
        var correctDay = (x - (patternStartIndex - j)) % 4;
        if (correctDay <= 0) correctDay += 4;


        schoolDayCells[j].textContent = 'Day ' + correctDay;
    }
    }
}


var today = new Date();
var realMonthName = today.toLocaleString('default', {month: 'long'});
var realYear = today.getFullYear();
var x = new Date(realYear, today.getMonth() + 1, 0).getDate();
generatecalender(realMonthName, x, realMonthName);

function showArrows() {
    document.querySelectorAll('.arrow').forEach(function (arrow) {
    arrow.style.display = 'inline';
    });
}

function hideArrows() {
    document.querySelectorAll('.arrow').forEach(function (arrow) {
    arrow.style.display = 'none';
    });
}

//

toggledYear = realYear
toggledMonth = today.getMonth(); // Track the currently displayed month
function previousMonth() { 
    toggledMonth--;
    if (toggledMonth < 0) {
        toggledMonth = 11; // December
        toggledYear--;
    }
    const previousMonthDays = new Date(toggledYear, toggledMonth + 1, 0).getDate();
    const previousMonthName = new Date(toggledYear, toggledMonth, 1).toLocaleString('default', { month: 'long' });
    generatecalender(previousMonthName, previousMonthDays, realMonthName);
}

function nextMonth() {
    toggledMonth++;
    if (toggledMonth > 11) {
        toggledMonth = 0; // January
        toggledYear++;
    }
    const nextMonthDays = new Date(toggledYear, toggledMonth + 1, 0).getDate();
    const nextMonthName = new Date(toggledYear, toggledMonth, 1).toLocaleString('default', { month: 'long' });
    generatecalender(nextMonthName, nextMonthDays, realMonthName);
}























// tmp 
