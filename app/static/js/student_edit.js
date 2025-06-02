document.addEventListener('DOMContentLoaded', function () {
    const studyProgramSelect = document.getElementById('study_program_id');
    const groupSelect = document.getElementById('group_id');
    const currentGroupId = groupSelect.getAttribute('data-current');

    function loadGroups(studyProgramId, selectedGroupId = null) {
        fetch(`/api/groups/${studyProgramId}`)
            .then(response => response.json())
            .then(data => {
                groupSelect.innerHTML = '';

                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.text = 'Select Group';
                groupSelect.appendChild(defaultOption);

                data.forEach(group => {
                    const option = document.createElement('option');
                    option.value = group[0];
                    option.text = group[1];
                    if (selectedGroupId && parseInt(selectedGroupId) === group[0]) {
                        option.selected = true;
                    }
                    groupSelect.appendChild(option);
                });
            })
            .catch(err => console.error('Error loading groups:', err));
    }

    // Load groups on initial page load if study program selected
    if (studyProgramSelect.value) {
        loadGroups(studyProgramSelect.value, currentGroupId);
    }

    // Listen for changes on study program select
    studyProgramSelect.addEventListener('change', function () {
        loadGroups(this.value);
    });
});
