// API Configuration
const API_BASE_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? 'http://localhost:8000/api'
    : '/api';

// State
let currentFilter = 'all';
let predictions = [];
let stats = null;
let profile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initPredictionForm();
    initFilters();
    loadPredictions();
    loadStats();
    loadProfile();
});

// Tab Management
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
}

// Prediction Form
function initPredictionForm() {
    const newBtn = document.getElementById('new-prediction-btn');
    const form = document.getElementById('prediction-form');
    const cancelBtn = document.getElementById('cancel-prediction-btn');
    const createForm = document.getElementById('create-prediction-form');
    const probabilitySlider = document.getElementById('probability');
    const probabilityValue = document.getElementById('probability-value');
    const getSuggestionsBtn = document.getElementById('get-suggestions-btn');

    newBtn.addEventListener('click', () => {
        form.classList.remove('hidden');
        newBtn.style.display = 'none';
    });

    cancelBtn.addEventListener('click', () => {
        form.classList.add('hidden');
        newBtn.style.display = 'block';
        createForm.reset();
    });

    probabilitySlider.addEventListener('input', (e) => {
        probabilityValue.textContent = `${e.target.value}%`;
    });

    getSuggestionsBtn.addEventListener('click', async () => {
        const description = document.getElementById('description').value;
        if (!description.trim()) {
            alert('Please enter a prediction description first');
            return;
        }
        await getAISuggestions(description);
    });

    createForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await createPrediction();
    });
}

// Filters
function initFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.filter;
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderPredictions();
        });
    });
}

// API Calls
async function loadPredictions() {
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/`);
        if (!response.ok) throw new Error('Failed to load predictions');
        predictions = await response.json();
        renderPredictions();
    } catch (error) {
        console.error('Error loading predictions:', error);
        document.getElementById('predictions-list').innerHTML =
            '<div class="loading">Error loading predictions. Please try again.</div>';
    }
}

async function createPrediction() {
    const description = document.getElementById('description').value;
    const probability = parseFloat(document.getElementById('probability').value) / 100;
    const resolveBy = document.getElementById('resolve_by').value;

    const data = {
        description,
        probability,
    };

    if (resolveBy) {
        data.resolve_by = new Date(resolveBy).toISOString();
    }

    try {
        const response = await fetch(`${API_BASE_URL}/predictions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.text();
            console.error('Server error:', response.status, errorData);
            throw new Error(`Failed to create prediction: ${response.status} - ${errorData}`);
        }

        // Reset form and reload
        document.getElementById('create-prediction-form').reset();
        document.getElementById('prediction-form').classList.add('hidden');
        document.getElementById('new-prediction-btn').style.display = 'block';
        document.getElementById('probability-value').textContent = '50%';

        await loadPredictions();
        await loadStats();
    } catch (error) {
        console.error('Error creating prediction:', error);
        alert('Failed to create prediction. Check console for details.');
    }
}

async function resolvePrediction(id, outcome) {
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/${id}/resolve/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ outcome }),
        });

        if (!response.ok) throw new Error('Failed to resolve prediction');

        await loadPredictions();
        await loadStats();
        closeModal();
    } catch (error) {
        console.error('Error resolving prediction:', error);
        alert('Failed to resolve prediction. Please try again.');
    }
}

async function deletePrediction(id) {
    if (!confirm('Are you sure you want to delete this prediction?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/predictions/${id}/`, {
            method: 'DELETE',
        });

        if (!response.ok) throw new Error('Failed to delete prediction');

        await loadPredictions();
        await loadStats();
        closeModal();
    } catch (error) {
        console.error('Error deleting prediction:', error);
        alert('Failed to delete prediction. Please try again.');
    }
}

async function loadStats() {
    try {
        // Request stats with AI summary
        const response = await fetch(`${API_BASE_URL}/predictions/stats/?ai_summary=true`);
        if (!response.ok) throw new Error('Failed to load stats');
        stats = await response.json();
        renderStats();
    } catch (error) {
        console.error('Error loading stats:', error);
        document.getElementById('stats-content').innerHTML =
            '<div class="loading">Error loading statistics. Create some predictions first!</div>';
    }
}

