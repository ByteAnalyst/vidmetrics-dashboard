import {useState, useEffect} from 'react';

function App() {
    const [overview, setOverview] = useState(null);

    useEffect(() => {
        fetch('http://localhost:8000/overview/')
            .then(response => response.json())
            .then(data => setOverview(data))
            console.log(overview)
    }, []);
}
