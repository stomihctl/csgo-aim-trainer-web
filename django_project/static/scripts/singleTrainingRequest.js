
// document.addEventListener("DOMContentLoaded", () => {
//   const chooseTypeBtn = document.getElementById("chooseTypeBtn");
//   const dropdownMenu = document.getElementById("dropdownMenu");
//   const confirmType = document.getElementById("confirmType");
//   const generateBtn = document.getElementById("generateBtn");
//   const exerciseType = document.getElementById("exerciseType");
//   const exerciseName = document.getElementById("exerciseName");
//   const exerciseDesc = document.getElementById("exerciseDesc");
//   const exerciseDetails = document.getElementById("exerciseDetails");
//
//   dropdownMenu.style.display = "none";
//   exerciseDetails.style.display = "none";
//
//   chooseTypeBtn.addEventListener("click", () => {
//     dropdownMenu.style.display = "block";
//   });
//
//   confirmType.addEventListener("click", () => {
//     const selectedType = exerciseType.value;
//     if (!selectedType) {
//       alert("Please select an exercise type first!");
//       return;
//     }
//     alert(`Selected: ${selectedType}`);
//   });
//
//   generateBtn.addEventListener("click", async (e) => {
//     e.preventDefault();
//     const selectedType = exerciseType.value;
//
//     try {
//       const response = await fetch(`/get_random_exercise/?type=${encodeURIComponent(selectedType)}`);
//       const data = await response.json();
//
//       if (response.ok) {
//         exerciseName.textContent = data.name;
//         exerciseDesc.textContent = data.description;
//         exerciseDetails.style.display = "block";
//       } else {
//         exerciseName.textContent = "No exercise found";
//         exerciseDesc.textContent = data.error || "";
//         exerciseDetails.style.display = "block";
//       }
//     } catch (err) {
//       console.error("Error fetching exercise:", err);
//       alert("Something went wrong while fetching exercise.");
//     }
//   });
// });
