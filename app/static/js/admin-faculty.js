document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.view-details-btn');
    const infoCard = document.getElementById('faculty-info');
    const nameEl = document.getElementById('faculty-name');
    const descEl = document.getElementById('faculty-description');

    // Add extra fields
    const addressEl = document.createElement('p');
    const programsEl = document.createElement('ul');

    infoCard.querySelector('.card-body').appendChild(addressEl);
    infoCard.querySelector('.card-body').appendChild(programsEl);

    buttons.forEach(button => {
        button.addEventListener('click', async function () {
            const facultyId = this.dataset.id;
            const response = await fetch(`/api/faculty_detail/${facultyId}`);
            if (!response.ok) {
                alert('Faculty not found.');
                return;
            }

            const data = await response.json();
            nameEl.textContent = data.name;
            descEl.textContent = data.description;
            addressEl.textContent = 'Address: ' + data.full_address;

            // Clear and add programs
            programsEl.innerHTML = '';
            if (data.programs.length > 0) {
                data.programs.forEach(program => {
                    const li = document.createElement('li');
                    li.textContent = program;
                    programsEl.appendChild(li);
                });
            } else {
                const li = document.createElement('li');
                li.textContent = 'No programs available.';
                programsEl.appendChild(li);
            }

            infoCard.style.display = 'block';
        });
    });
});
