import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Overview from './overview.jsx';

function App() {
    const [period, setPeriod] = useState('month');
    const [videoData, setVideoData] = useState([]);
    

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/video_performance?period=${period}`)
            .then(response => response.json())
            .then(data => setVideoData(data))
    }, [period]);

    const formatDate = (value) => {const date = new Date(String(value).split('/')[0]);
        if (period === 'year') return String(date.getFullYear());
        if (period === 'month') return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    };

    return (    
        <div>

            <Overview />
            <h1>Video Performance</h1>
            <div>
                <button onClick={() => setPeriod('day')}>Daily</button>
                <button onClick={() => setPeriod('week')}>Weekly</button>
                <button onClick={() => setPeriod('month')}>Monthly</button>
                <button onClick={() => setPeriod('year')}>Yearly</button>
            </div>
            {videoData?.length > 0 && (
                <div>
                    <ResponsiveContainer width='100%' height={300}>
                        <LineChart data={videoData}>
                            <CartesianGrid strokeDasharray='3 3' />
                            <XAxis dataKey='published_date' tickFormatter={formatDate} minTickGap={30} />
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