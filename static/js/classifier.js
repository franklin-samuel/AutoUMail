const tabs = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(tc => {
            tc.classList.remove('active');
            tc.classList.add('hidden');
        });
        
        tab.classList.add('active');
        const targetContent = document.getElementById(`${tabName}-tab`);
        targetContent.classList.remove('hidden');
        targetContent.classList.add('active');
        
        if (tabName === 'text') {
            document.getElementById('emailFile').value = '';
            document.getElementById('fileName').textContent = '';
        } else {
            document.getElementById('emailText').value = '';
        }
    });
});

const fileInput = document.getElementById('emailFile');
const fileNameDisplay = document.getElementById('fileName');
const fileUploadArea = document.getElementById('fileUploadArea');

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileNameDisplay.textContent = `📎 ${file.name}`;
    } else {
        fileNameDisplay.textContent = '';
    }
});

fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('border-orange-500', 'bg-gray-800/30');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('border-orange-500', 'bg-gray-800/30');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('border-orange-500', 'bg-gray-800/30');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        fileNameDisplay.textContent = `📎 ${file.name}`;
    }
});

const textForm = document.getElementById('textForm');

textForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const button = e.target.querySelector('button[type="submit"]');
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    button.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    btnLoader.classList.add('flex');
    
    try {
        const formData = new FormData(textForm);
        
        const response = await fetch('/api/classify/text', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error processing request');
        }
        
        showSuccessModal(data);
        
    } catch (error) {
        showErrorToast(error.message);
    } finally {
        // Reset button
        button.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
        btnLoader.classList.remove('flex');
    }
});

const fileForm = document.getElementById('fileForm');

fileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const button = e.target.querySelector('button[type="submit"]');
    const btnText = button.querySelector('.btn-text');
    const btnLoader = button.querySelector('.btn-loader');
    
    button.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    btnLoader.classList.add('flex');
    
    try {
        const formData = new FormData(fileForm);
        
        const response = await fetch('/api/classify/file', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error processing request');
        }
        
        showSuccessModal(data);
        
    } catch (error) {
        showErrorToast(error.message);
    } finally {
        // Reset button
        button.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
        btnLoader.classList.remove('flex');
    }
});

function showSuccessModal(data) {
    const modal = document.getElementById('successModal');
    const categoryEl = document.getElementById('resultCategory');
    const responseEl = document.getElementById('resultResponse');
    
    categoryEl.textContent = data.category;
    categoryEl.className = `inline-block px-8 py-3 rounded-2xl text-lg font-bold category-badge ${data.category.toLowerCase()}`;
    
    responseEl.textContent = data.suggested_response;
    
    modal.classList.remove('hidden');
    
    document.body.style.overflow = 'hidden';
}

document.getElementById('closeModal').addEventListener('click', () => {
    const modal = document.getElementById('successModal');
    modal.classList.add('hidden');
    
    // Reset forms
    textForm.reset();
    fileForm.reset();
    fileNameDisplay.textContent = '';
    
    // Restore body scroll
    document.body.style.overflow = 'auto';
});

document.getElementById('copyButton').addEventListener('click', async () => {
    const response = document.getElementById('resultResponse').textContent;
    const button = document.getElementById('copyButton');

    const originalContent = button.innerHTML;

    try {
        await navigator.clipboard.writeText(response);
        
        button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 mx-auto">
          <path fill-rule="evenodd" d="M19.916 4.626a.75.75 0 0 1 .208 1.04l-9 13.5a.75.75 0 0 1-1.154.114l-6-6a.75.75 0 0 1 1.06-1.06l5.353 5.353 8.493-12.74a.75.75 0 0 1 1.04-.207Z" clip-rule="evenodd" />
        </svg>
        `;
        button.classList.add('bg-green-600');
        button.classList.remove('from-orange-500', 'to-orange-600');

        setTimeout(() => {
            button.innerHTML = originalContent;
            button.classList.remove('bg-green-600');
            button.classList.add('from-orange-500', 'to-orange-600');
        }, 2000);
    } catch (err) {
        showErrorToast('Erro ao copiar. Tente selecionar manualmente.');
    }
});

function showErrorToast(message) {
    const container = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = 'animate-slideInRight bg-red-600/95 backdrop-blur-xl text-white px-6 py-4 rounded-2xl shadow-2xl border border-red-500/50 flex items-start gap-4 max-w-md';
    
    toast.innerHTML = `
         <div class="flex flex-row justify-center items-center gap-5">
            <div class="flex-shrink-0 text-2xl">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-7">
                  <path fill-rule="evenodd" d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
                </svg>
            </div>
            <div class="flex-1">
                <p class="font-semibold mb-1">Erro</p>
                <p class="text-sm text-red-100">${message}</p>
            </div>
            <button class="flex-shrink-0 text-white hover:text-red-200 font-bold text-xl" onclick="this.closest('.animate-slideInRight').remove()">
                x
            </button>
         </div>
        `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.remove('animate-slideInRight');
            toast.classList.add('animate-slideOutRight');
            
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        }
    }, 5000);
}