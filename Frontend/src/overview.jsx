import {useState, useEffect} from 'react';


function Overview(){
    
    const [overviewData, setOverviewData] = useState(null)
        
    useEffect(() => {

    fetch('http://127.0.0.1:8000/overview')
    .then(response => response.json())
    .then(data =>setOverviewData(data))
}, []);

return (
    <div>
        <h2>Channel Overview</h2>
        {overviewData ? (
        <div>
        <p> Total Views: {overviewData.total_views?.toLocaleString()}</p>
        <p> Total Likes: {overviewData.total_likes?.toLocaleString()}</p>
        <p> Total Comments: {overviewData.total_comments?.toLocaleString()}</p>
        <p> Average Views: {overviewData.average_views?.toLocaleString()}</p>
        <p> Average Engagement: {overviewData.average_engagement?.toLocaleString()}</p>
        </div>
        ) : (
            <p>Loading Overview...</p>
        )}
    </div>
)};

export default Overview;