async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/profile/`);
        if (!response.ok) throw new Error('Failed to load profile');
        const profiles = await response.json();
        profile = profiles[0] || { name: '', notes: '' };
        renderProfile();
    } catch (error) {
        console.error('Error loading profile:', error);
        document.getElementById('profile-content').innerHTML =
            '<div class="loading">Error loading profile.</div>';
    }
}

async function updateProfile() {
    const name = document.getElementById('profile-name').value;
    const notes = document.getElementById('profile-notes').value;

    const data = { name, notes };
    const method = profile.id ? 'PATCH' : 'POST';
    const url = profile.id
        ? `${API_BASE_URL}/profile/${profile.id}/`
        : `${API_BASE_URL}/profile/`;

    try {
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) throw new Error('Failed to update profile');

        await loadProfile();
        alert('Profile updated successfully!');
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
    }
}

async function getAISuggestions(description) {
    const btn = document.getElementById('get-suggestions-btn');
    const suggestionsDiv = document.getElementById('ai-suggestions');

    btn.disabled = true;
    btn.textContent = 'Getting suggestions...';

    try {
        const response = await fetch(`${API_BASE_URL}/predictions/ai_suggest/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description }),
        });

        if (!response.ok) throw new Error('Failed to get AI suggestions');

        const data = await response.json();

        suggestionsDiv.innerHTML = `
            <h4>✨ AI Suggestions</h4>
            <div style="white-space: pre-wrap;">${escapeHtml(data.suggestions)}</div>
        `;
        suggestionsDiv.classList.remove('hidden');
    } catch (error) {
        console.error('Error getting AI suggestions:', error);
        suggestionsDiv.innerHTML = `
            <h4>AI Suggestions</h4>
            <p style="color: var(--danger-color);">Failed to get suggestions. Make sure your GEMINI_API_KEY is configured.</p>
        `;
        suggestionsDiv.classList.remove('hidden');
    }

    btn.disabled = false;
    btn.textContent = 'Get AI Suggestions';
}

// Rendering
function renderPredictions() {
    const container = document.getElementById('predictions-list');

    let filtered = predictions;
    if (currentFilter === 'pending') {
        filtered = predictions.filter(p => !p.resolved);
    } else if (currentFilter === 'resolved') {
        filtered = predictions.filter(p => p.resolved);
    }

    if (filtered.length === 0) {
        container.innerHTML = '<div class="loading">No predictions found. Create your first one!</div>';
        return;
    }

    container.innerHTML = filtered.map(prediction => `
        <div class="prediction-card ${prediction.resolved ? 'resolved' : ''}" data-prediction-id="${prediction.id}">
            <div class="prediction-header">
                <div class="prediction-description">${escapeHtml(prediction.description)}</div>
                <div class="prediction-probability">${Math.round(prediction.probability * 100)}%</div>
            </div>
            <div class="prediction-meta">
                <span class="prediction-status status-${prediction.resolved ? 'resolved' : 'pending'}">
                    ${prediction.resolved ? 'Resolved' : 'Pending'}
                </span>
                ${prediction.resolved ? `
                    <span class="outcome-${prediction.outcome}">
                        ${prediction.outcome ? '✓ Happened' : '✗ Did not happen'}
                    </span>
                ` : ''}
                <span>Created: ${new Date(prediction.created_at).toLocaleDateString()}</span>
                ${prediction.resolve_by ? `
                    <span>Resolve by: ${new Date(prediction.resolve_by).toLocaleDateString()}</span>
                ` : ''}
            </div>
        </div>
    `).join('');

    // Add click event listeners
    container.querySelectorAll('.prediction-card').forEach(card => {
        card.addEventListener('click', () => {
            const predictionId = card.dataset.predictionId;
            showPredictionDetail(predictionId);
        });
    });
}

