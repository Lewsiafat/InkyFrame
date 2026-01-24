// Inky Photo Display - Frontend JavaScript

// State
let currentPhotoId = null;
let photos = [];

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
const uploadProgress = document.getElementById('upload-progress');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const gallery = document.getElementById('gallery');
const photoCount = document.getElementById('photo-count');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');
const previewModal = document.getElementById('preview-modal');
const previewImage = document.getElementById('preview-image');
const modalClose = document.getElementById('modal-close');
const displayBtn = document.getElementById('display-btn');
const deleteBtn = document.getElementById('delete-btn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadPhotos();
    startStatusPolling();
});

// Event Listeners
function setupEventListeners() {
    // Dropzone
    dropzone.addEventListener('click', () => fileInput.click());
    dropzone.addEventListener('dragover', handleDragOver);
    dropzone.addEventListener('dragleave', handleDragLeave);
    dropzone.addEventListener('drop', handleDrop);

    // File input
    fileInput.addEventListener('change', handleFileSelect);

    // Modal
    modalClose.addEventListener('click', closeModal);
    previewModal.addEventListener('click', (e) => {
        if (e.target === previewModal) closeModal();
    });

    // Modal buttons
    displayBtn.addEventListener('click', handleDisplay);
    deleteBtn.addEventListener('click', handleDelete);
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    dropzone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    dropzone.classList.remove('drag-over');
    const files = Array.from(e.dataTransfer.files);
    uploadFiles(files);
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    uploadFiles(files);
    fileInput.value = ''; // Reset input
}

// File Upload
async function uploadFiles(files) {
    for (const file of files) {
        await uploadFile(file);
    }
}

async function uploadFile(file) {
    // Show progress
    dropzone.querySelector('.dropzone-content').classList.add('hidden');
    uploadProgress.classList.remove('hidden');
    progressFill.style.width = '0%';
    progressText.textContent = `Uploading ${file.name}...`;

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        // Simulate progress
        progressFill.style.width = '100%';

        showToast('Photo uploaded successfully!', 'success');
        await loadPhotos();

    } catch (error) {
        console.error('Upload error:', error);
        showToast(error.message, 'error');
    } finally {
        // Reset upload UI
        setTimeout(() => {
            dropzone.querySelector('.dropzone-content').classList.remove('hidden');
            uploadProgress.classList.add('hidden');
        }, 500);
    }
}

// Load Photos
async function loadPhotos() {
    try {
        const response = await fetch('/api/photos');
        const data = await response.json();
        photos = data.photos;
        renderGallery();
    } catch (error) {
        console.error('Failed to load photos:', error);
        showToast('Failed to load photos', 'error');
    }
}

// Render Gallery
function renderGallery() {
    photoCount.textContent = `${photos.length} photo${photos.length !== 1 ? 's' : ''}`;

    if (photos.length === 0) {
        gallery.innerHTML = '<div class="empty-state"><p>No photos yet. Upload your first photo above!</p></div>';
        return;
    }

    gallery.innerHTML = photos.map(photo => `
        <div class="photo-card" data-photo-id="${photo.id}">
            <img src="${photo.thumbnail_url}" alt="${photo.filename}" class="photo-thumbnail">
            <div class="photo-info">
                <div class="photo-filename">${photo.filename}</div>
                <div class="photo-meta">${formatFileSize(photo.size)} • ${formatDate(photo.timestamp)}</div>
            </div>
        </div>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.photo-card').forEach(card => {
        card.addEventListener('click', () => {
            const photoId = card.dataset.photoId;
            showPreview(photoId);
        });
    });
}

// Show Preview Modal
function showPreview(photoId) {
    currentPhotoId = photoId;
    const photo = photos.find(p => p.id === photoId);
    if (!photo) return;

    previewImage.src = `/uploads/optimized/${photoId}.jpg`;
    previewModal.classList.remove('hidden');
}

function closeModal() {
    previewModal.classList.add('hidden');
    currentPhotoId = null;
}

// Display Photo on Inky
async function handleDisplay() {
    if (!currentPhotoId) return;

    displayBtn.disabled = true;
    displayBtn.textContent = 'Sending to display...';

    try {
        const response = await fetch(`/api/display/${currentPhotoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ saturation: 0.5 })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Display failed');
        }

        const data = await response.json();
        showToast(`Display updating... (~${data.estimated_time}s)`, 'success');
        closeModal();

    } catch (error) {
        console.error('Display error:', error);
        showToast(error.message, 'error');
    } finally {
        displayBtn.disabled = false;
        displayBtn.textContent = 'Display on Inky';
    }
}

