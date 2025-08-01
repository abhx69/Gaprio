// Wait for the entire page to load before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get references to all the necessary HTML elements
    const uploadForm = document.getElementById('upload-form');
    const submitButton = document.getElementById('submit-button');
    const audioFileInput = document.getElementById('audio-file');
    const loadingSpinner = document.getElementById('loading-spinner');
    const resultsContainer = document.getElementById('results-container');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');
    
    const transcriptText = document.getElementById('transcript-text');
    const contractText = document.getElementById('contract-text');
    const pdfDownloadLink = document.getElementById('pdf-download-link');

    // This is the URL of your locally running FastAPI backend
    // IMPORTANT: Make sure the port number matches the one your server is running on.
    const apiUrl = 'http://127.0.0.1:8001/generate_contract/';

    // Listen for the form submission event
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default browser form submission

        const file = audioFileInput.files[0];
        if (!file) {
            showError('Please select an audio file first.');
            return;
        }

        // --- UI Updates: Show loading state ---
        loadingSpinner.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        errorMessage.classList.add('hidden');
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';

        // Create a FormData object to send the file
        const formData = new FormData();
        formData.append('file', file);

        try {
            // --- API Call ---
            // Use the fetch API to send the file to your backend
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                // If the server returns an error (like 4xx or 5xx)
                throw new Error(data.error || 'An unknown error occurred.');
            }

            // --- UI Updates: Populate results ---
            transcriptText.textContent = data.transcript;
            contractText.textContent = data.contract_text;
            
            // Construct the full URL for the PDF download
            const backendBaseUrl = 'http://127.0.0.1:8001';
            pdfDownloadLink.href = backendBaseUrl + data.pdf_path;
            
            resultsContainer.classList.remove('hidden');

        } catch (err) {
            // --- UI Updates: Show error message ---
            console.error('Fetch error:', err);
            showError(err.message);
        } finally {
            // --- UI Updates: Reset form state ---
            loadingSpinner.classList.add('hidden');
            submitButton.disabled = false;
            submitButton.textContent = 'Generate Contract';
        }
    });

    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
    }
});