function renderStats() {
    const container = document.getElementById('stats-content');

    if (!stats || stats.total_predictions === 0) {
        container.innerHTML = '<div class="loading">Create and resolve predictions to see your calibration statistics!</div>';
        return;
    }

    const brierScore = stats.brier_score !== null ? stats.brier_score.toFixed(4) : 'N/A';

    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${stats.total_predictions}</div>
                <div class="stat-label">Total Predictions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.resolved_predictions}</div>
                <div class="stat-label">Resolved</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${brierScore}</div>
                <div class="stat-label">Brier Score</div>
            </div>
        </div>

        ${stats.calibration_bins.length > 0 ? `
            <div class="calibration-bins">
                <h3>Calibration by Confidence Level</h3>
                ${stats.calibration_bins.map(bin => `
                    <div class="calibration-bar">
                        <div class="bin-label">${bin.range}</div>
                        <div class="bin-bar-container">
                            <div class="bin-bar" style="width: ${bin.actual_frequency}%"></div>
                        </div>
                        <div class="bin-value">${bin.actual_frequency.toFixed(0)}% (${bin.count})</div>
                    </div>
                `).join('')}
                <p style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                    <strong>How to read this:</strong> If you're well calibrated, the bars should roughly match the confidence range.
                    For example, for predictions where you said 60-70%, about 60-70% should have happened.
                </p>
            </div>
        ` : ''}

        ${stats.ai_summary ? `
            <div class="ai-summary">
                <h3>✨ AI-Powered Insights</h3>
                <div style="white-space: pre-wrap; line-height: 1.8;">${escapeHtml(stats.ai_summary)}</div>
            </div>
        ` : stats.resolved_predictions > 0 ? `
            <div class="ai-summary">
                <h3>AI-Powered Insights</h3>
                <p style="color: var(--danger-color);"><em>AI summary unavailable. Check if GEMINI_API_KEY is configured.</em></p>
            </div>
        ` : ''}
    `;
}

function renderProfile() {
    const container = document.getElementById('profile-content');

    container.innerHTML = `
        <div class="profile-card">
            <form id="profile-form" onsubmit="event.preventDefault(); updateProfile();">
                <div class="profile-field">
                    <label for="profile-name">Name</label>
                    <input type="text" id="profile-name" value="${escapeHtml(profile.name || '')}" placeholder="Your name">
                </div>
                <div class="profile-field">
                    <label for="profile-notes">Notes</label>
                    <textarea id="profile-notes" rows="5" placeholder="Your notes about calibration, goals, etc.">${escapeHtml(profile.notes || '')}</textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save Profile</button>
            </form>
        </div>
    `;
}

// Modal
function showPredictionDetail(id) {
    const prediction = predictions.find(p => p.id === id);
    if (!prediction) return;

    const modal = document.getElementById('prediction-modal');
    const detail = document.getElementById('prediction-detail');

    detail.innerHTML = `
        <h2>${escapeHtml(prediction.description)}</h2>
        <div class="prediction-meta" style="margin: 1.5rem 0;">
            <span class="prediction-probability" style="font-size: 2rem;">${Math.round(prediction.probability * 100)}%</span>
            <span class="prediction-status status-${prediction.resolved ? 'resolved' : 'pending'}">
                ${prediction.resolved ? 'Resolved' : 'Pending'}
            </span>
        </div>

        <div style="margin: 1rem 0;">
            <p><strong>Created:</strong> ${new Date(prediction.created_at).toLocaleString()}</p>
            ${prediction.resolve_by ? `<p><strong>Resolve by:</strong> ${new Date(prediction.resolve_by).toLocaleString()}</p>` : ''}
            ${prediction.resolved ? `
                <p><strong>Outcome:</strong> <span class="outcome-${prediction.outcome}">
                    ${prediction.outcome ? 'Happened ✓' : 'Did not happen ✗'}
                </span></p>
            ` : ''}
        </div>

        ${!prediction.resolved ? `
            <div class="resolve-actions">
                <button class="btn btn-success" data-action="resolve-true" data-id="${prediction.id}">
                    ✓ It Happened
                </button>
                <button class="btn btn-danger" data-action="resolve-false" data-id="${prediction.id}">
                    ✗ It Didn't Happen
                </button>
            </div>
        ` : ''}

        <div style="margin-top: 2rem;">
            <button class="btn btn-danger" data-action="delete" data-id="${prediction.id}">
                Delete Prediction
            </button>
        </div>
    `;

    // Add event listeners to modal buttons
    detail.querySelectorAll('button[data-action]').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            const id = btn.dataset.id;

            if (action === 'resolve-true') {
                resolvePrediction(id, true);
            } else if (action === 'resolve-false') {
                resolvePrediction(id, false);
            } else if (action === 'delete') {
                deletePrediction(id);
            }
        });
    });

    modal.classList.add('active');
}

function closeModal() {
    const modal = document.getElementById('prediction-modal');
    modal.classList.remove('active');
}

// Close modal on background click
document.getElementById('prediction-modal').addEventListener('click', (e) => {
    if (e.target.id === 'prediction-modal') {
        closeModal();
    }
});

// Close modal on X click
document.querySelector('.close').addEventListener('click', closeModal);

// Utilities
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
