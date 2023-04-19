fetch("/api/competencies", {
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        
    }
}).then((response) => response.json())
