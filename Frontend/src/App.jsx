import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
    const [videoData, setVideoData] = useState(null);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/video_performance')
            .then(response => response.json())
            .then(data => setVideoData(data))
    }, []);

    return (
        <div>
            <h1>Video Performance</h1>
            {videoData?.length > 0 && (
                <div>
                    {videoData.map(item => (
                        <div key={item.published_date}>
                            <p>Date: {item.published_date}</p>
                            <p>Views: {item.view_count}</p>
                            <p>Likes: {item.like_count}</p>
                            <p>Comments: {item.comment_count}</p>
                        </div>
                    ))}
                    <ResponsiveContainer width='100%' height={300}>
                        <LineChart data={videoData}>
                            <CartesianGrid strokeDasharray='3 3' />
                            <XAxis dataKey='published_date' />
                            <YAxis yAxisId='left' orientation='left' />
                            <YAxis yAxisId='right' orientation='right' />
                            <Tooltip />
                            <Legend />
                            <Line type='monotone' yAxisId='left' dataKey='view_count' stroke='#8884d8' />
                            <Line type='monotone' yAxisId='right' dataKey='like_count' stroke='#82ca9d' />
                            <Line type='monotone' yAxisId='right' dataKey='comment_count' stroke='#ffc658' />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    );
}

export default App;