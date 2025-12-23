document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById("submitBtn");
    const queryBox = document.getElementById("query");
    const fileInput = document.getElementById("fileInput");
    const outputBox = document.getElementById("outputBox");
    const outputText = document.getElementById("outputText");
    const loading = document.getElementById("loading");
    const historyList = document.getElementById("historyList");
    const newChatBtn = document.getElementById("newChatBtn");
    const copyBtn = document.getElementById("copyBtn");
    const shareBtn = document.getElementById("shareBtn");
    const summary = document.getElementById("summary");
    const researchPapers = document.getElementById("researchPapers");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
    const themeToggle = document.getElementById("themeToggle");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".sidebar");
    const mainContainer = document.querySelector(".main-container");
    const customFileInputButton = document.getElementById("customFileInputButton"); // Get custom file input button
    const selectedFilesDisplay = document.getElementById("selectedFilesDisplay"); // Get span for displaying selected files

    let currentChatId = null;

    // Sidebar toggle logic
    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.toggle("sidebar-open");
    });

    // Theme logic
    const setTheme = (isDarkMode) => {
        if (isDarkMode) {
            document.body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark");
        } else {
            document.body.classList.remove("dark-mode");
            localStorage.setItem("theme", "light");
        }
        themeToggle.checked = isDarkMode; // Update toggle state
    };

    // Apply theme on page load
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        setTheme(true);
    } else {
        setTheme(false); // Default to light if no preference or 'light'
    }

    // Event listener for theme toggle
    themeToggle.addEventListener("change", () => {
        setTheme(themeToggle.checked);
    });

    // Custom file input logic
    customFileInputButton.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            let fileNames = Array.from(fileInput.files).map(file => file.name).join(", ");
            selectedFilesDisplay.textContent = `Selected: ${fileNames}`;
        } else {
            selectedFilesDisplay.textContent = "";
        }
    });


    const copyOutput = () => {
        const textToCopy = outputText.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
            alert("Output copied to clipboard!");
        }).catch(err => {
            console.error("Error copying text: ", err);
        });
    };

    const shareOutput = () => {
        const textToShare = outputText.innerText;
        if (navigator.share) {
            navigator.share({
                title: 'Deep Research AI Output',
                text: textToShare,
            }).catch(err => console.error("Error sharing: ", err));
        } else {
            copyOutput();
        }
    };

    copyBtn.addEventListener('click', copyOutput);
    shareBtn.addEventListener('click', shareOutput);

    const fetchHistory = async () => {
        try {
            const res = await fetch("/get_history");
            const data = await res.json();
            historyList.innerHTML = "";
            data.forEach(chat => {
                const li = document.createElement("li");
                li.textContent = chat.title;
                li.dataset.chatId = chat.id;
                
                const deleteBtn = document.createElement("span");
                deleteBtn.textContent = "🗑️";
                deleteBtn.classList.add("delete-btn");
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    deleteChat(chat.id);
                });

                li.appendChild(deleteBtn);
                li.addEventListener('click', () => fetchChat(chat.id));
                historyList.appendChild(li);
            });
        } catch (err) {
            console.error("Error fetching history:", err);
        }
    };

    const deleteChat = async (chatId) => {
        if (!confirm("Are you sure you want to delete this chat?")) {
            return;
        }

        try {
            const res = await fetch(`/delete_chat/${chatId}`, {
                method: 'POST'
            });

            if (res.ok) {
                if (currentChatId === chatId) {
                    newChatBtn.click();
                }
                fetchHistory();
            } else {
                alert('Failed to delete chat.');
            }
        } catch (err) {
            console.error("Error deleting chat:", err);
            alert('Failed to delete chat.');
        }
    };

    const appendMessage = (msg) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `message-${msg.role}`);
        
        if (msg.role === 'assistant') {
                            if (typeof msg.content === 'object') {
                                const contentP = document.createElement('p');
                                contentP.innerHTML = marked.parse(msg.content.body);
                                messageDiv.appendChild(contentP);
            
                                if (msg.content.summary) {
                                    const summaryDiv = document.createElement('div');
                                    summaryDiv.classList.add('message-summary');
                                    summaryDiv.innerHTML = `
                                        <h3>Summary</h3>
                                        <p>${msg.content.summary}</p>
                                    `;
                                    messageDiv.appendChild(summaryDiv);
                                }
            
                                if (msg.content.research_papers && msg.content.research_papers.length > 0) {
                                    const researchPapersDiv = document.createElement('div');
                                    researchPapersDiv.classList.add('message-research-papers');
                                    let papersHTML = '<h3>Research Papers</h3><ul>';
                                    msg.content.research_papers.forEach(source => {
                                        papersHTML += `<li><a href="${source.href}" target="_blank">${source.title || source.href}</a></li>`;
                                    });
                                    papersHTML += '</ul>';
                                    researchPapersDiv.innerHTML = papersHTML;
                                    messageDiv.appendChild(researchPapersDiv);
                                }
                            } else {                const contentP = document.createElement('p');
                contentP.innerText = msg.content;
                messageDiv.appendChild(contentP);
            }
        } else {
            const contentP = document.createElement('p');
            contentP.innerText = msg.content;
            messageDiv.appendChild(contentP);
        }
        outputText.appendChild(messageDiv);
        outputBox.scrollTop = outputBox.scrollHeight;
    };

    const fetchChat = async (chatId) => {
        try {
            loading.classList.remove("hidden");
            outputBox.classList.add("hidden");
            const res = await fetch(`/get_chat/${chatId}`);
            const data = await res.json();
            
            outputText.innerHTML = ""; // Clear previous messages

            data.forEach(msg => {
                if(msg.role !== 'context') {
                    appendMessage(msg);
                }
            });

            currentChatId = chatId;
            outputBox.classList.remove("hidden");
        } catch (err) {
            console.error("Error fetching chat:", err);
        } finally {
            loading.classList.add("hidden");
        }
    };

    submitBtn.addEventListener("click", async () => {
        const query = queryBox.value.trim();
        const files = fileInput.files;

        if (!query && files.length === 0) {
            alert("Please enter a question or select a file!");
            return;
        }

        appendMessage({role: 'user', content: query});
        loading.classList.remove("hidden");
        outputBox.classList.remove("hidden");
        queryBox.value = "";
        fileInput.value = "";
<<<<<<< HEAD
=======
        selectedFilesDisplay.textContent = "";
>>>>>>> 8a15bb9 (feat: Deploy on Render)


        const formData = new FormData();
        formData.append("user_input", query);
        if (currentChatId !== null) {
            formData.append("chat_id", currentChatId);
        }
        for (const file of files) {
            formData.append("file", file);
        }
        
        try {
            const res = await fetch("/chat", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (data.error) {
                appendMessage({role: 'assistant', content: "Error: " + data.error});
            } else {
                currentChatId = data.chat_id;
                appendMessage({role: 'assistant', content: data.assistant_message.content});
                fetchHistory(); 
            }
        } catch (err) {
            appendMessage({role: 'assistant', content: "Error: " + err.message});
        } finally {
            loading.classList.add("hidden");
        }
    });

    newChatBtn.addEventListener('click', () => {
        currentChatId = null;
        queryBox.value = "";
        fileInput.value = "";
        outputText.innerHTML = "";
        outputBox.classList.add("hidden");
    });

    clearHistoryBtn.addEventListener('click', async () => {
        try {
            const res = await fetch("/clear_history", {
                method: "POST"
            });
            if (res.ok) {
                currentChatId = null;
                queryBox.value = "";
                fileInput.value = "";
                outputText.innerHTML = "";
                summary.innerHTML = "";
                researchPapers.innerHTML = "";
                outputBox.classList.add("hidden");
                fetchHistory(); // Refresh history list
            } else {
                console.error("Error clearing history:", res.statusText);
                alert("Failed to clear history.");
            }
        } catch (err) {
            console.error("Error clearing history:", err);
            alert("Failed to clear history.");
        }
    });

    fetchHistory();
});
