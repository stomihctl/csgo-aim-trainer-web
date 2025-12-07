const statsForm = document.getElementById('statsForm');
const message = document.getElementById('message');

statsForm.addEventListener('submit', function(e) {
    // očistimo prethodnu poruku
    message.textContent = '';

    const exercise = document.getElementById('exercise').value;
    const score = document.getElementById('score').value;
    const time = document.getElementById('time').value;

    // validacija
    if (!exercise || !score || !time) {
        e.preventDefault(); // blokira samo ako polja nisu popunjena
        message.style.color = 'red';
        message.textContent = 'Please fill required fields.';
        return;
    }

    // pretvori u HH:MM:SS za Django TimeField
    const durMinutes = parseInt(time);
    const hours = Math.floor(durMinutes / 60);
    const minutes = durMinutes % 60;
    //document.getElementById('time').value = `${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}:00`;

    // sad se forma šalje normalno POST-om
});
