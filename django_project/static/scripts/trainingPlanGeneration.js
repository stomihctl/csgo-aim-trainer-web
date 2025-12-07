const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    let currentDayIndex = 0;
    let plan = {};

    function updateDayLabel() {
      document.getElementById('day-label').textContent = `Day ${currentDayIndex + 1}: ${days[currentDayIndex]}`;
      document.getElementById('exercise-input').value = plan[days[currentDayIndex]] || "";
      const nextBtn = document.getElementById('next-btn');
      nextBtn.textContent = currentDayIndex === days.length - 1 ? "Finish" : "Next";
      nextBtn.className = currentDayIndex === days.length - 1 ? "finish" : "";
    }

    function nextDay() {
      plan[days[currentDayIndex]] = document.getElementById('exercise-input').value.trim();
      if (currentDayIndex < days.length - 1) {
        currentDayIndex++;
        updateDayLabel();
      } else {
        alert("Plan sent to user!\n" + JSON.stringify(plan, null, 2));
        // Redirect to home (simulation)
        window.location.href = "#home";
      }
    }

    function cancelPlan() {
      if (confirm("Are you sure you want to cancel the plan?")) {
        plan = {};
        alert("Plan cancelled. Returning to home.");
        window.location.href = "#home";
      }
    }

    // Initialize
    updateDayLabel();