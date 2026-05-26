// Global state
let features = [];
let installationSteps = [];
let generatedReadme = '';

// Add feature to list
function addFeature() {
    const input = document.getElementById('featureInput');
    const feature = input.value.trim();
    
    if (!feature) {
        alert('Please enter a feature');
        return;
    }
    
    if (features.includes(feature)) {
        alert('This feature already exists');
        return;
    }
    
    features.push(feature);
    input.value = '';
    renderFeatures();
}

// Remove feature
function removeFeature(index) {
    features.splice(index, 1);
    renderFeatures();
}

// Render features list
function renderFeatures() {
    const list = document.getElementById('featuresList');
    list.innerHTML = '';
    
    features.forEach((feature, index) => {
        const tag = document.createElement('div');
        tag.className = 'feature-tag';
        tag.innerHTML = `
            ${feature}
            <button type="button" onclick="removeFeature(${index})">✕</button>
        `;
        list.appendChild(tag);
    });
}

// Add installation step
function addStep() {
    const input = document.getElementById('stepInput');
    const step = input.value.trim();
    
    if (!step) {
        alert('Please enter an installation step');
        return;
    }
    
    installationSteps.push(step);
    input.value = '';
    renderSteps();
}

// Remove installation step
function removeStep(index) {
    installationSteps.splice(index, 1);
    renderSteps();
}

// Render steps list
function renderSteps() {
    const list = document.getElementById('stepsList');
    list.innerHTML = '';
    
    installationSteps.forEach((step, index) => {
        const tag = document.createElement('div');
        tag.className = 'step-tag';
        tag.innerHTML = `
            ${step}
            <button type="button" onclick="removeStep(${index})">✕</button>
        `;
        list.appendChild(tag);
    });
}

// Handle Enter key in feature input
document.addEventListener('DOMContentLoaded', function() {
    const featureInput = document.getElementById('featureInput');
    if (featureInput) {
        featureInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addFeature();
            }
        });
    }
    
    const stepInput = document.getElementById('stepInput');
    if (stepInput) {
        stepInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addStep();
            }
        });
    }
    
    // File upload drag and drop
    const fileUpload = document.getElementById('projectUpload');
    if (fileUpload) {
        const uploadArea = fileUpload.parentElement;
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.background = 'rgba(99, 102, 241, 0.2)';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.background = 'rgba(99, 102, 241, 0.05)';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.background = 'rgba(99, 102, 241, 0.05)';
            fileUpload.files = e.dataTransfer.files;
        });
        
        uploadArea.addEventListener('click', () => {
            fileUpload.click();
        });
    }
});

// Generate README
document.getElementById('readmeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const projectName = document.getElementById('projectName').value;
    const description = document.getElementById('description').value;
    
    if (!projectName || !description) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Show loading state
    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = '⏳ Generating...';
    submitButton.disabled = true;
    
    try {
        const response = await fetch('/api/generate-readme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                project_name: projectName,
                description: description,
                features: features,
                installation_steps: installationSteps,
                project_structure: ''
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate README');
        }
        
        const data = await response.json();
        generatedReadme = data.readme;
        
        // Update preview
        const preview = document.getElementById('preview');
        preview.innerHTML = `<div class="markdown-content">${marked(generatedReadme)}</div>`;
        
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
});

// Copy to clipboard
function copyToClipboard() {
    if (!generatedReadme) {
        alert('No README generated yet');
        return;
    }
    
    navigator.clipboard.writeText(generatedReadme).then(() => {
        alert('README copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}

// Download README
function downloadReadme() {
    if (!generatedReadme) {
        alert('No README generated yet');
        return;
    }
    
    fetch('/api/export-markdown', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: generatedReadme,
            filename: 'README'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.download_url;
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => alert('Download failed: ' + error));
}