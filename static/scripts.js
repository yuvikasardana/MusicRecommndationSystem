document.getElementById('detect-button').addEventListener('click', async () => {
    const songList = document.getElementById('song-list');
    const emotionSpan = document.getElementById('detected-emotion');
    songList.innerHTML = ''; // Clear previous results
    emotionSpan.textContent = 'Detecting...';
    console.log("songs dila do")
    try {
        const response = await fetch('/detect-emotion-and-recommend', {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch recommendations.');
        }

        const data = await response.json();

        // Update UI with the emotion and recommended songs
        emotionSpan.textContent = data.emotion;
        songList.innerHTML = data.songs
            .map((song) => `<li>${song}</li>`)
            .join('');
        document.querySelector('.result-section').style.display = 'block';
    } catch (error) {
        console.error(error);
        emotionSpan.textContent = 'Error detecting emotion.';
    }
});