// Delete Photo
async function handleDelete() {
    if (!currentPhotoId) return;

    if (!confirm('Are you sure you want to delete this photo?')) return;

    deleteBtn.disabled = true;

    try {
        const response = await fetch(`/api/photos/${currentPhotoId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Delete failed');
        }

        showToast('Photo deleted', 'success');
        closeModal();
        await loadPhotos();

    } catch (error) {
        console.error('Delete error:', error);
        showToast('Failed to delete photo', 'error');
    } finally {
        deleteBtn.disabled = false;
    }
}

// Status Polling
function startStatusPolling() {
    updateStatus();
    setInterval(updateStatus, 3000); // Poll every 3 seconds
}

async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        statusIndicator.className = `status-${data.status}`;

        switch (data.status) {
            case 'idle':
                statusText.textContent = 'Display: Idle';
                break;
            case 'updating':
                statusText.textContent = 'Display: Updating...';
                break;
            case 'error':
                statusText.textContent = 'Display: Error';
                break;
        }
    } catch (error) {
        console.error('Status update failed:', error);
    }
}

// Toast Notification
function showToast(message, type = 'info') {
    toastMessage.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
    if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
    return date.toLocaleDateString();
}

// Weather icon mapping
const weatherIcons = {
    "01d": "☀️", "01n": "🌙",
    "02d": "⛅", "02n": "☁️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️"
};

// Tab Navigation
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;

        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Show/hide sections
        if (targetTab === 'photos') {
            document.querySelector('.upload-section').classList.remove('hidden');
            document.querySelector('.gallery-section').classList.remove('hidden');
            document.querySelector('.weather-section').classList.add('hidden');
        } else if (targetTab === 'weather') {
            document.querySelector('.upload-section').classList.add('hidden');
            document.querySelector('.gallery-section').classList.add('hidden');
            document.querySelector('.weather-section').classList.remove('hidden');
            loadWeather();
        }
    });
});

// Load Weather Data
async function loadWeather() {
    const weatherContent = document.getElementById('weather-content');
    const weatherDisplay = document.getElementById('weather-display');

    try {
        // Show loading
        weatherContent.classList.remove('hidden');
        weatherDisplay.classList.add('hidden');

        // Fetch current weather and forecast
        const [currentResponse, forecastResponse] = await Promise.all([
            fetch('/api/weather/current'),
            fetch('/api/weather/forecast')
        ]);

        if (!currentResponse.ok || !forecastResponse.ok) {
            throw new Error('Failed to fetch weather data');
        }

        const current = await currentResponse.json();
        const forecast = await forecastResponse.json();

        // Update UI
        displayWeatherData(current, forecast);

        // Hide loading, show weather
        weatherContent.classList.add('hidden');
        weatherDisplay.classList.remove('hidden');

    } catch (error) {
        console.error('Weather load error:', error);
        weatherContent.innerHTML = '<div class="weather-loading">Failed to load weather data. Please check API key configuration.</div>';
    }
}

// Display Weather Data
function displayWeatherData(current, forecast) {
    // Current weather
    document.getElementById('weather-location').textContent = current.location;
    document.getElementById('weather-temp').textContent = `${Math.round(current.temperature)}°`;
    document.getElementById('weather-icon').textContent = weatherIcons[current.icon] || '🌤️';
    document.getElementById('weather-description').textContent = current.description;
    document.getElementById('weather-feels').textContent = `${Math.round(current.feels_like)}°`;
    document.getElementById('weather-humidity').textContent = `${current.humidity}%`;
    document.getElementById('weather-wind').textContent = `${current.wind_speed} m/s`;

    // Forecast cards
    const forecastCards = document.getElementById('forecast-cards');
    forecastCards.innerHTML = forecast.days.map(day => `
        <div class="forecast-card">
            <div class="day-name">${day.day_name}</div>
            <div class="forecast-icon">${weatherIcons[day.icon] || '🌤️'}</div>
            <div class="temp-high">${Math.round(day.temp_high)}°</div>
            <div class="temp-low">${Math.round(day.temp_low)}°</div>
        </div>
    `).join('');
}

// Display Weather on Inky
document.getElementById('display-weather-btn').addEventListener('click', async () => {
    const btn = document.getElementById('display-weather-btn');
    btn.disabled = true;
    btn.textContent = 'Sending to display...';

    try {
        const response = await fetch('/api/weather/display', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Display failed');
        }

        const data = await response.json();
        showToast(`Weather display updating... (~${data.estimated_time}s)`, 'success');

    } catch (error) {
        console.error('Display error:', error);
        showToast(error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Display Weather on Inky';
    }
});

